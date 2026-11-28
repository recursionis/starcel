// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class AActor;
class UActorComponent;
struct FVector;
struct FGetWaterInfoResult;
#ifdef WATERPHYSICS_WaterPhysics_WaterBodyBase_generated_h
#error "WaterPhysics_WaterBodyBase.generated.h already included, missing '#pragma once' in WaterPhysics_WaterBodyBase.h"
#endif
#define WATERPHYSICS_WaterPhysics_WaterBodyBase_generated_h

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_11_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FWaterBodyArray_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FWaterBodyArray>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_SPARSE_DATA
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_RPC_WRAPPERS \
 \
	DECLARE_FUNCTION(execOnActorEndOverlapWaterBody); \
	DECLARE_FUNCTION(execOnActorBeginOverlapWaterBody);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_RPC_WRAPPERS_NO_PURE_DECLS \
 \
	DECLARE_FUNCTION(execOnActorEndOverlapWaterBody); \
	DECLARE_FUNCTION(execOnActorBeginOverlapWaterBody);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_EVENT_PARMS \
	struct WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms \
	{ \
		AActor* WaterBody; \
		const UActorComponent* Component; \
		FVector Location; \
		FGetWaterInfoResult ReturnValue; \
	};


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_CALLBACK_WRAPPERS
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesAWaterPhysics_WaterBodyBase(); \
	friend struct Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics; \
public: \
	DECLARE_CLASS(AWaterPhysics_WaterBodyBase, AWaterPhysicsActor, COMPILED_IN_FLAGS(CLASS_Abstract | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(AWaterPhysics_WaterBodyBase)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_INCLASS \
private: \
	static void StaticRegisterNativesAWaterPhysics_WaterBodyBase(); \
	friend struct Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics; \
public: \
	DECLARE_CLASS(AWaterPhysics_WaterBodyBase, AWaterPhysicsActor, COMPILED_IN_FLAGS(CLASS_Abstract | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(AWaterPhysics_WaterBodyBase)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_STANDARD_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API AWaterPhysics_WaterBodyBase(const FObjectInitializer& ObjectInitializer); \
	DEFINE_ABSTRACT_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(AWaterPhysics_WaterBodyBase) \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, AWaterPhysics_WaterBodyBase); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(AWaterPhysics_WaterBodyBase); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API AWaterPhysics_WaterBodyBase(AWaterPhysics_WaterBodyBase&&); \
	NO_API AWaterPhysics_WaterBodyBase(const AWaterPhysics_WaterBodyBase&); \
public:


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API AWaterPhysics_WaterBodyBase(AWaterPhysics_WaterBodyBase&&); \
	NO_API AWaterPhysics_WaterBodyBase(const AWaterPhysics_WaterBodyBase&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, AWaterPhysics_WaterBodyBase); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(AWaterPhysics_WaterBodyBase); \
	DEFINE_ABSTRACT_DEFAULT_CONSTRUCTOR_CALL(AWaterPhysics_WaterBodyBase)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_PRIVATE_PROPERTY_OFFSET \
	FORCEINLINE static uint32 __PPO__ActorCurrentWaterBodies() { return STRUCT_OFFSET(AWaterPhysics_WaterBodyBase, ActorCurrentWaterBodies); }


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_22_PROLOG \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_EVENT_PARMS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_GENERATED_BODY_LEGACY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_RPC_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_CALLBACK_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_INCLASS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_STANDARD_CONSTRUCTORS \
public: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_RPC_WRAPPERS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_CALLBACK_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_INCLASS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h_25_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> WATERPHYSICS_API UClass* StaticClass<class AWaterPhysics_WaterBodyBase>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterBodyBase_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
