"""
build_rice_material.py — builds /Game/Materials/M_RiceIcon (editor only).

Why a new material: the rice grain mesh (rice grain.fbx) has NO UV layer,
so any material that samples a texture by UV (M_TexturePicture) reads a
single pixel across the whole grain. M_RiceIcon makes its own UVs instead:
it projects the icon flat onto the grain's broad face, using the grain's
local-space position.

Graph
    WorldPosition -> TransformPosition(World -> Local) = P
    U = dot(P, IconU.rgb) + IconUOffset
    V = dot(P, IconV.rgb) + IconVOffset
    Texture sampled at saturate(U, V)     (clamped: edge pixels repeat)
    BaseColor = lerp(RiceColor, Texture.rgb, Texture.a * IconStrength)
    Emissive  = Fresnel * RimColor * RimStrength   (soft translucent rim)
    Roughness = Roughness param,  Specular = Specular param, two-sided

IconU / IconV / offsets are set per grain by maps.rice_bowl.pyactor_main
from the mesh bounds, so the icon stays square and centred whatever way
the grain was imported.

Run once in the editor (not during Play), from the Python console:
    import maps.rice_bowl.build_rice_material as b; b.build()
Running it again rebuilds the graph in place.
"""

import unreal_engine as ue
from unreal_engine import FLinearColor


MATERIAL_PATH   = '/Game/Materials/M_RiceIcon'
DEFAULT_TEXTURE = '/Engine/EngineResources/DefaultTexture.DefaultTexture'

# EMaterialPositionTransformSource
_TRANSFORMPOSSOURCE_LOCAL = 0
_TRANSFORMPOSSOURCE_WORLD = 1


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


def build():
    from unreal_engine.classes import (
        Material, MaterialFactoryNew, Texture2D,
        MaterialExpressionWorldPosition, MaterialExpressionTransformPosition,
        MaterialExpressionDotProduct, MaterialExpressionAdd,
        MaterialExpressionAppendVector, MaterialExpressionSaturate,
        MaterialExpressionTextureSampleParameter2D,
        MaterialExpressionMultiply, MaterialExpressionLinearInterpolate,
        MaterialExpressionFresnel,
    )
    from unreal_engine.structs import (
        ExpressionInput, ColorMaterialInput, ScalarMaterialInput,
    )

    name = MATERIAL_PATH.split('/')[-1]
    mat = None
    try:
        mat = ue.load_object(Material, f'{MATERIAL_PATH}.{name}')
    except Exception:
        mat = None
    if mat is None:
        mat = MaterialFactoryNew().factory_create_new(MATERIAL_PATH)
        ue.log(f'build_rice_material: created {MATERIAL_PATH}')
    else:
        ue.log(f'build_rice_material: rebuilding {MATERIAL_PATH}')
    mat.modify()

    def rgb(e):
        return ExpressionInput(Expression=e, Mask=1, MaskR=1, MaskG=1, MaskB=1)

    def alpha(e):
        return ExpressionInput(Expression=e, Mask=1, MaskA=1)

    # --- projection: local position -> icon UV --------------------------
    wpos = _node(MaterialExpressionWorldPosition, mat, -1800, 0)
    lpos = _node(MaterialExpressionTransformPosition, mat, -1600, 0)
    lpos.Input = ExpressionInput(Expression=wpos)
    lpos.TransformSourceType = _TRANSFORMPOSSOURCE_WORLD
    lpos.TransformType = _TRANSFORMPOSSOURCE_LOCAL

    icon_u = _vector(mat, 'IconU', (0.0, 0.0, 0.01, 0.0), -1600, -250)
    icon_v = _vector(mat, 'IconV', (0.01, 0.0, 0.0, 0.0), -1600, 250)
    u_off = _scalar(mat, 'IconUOffset', 0.5, -1350, -150)
    v_off = _scalar(mat, 'IconVOffset', 0.5, -1350, 150)

    dot_u = _node(MaterialExpressionDotProduct, mat, -1350, -50)
    dot_u.A = ExpressionInput(Expression=lpos)
    dot_u.B = rgb(icon_u)
    dot_v = _node(MaterialExpressionDotProduct, mat, -1350, 50)
    dot_v.A = ExpressionInput(Expression=lpos)
    dot_v.B = rgb(icon_v)

    add_u = _node(MaterialExpressionAdd, mat, -1150, -50)
    add_u.A = ExpressionInput(Expression=dot_u)
    add_u.B = ExpressionInput(Expression=u_off)
    add_v = _node(MaterialExpressionAdd, mat, -1150, 50)
    add_v.A = ExpressionInput(Expression=dot_v)
    add_v.B = ExpressionInput(Expression=v_off)

    uv = _node(MaterialExpressionAppendVector, mat, -950, 0)
    uv.A = ExpressionInput(Expression=add_u)
    uv.B = ExpressionInput(Expression=add_v)
    uv_clamped = _node(MaterialExpressionSaturate, mat, -800, 0)
    uv_clamped.Input = ExpressionInput(Expression=uv)

    # --- icon over rice -------------------------------------------------
    tex = _node(MaterialExpressionTextureSampleParameter2D, mat, -600, 0)
    tex.ParameterName = 'Texture'
    tex.Texture = ue.load_object(Texture2D, DEFAULT_TEXTURE)
    tex.Coordinates = ExpressionInput(Expression=uv_clamped)

    strength = _scalar(mat, 'IconStrength', 1.0, -600, 250)
    icon_alpha = _node(MaterialExpressionMultiply, mat, -350, 150)
    icon_alpha.A = alpha(tex)
    icon_alpha.B = ExpressionInput(Expression=strength)

    rice_color = _vector(mat, 'RiceColor', (0.93, 0.91, 0.84, 1.0), -600, -250)
    base = _node(MaterialExpressionLinearInterpolate, mat, -150, 0)
    base.A = rgb(rice_color)
    base.B = rgb(tex)
    base.Alpha = ExpressionInput(Expression=icon_alpha)

    # --- soft rim: fakes the slightly translucent edge of a rice grain ---
    fresnel = _node(MaterialExpressionFresnel, mat, -600, 450)
    fresnel.Exponent = 3.0
    rim_color = _vector(mat, 'RimColor', (1.0, 0.98, 0.92, 1.0), -600, 600)
    rim_strength = _scalar(mat, 'RimStrength', 0.15, -600, 750)
    rim = _node(MaterialExpressionMultiply, mat, -350, 500)
    rim.A = ExpressionInput(Expression=fresnel)
    rim.B = rgb(rim_color)
    rim_out = _node(MaterialExpressionMultiply, mat, -150, 500)
    rim_out.A = ExpressionInput(Expression=rim)
    rim_out.B = ExpressionInput(Expression=rim_strength)

    roughness = _scalar(mat, 'Roughness', 0.45, -150, 250)
    specular = _scalar(mat, 'Specular', 0.35, -150, 350)

    mat.Expressions = [
        wpos, lpos, icon_u, icon_v, u_off, v_off, dot_u, dot_v,
        add_u, add_v, uv, uv_clamped, tex, strength, icon_alpha,
        rice_color, base, fresnel, rim_color, rim_strength, rim, rim_out,
        roughness, specular,
    ]
    mat.BaseColor = ColorMaterialInput(Expression=base)
    mat.EmissiveColor = ColorMaterialInput(Expression=rim_out)
    mat.Roughness = ScalarMaterialInput(Expression=roughness)
    mat.Specular = ScalarMaterialInput(Expression=specular)
    mat.TwoSided = True   # the FBX has CullingOff

    mat.post_edit_change()
    mat.save_package()
    ue.log(f'build_rice_material: saved {MATERIAL_PATH}')
    return mat
