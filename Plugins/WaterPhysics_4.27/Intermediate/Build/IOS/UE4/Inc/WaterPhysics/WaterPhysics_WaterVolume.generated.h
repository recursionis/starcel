// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class UPrimitiveComponent;
class AActor;
struct FHitResult;
enum class EWaterVolumeOverlapMethod : uint8;
class UBoxComponent;
#ifdef WATERPHYSICS_WaterPhysics_WaterVolume_generated_h
#error "WaterPhysics_WaterVolume.generated.h already included, missing '#pragma once' in WaterPhysics_WaterVolume.h"
#endif
#define WATERPHYSICS_WaterPhysics_WaterVolume_generated_h

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_SPARSE_DATA
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_RPC_WRAPPERS \
 \
	DECLARE_FUNCTION(execOnVolumeEndOverlap); \
	DECLARE_FUNCTION(execOnVolumeBeginOverlap); \
	DECLARE_FUNCTION(execSetOverlapMethod); \
	DECLARE_FUNCTION(execGetBoxComponent);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_RPC_WRAPPERS_NO_PURE_DECLS \
 \
	DECLARE_FUNCTION(execOnVolumeEndOverlap); \
	DECLARE_FUNCTION(execOnVolumeBeginOverlap); \
	DECLARE_FUNCTION(execSetOverlapMethod); \
	DECLARE_FUNCTION(execGetBoxComponent);


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesAWaterPhysics_WaterVolume(); \
	friend struct Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics; \
public: \
	DECLARE_CLASS(AWaterPhysics_WaterVolume, AWaterPhysicsActor, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(AWaterPhysics_WaterVolume)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_INCLASS \
private: \
	static void StaticRegisterNativesAWaterPhysics_WaterVolume(); \
	friend struct Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics; \
public: \
	DECLARE_CLASS(AWaterPhysics_WaterVolume, AWaterPhysicsActor, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/WaterPhysics"), NO_API) \
	DECLARE_SERIALIZER(AWaterPhysics_WaterVolume)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_STANDARD_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API AWaterPhysics_WaterVolume(const FObjectInitializer& ObjectInitializer); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(AWaterPhysics_WaterVolume) \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, AWaterPhysics_WaterVolume); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(AWaterPhysics_WaterVolume); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API AWaterPhysics_WaterVolume(AWaterPhysics_WaterVolume&&); \
	NO_API AWaterPhysics_WaterVolume(const AWaterPhysics_WaterVolume&); \
public:


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	NO_API AWaterPhysics_WaterVolume(AWaterPhysics_WaterVolume&&); \
	NO_API AWaterPhysics_WaterVolume(const AWaterPhysics_WaterVolume&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, AWaterPhysics_WaterVolume); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(AWaterPhysics_WaterVolume); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(AWaterPhysics_WaterVolume)


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_PRIVATE_PROPERTY_OFFSET \
	FORCEINLINE static uint32 __PPO__OverlappingActors() { return STRUCT_OFFSET(AWaterPhysics_WaterVolume, OverlappingActors); } \
	FORCEINLINE static uint32 __PPO__NewOverlappingActors() { return STRUCT_OFFSET(AWaterPhysics_WaterVolume, NewOverlappingActors); } \
	FORCEINLINE static uint32 __PPO__BoxComponent() { return STRUCT_OFFSET(AWaterPhysics_WaterVolume, BoxComponent); } \
	FORCEINLINE static uint32 __PPO__OverlapMethod() { return STRUCT_OFFSET(AWaterPhysics_WaterVolume, OverlapMethod); }


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_15_PROLOG
#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_GENERATED_BODY_LEGACY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_RPC_WRAPPERS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_INCLASS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_STANDARD_CONSTRUCTORS \
public: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_PRIVATE_PROPERTY_OFFSET \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_SPARSE_DATA \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_RPC_WRAPPERS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_INCLASS_NO_PURE_DECLS \
	HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h_18_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> WATERPHYSICS_API UClass* StaticClass<class AWaterPhysics_WaterVolume>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsSimulations_WaterPhysics_WaterVolume_h


#define FOREACH_ENUM_EWATERVOLUMEOVERLAPMETHOD(op) \
	op(EWaterVolumeOverlapMethod::Overlap) \
	op(EWaterVolumeOverlapMethod::Trace) 

enum class EWaterVolumeOverlapMethod : uint8;
template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterVolumeOverlapMethod>();

PRAGMA_ENABLE_DEPRECATION_WARNINGS
