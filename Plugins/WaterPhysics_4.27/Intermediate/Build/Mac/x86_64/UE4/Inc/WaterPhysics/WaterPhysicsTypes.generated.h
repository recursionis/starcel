// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
#ifdef WATERPHYSICS_WaterPhysicsTypes_generated_h
#error "WaterPhysicsTypes.generated.h already included, missing '#pragma once' in WaterPhysicsTypes.h"
#endif
#define WATERPHYSICS_WaterPhysicsTypes_generated_h

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h_402_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FWaterPhysicsFilter>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h_373_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FActorComponentsSelection_Statics; \
	static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FActorComponentsSelection>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h_92_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics; \
	static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FWaterPhysicsSettings>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h_74_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics; \
	static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FTriangleSubdivisionSettings>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h_57_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FTessellationSettings_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FTessellationSettings>();

#define HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h_15_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics; \
	WATERPHYSICS_API static class UScriptStruct* StaticStruct();


template<> WATERPHYSICS_API UScriptStruct* StaticStruct<struct FGetWaterInfoResult>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID HostProject_Plugins_WaterPhysics_Source_WaterPhysics_Public_WaterPhysicsTypes_h


#define FOREACH_ENUM_EWATERPHYSICSFILTERTYPE(op) \
	op(EWaterPhysicsFilterType::Tag) \
	op(EWaterPhysicsFilterType::ActorClass) \
	op(EWaterPhysicsFilterType::ComponentClass) 

enum class EWaterPhysicsFilterType : uint8;
template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsFilterType>();

#define FOREACH_ENUM_EWATERPHYSICSFILTEROPERATION(op) \
	op(EWaterPhysicsFilterOperation::And) \
	op(EWaterPhysicsFilterOperation::Or) 

enum class EWaterPhysicsFilterOperation : uint8;
template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsFilterOperation>();

#define FOREACH_ENUM_EWATERPHYSICSTESSELLATIONMODE(op) \
	op(EWaterPhysicsTessellationMode::Levels) \
	op(EWaterPhysicsTessellationMode::Area) 

enum class EWaterPhysicsTessellationMode : uint8;
template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsTessellationMode>();

#define FOREACH_ENUM_EWATERPHYSICSDEBUGLEVEL(op) \
	op(EWaterPhysicsDebugLevel::None) \
	op(EWaterPhysicsDebugLevel::Normal) \
	op(EWaterPhysicsDebugLevel::Verbose) 

enum class EWaterPhysicsDebugLevel : uint8;
template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsDebugLevel>();

#define FOREACH_ENUM_EWATERINFOFETCHINGMETHOD(op) \
	op(EWaterInfoFetchingMethod::WaterSurfaceProvider) \
	op(EWaterInfoFetchingMethod::PerVertex) \
	op(EWaterInfoFetchingMethod::PerObject) 

enum class EWaterInfoFetchingMethod : uint8;
template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterInfoFetchingMethod>();

PRAGMA_ENABLE_DEPRECATION_WARNINGS
