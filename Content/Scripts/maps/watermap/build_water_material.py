"""
build_water_material.py — builds /Game/Materials/M_MovingWater (editor only).

A cheap, opaque, animated water surface meant for a huge flat plane
(e.g. the engine Plane at scale 100,100,100 = 10,000 x 10,000 UU).

Why world-aligned UVs: the plane's own UVs stretch 0..1 across the whole
mesh, so a texture would be blown up 100x. Instead the ripples are sampled
from WorldPosition.xy / TileSize, so they keep the same real-world size no
matter how far the plane is scaled, and neighbouring planes line up.

Graph
    UV       = WorldPosition.xy / TileSize
    Normal A = WaveNormal( Panner(UV,       SpeedA) )           small ripples
    Normal B = WaveNormal( Panner(UV * 0.27, SpeedB) )          big slow swells
    N        = lerp( (0,0,1), (A + B) * 0.5, NormalStrength )   flatten/sharpen
    Base     = lerp( DeepColor, ShallowColor, Fresnel )
    Roughness/Specular params, Metallic 0, opaque, default lit.

Note: the engine Plane mesh is only 2 triangles, so there is no geometry
to displace — the motion is all in the normal map (no World Position
Offset).

Run once in the editor (not during Play), from the Python console:
    import maps.watermap.build_water_material as b; b.build()
Running it again rebuilds the graph in place. Then drag M_MovingWater
onto the plane (or set it in the plane's Materials slot).
"""

import unreal_engine as ue
from unreal_engine import FLinearColor


MATERIAL_PATH = '/Game/Materials/M_MovingWater'

# Tiling wave normal from the engine's Water plugin (enabled in this
# project); falls back to the imported 4k wave normal.
NORMAL_TEXTURES = [
    '/Water/Textures/Normals/T_Water_TilingNormal_Waves_02.T_Water_TilingNormal_Waves_02',
    '/Game/Models/4kWave_Normal.4kWave_Normal',
]

# EMaterialSamplerType::SAMPLERTYPE_Normal
_SAMPLERTYPE_NORMAL = 3


def _node(cls, mat, x, y):
    n = cls('', mat)
    n.MaterialExpressionEditorX = x
    n.MaterialExpressionEditorY = y
    return n


def _scalar(mat, name, value, x, y):
    from unreal_engine.classes import MaterialExpressionScalarParameter
    n = _node(MaterialExpressionScalarParameter, mat, x, y)
    n.ParameterName = name
    n.DefaultValue = value
    return n


def _vector(mat, name, rgba, x, y):
    from unreal_engine.classes import MaterialExpressionVectorParameter
    n = _node(MaterialExpressionVectorParameter, mat, x, y)
    n.ParameterName = name
    n.DefaultValue = FLinearColor(*rgba)
    return n


def _load_normal_texture():
    from unreal_engine.classes import Texture2D
    for path in NORMAL_TEXTURES:
        try:
            tex = ue.load_object(Texture2D, path)
        except Exception:
            tex = None
        if tex is not None:
            ue.log(f'build_water_material: wave normal {path}')
            return tex
    raise RuntimeError('build_water_material: no wave normal texture found in '
                       + ', '.join(NORMAL_TEXTURES))


def build():
    from unreal_engine.classes import (
        Material, MaterialFactoryNew,
        MaterialExpressionWorldPosition, MaterialExpressionDivide,
        MaterialExpressionMultiply, MaterialExpressionAdd,
        MaterialExpressionPanner, MaterialExpressionTextureSample,
        MaterialExpressionConstant3Vector, MaterialExpressionConstant,
        MaterialExpressionLinearInterpolate, MaterialExpressionFresnel,
    )
    from unreal_engine.structs import (
        ExpressionInput, ColorMaterialInput, ScalarMaterialInput,
        VectorMaterialInput,
    )

    normal_tex = _load_normal_texture()

    name = MATERIAL_PATH.split('/')[-1]
    mat = None
    try:
        mat = ue.load_object(Material, f'{MATERIAL_PATH}.{name}')
    except Exception:
        mat = None
    if mat is None:
        mat = MaterialFactoryNew().factory_create_new(MATERIAL_PATH)
        ue.log(f'build_water_material: created {MATERIAL_PATH}')
    else:
        ue.log(f'build_water_material: rebuilding {MATERIAL_PATH}')
    mat.modify()

    def rgb(e):
        return ExpressionInput(Expression=e, Mask=1, MaskR=1, MaskG=1, MaskB=1)

    def rg(e):
        return ExpressionInput(Expression=e, Mask=1, MaskR=1, MaskG=1)

    def inp(e):
        return ExpressionInput(Expression=e)

    # --- world-aligned UVs ------------------------------------------------
    wpos = _node(MaterialExpressionWorldPosition, mat, -1900, 0)
    tile = _scalar(mat, 'TileSize', 1500.0, -1900, 150)   # UU per texture repeat
    uv = _node(MaterialExpressionDivide, mat, -1700, 0)
    uv.A = rg(wpos)
    uv.B = inp(tile)

    # --- two panning normal samples --------------------------------------
    pan_a = _node(MaterialExpressionPanner, mat, -1450, -150)
    pan_a.Coordinate = inp(uv)
    pan_a.SpeedX = 0.015
    pan_a.SpeedY = 0.010

    big_scale = _node(MaterialExpressionConstant, mat, -1700, 250)
    big_scale.R = 0.27
    uv_big = _node(MaterialExpressionMultiply, mat, -1550, 200)
    uv_big.A = inp(uv)
    uv_big.B = inp(big_scale)
    pan_b = _node(MaterialExpressionPanner, mat, -1350, 200)
    pan_b.Coordinate = inp(uv_big)
    pan_b.SpeedX = -0.006
    pan_b.SpeedY = 0.009

    samp_a = _node(MaterialExpressionTextureSample, mat, -1150, -150)
    samp_a.Texture = normal_tex
    samp_a.SamplerType = _SAMPLERTYPE_NORMAL
    samp_a.Coordinates = inp(pan_a)

    samp_b = _node(MaterialExpressionTextureSample, mat, -1150, 200)
    samp_b.Texture = normal_tex
    samp_b.SamplerType = _SAMPLERTYPE_NORMAL
    samp_b.Coordinates = inp(pan_b)

    n_sum = _node(MaterialExpressionAdd, mat, -900, 0)
    n_sum.A = rgb(samp_a)
    n_sum.B = rgb(samp_b)
    half = _node(MaterialExpressionConstant, mat, -900, 120)
    half.R = 0.5
    n_avg = _node(MaterialExpressionMultiply, mat, -750, 0)
    n_avg.A = inp(n_sum)
    n_avg.B = inp(half)

    flat = _node(MaterialExpressionConstant3Vector, mat, -750, -150)
    flat.Constant = FLinearColor(0.0, 0.0, 1.0, 1.0)
    strength = _scalar(mat, 'NormalStrength', 0.8, -750, 150)
    normal = _node(MaterialExpressionLinearInterpolate, mat, -550, 0)
    normal.A = inp(flat)
    normal.B = inp(n_avg)
    normal.Alpha = inp(strength)

    # --- colour: deep looking down, lighter at grazing angles -------------
    deep = _vector(mat, 'DeepColor', (0.004, 0.035, 0.06, 1.0), -750, -450)
    shallow = _vector(mat, 'ShallowColor', (0.03, 0.17, 0.22, 1.0), -750, -300)
    fresnel = _node(MaterialExpressionFresnel, mat, -550, -200)
    fresnel.Exponent = 5.0
    fresnel.BaseReflectFraction = 0.04
    base = _node(MaterialExpressionLinearInterpolate, mat, -350, -350)
    base.A = rgb(deep)
    base.B = rgb(shallow)
    base.Alpha = inp(fresnel)

    roughness = _scalar(mat, 'Roughness', 0.06, -350, 150)
    specular = _scalar(mat, 'Specular', 0.8, -350, 250)
    metallic = _node(MaterialExpressionConstant, mat, -350, 350)
    metallic.R = 0.0

    mat.Expressions = [
        wpos, tile, uv, pan_a, big_scale, uv_big, pan_b, samp_a, samp_b,
        n_sum, half, n_avg, flat, strength, normal,
        deep, shallow, fresnel, base, roughness, specular, metallic,
    ]
    mat.BaseColor = ColorMaterialInput(Expression=base)
    mat.Normal = VectorMaterialInput(Expression=normal)
    mat.Roughness = ScalarMaterialInput(Expression=roughness)
    mat.Specular = ScalarMaterialInput(Expression=specular)
    mat.Metallic = ScalarMaterialInput(Expression=metallic)

    mat.post_edit_change()
    mat.save_package()
    ue.log(f'build_water_material: saved {MATERIAL_PATH}')
    return mat
