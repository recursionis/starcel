"""Shared utility functions used across multiple modules."""
from __future__ import annotations

from typing import Optional


# Human-readable byte sizes

def human_size(n) -> Optional[str]:
    """Convert byte count to human-readable string, e.g. '22.51 MB'.

    Returns None if *n* is None; returns '?' on conversion failure.
    """
    if n is None:
        return None
    try:
        val = float(n)
    except (TypeError, ValueError):
        return '?'
    if val == 0:
        return '0 B'
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if val < 1024.0 or unit == 'TB':
            return f"{val:.2f} {unit}" if unit != 'B' else f"{int(val)} B"
        val /= 1024.0
    return f"{val:.2f} PB"
