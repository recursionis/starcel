"""
Zarr integration for nD Table.

Adds ZarrTable, a Table subclass that uses a `zarr.Array` (inside a
`zarr.Group`) as its persistent storage backend. The full nd_table API
keeps working — indexing, formulas, named cells, dependency graph,
undo/redo, the Unreal renderer, the spread engine — but every write
also lands in a Zarr store on disk (DirectoryStore), in memory
(MemoryStore), in a zip file (ZipStore), or in any other store the
user hands in.

Public surface (in order of likely use):

    ZarrTable(store, path='', shape=..., axes=..., chunks=..., ...)
        Create or open a Zarr-backed table. `store` accepts a filesystem
        path (str / pathlib), a `zarr.Store`, or None for in-memory.

    ZarrTable.open(store, path='', mode='r+')
        Reload an existing Zarr-backed table. Axes, named cells, and
        formulas are restored from group attrs; raw values from the
        data array.

    ZarrTable.from_table(table, store, path='', ...)
        Snapshot an existing Table (or any subclass) into a new
        Zarr-backed table.

    zt.zarr_array               -> underlying zarr.Array
    zt.zarr_group               -> underlying zarr.Group (contains data + meta)
    zt.store                    -> underlying store
    zt.chunks / zt.nchunks      -> chunk shape / chunk count
    zt.write_region(slices, np.ndarray)
        Bulk-write a numpy region in one shot. Bypasses per-cell undo
        for speed; still mirrors into `self.cells`.
    zt.read_region(slices)      -> numpy view of a region (loads only
                                   the needed chunks).
    zt.sync()                   -> flush attrs (for stores that buffer).
    zt.close()                  -> close the underlying store (mandatory
                                   for ZipStore, harmless otherwise).
    zt.consolidate_metadata()   -> consolidate group metadata for fast
                                   remote opens.
    zt.info                     -> zarr-native info string.
    zt.copy_to(other_store, path='') -> deep copy to another zarr root.

Persistence layout::

    <store>/<path>/                 (zarr Group)
        .zattrs                     {"nd_table": {...metadata...}}
        data/                       (zarr Array, shape == table.shape)
            .zarray                 shape, chunks, dtype, compressor
            <chunks>

The `nd_table` attrs key holds: schema version, axes specs (start, end,
name, custom_labels, include_zero, ...), named cells, formulas keyed by
str(idx), and the table mode. That makes ZarrTable.open() a true
round-trip — nothing user-visible is lost on disk.

Notes on dtype:
    * Default is dtype=object with a numcodecs.Pickle codec, which lets
      cells hold mixed types (str, int, float, CellReference, callables).
    * Pass a numeric dtype (e.g. 'float64') for tabular numeric data —
      it'll be much smaller on disk and chunks compress well.
    * Object dtype + ZipStore + read mode is fine; writing into a
      ZipStore requires the store to be opened with mode='a' or 'w'.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

try:
    import zarr
    from zarr.errors import ContainsArrayError, ContainsGroupError, PathNotFoundError
    _ZARR_OK = True
    _ZARR_IMPORT_ERR: Optional[BaseException] = None
except Exception as _e:
    zarr = None
    _ZARR_OK = False
    _ZARR_IMPORT_ERR = _e

try:
    import numcodecs
    from numcodecs import Pickle as _PickleCodec
except Exception:
    numcodecs = None
    _PickleCodec = None

from .ndtable import Table, Axis, Cell


_SCHEMA_VERSION = 1
_DATA_ARRAY_NAME = "data"
_META_KEY = "nd_table"


def _require_zarr() -> None:
    if not _ZARR_OK:
        raise ImportError(
            "zarr is not installed. `pip install zarr numcodecs` "
            f"(import failed with: {_ZARR_IMPORT_ERR!r})"
        )


# ---------------------------------------------------------------------------
# Axis (de)serialization — group attrs are JSON, so we round-trip Axis
# through a plain dict.
# ---------------------------------------------------------------------------

def _axis_to_dict(axis: Axis) -> Dict[str, Any]:
    return {
        "start": int(axis.start),
        "end": int(axis.end),
        "name": axis.name,
        "custom_labels": list(axis.custom_labels) if axis.custom_labels else None,
        "include_zero": bool(axis.include_zero),
        "include_negative_zero": bool(axis.include_negative_zero),
        "include_positive_zero": bool(axis.include_positive_zero),
        "use_spreadsheet_labels": bool(axis.use_spreadsheet_labels),
        "spreadsheet_axis": bool(axis.spreadsheet_axis),
    }


def _axis_from_dict(d: Dict[str, Any]) -> Axis:
    return Axis(
        start=int(d["start"]),
        end=int(d["end"]),
        name=d.get("name"),
        labels=d.get("custom_labels"),
        include_zero=d.get("include_zero", True),
        include_negative_zero=d.get("include_negative_zero", False),
        include_positive_zero=d.get("include_positive_zero", False),
        use_spreadsheet_labels=d.get("use_spreadsheet_labels", False),
        spreadsheet_axis=d.get("spreadsheet_axis", False),
    )


def _idx_to_key(idx: Tuple[int, ...]) -> str:
    """Stable JSON-safe key for a cell index tuple."""
    return ",".join(str(int(i)) for i in idx)


def _key_to_idx(key: str) -> Tuple[int, ...]:
    return tuple(int(p) for p in key.split(",")) if key else ()


# ---------------------------------------------------------------------------
# Store resolution
# ---------------------------------------------------------------------------

def _resolve_store(store):
    """Accept a path str, pathlib.Path, an existing zarr.Store, or None.

    None -> MemoryStore. A string ending in '.zip' -> ZipStore opened in 'a'
    mode. Everything else string-like -> DirectoryStore.
    """
    _require_zarr()
    if store is None:
        return zarr.MemoryStore()
    if isinstance(store, str) or hasattr(store, "__fspath__"):
        spath = os.fspath(store)
        if spath.lower().endswith(".zip"):
            return zarr.ZipStore(spath, mode="a")
        return zarr.DirectoryStore(spath)
    return store


# ---------------------------------------------------------------------------
# ZarrTable
# ---------------------------------------------------------------------------

class ZarrTable(Table):
    """
    Table subclass whose cells live in a zarr.Array.

    Every set/get continues to work through the inherited Table API —
    formulas, named cells, the dependency graph, undo/redo, and the
    Unreal renderer all see a normal Table. Under the hood, writes also
    land in a zarr Array inside a zarr Group, and the group's attrs
    carry the axes/formulas/named-cells so a later `ZarrTable.open()`
    fully reconstitutes the table.
    """

    DEFAULT_DTYPE = object

    def __init__(
        self,
        store: Any = None,
        path: str = "",
        shape: Union[Tuple, List, None] = None,
        axes: Optional[List[Axis]] = None,
        chunks: Union[Tuple, List, bool, None] = True,
        dtype: Any = None,
        fill_value: Any = None,
        compressor: Any = "default",
        object_codec: Any = None,
        zarr_mode: str = "a",
        overwrite: bool = False,
        # Forwarded to Table:
        mode: str = "normal",
        lazy_eval: bool = True,
        always_reevaluate: bool = False,
        enable_undo: bool = True,
        debug: bool = False,
        aggressive_debug: bool = False,
    ):
        """
        Args:
            store: Path str, zarr.Store, or None (MemoryStore).
            path: Group key inside the store (use '' for the root group).
            shape / axes: Same semantics as Table; required only when
                creating a new group.
            chunks: Zarr chunk shape. True = auto-chunk (zarr's heuristic),
                or pass a tuple matching shape.
            dtype: Numpy/Zarr dtype for cell values. Defaults to object
                with a Pickle codec — safe for mixed types but bulkier.
                Pass 'float64' / 'int32' for tabular numeric data.
            fill_value: Default for unwritten cells (None for object dtype,
                0 for numeric).
            compressor: Passed to zarr; 'default' lets zarr pick Blosc.
            object_codec: Required when dtype=object; defaults to Pickle.
            zarr_mode: 'r' (read), 'r+' (read/write existing), 'a' (open
                or create), 'w' (create, overwrite), 'w-' (create, error
                if exists). Maps roughly to zarr.open() modes.
            overwrite: Force a fresh array even if one exists.
            mode/lazy_eval/.../aggressive_debug: Passed to Table.__init__.
        """
        _require_zarr()

        # Set up the parent Table FIRST so axes/shape/cells/etc exist before
        # we hook into them. We pass the same shape/axes through; the Table
        # uses them to set self.axes, self.cells, self.named_cells, etc.
        super().__init__(
            shape=shape,
            axes=axes,
            mode=mode,
            lazy_eval=lazy_eval,
            always_reevaluate=always_reevaluate,
            use_numpy_backend=False,
            enable_undo=enable_undo,
            debug=debug,
            aggressive_debug=aggressive_debug,
        )

        # Stash the zarr-side state.
        self._store = _resolve_store(store)
        self._zarr_path = path
        self._owns_store_close = isinstance(store, (str, bytes)) or hasattr(store, "__fspath__")

        # Default dtype + codec for object storage.
        if dtype is None:
            dtype = self.DEFAULT_DTYPE
        if np.dtype(dtype) == object and object_codec is None:
            if _PickleCodec is None:
                raise ImportError(
                    "numcodecs is required for object dtype; "
                    "`pip install numcodecs`"
                )
            object_codec = _PickleCodec()
        self._dtype = np.dtype(dtype)
        self._fill_value = fill_value if fill_value is not None else (
            None if self._dtype == object else 0
        )

        # Try to open an existing group at this path; create if absent.
        self._zarr_group, self._zarr_arr, _created = self._open_or_create_group(
            chunks=chunks,
            compressor=compressor,
            object_codec=object_codec,
            zarr_mode=zarr_mode,
            overwrite=overwrite,
        )

        if _created:
            self._write_metadata_to_attrs()
        else:
            # Hydrate self.axes / self.named_cells / formulas from attrs,
            # and self.cells from the array data, so the Table view matches
            # what's on disk.
            self._restore_from_zarr()

        if self.aggressive_debug:
            print(
                f"[ZARR TABLE] backend={type(self._store).__name__} "
                f"path={self._zarr_path!r} shape={self.shape} "
                f"chunks={self._zarr_arr.chunks} dtype={self._zarr_arr.dtype}"
            )

    # ----- store/group setup -------------------------------------------------

    def _open_or_create_group(
        self,
        chunks,
        compressor,
        object_codec,
        zarr_mode: str,
        overwrite: bool,
    ) -> Tuple[Any, Any, bool]:
        """Open the group at self._zarr_path or create it. Returns
        (group, data_array, created_flag)."""

        # Open (or create) the group itself.
        if zarr_mode == "r":
            group = zarr.open_group(self._store, path=self._zarr_path, mode="r")
            arr_exists = _DATA_ARRAY_NAME in group
            if not arr_exists:
                raise PathNotFoundError(
                    f"No '{_DATA_ARRAY_NAME}' array under {self._zarr_path!r}"
                )
            arr = group[_DATA_ARRAY_NAME]
            return group, arr, False

        # For non-read modes, prefer open-or-create semantics.
        try:
            group = zarr.open_group(self._store, path=self._zarr_path, mode="a")
        except Exception:
            group = zarr.open_group(self._store, path=self._zarr_path, mode="w")

        arr_exists = _DATA_ARRAY_NAME in group
        if arr_exists and not overwrite and zarr_mode not in ("w",):
            arr = group[_DATA_ARRAY_NAME]
            return group, arr, False

        # Create the data array.
        target_shape = self.shape
        if not target_shape:
            raise ValueError(
                "Cannot create a new ZarrTable without shape or axes"
            )
        if isinstance(chunks, (list, tuple)):
            chunks = tuple(chunks)

        arr = group.create_dataset(
            name=_DATA_ARRAY_NAME,
            shape=target_shape,
            chunks=chunks,
            dtype=self._dtype,
            fill_value=self._fill_value,
            compressor=compressor,
            object_codec=object_codec,
            overwrite=True,
        )
        return group, arr, True

    # ----- metadata round-trip ----------------------------------------------

    def _write_metadata_to_attrs(self) -> None:
        meta = {
            "version": _SCHEMA_VERSION,
            "table_mode": self.mode,
            "lazy_eval": self.lazy_eval,
            "always_reevaluate": self.always_reevaluate,
            "axes": [_axis_to_dict(a) for a in self.axes],
            "named_cells": {
                name: list(int(i) for i in idx)
                for name, idx in self.named_cells.items()
            },
            "formulas": {},
        }
        self._zarr_group.attrs[_META_KEY] = meta

    def _restore_from_zarr(self) -> None:
        meta = self._zarr_group.attrs.get(_META_KEY)
        if meta is None:
            # Pre-existing zarr array without nd_table metadata — wrap it
            # using whatever axes the user passed in (or default ones based
            # on array shape).
            return

        # Axes
        axes = [_axis_from_dict(d) for d in meta.get("axes", [])]
        if axes:
            self.axes = axes
            self._setup_spreadsheet_labels()

        # Table-level flags (preserve user-passed values if attrs is silent).
        if "table_mode" in meta:
            self.mode = meta["table_mode"]
        if "lazy_eval" in meta:
            self.lazy_eval = bool(meta["lazy_eval"])
        if "always_reevaluate" in meta:
            self.always_reevaluate = bool(meta["always_reevaluate"])

        # Named cells
        self.named_cells = {
            name: tuple(int(i) for i in idx)
            for name, idx in meta.get("named_cells", {}).items()
        }

        # Hydrate self.cells. We walk every position in the zarr array
        # (cheap for the small tables nd_table is typically used with;
        # users who want lazy access can read directly from zarr_array).
        formulas = meta.get("formulas", {})
        arr = self._zarr_arr
        self.cells = {}
        for arr_pos in np.ndindex(*arr.shape):
            value = arr[arr_pos]
            if self._is_empty(value):
                # Still create a Cell if there's a formula or name pointing
                # here; otherwise skip.
                idx = self._array_pos_to_idx(arr_pos)
                key = _idx_to_key(idx)
                if key in formulas:
                    self.cells[idx] = Cell(formula=formulas[key])
                continue
            idx = self._array_pos_to_idx(arr_pos)
            key = _idx_to_key(idx)
            cell = Cell(raw_value=value)
            if key in formulas:
                cell.formula = formulas[key]
            self.cells[idx] = cell

        # Re-link named-cell -> cell.name so get_cell_by_name continues
        # to work and renders honor names.
        for name, idx in self.named_cells.items():
            cell = self.cells.get(idx)
            if cell is None:
                cell = Cell(name=name)
                self.cells[idx] = cell
            else:
                cell.name = name

    def _is_empty(self, value) -> bool:
        if value is None and (self._fill_value is None):
            return True
        if self._dtype == object:
            return value is None
        try:
            return value == self._fill_value
        except Exception:
            return False

    def _array_pos_to_idx(self, arr_pos: Tuple[int, ...]) -> Tuple[int, ...]:
        return tuple(self.axes[i].indices[p] for i, p in enumerate(arr_pos))

    # ----- read fallback to zarr --------------------------------------------

    def __getitem__(self, key):
        """Override: if the cells mirror has nothing for this position,
        fall back to the zarr-side value (which may be the fill_value or
        a value written via write_region with mirror_cells=False)."""
        result = super().__getitem__(key)
        if result is not None:
            return result
        # Translate the key to an array position; bail on anything that
        # isn't a simple cell access (slices, cross-table, etc).
        try:
            from .ndtable import CellReference
            if isinstance(key, str) and key in self.named_cells:
                key = self.named_cells[key]
            if isinstance(key, CellReference):
                key = key.ref
            if isinstance(key, list):
                key = tuple(key)
            idx = self._normalize_index(key)
        except Exception:
            return None
        if not isinstance(idx, tuple) or any(isinstance(i, slice) for i in idx):
            return None
        try:
            arr_pos = self._array_position(idx)
        except (ValueError, IndexError):
            return None
        zv = self._zarr_arr[arr_pos]
        # For object dtype, treat None as "no cell here". For numeric
        # dtypes the fill_value is a real value the user is entitled to
        # read back, so return it as-is.
        if self._dtype == object and zv is None:
            return None
        return zv

    # ----- write-through hook -----------------------------------------------

    def _set_cell(self, idx, value):
        """Override: delegate to Table, then mirror the resulting state
        into the zarr array (and persist formulas via attrs)."""
        if isinstance(idx, list):
            idx = tuple(idx)

        # Let the parent handle: undo recording, dependency invalidation,
        # formula parsing, and self.cells mutation.
        super()._set_cell(idx, value)

        # Now mirror the post-state into zarr.
        try:
            arr_pos = self._array_position(idx)
        except (ValueError, IndexError):
            # Index falls outside the array shape — e.g. add_row appended
            # without resizing the zarr backend. Resize on demand.
            self._resize_to_cover(idx)
            arr_pos = self._array_position(idx)

        cell = self.cells.get(idx)
        if cell is None:
            self._zarr_arr[arr_pos] = self._fill_value
        elif cell.formula:
            # Try to write the cached value too so the array reflects
            # what a fresh Reader would compute; fall back to fill if the
            # formula hasn't been evaluated yet.
            raw = cell._cached_value if cell._evaluated else cell.raw_value
            self._zarr_arr[arr_pos] = raw if raw is not None else self._fill_value
            self._set_formula_attr(idx, cell.formula)
        else:
            self._zarr_arr[arr_pos] = (
                cell.raw_value if cell.raw_value is not None else self._fill_value
            )
            self._clear_formula_attr(idx)

    def _set_formula_attr(self, idx, formula: str) -> None:
        meta = dict(self._zarr_group.attrs.get(_META_KEY, {}))
        formulas = dict(meta.get("formulas", {}))
        formulas[_idx_to_key(tuple(int(i) for i in idx))] = formula
        meta["formulas"] = formulas
        self._zarr_group.attrs[_META_KEY] = meta

    def _clear_formula_attr(self, idx) -> None:
        meta = dict(self._zarr_group.attrs.get(_META_KEY, {}))
        formulas = dict(meta.get("formulas", {}))
        key = _idx_to_key(tuple(int(i) for i in idx))
        if key in formulas:
            del formulas[key]
            meta["formulas"] = formulas
            self._zarr_group.attrs[_META_KEY] = meta

    def _resize_to_cover(self, idx) -> None:
        """Grow the zarr array if a write lands past its current shape.
        Triggered by add_row/add_column/add_depth followed by a write."""
        new_shape = tuple(len(a) for a in self.axes)
        if new_shape != self._zarr_arr.shape:
            self._zarr_arr.resize(new_shape)
            if self.aggressive_debug:
                print(f"[ZARR TABLE] resized data to {new_shape}")

    def name_cell(self, idx, name: str) -> None:
        super().name_cell(idx, name)
        # Persist updated named-cells map.
        meta = dict(self._zarr_group.attrs.get(_META_KEY, {}))
        meta["named_cells"] = {
            n: list(int(i) for i in ix) for n, ix in self.named_cells.items()
        }
        self._zarr_group.attrs[_META_KEY] = meta

    # ----- bulk region API (zarr's superpower) ------------------------------

    def write_region(
        self,
        slices: Union[Sequence[slice], Tuple],
        data: np.ndarray,
        mirror_cells: bool = True,
    ) -> None:
        """Bulk-write a numpy region into the underlying zarr array.

        Faster than per-cell setitem for big writes — only the relevant
        chunks are touched. By default also mirrors the values into
        `self.cells` so the rest of the nd_table layer sees them; pass
        `mirror_cells=False` to skip that (useful for write-then-forget
        bulk loads where you'll re-open later).
        """
        slices = tuple(slices)
        data = np.asarray(data)
        self._zarr_arr[slices] = data

        if not mirror_cells:
            return

        # Walk the region and mirror into cells.
        # zarr Array slices accept plain slices; convert to numpy-style
        # ranges so we can re-emit indices.
        ranges = []
        for axis_i, sl in enumerate(slices):
            if isinstance(sl, slice):
                start, stop, step = sl.indices(self._zarr_arr.shape[axis_i])
                ranges.append(list(range(start, stop, step)))
            else:
                ranges.append([int(sl)])
        from itertools import product
        for arr_pos in product(*ranges):
            idx = self._array_pos_to_idx(arr_pos)
            # Index into data using the same relative offsets.
            data_pos = tuple(
                ranges[i].index(arr_pos[i]) for i in range(len(ranges))
            )
            try:
                value = data[data_pos] if data.shape else data.item()
            except IndexError:
                value = data  # broadcast scalar
            self.cells[idx] = Cell(raw_value=value)

    def read_region(self, slices: Union[Sequence[slice], Tuple]) -> np.ndarray:
        """Read a region from zarr as a numpy array (loads only the
        chunks the slice intersects)."""
        return self._zarr_arr[tuple(slices)]

    # ----- inspection / control --------------------------------------------

    @property
    def zarr_array(self):
        return self._zarr_arr

    @property
    def zarr_group(self):
        return self._zarr_group

    @property
    def store(self):
        return self._store

    @property
    def chunks(self) -> Tuple[int, ...]:
        return tuple(self._zarr_arr.chunks)

    @property
    def nchunks(self) -> int:
        return self._zarr_arr.nchunks

    @property
    def info(self) -> str:
        return str(self._zarr_arr.info)

    def sync(self) -> None:
        """Flush any buffered attrs/data. Most stores write synchronously
        so this is usually a no-op; ZipStore and consolidated metadata
        benefit from it."""
        # Touch the attrs to force a write-through on stores that defer.
        # zarr re-serializes .zattrs on every assignment, so just
        # re-assigning the existing meta dict is enough.
        current = self._zarr_group.attrs.get(_META_KEY)
        if current is not None:
            self._zarr_group.attrs[_META_KEY] = current

    def consolidate_metadata(self):
        """Consolidate group metadata into a single .zmetadata key for
        fast remote opens. Returns the consolidated group."""
        return zarr.consolidate_metadata(self._store, path=self._zarr_path)

    def close(self) -> None:
        """Close the underlying store. Required for ZipStore. Safe to
        call on any store; subsequent reads/writes will fail."""
        if hasattr(self._store, "close"):
            try:
                self._store.close()
            except Exception:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ----- copy / convert ---------------------------------------------------

    def copy_to(self, other_store, other_path: str = "") -> "ZarrTable":
        """Copy this table's group (data + attrs) into another store."""
        target_store = _resolve_store(other_store)
        zarr.copy(
            source=self._zarr_group,
            dest=zarr.open_group(target_store, path=other_path, mode="a"),
            name=None,
            log=None,
            if_exists="replace",
        )
        return ZarrTable.open(target_store, path=other_path, mode="r+")

    def to_numpy(self, fill_value=None) -> np.ndarray:
        """Override: read straight from zarr instead of walking
        self.cells. Loads the whole array into memory — for big tables
        prefer read_region()."""
        if fill_value is None:
            return self._zarr_arr[...]
        # For non-default fill, write into a fresh array.
        out = np.full(self.shape, fill_value, dtype=self._dtype)
        chunk = self._zarr_arr[...]
        if self._dtype == object:
            mask = np.vectorize(lambda v: v is not None)(chunk)
        else:
            mask = chunk != self._fill_value
        out[mask] = chunk[mask]
        return out

    # ----- class methods ----------------------------------------------------

    @classmethod
    def open(
        cls,
        store,
        path: str = "",
        mode: str = "r+",
        **table_kwargs,
    ) -> "ZarrTable":
        """Reopen an existing Zarr-backed table.

        `mode='r'` opens read-only. `mode='r+'` opens read/write.
        Any keyword arg accepted by Table.__init__ (lazy_eval,
        aggressive_debug, ...) can be passed through.
        """
        _require_zarr()
        resolved = _resolve_store(store)
        group = zarr.open_group(resolved, path=path, mode=mode)
        if _DATA_ARRAY_NAME not in group:
            raise PathNotFoundError(
                f"No nd_table data array under {path!r} in {store!r}"
            )
        arr = group[_DATA_ARRAY_NAME]
        meta = group.attrs.get(_META_KEY, {})

        if meta.get("axes"):
            axes = [_axis_from_dict(d) for d in meta["axes"]]
            shape = None
        else:
            axes = None
            shape = arr.shape

        zt = cls(
            store=resolved,
            path=path,
            shape=shape,
            axes=axes,
            dtype=arr.dtype,
            zarr_mode=mode,
            **table_kwargs,
        )
        return zt

    @classmethod
    def from_table(
        cls,
        source: Table,
        store,
        path: str = "",
        chunks: Union[Tuple, List, bool, None] = True,
        dtype: Any = None,
        overwrite: bool = True,
        **kwargs,
    ) -> "ZarrTable":
        """Snapshot an existing Table into a new Zarr-backed table.

        Cells, formulas, named cells, and axes are all copied. The
        source table is not mutated.
        """
        # Clone axes (cheap; avoids shared references).
        axes = [_axis_from_dict(_axis_to_dict(a)) for a in source.axes]

        zt = cls(
            store=store,
            path=path,
            axes=axes,
            chunks=chunks,
            dtype=dtype,
            overwrite=overwrite,
            mode=getattr(source, "mode", "normal"),
            lazy_eval=source.lazy_eval,
            always_reevaluate=source.always_reevaluate,
            enable_undo=source.undo_system is not None,
            debug=source.debug,
            aggressive_debug=source.aggressive_debug,
        )

        # Replay cells through the public API so dependencies + formulas
        # come along intact.
        for idx, cell in source.cells.items():
            if cell.formula:
                zt[idx] = "=" + cell.formula
            elif cell.raw_value is not None:
                zt[idx] = cell.raw_value

        for name, idx in source.named_cells.items():
            zt.name_cell(idx, name)

        return zt


__all__ = ["ZarrTable"]
