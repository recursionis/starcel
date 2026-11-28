// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
struct FGetWaterInfoResult;
class UActorComponent;
struct FVector;
struct FWaterPhysicsActingForces;
struct FWaterPhysicsSettings;
class AActor;
#ifdef WATERPHYSICS_WaterPhysicsSceneComponent_generated_h
#error "WaterPhysicsSceneComponent.generated.h already included, missing '#pragma once' in WaterPhysicsSceneComponent.h"
#endif
#define WATERPHYSICS_WaterPhysicsSceneComponent_generated_h

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_13_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FWaterPhysicsActingForces>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_67_DELEGATE \
static inline void FK2_PreStepWaterPhysicsScene_DelegateWrapper(const FMulticastScriptDelegate& K2_PreStepWaterPhysicsScene) \
{ \
	K2_PreStepWaterPhysicsScene.ProcessMulticastDelegate<UObject>(NULL); \
}


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_66_DELEGATE \
struct _Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms \
{ \
	const UActorComponent* Component; \
	FVector Location; \
	FGetWaterInfoResult ReturnValue; \
}; \
static inline FGetWaterInfoResult FBlueprintGetWaterInfoAtLocation_DelegateWrapper(const FScriptDelegate& BlueprintGetWaterInfoAtLocation, const UActorComponent* Component, FVector const& Location) \
{ \
	_Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms Parms; \
	Parms.Component=Component; \
	Parms.Location=Location; \
	BlueprintGetWaterInfoAtLocation.ProcessDelegate<UObject>(&Parms); \
	return Parms.ReturnValue; \
}


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_SPARSE_DATA
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_RPC_WRAPPERS \
 \
	DECLARE_FUNCTION(execK2_SetWaterInfoGetter); \
	DECLARE_FUNCTION(execGetComponentBodySubmergedArea); \
	DECLARE_FUNCTION(execGetComponentSubmergedArea); \
	DECLARE_FUNCTION(execGetComponentBodyActingWaterPhysicsForces); \
	DECLARE_FUNCTION(execGetComponentActingWaterPhysicsForces); \
	DECLARE_FUNCTION(execContainsComponentBody); \
	DECLARE_FUNCTION(execContainsComponent); \
	DECLARE_FUNCTION(execSetComponentWaterPhysicsSettings); \
	DECLARE_FUNCTION(execRemoveComponentFromWaterPhysics); \
	DECLARE_FUNCTION(execAddComponentToWaterPhysics); \
	DECLARE_FUNCTION(execRemoveActorsFromWaterPhysics); \
	DECLARE_FUNCTION(execAddActorsToWaterPhysics); \
	DECLARE_FUNCTION(execRemoveActorFromWaterPhysics); \
	DECLARE_FUNCTION(execAddActorToWaterPhysics);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_RPC_WRAPPERS_NO_PURE_DECLS \
 \
	DECLARE_FUNCTION(execK2_SetWaterInfoGetter); \
	DECLARE_FUNCTION(execGetComponentBodySubmergedArea); \
	DECLARE_FUNCTION(execGetComponentSubmergedArea); \
	DECLARE_FUNCTION(execGetComponentBodyActingWaterPhysicsForces); \
	DECLARE_FUNCTION(execGetComponentActingWaterPhysicsForces); \
	DECLARE_FUNCTION(execContainsComponentBody); \
	DECLARE_FUNCTION(execContainsComponent); \
	DECLARE_FUNCTION(execSetComponentWaterPhysicsSettings); \
	DECLARE_FUNCTION(execRemoveComponentFromWaterPhysics); \
	DECLARE_FUNCTION(execAddComponentToWaterPhysics); \
	DECLARE_FUNCTION(execRemoveActorsFromWaterPhysics); \
	DECLARE_FUNCTION(execAddActorsToWaterPhysics); \
	DECLARE_FUNCTION(execRemoveActorFromWaterPhysics); \
	DECLARE_FUNCTION(execAddActorToWaterPhysics);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUWaterPhysicsSceneComponent(); \
	friend struct Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics; \
public: \
	DECLARE_CLASS(UWaterPhysicsSceneComponent, UActorComponent, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(UWaterPhysicsSceneComponent)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_INCLASS \
private: \
	static void StaticRegisterNativesUWaterPhysicsSceneComponent(); \
	friend struct Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics; \
public: \
	DECLARE_CLASS(UWaterPhysicsSceneComponent, UActorComponent, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(UWaterPhysicsSceneComponent)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_STANDARD_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API UWaterPhysicsSceneComponent(const FObjectInitializer& ObjectInitializer); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(UWaterPhysicsSceneComponent) \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UWaterPhysicsSceneComponent); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UWaterPhysicsSceneComponent); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API UWaterPhysicsSceneComponent(UWaterPhysicsSceneComponent&&); \
	NO_API UWaterPhysicsSceneComponent(const UWaterPhysicsSceneComponent&); \
public:


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API UWaterPhysicsSceneComponent(UWaterPhysicsSceneComponent&&); \
	NO_API UWaterPhysicsSceneComponent(const UWaterPhysicsSceneComponent&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UWaterPhysicsSceneComponent); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UWaterPhysicsSceneComponent); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(UWaterPhysicsSceneComponent)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_PRIVATE_PROPERTY_OFFSET
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_71_PROLOG
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_GENERATED_BODY_LEGACY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_RPC_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_INCLASS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_STANDARD_CONSTRUCTORS \
public: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_RPC_WRAPPERS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_INCLASS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h_74_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> WATERPHYSICS_API UClass* StaticClass<class UWaterPhysicsSceneComponent>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSceneComponent_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
