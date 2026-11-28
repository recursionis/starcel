"""
build_hacker_material.py — builds HackerMap's two glow materials (editor only).

    /Game/Materials/M_HackerGlow
        Unlit. Emissive = Color * Emissive Multiplier.
        Used for every bar, line, cube, Text3D glyph and the logo.

    /Game/Materials/M_HackerGlowTex
        Unlit, Masked, two-sided. Emissive = Texture.rgb * Tint *
        Emissive Multiplier, Opacity Mask = Texture.a.
        Used by Screen Cubes (PIL images: graphs, crosshair, icons, boot
        log) so transparent pixels disappear and the rest glows.

    /Game/Materials/M_HackerGlowRT
        Unlit, opaque. Emissive = Texture.rgb * Tint * Emissive Multiplier.
        Shows the globe's scene-capture render target in the NETWORK panel
        (opaque, because scene-capture alpha isn't usable as a mask).

Parameter names match M_Color / M_TextureUnlit ('Color', 'Texture',
'Emissive Multiplier'), so maps.hacker_map.theme falls back to those when
these haven't been built yet.

Run once in the editor (not during Play), from the Python console:
    import importlib, maps.hacker_map.build_hacker_material as b; importlib.reload(b); b.build()
Running it again rebuilds both graphs in place.
"""

import unreal_engine as ue
from unreal_engine import FLinearColor

GLOW_PATH = '/Game/Materials/M_HackerGlow'
GLOW_TEX_PATH = '/Game/Materials/M_HackerGlowTex'
GLOW_RT_PATH = '/Game/Materials/M_HackerGlowRT'
DEFAULT_TEXTURE = '/Engine/EngineResources/DefaultTexture.DefaultTexture'

# EMaterialShadingModel / EBlendMode values
MSM_UNLIT = 0
BLEND_MASKED = 1


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


def _load_or_create(path):
    from unreal_engine.classes import Material, MaterialFactoryNew
    name = path.split('/')[-1]
    try:
        mat = ue.load_object(Material, f'{path}.{name}')
    except Exception:
        mat = None
    if mat is None:
        mat = MaterialFactoryNew().factory_create_new(path)
        ue.log(f'build_hacker_material: created {path}')
    else:
        ue.log(f'build_hacker_material: rebuilding {path}')
    mat.modify()
    return mat


def _unlit(mat):
    for attr, val in (('ShadingModel', MSM_UNLIT),):
        try:
            setattr(mat, attr, val)
        except Exception as e:
            ue.log_warning(f'build_hacker_material: could not set {attr} ({e}); '
                           f'set Shading Model = Unlit on {mat.get_name()} by hand')


def _finish(mat, path):
    mat.post_edit_change()
    mat.save_package()
    ue.log(f'build_hacker_material: saved {path}')


def build_glow():
    from unreal_engine.classes import MaterialExpressionMultiply
    from unreal_engine.structs import ExpressionInput, ColorMaterialInput

    mat = _load_or_create(GLOW_PATH)
    color = _vector(mat, 'Color', (0.12, 1.0, 0.42, 1.0), -600, -100)
    mult = _scalar(mat, 'Emissive Multiplier', 8.0, -600, 100)
    emissive = _node(MaterialExpressionMultiply, mat, -300, 0)
    emissive.A = ExpressionInput(Expression=color, Mask=1, MaskR=1, MaskG=1, MaskB=1)
    emissive.B = ExpressionInput(Expression=mult)

    mat.Expressions = [color, mult, emissive]
    _unlit(mat)
    mat.EmissiveColor = ColorMaterialInput(Expression=emissive)
    mat.TwoSided = True
    _finish(mat, GLOW_PATH)
    return mat


def build_glow_tex():
    from unreal_engine.classes import (
        Texture2D, MaterialExpressionMultiply,
        MaterialExpressionTextureSampleParameter2D,
        MaterialExpressionComponentMask,
    )
    from unreal_engine.structs import (
        ExpressionInput, ColorMaterialInput, ScalarMaterialInput,
    )

    mat = _load_or_create(GLOW_TEX_PATH)

    tex = _node(MaterialExpressionTextureSampleParameter2D, mat, -800, 0)
    tex.ParameterName = 'Texture'
    tex.Texture = ue.load_object(Texture2D, DEFAULT_TEXTURE)

    tint = _vector(mat, 'Tint', (1.0, 1.0, 1.0, 1.0), -800, -250)
    mult = _scalar(mat, 'Emissive Multiplier', 3.0, -800, 250)

    tinted = _node(MaterialExpressionMultiply, mat, -500, -100)
    tinted.A = ExpressionInput(Expression=tex, Mask=1, MaskR=1, MaskG=1, MaskB=1)
    tinted.B = ExpressionInput(Expression=tint, Mask=1, MaskR=1, MaskG=1, MaskB=1)
    emissive = _node(MaterialExpressionMultiply, mat, -300, 0)
    emissive.A = ExpressionInput(Expression=tinted)
    emissive.B = ExpressionInput(Expression=mult)

    opacity = _node(MaterialExpressionComponentMask, mat, -500, 200)
    opacity.Input = ExpressionInput(Expression=tex)
    opacity.R, opacity.G, opacity.B, opacity.A = False, False, False, True

    mat.Expressions = [tex, tint, mult, tinted, emissive, opacity]
    _unlit(mat)
    try:
        mat.BlendMode = BLEND_MASKED
    except Exception as e:
        ue.log_warning(f'build_hacker_material: could not set BlendMode ({e})')
    mat.EmissiveColor = ColorMaterialInput(Expression=emissive)
    mat.OpacityMask = ScalarMaterialInput(Expression=opacity)
    mat.OpacityMaskClipValue = 0.2
    # one-sided: Screen Cubes are thin cubes, a two-sided material would let
    # the (mirrored) back face show through transparent pixels
    mat.TwoSided = False
    _finish(mat, GLOW_TEX_PATH)
    return mat


def build_glow_rt():
    from unreal_engine.classes import (
        Texture2D, MaterialExpressionMultiply,
        MaterialExpressionTextureSampleParameter2D,
    )
    from unreal_engine.structs import ExpressionInput, ColorMaterialInput

    mat = _load_or_create(GLOW_RT_PATH)
    tex = _node(MaterialExpressionTextureSampleParameter2D, mat, -800, 0)
    tex.ParameterName = 'Texture'
    tex.Texture = ue.load_object(Texture2D, DEFAULT_TEXTURE)
    tint = _vector(mat, 'Tint', (1.0, 1.0, 1.0, 1.0), -800, -250)
    mult = _scalar(mat, 'Emissive Multiplier', 1.0, -800, 250)
    tinted = _node(MaterialExpressionMultiply, mat, -500, -100)
    tinted.A = ExpressionInput(Expression=tex, Mask=1, MaskR=1, MaskG=1, MaskB=1)
    tinted.B = ExpressionInput(Expression=tint, Mask=1, MaskR=1, MaskG=1, MaskB=1)
    emissive = _node(MaterialExpressionMultiply, mat, -300, 0)
    emissive.A = ExpressionInput(Expression=tinted)
    emissive.B = ExpressionInput(Expression=mult)
    mat.Expressions = [tex, tint, mult, tinted, emissive]
    _unlit(mat)
    mat.EmissiveColor = ColorMaterialInput(Expression=emissive)
    _finish(mat, GLOW_RT_PATH)
    return mat


def build():
    return build_glow(), build_glow_tex(), build_glow_rt()
