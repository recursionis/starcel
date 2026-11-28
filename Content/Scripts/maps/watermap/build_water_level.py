"""
build_water_level.py — places a UE Water Body Ocean in the open level
(editor only, not during Play).

Why not spawn the ocean at Play time from pyactor_main: water bodies are
built by the editor when placed — the Water plugin's actor factory sets up
the ocean's spline, collision and default Gerstner waves, and the Water
editor module adds the WaterMeshActor that renders it. A plain runtime
spawn skips all of that and draws nothing. EditorLevelLibrary.
SpawnActorFromClass goes through the same factory as dragging the actor
in from Place Actors, so this script does exactly what the manual step
would.

Run once with WaterMap open, from the Python console:
    import importlib, maps.watermap.build_water_level as b; importlib.reload(b); b.build()
It does nothing if the level already has a water body. Then press Play:
maps.watermap.pyactor_main finds the ocean, links it to the WaterPhysics
plugin and floats the icon balls on its waves.
"""

import unreal_engine as ue
from unreal_engine import FVector, FRotator


OCEAN_LOCATION = (0.0, 0.0, 0.0)
OCEAN_WAVES = '/Water/Waves/GerstnerWaves_Ocean.GerstnerWaves_Ocean'
OCEAN_MATERIAL = '/Water/Materials/WaterSurface/Water_Material_Ocean.Water_Material_Ocean'
FAR_MESH_MATERIAL = '/Water/Materials/WaterSurface/Water_FarMesh.Water_FarMesh'
UNDERWATER_MATERIAL = ('/Water/Materials/PostProcessing/M_UnderWater_PostProcess_Volume.'
                       'M_UnderWater_PostProcess_Volume')


def _water_bodies(world):
    body_cls = ue.find_class('WaterBody')
    found = []
    for a in world.all_actors():
        try:
            cls = a.get_class().get_name()
            if cls.startswith('WaterPhysics'):
                continue
            if body_cls is not None and a.is_a(body_cls):
                found.append(a)
        except Exception:
            continue
    return found


def _ensure_waves(ocean):
    """The factory normally assigns the default ocean waves; if it didn't,
    assign /Water/Waves/GerstnerWaves_Ocean ourselves."""
    try:
        if ocean.GetMaxWaveHeight() > 0.0:
            return True
    except Exception:
        pass
    try:
        asset = ue.load_object(ue.find_class('WaterWavesAsset'), OCEAN_WAVES)
        ref = ue.new_object(ue.find_class('WaterWavesAssetReference'), ocean)
        try:
            ref.SetWaterWavesAsset(asset)
        except Exception:
            ref.WaterWavesAsset = asset
        ocean.SetWaterWaves(ref)
        ue.log(f'build_water_level: assigned waves {OCEAN_WAVES}')
        return True
    except Exception as e:
        ue.log_warning(f'build_water_level: could not assign waves ({e}). Select the '
                       f'ocean and set Water Waves > GerstnerWaves_Ocean by hand.')
        return False


def _ensure_material(ocean):
    """Ocean/lake/river bodies are drawn by the WaterMeshActor using the
    body's WaterMaterial; the editor factory assigns a default one, a
    scripted spawn may not."""
    from unreal_engine.classes import MaterialInterface
    try:
        if ocean.GetWaterMaterial() is not None:
            return
    except Exception:
        pass
    try:
        ocean.WaterMaterial = ue.load_object(MaterialInterface, OCEAN_MATERIAL)
        ue.log(f'build_water_level: assigned material {OCEAN_MATERIAL}')
    except Exception as e:
        ue.log_warning(f'build_water_level: could not assign water material ({e}); '
                       f'set Water Material > Water_Material_Ocean on the ocean by hand')
    try:
        ocean.UnderwaterPostProcessMaterial = ue.load_object(
            MaterialInterface, UNDERWATER_MATERIAL)
    except Exception:
        pass   # optional: only affects looking from below the surface


def _ensure_water_mesh(world):
    """Spawn the WaterMeshActor (the actor that actually renders ocean,
    lake and river surfaces) if the level doesn't have one."""
    from unreal_engine.classes import EditorLevelLibrary, MaterialInterface
    for a in world.all_actors():
        try:
            if a.get_class().get_name() == 'WaterMeshActor':
                return a
        except Exception:
            continue
    cls = ue.find_class('WaterMeshActor')
    if cls is None:
        ue.log_warning('build_water_level: WaterMeshActor class not found; '
                       'the ocean will not render')
        return None
    mesh = EditorLevelLibrary.SpawnActorFromClass(
        cls, FVector(0, 0, 0), FRotator(0, 0, 0), False)
    try:
        mesh.FarDistanceMaterial = ue.load_object(MaterialInterface, FAR_MESH_MATERIAL)
    except Exception:
        pass
    ue.log(f'build_water_level: spawned {mesh.get_name()} (renders the water surface)')
    return mesh


def _ensure_water_physics(world, ocean):
    """Place a "Water Physics - UE4 Water Body" actor with the ocean in its
    Water Bodies list. It must exist BEFORE Play: it binds to the ocean's
    overlap events in BeginPlay, so one spawned at runtime (and filled in
    afterwards) never sees the balls enter the water."""
    from unreal_engine.classes import EditorLevelLibrary
    from unreal_engine.structs import WaterBodySetup
    physics = None
    for a in world.all_actors():
        try:
            if a.get_class().get_name() == 'WaterPhysics_WaterBody':
                physics = a
                break
        except Exception:
            continue
    if physics is None:
        cls = ue.find_class('WaterPhysics_WaterBody')
        if cls is None:
            ue.log_warning('build_water_level: WaterPhysics_WaterBody class not found '
                           '(is the WaterPhysics plugin enabled?)')
            return None
        physics = EditorLevelLibrary.SpawnActorFromClass(
            cls, FVector(0, 0, 0), FRotator(0, 0, 0), False)
        ue.log(f'build_water_level: placed {physics.get_name()}')
    try:
        physics.WaterBodies = [WaterBodySetup(WaterBody=ocean, bIncludeWaves=True,
                                              bUseSimpleWaves=True, bIncludeVelocity=True)]
        physics.post_edit_change()
        ue.log(f'build_water_level: {physics.get_name()} Water Bodies = [{ocean.get_name()}]')
    except Exception as e:
        ue.log_warning(f'build_water_level: could not set Water Bodies ({e}). Select '
                       f'{physics.get_name()} and add {ocean.get_name()} to its '
                       f'"Water Bodies" list by hand.')
    return physics


def build(save=True):
    """Place (or repair) the ocean: water body, waves, material and the
    WaterMeshActor that draws it. Safe to run again."""
    from unreal_engine.classes import EditorLevelLibrary

    world = ue.get_editor_world()
    existing = [a for a in _water_bodies(world)
                if a.get_class().get_name() == 'WaterBodyOcean']
    if existing:
        ocean = existing[0]
        ue.log(f'build_water_level: repairing existing {ocean.get_name()}')
    else:
        cls = ue.find_class('WaterBodyOcean')
        if cls is None:
            raise RuntimeError('build_water_level: WaterBodyOcean class not found '
                               '(is the Water plugin enabled?)')
        x, y, z = OCEAN_LOCATION
        ocean = EditorLevelLibrary.SpawnActorFromClass(
            cls, FVector(x, y, z), FRotator(0, 0, 0), False)
        if ocean is None:
            raise RuntimeError('build_water_level: SpawnActorFromClass returned None')
        ue.log(f'build_water_level: placed {ocean.get_name()} at {OCEAN_LOCATION}')

    _ensure_waves(ocean)
    _ensure_material(ocean)
    mesh = _ensure_water_mesh(world)

    # Re-run the body's editor update so the mesh picks up the material.
    for obj in (ocean, mesh):
        if obj is None:
            continue
        try:
            obj.post_edit_change()
        except Exception:
            pass
    try:
        mesh.MarkWaterMeshComponentForRebuild()
    except Exception:
        pass

    _ensure_water_physics(world, ocean)

    if save:
        try:
            EditorLevelLibrary.SaveCurrentLevel()
            ue.log('build_water_level: level saved')
        except Exception as e:
            ue.log_warning(f'build_water_level: save failed ({e}); press Ctrl+S')
    return ocean
