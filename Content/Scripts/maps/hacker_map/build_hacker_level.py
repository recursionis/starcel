"""
build_hacker_level.py — sets up the empty HackerMap level (editor only).

Places and saves, so they exist before BeginPlay:
  * BP_PyActorEmpty with PythonModule = maps.hacker_map.pyactor_main,
    PythonClass = Main. StarcelGameInstance sees it and skips auto-spawning
    main.Main in this map. Any placed BP_PyActor / PyActor running 'main'
    is deleted, so main.py never runs here.
  * a dim green SkyLight; any ExponentialHeightFog is switched off (the
    background is black space - the star map sky is spawned at runtime)
  * an unbound PostProcessVolume: strong bloom (the glow), a green scene
    tint (turns everything — including the Cesium night globe and file
    icons — green), vignette, a little grain and chromatic aberration,
    locked exposure so the glow levels don't pump.

Post-process is set here, in the editor, because its struct overrides don't
stick reliably when written at runtime through UnrealEnginePython.

Run once with HackerMap open, from the Python console:
    import importlib, maps.hacker_map.build_hacker_level as b; importlib.reload(b); b.build()
Safe to run again: existing actors are reused and re-configured.
"""

import unreal_engine as ue
from unreal_engine import FVector, FRotator, FLinearColor

PYACTOR_BP = '/Game/Blueprints/Assets/BP_PyActorEmpty.BP_PyActorEmpty'
MODULE = 'maps.hacker_map.pyactor_main'
TAG = 'HackerMap'


def _find(world, class_name, pred=None):
    for a in world.all_actors():
        try:
            if a.get_class().get_name() == class_name and (pred is None or pred(a)):
                return a
        except Exception:
            continue
    return None


def _spawn(cls, loc=(0, 0, 0)):
    from unreal_engine.classes import EditorLevelLibrary
    return EditorLevelLibrary.SpawnActorFromClass(
        cls, FVector(*loc), FRotator(0, 0, 0), False)


def _set(obj, name, value):
    try:
        setattr(obj, name, value)
        return True
    except Exception as e:
        ue.log_warning(f'build_hacker_level: {obj.get_name()}.{name} failed ({e})')
        return False


def _ensure_pyactor(world):
    from unreal_engine_tools import load_blueprint_class
    cls = load_blueprint_class(PYACTOR_BP)
    cls_name = cls.get_name()
    a = _find(world, cls_name, lambda x: str(getattr(x, 'PythonModule', '') or '') == MODULE)
    if a is None:
        a = _find(world, cls_name)
    if a is None:
        a = _spawn(cls, (0, 0, 0))
        ue.log(f'build_hacker_level: placed {a.get_name()}')
    _set(a, 'PythonModule', MODULE)
    _set(a, 'PythonClass', 'Main')
    try:
        a.set_actor_label('HackerMapController')
    except Exception:
        pass
    _remove_main_pyactors(world, keep=a)
    return a


def _remove_main_pyactors(world, keep):
    """Delete placed PyActors that would run main.Main in this map (a
    BP_PyActor, whose default module is 'main'). main.Main possesses the
    drone and spawns test_earth's globes at the origin — right where
    HackerMap's fixed camera sits. Other PyActors are left alone."""
    from unreal_engine.classes import EditorLevelLibrary
    for a in list(world.all_actors()):
        if a is keep:
            continue
        try:
            cname = a.get_class().get_name()
            module = str(getattr(a, 'PythonModule', '') or '')
        except Exception:
            continue
        if cname == 'BP_PyActor_C' or module == 'main':
            name = a.get_name()
            try:
                EditorLevelLibrary.DestroyActor(a)
            except Exception:
                try:
                    a.actor_destroy()
                except Exception as e:
                    ue.log_warning(f'build_hacker_level: could not remove {name} ({e}); '
                                   f'delete it in the World Outliner')
                    continue
            ue.log(f'build_hacker_level: removed {name} ({cname}, module "{module}") '
                   f'so main.Main does not run in HackerMap')


def _ensure_sky_light(world):
    a = _find(world, 'SkyLight')
    if a is None:
        a = _spawn(ue.find_class('SkyLight'), (0, 0, 2000))
    try:
        c = a.get_actor_component_by_type(ue.find_class('SkyLightComponent'))
    except Exception:
        c = None
    if c is None:
        try:
            c = a.LightComponent
        except Exception:
            c = None
    if c is not None:
        _set(c, 'Intensity', 0.25)
        try:
            c.SetLightColor(FLinearColor(0.2, 1.0, 0.45, 1.0))
        except Exception as e:
            ue.log_warning(f'build_hacker_level: SkyLight colour not set ({e})')
    return a


def _ensure_fog(world):
    """No fog: an earlier version of this script added one. Turn it off."""
    a = _find(world, 'ExponentialHeightFog')
    if a is None:
        return None
    try:
        c = a.get_actor_component_by_type(ue.find_class('ExponentialHeightFogComponent'))
    except Exception:
        c = None
    if c is not None:
        _set(c, 'FogDensity', 0.0)
        _set(c, 'FogMaxOpacity', 0.0)
    return a


# (override flag, property, value) — value may be a callable building it
def _pp_values():
    from unreal_engine.structs import Vector4
    def v4(x, y, z, w):
        return Vector4(X=x, Y=y, Z=z, W=w)
    return [
        ('bOverride_BloomIntensity', 'BloomIntensity', 3.5),
        ('bOverride_BloomThreshold', 'BloomThreshold', 0.4),
        ('bOverride_SceneColorTint', 'SceneColorTint', FLinearColor(0.55, 1.0, 0.62, 1.0)),
        ('bOverride_ColorSaturation', 'ColorSaturation', lambda: v4(0.75, 1.0, 0.75, 1.0)),
        ('bOverride_ColorGain', 'ColorGain', lambda: v4(0.7, 1.15, 0.8, 1.0)),
        ('bOverride_VignetteIntensity', 'VignetteIntensity', 0.55),
        ('bOverride_GrainIntensity', 'GrainIntensity', 0.12),
        ('bOverride_SceneFringeIntensity', 'SceneFringeIntensity', 1.2),
        ('bOverride_AutoExposureMinBrightness', 'AutoExposureMinBrightness', 1.0),
        ('bOverride_AutoExposureMaxBrightness', 'AutoExposureMaxBrightness', 1.0),
        ('bOverride_AutoExposureBias', 'AutoExposureBias', 0.0),
    ]


def _ensure_post_process(world):
    a = _find(world, 'PostProcessVolume')
    if a is None:
        a = _spawn(ue.find_class('PostProcessVolume'), (0, 0, 0))
        ue.log(f'build_hacker_level: placed {a.get_name()}')
    _set(a, 'bUnbound', True)
    _set(a, 'Priority', 10.0)
    try:
        settings = a.Settings
    except Exception as e:
        ue.log_warning(f'build_hacker_level: cannot read PostProcessVolume.Settings ({e})')
        return a
    ok, failed = 0, []
    for flag, prop, value in _pp_values():
        try:
            if callable(value):
                value = value()
            setattr(settings, prop, value)
            setattr(settings, flag, True)
            ok += 1
        except Exception:
            failed.append(prop)
    try:
        a.Settings = settings
    except Exception as e:
        ue.log_warning(f'build_hacker_level: writing Settings back failed ({e})')
    ue.log(f'build_hacker_level: post-process set {ok} values'
           + (f'; set these by hand: {failed}' if failed else ''))
    return a


def build(save=True):
    world = ue.get_editor_world()
    _ensure_pyactor(world)
    for step in (_ensure_sky_light, _ensure_fog, _ensure_post_process):
        try:
            step(world)
        except Exception as e:
            ue.log_warning(f'build_hacker_level: {step.__name__} failed ({e})')
    if save:
        try:
            from unreal_engine.classes import EditorLevelLibrary
            EditorLevelLibrary.SaveCurrentLevel()
            ue.log('build_hacker_level: level saved')
        except Exception as e:
            ue.log_warning(f'build_hacker_level: save failed ({e}); press Ctrl+S')
