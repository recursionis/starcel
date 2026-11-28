// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class UWaterPhysicsSceneComponent;
class AActor;
struct FGatherWaterPhysicsSettingsResult;
#ifdef WATERPHYSICS_WaterPhysicsSettingsComponent_generated_h
#error "WaterPhysicsSettingsComponent.generated.h already included, missing '#pragma once' in WaterPhysicsSettingsComponent.h"
#endif
#define WATERPHYSICS_WaterPhysicsSettingsComponent_generated_h

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_30_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FGatherWaterPhysicsSettingsResult_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FGatherWaterPhysicsSettingsResult>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_16_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FComponentsWaterPhysicsSettings_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FComponentsWaterPhysicsSettings>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_11_DELEGATE \
struct _Script_WaterPhysics_eventOnActorRemovedFromWaterPhysics_Parms \
{ \
	UWaterPhysicsSceneComponent* WaterPhysicsSceneComponent; \
}; \
static inline void FOnActorRemovedFromWaterPhysics_DelegateWrapper(const FMulticastScriptDelegate& OnActorRemovedFromWaterPhysics, UWaterPhysicsSceneComponent* WaterPhysicsSceneComponent) \
{ \
	_Script_WaterPhysics_eventOnActorRemovedFromWaterPhysics_Parms Parms; \
	Parms.WaterPhysicsSceneComponent=WaterPhysicsSceneComponent; \
	OnActorRemovedFromWaterPhysics.ProcessMulticastDelegate<UObject>(&Parms); \
}


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_10_DELEGATE \
struct _Script_WaterPhysics_eventOnActorAddedToWaterPhysics_Parms \
{ \
	UWaterPhysicsSceneComponent* WaterPhysicsSceneComponent; \
}; \
static inline void FOnActorAddedToWaterPhysics_DelegateWrapper(const FMulticastScriptDelegate& OnActorAddedToWaterPhysics, UWaterPhysicsSceneComponent* WaterPhysicsSceneComponent) \
{ \
	_Script_WaterPhysics_eventOnActorAddedToWaterPhysics_Parms Parms; \
	Parms.WaterPhysicsSceneComponent=WaterPhysicsSceneComponent; \
	OnActorAddedToWaterPhysics.ProcessMulticastDelegate<UObject>(&Parms); \
}


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_SPARSE_DATA
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_RPC_WRAPPERS \
 \
	DECLARE_FUNCTION(execGatherActorWaterPhysicsSettings); \
	DECLARE_FUNCTION(execNotifyWaterPhysicsSettingsChanged);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_RPC_WRAPPERS_NO_PURE_DECLS \
 \
	DECLARE_FUNCTION(execGatherActorWaterPhysicsSettings); \
	DECLARE_FUNCTION(execNotifyWaterPhysicsSettingsChanged);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUWaterPhysicsSettingsComponent(); \
	friend struct Z_Construct_UClass_UWaterPhysicsSettingsComponent_Statics; \
public: \
	DECLARE_CLASS(UWaterPhysicsSettingsComponent, UActorComponent, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(UWaterPhysicsSettingsComponent)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_INCLASS \
private: \
	static void StaticRegisterNativesUWaterPhysicsSettingsComponent(); \
	friend struct Z_Construct_UClass_UWaterPhysicsSettingsComponent_Statics; \
public: \
	DECLARE_CLASS(UWaterPhysicsSettingsComponent, UActorComponent, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(UWaterPhysicsSettingsComponent)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_STANDARD_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API UWaterPhysicsSettingsComponent(const FObjectInitializer& ObjectInitializer); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(UWaterPhysicsSettingsComponent) \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UWaterPhysicsSettingsComponent); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UWaterPhysicsSettingsComponent); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API UWaterPhysicsSettingsComponent(UWaterPhysicsSettingsComponent&&); \
	NO_API UWaterPhysicsSettingsComponent(const UWaterPhysicsSettingsComponent&); \
public:


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API UWaterPhysicsSettingsComponent(UWaterPhysicsSettingsComponent&&); \
	NO_API UWaterPhysicsSettingsComponent(const UWaterPhysicsSettingsComponent&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UWaterPhysicsSettingsComponent); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UWaterPhysicsSettingsComponent); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(UWaterPhysicsSettingsComponent)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_PRIVATE_PROPERTY_OFFSET
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_47_PROLOG
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_GENERATED_BODY_LEGACY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_RPC_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_INCLASS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_STANDARD_CONSTRUCTORS \
public: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_RPC_WRAPPERS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_INCLASS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h_50_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> WATERPHYSICS_API UClass* StaticClass<class UWaterPhysicsSettingsComponent>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSettingsComponent_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
