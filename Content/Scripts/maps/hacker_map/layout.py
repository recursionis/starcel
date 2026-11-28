"""
layout.py — where the panels go: one fixed screen, like the video.

Panel rectangles are in reference-video pixels (1920x1080), measured from
m2-res_1080p.mp4. 1 px = theme.S UU on the wall (S is derived from the
smallest usable Cesium globe, see theme.py).

The camera is fixed at CAMERA_LOC looking +X with a 90 deg horizontal field
of view; the wall sits exactly WALL_W / 2 in front of it, so the 1920 px
wide layout fills the screen edge to edge.
"""

import math

from unreal_engine import FVector

from maps.hacker_map.theme import S, rot

# x, y, w, h in reference-video pixels
PANELS = {
    'system':     (12,   36, 300, 676),
    'network':    (326,  36, 300, 676),
    'terminal':   (640,  40, 1266, 668),
    'filesystem': (12,  748, 828, 316),
    'keyboard':   (868, 748, 1040, 316),
}
SCREEN_W, SCREEN_H = 1920, 1080

FOV = 90.0
WALL_W = SCREEN_W * S
WALL_H = SCREEN_H * S
WALL_X = (WALL_W / 2.0) / math.tan(math.radians(FOV / 2.0))   # wall fills the view
WALL_Z = 0.0
CAMERA_LOC = FVector(0.0, 0.0, WALL_Z)


def flat_pivot(rect):
    """Top-left of a panel on the wall."""
    x, y, w, h = rect
    return FVector(WALL_X, -WALL_W / 2.0 + x * S, WALL_Z + WALL_H / 2.0 - y * S)


def camera_spot():
    return FVector(CAMERA_LOC.x, CAMERA_LOC.y, CAMERA_LOC.z), rot()


def push_back(point, back):
    """Move a wall-space *point* *back* UU further from the camera along the
    camera ray, returning (new_point, scale) where scale keeps its on-screen
    size the same. Used for things that should sit deep behind the panel
    plane (the Starcel logo) but still look like part of the screen."""
    c = CAMERA_LOC
    dx = point.x - c.x
    if dx <= 1.0:
        return point, 1.0
    k = (dx + back) / dx
    return FVector(c.x + (point.x - c.x) * k, c.y + (point.y - c.y) * k,
                   c.z + (point.z - c.z) * k), k
