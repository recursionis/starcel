// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class UWaterPhysicsSettingsComponent;
class AActor;
class UWaterPhysicsSceneComponent;
class UActorComponent;
struct FVector;
struct FGetWaterInfoResult;
#ifdef WATERPHYSICS_WaterPhysicsActor_generated_h
#error "WaterPhysicsActor.generated.h already included, missing '#pragma once' in WaterPhysicsActor.h"
#endif
#define WATERPHYSICS_WaterPhysicsActor_generated_h

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_SPARSE_DATA
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_RPC_WRAPPERS \
 \
	DECLARE_FUNCTION(execNotifyWaterPhysicsSettingsChanged); \
	DECLARE_FUNCTION(execRemoveActorFromWater); \
	DECLARE_FUNCTION(execAddActorToWater); \
	DECLARE_FUNCTION(execGetWaterPhysicsSceneComponent);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_RPC_WRAPPERS_NO_PURE_DECLS \
 \
	DECLARE_FUNCTION(execNotifyWaterPhysicsSettingsChanged); \
	DECLARE_FUNCTION(execRemoveActorFromWater); \
	DECLARE_FUNCTION(execAddActorToWater); \
	DECLARE_FUNCTION(execGetWaterPhysicsSceneComponent);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_EVENT_PARMS \
	struct WaterPhysicsActor_eventReceiveCalculateWaterInfo_Parms \
	{ \
		const UActorComponent* Component; \
		FVector Location; \
		FGetWaterInfoResult ReturnValue; \
	}; \
	struct WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms \
	{ \
		AActor* Actor; \
		bool ReturnValue; \
 \
		/** Constructor, initializes return property only **/ \
		WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms() \
			: ReturnValue(false) \
		{ \
		} \
	}; \
	struct WaterPhysicsActor_eventReceiveOnActorAddedToWater_Parms \
	{ \
		AActor* Actor; \
	}; \
	struct WaterPhysicsActor_eventReceiveOnActorRemovedFromWater_Parms \
	{ \
		AActor* Actor; \
	};


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_CALLBACK_WRAPPERS
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesAWaterPhysicsActor(); \
	friend struct Z_Construct_UClass_AWaterPhysicsActor_Statics; \
public: \
	DECLARE_CLASS(AWaterPhysicsActor, AActor, COMPILED_IN_FLAGS(CLASS_Abstract | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(AWaterPhysicsActor)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_INCLASS \
private: \
	static void StaticRegisterNativesAWaterPhysicsActor(); \
	friend struct Z_Construct_UClass_AWaterPhysicsActor_Statics; \
public: \
	DECLARE_CLASS(AWaterPhysicsActor, AActor, COMPILED_IN_FLAGS(CLASS_Abstract | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(AWaterPhysicsActor)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_STANDARD_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API AWaterPhysicsActor(const FObjectInitializer& ObjectInitializer); \
	DEFINE_ABSTRACT_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(AWaterPhysicsActor) \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, AWaterPhysicsActor); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(AWaterPhysicsActor); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API AWaterPhysicsActor(AWaterPhysicsActor&&); \
	NO_API AWaterPhysicsActor(const AWaterPhysicsActor&); \
public:


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API AWaterPhysicsActor(AWaterPhysicsActor&&); \
	NO_API AWaterPhysicsActor(const AWaterPhysicsActor&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, AWaterPhysicsActor); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(AWaterPhysicsActor); \
	DEFINE_ABSTRACT_DEFAULT_CONSTRUCTOR_CALL(AWaterPhysicsActor)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_PRIVATE_PROPERTY_OFFSET \
	FORCEINLINE static uint32 __PPO__WaterPhysicsSceneComponent() { return STRUCT_OFFSET(AWaterPhysicsActor, WaterPhysicsSceneComponent); }


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_8_PROLOG \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_EVENT_PARMS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_GENERATED_BODY_LEGACY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_RPC_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_CALLBACK_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_INCLASS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_STANDARD_CONSTRUCTORS \
public: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_RPC_WRAPPERS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_CALLBACK_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_INCLASS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h_11_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> WATERPHYSICS_API UClass* StaticClass<class AWaterPhysicsActor>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysicsActor_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
