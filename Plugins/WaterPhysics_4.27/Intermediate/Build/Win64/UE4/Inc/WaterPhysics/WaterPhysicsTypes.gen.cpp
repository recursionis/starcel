// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsTypes.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysicsTypes() {}
// Cross Module References
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterType();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterOperation();
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsTessellationMode();
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel();
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterInfoFetchingMethod();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsFilter();
	COREUOBJECT_API UClass* Z_Construct_UClass_UClass();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	ENGINE_API UClass* Z_Construct_UClass_UActorComponent_NoRegister();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FActorComponentsSelection();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsSettings();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FTriangleSubdivisionSettings();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FTessellationSettings();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FGetWaterInfoResult();
	COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector();
// End Cross Module References
	static UEnum* EWaterPhysicsFilterType_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterType, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterPhysicsFilterType"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsFilterType>()
	{
		return EWaterPhysicsFilterType_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterPhysicsFilterType(EWaterPhysicsFilterType_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterPhysicsFilterType"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterType_Hash() { return 972681957U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterType()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterPhysicsFilterType"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterType_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterPhysicsFilterType::Tag", (int64)EWaterPhysicsFilterType::Tag },
				{ "EWaterPhysicsFilterType::ActorClass", (int64)EWaterPhysicsFilterType::ActorClass },
				{ "EWaterPhysicsFilterType::ComponentClass", (int64)EWaterPhysicsFilterType::ComponentClass },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "ActorClass.Comment", "// Filter based on actor tag\n" },
				{ "ActorClass.Name", "EWaterPhysicsFilterType::ActorClass" },
				{ "ActorClass.ToolTip", "Filter based on actor tag" },
				{ "BlueprintType", "true" },
				{ "ComponentClass.Comment", "// Filter based on actor class\n" },
				{ "ComponentClass.Name", "EWaterPhysicsFilterType::ComponentClass" },
				{ "ComponentClass.ToolTip", "Filter based on actor class" },
				{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
				{ "Tag.Name", "EWaterPhysicsFilterType::Tag" },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterPhysicsFilterType",
				"EWaterPhysicsFilterType",
				Enumerators,
				UE_ARRAY_COUNT(Enumerators),
				RF_Public|RF_Transient|RF_MarkAsNative,
				EEnumFlags::None,
				UE4CodeGen_Private::EDynamicType::NotDynamic,
				(uint8)UEnum::ECppForm::EnumClass,
				METADATA_PARAMS(Enum_MetaDataParams, UE_ARRAY_COUNT(Enum_MetaDataParams))
			};
			UE4CodeGen_Private::ConstructUEnum(ReturnEnum, EnumParams);
		}
		return ReturnEnum;
	}
	static UEnum* EWaterPhysicsFilterOperation_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterOperation, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterPhysicsFilterOperation"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsFilterOperation>()
	{
		return EWaterPhysicsFilterOperation_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterPhysicsFilterOperation(EWaterPhysicsFilterOperation_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterPhysicsFilterOperation"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterOperation_Hash() { return 1360790103U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterOperation()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterPhysicsFilterOperation"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterOperation_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterPhysicsFilterOperation::And", (int64)EWaterPhysicsFilterOperation::And },
				{ "EWaterPhysicsFilterOperation::Or", (int64)EWaterPhysicsFilterOperation::Or },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "And.Name", "EWaterPhysicsFilterOperation::And" },
				{ "BlueprintType", "true" },
				{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
				{ "Or.Name", "EWaterPhysicsFilterOperation::Or" },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterPhysicsFilterOperation",
				"EWaterPhysicsFilterOperation",
				Enumerators,
				UE_ARRAY_COUNT(Enumerators),
				RF_Public|RF_Transient|RF_MarkAsNative,
				EEnumFlags::None,
				UE4CodeGen_Private::EDynamicType::NotDynamic,
				(uint8)UEnum::ECppForm::EnumClass,
				METADATA_PARAMS(Enum_MetaDataParams, UE_ARRAY_COUNT(Enum_MetaDataParams))
			};
			UE4CodeGen_Private::ConstructUEnum(ReturnEnum, EnumParams);
		}
		return ReturnEnum;
	}
	static UEnum* EWaterPhysicsTessellationMode_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterPhysicsTessellationMode, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterPhysicsTessellationMode"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsTessellationMode>()
	{
		return EWaterPhysicsTessellationMode_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterPhysicsTessellationMode(EWaterPhysicsTessellationMode_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterPhysicsTessellationMode"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsTessellationMode_Hash() { return 1098189637U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsTessellationMode()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterPhysicsTessellationMode"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsTessellationMode_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterPhysicsTessellationMode::Levels", (int64)EWaterPhysicsTessellationMode::Levels },
				{ "EWaterPhysicsTessellationMode::Area", (int64)EWaterPhysicsTessellationMode::Area },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "Area.Name", "EWaterPhysicsTessellationMode::Area" },
				{ "Levels.Name", "EWaterPhysicsTessellationMode::Levels" },
				{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterPhysicsTessellationMode",
				"EWaterPhysicsTessellationMode",
				Enumerators,
				UE_ARRAY_COUNT(Enumerators),
				RF_Public|RF_Transient|RF_MarkAsNative,
				EEnumFlags::None,
				UE4CodeGen_Private::EDynamicType::NotDynamic,
				(uint8)UEnum::ECppForm::EnumClass,
				METADATA_PARAMS(Enum_MetaDataParams, UE_ARRAY_COUNT(Enum_MetaDataParams))
			};
			UE4CodeGen_Private::ConstructUEnum(ReturnEnum, EnumParams);
		}
		return ReturnEnum;
	}
	static UEnum* EWaterPhysicsDebugLevel_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterPhysicsDebugLevel"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsDebugLevel>()
	{
		return EWaterPhysicsDebugLevel_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterPhysicsDebugLevel(EWaterPhysicsDebugLevel_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterPhysicsDebugLevel"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel_Hash() { return 3153083705U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterPhysicsDebugLevel"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterPhysicsDebugLevel::None", (int64)EWaterPhysicsDebugLevel::None },
				{ "EWaterPhysicsDebugLevel::Normal", (int64)EWaterPhysicsDebugLevel::Normal },
				{ "EWaterPhysicsDebugLevel::Verbose", (int64)EWaterPhysicsDebugLevel::Verbose },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
				{ "None.Name", "EWaterPhysicsDebugLevel::None" },
				{ "Normal.Name", "EWaterPhysicsDebugLevel::Normal" },
				{ "Verbose.Name", "EWaterPhysicsDebugLevel::Verbose" },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterPhysicsDebugLevel",
				"EWaterPhysicsDebugLevel",
				Enumerators,
				UE_ARRAY_COUNT(Enumerators),
				RF_Public|RF_Transient|RF_MarkAsNative,
				EEnumFlags::None,
				UE4CodeGen_Private::EDynamicType::NotDynamic,
				(uint8)UEnum::ECppForm::EnumClass,
				METADATA_PARAMS(Enum_MetaDataParams, UE_ARRAY_COUNT(Enum_MetaDataParams))
			};
			UE4CodeGen_Private::ConstructUEnum(ReturnEnum, EnumParams);
		}
		return ReturnEnum;
	}
	static UEnum* EWaterInfoFetchingMethod_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterInfoFetchingMethod, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterInfoFetchingMethod"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterInfoFetchingMethod>()
	{
		return EWaterInfoFetchingMethod_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterInfoFetchingMethod(EWaterInfoFetchingMethod_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterInfoFetchingMethod"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterInfoFetchingMethod_Hash() { return 1404543407U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterInfoFetchingMethod()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterInfoFetchingMethod"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterInfoFetchingMethod_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterInfoFetchingMethod::WaterSurfaceProvider", (int64)EWaterInfoFetchingMethod::WaterSurfaceProvider },
				{ "EWaterInfoFetchingMethod::PerVertex", (int64)EWaterInfoFetchingMethod::PerVertex },
				{ "EWaterInfoFetchingMethod::PerObject", (int64)EWaterInfoFetchingMethod::PerObject },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
				{ "PerObject.Comment", "// Only fetch the water surface once per object. Will greatly improve performance at the cost of wave accuracy.\n" },
				{ "PerObject.Name", "EWaterInfoFetchingMethod::PerObject" },
				{ "PerObject.ToolTip", "Only fetch the water surface once per object. Will greatly improve performance at the cost of wave accuracy." },
				{ "PerVertex.Comment", "// Force fetch the water surface once per vertex. Might get expensive if object has a high number of vertices.\n" },
				{ "PerVertex.Name", "EWaterInfoFetchingMethod::PerVertex" },
				{ "PerVertex.ToolTip", "Force fetch the water surface once per vertex. Might get expensive if object has a high number of vertices." },
				{ "WaterSurfaceProvider.Comment", "// Uses the Water Surface Provider to fetch water surface information. Uses the WorldAlignedWaterSurfaceProvider by default.\n" },
				{ "WaterSurfaceProvider.Name", "EWaterInfoFetchingMethod::WaterSurfaceProvider" },
				{ "WaterSurfaceProvider.ToolTip", "Uses the Water Surface Provider to fetch water surface information. Uses the WorldAlignedWaterSurfaceProvider by default." },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterInfoFetchingMethod",
				"EWaterInfoFetchingMethod",
				Enumerators,
				UE_ARRAY_COUNT(Enumerators),
				RF_Public|RF_Transient|RF_MarkAsNative,
				EEnumFlags::None,
				UE4CodeGen_Private::EDynamicType::NotDynamic,
				(uint8)UEnum::ECppForm::EnumClass,
				METADATA_PARAMS(Enum_MetaDataParams, UE_ARRAY_COUNT(Enum_MetaDataParams))
			};
			UE4CodeGen_Private::ConstructUEnum(ReturnEnum, EnumParams);
		}
		return ReturnEnum;
	}
class UScriptStruct* FWaterPhysicsFilter::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsFilter_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FWaterPhysicsFilter, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("WaterPhysicsFilter"), sizeof(FWaterPhysicsFilter), Get_Z_Construct_UScriptStruct_FWaterPhysicsFilter_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FWaterPhysicsFilter>()
{
	return FWaterPhysicsFilter::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FWaterPhysicsFilter(FWaterPhysicsFilter::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("WaterPhysicsFilter"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsFilter
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsFilter()
	{
		UScriptStruct::DeferCppStructOps<FWaterPhysicsFilter>(FName(TEXT("WaterPhysicsFilter")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsFilter;
	struct Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Not_MetaData[];
#endif
		static void NewProp_Not_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_Not;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_FilterOperation_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_FilterOperation_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_FilterOperation;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_FilterType_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_FilterType_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_FilterType;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Tag_MetaData[];
#endif
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_Tag;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ActorsClass_MetaData[];
#endif
		static const UE4CodeGen_Private::FClassPropertyParams NewProp_ActorsClass;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ComponentClass_MetaData[];
#endif
		static const UE4CodeGen_Private::FClassPropertyParams NewProp_ComponentClass;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FWaterPhysicsFilter>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not_MetaData[] = {
		{ "Category", "Filters" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not_SetBit(void* Obj)
	{
		((FWaterPhysicsFilter*)Obj)->Not = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not = { "Not", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterPhysicsFilter), &Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation_MetaData[] = {
		{ "Category", "Filters" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation = { "FilterOperation", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsFilter, FilterOperation), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterOperation, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType_MetaData[] = {
		{ "Category", "Filters" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType = { "FilterType", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsFilter, FilterType), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsFilterType, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Tag_MetaData[] = {
		{ "Category", "Filters" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Tag = { "Tag", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsFilter, Tag), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Tag_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Tag_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ActorsClass_MetaData[] = {
		{ "Category", "Filters" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FClassPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ActorsClass = { "ActorsClass", nullptr, (EPropertyFlags)0x0014000000000005, UE4CodeGen_Private::EPropertyGenFlags::Class, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsFilter, ActorsClass), Z_Construct_UClass_AActor_NoRegister, Z_Construct_UClass_UClass, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ActorsClass_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ActorsClass_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ComponentClass_MetaData[] = {
		{ "Category", "Filters" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FClassPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ComponentClass = { "ComponentClass", nullptr, (EPropertyFlags)0x0014000000000005, UE4CodeGen_Private::EPropertyGenFlags::Class, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsFilter, ComponentClass), Z_Construct_UClass_UActorComponent_NoRegister, Z_Construct_UClass_UClass, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ComponentClass_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ComponentClass_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Not,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterOperation,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_FilterType,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_Tag,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ActorsClass,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::NewProp_ComponentClass,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"WaterPhysicsFilter",
		sizeof(FWaterPhysicsFilter),
		alignof(FWaterPhysicsFilter),
		Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsFilter()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsFilter_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("WaterPhysicsFilter"), sizeof(FWaterPhysicsFilter), Get_Z_Construct_UScriptStruct_FWaterPhysicsFilter_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FWaterPhysicsFilter_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsFilter_Hash() { return 1920664933U; }
class UScriptStruct* FActorComponentsSelection::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FActorComponentsSelection_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FActorComponentsSelection, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("ActorComponentsSelection"), sizeof(FActorComponentsSelection), Get_Z_Construct_UScriptStruct_FActorComponentsSelection_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FActorComponentsSelection>()
{
	return FActorComponentsSelection::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FActorComponentsSelection(FActorComponentsSelection::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("ActorComponentsSelection"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFActorComponentsSelection
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFActorComponentsSelection()
	{
		UScriptStruct::DeferCppStructOps<FActorComponentsSelection>(FName(TEXT("ActorComponentsSelection")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFActorComponentsSelection;
	struct Z_Construct_UScriptStruct_FActorComponentsSelection_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bSelectAll_MetaData[];
#endif
		static void NewProp_bSelectAll_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bSelectAll;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_ComponentNames_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ComponentNames_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_ComponentNames;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FActorComponentsSelection>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll_SetBit(void* Obj)
	{
		((FActorComponentsSelection*)Obj)->bSelectAll = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll = { "bSelectAll", nullptr, (EPropertyFlags)0x0010000000000000, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FActorComponentsSelection), &Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll_MetaData)) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames_Inner = { "ComponentNames", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames = { "ComponentNames", nullptr, (EPropertyFlags)0x0010000000000000, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FActorComponentsSelection, ComponentNames), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_bSelectAll,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::NewProp_ComponentNames,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"ActorComponentsSelection",
		sizeof(FActorComponentsSelection),
		alignof(FActorComponentsSelection),
		Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000201),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FActorComponentsSelection()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FActorComponentsSelection_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("ActorComponentsSelection"), sizeof(FActorComponentsSelection), Get_Z_Construct_UScriptStruct_FActorComponentsSelection_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FActorComponentsSelection_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FActorComponentsSelection_Hash() { return 1641218744U; }
class UScriptStruct* FWaterPhysicsSettings::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsSettings_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FWaterPhysicsSettings, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("WaterPhysicsSettings"), sizeof(FWaterPhysicsSettings), Get_Z_Construct_UScriptStruct_FWaterPhysicsSettings_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FWaterPhysicsSettings>()
{
	return FWaterPhysicsSettings::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FWaterPhysicsSettings(FWaterPhysicsSettings::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("WaterPhysicsSettings"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsSettings
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsSettings()
	{
		UScriptStruct::DeferCppStructOps<FWaterPhysicsSettings>(FName(TEXT("WaterPhysicsSettings")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsSettings;
	struct Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_FluidDensity_MetaData[];
#endif
		static void NewProp_bOverride_FluidDensity_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_FluidDensity;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_FluidKinematicViscocity_MetaData[];
#endif
		static void NewProp_bOverride_FluidKinematicViscocity_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_FluidKinematicViscocity;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_WaterInfoFetchingMethod_MetaData[];
#endif
		static void NewProp_bOverride_WaterInfoFetchingMethod_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_WaterInfoFetchingMethod;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_SubdivisionSettings_MetaData[];
#endif
		static void NewProp_bOverride_SubdivisionSettings_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_SubdivisionSettings;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_SubmergedTessellationSettings_MetaData[];
#endif
		static void NewProp_bOverride_SubmergedTessellationSettings_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_SubmergedTessellationSettings;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_PressureCoefficientOfLinearSpeed_MetaData[];
#endif
		static void NewProp_bOverride_PressureCoefficientOfLinearSpeed_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_PressureCoefficientOfLinearSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_PressureCoefficientOfExponentialSpeed_MetaData[];
#endif
		static void NewProp_bOverride_PressureCoefficientOfExponentialSpeed_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_PressureCoefficientOfExponentialSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_PressureAngularDependence_MetaData[];
#endif
		static void NewProp_bOverride_PressureAngularDependence_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_PressureAngularDependence;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_SuctionCoefficientOfLinearSpeed_MetaData[];
#endif
		static void NewProp_bOverride_SuctionCoefficientOfLinearSpeed_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_SuctionCoefficientOfLinearSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_MetaData[];
#endif
		static void NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_SuctionCoefficientOfExponentialSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_SuctionAngularDependence_MetaData[];
#endif
		static void NewProp_bOverride_SuctionAngularDependence_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_SuctionAngularDependence;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DragReferenceSpeed_MetaData[];
#endif
		static void NewProp_bOverride_DragReferenceSpeed_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DragReferenceSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_MaxSlammingForceAtAcceleration_MetaData[];
#endif
		static void NewProp_bOverride_MaxSlammingForceAtAcceleration_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_MaxSlammingForceAtAcceleration;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_SlammingForceExponent_MetaData[];
#endif
		static void NewProp_bOverride_SlammingForceExponent_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_SlammingForceExponent;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_bEnableBuoyancyForce_MetaData[];
#endif
		static void NewProp_bOverride_bEnableBuoyancyForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_bEnableBuoyancyForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_bEnableViscousFluidResistance_MetaData[];
#endif
		static void NewProp_bOverride_bEnableViscousFluidResistance_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_bEnableViscousFluidResistance;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_bEnablePressureDragForce_MetaData[];
#endif
		static void NewProp_bOverride_bEnablePressureDragForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_bEnablePressureDragForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_bEnableSlammingForce_MetaData[];
#endif
		static void NewProp_bOverride_bEnableSlammingForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_bEnableSlammingForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_bEnableForceClamping_MetaData[];
#endif
		static void NewProp_bOverride_bEnableForceClamping_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_bEnableForceClamping;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugSubmersion_MetaData[];
#endif
		static void NewProp_bOverride_DebugSubmersion_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugSubmersion;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugTriangleData_MetaData[];
#endif
		static void NewProp_bOverride_DebugTriangleData_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugTriangleData;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugBuoyancyForce_MetaData[];
#endif
		static void NewProp_bOverride_DebugBuoyancyForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugBuoyancyForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugViscousFluidResistance_MetaData[];
#endif
		static void NewProp_bOverride_DebugViscousFluidResistance_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugViscousFluidResistance;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugPressureDragForce_MetaData[];
#endif
		static void NewProp_bOverride_DebugPressureDragForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugPressureDragForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugSlammingForce_MetaData[];
#endif
		static void NewProp_bOverride_DebugSlammingForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugSlammingForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bOverride_DebugFluidVelocity_MetaData[];
#endif
		static void NewProp_bOverride_DebugFluidVelocity_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bOverride_DebugFluidVelocity;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_FluidDensity_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_FluidDensity;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_FluidKinematicViscocity_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_FluidKinematicViscocity;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_WaterInfoFetchingMethod_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterInfoFetchingMethod_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_WaterInfoFetchingMethod;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SubdivisionSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_SubdivisionSettings;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SubmergedTessellationSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_SubmergedTessellationSettings;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_PressureCoefficientOfLinearSpeed_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_PressureCoefficientOfLinearSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_PressureCoefficientOfExponentialSpeed_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_PressureCoefficientOfExponentialSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_PressureAngularDependence_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_PressureAngularDependence;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SuctionCoefficientOfLinearSpeed_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_SuctionCoefficientOfLinearSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SuctionCoefficientOfExponentialSpeed_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_SuctionCoefficientOfExponentialSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SuctionAngularDependence_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_SuctionAngularDependence;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DragReferenceSpeed_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_DragReferenceSpeed;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_MaxSlammingForceAtAcceleration_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_MaxSlammingForceAtAcceleration;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SlammingForceExponent_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_SlammingForceExponent;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bEnableBuoyancyForce_MetaData[];
#endif
		static void NewProp_bEnableBuoyancyForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bEnableBuoyancyForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bEnableViscousFluidResistance_MetaData[];
#endif
		static void NewProp_bEnableViscousFluidResistance_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bEnableViscousFluidResistance;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bEnablePressureDragForce_MetaData[];
#endif
		static void NewProp_bEnablePressureDragForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bEnablePressureDragForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bEnableSlammingForce_MetaData[];
#endif
		static void NewProp_bEnableSlammingForce_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bEnableSlammingForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bEnableForceClamping_MetaData[];
#endif
		static void NewProp_bEnableForceClamping_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bEnableForceClamping;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugSubmersion_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugSubmersion_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugSubmersion;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugTriangleData_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugTriangleData_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugTriangleData;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugBuoyancyForce_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugBuoyancyForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugBuoyancyForce;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugViscousFluidResistance_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugViscousFluidResistance_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugViscousFluidResistance;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugPressureDragForce_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugPressureDragForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugPressureDragForce;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugSlammingForce_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugSlammingForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugSlammingForce;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_DebugFluidVelocity_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DebugFluidVelocity_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_DebugFluidVelocity;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FWaterPhysicsSettings>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_FluidDensity = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity = { "bOverride_FluidDensity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_FluidKinematicViscocity = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity = { "bOverride_FluidKinematicViscocity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_WaterInfoFetchingMethod = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod = { "bOverride_WaterInfoFetchingMethod", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_SubdivisionSettings = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings = { "bOverride_SubdivisionSettings", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_SubmergedTessellationSettings = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings = { "bOverride_SubmergedTessellationSettings", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_PressureCoefficientOfLinearSpeed = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed = { "bOverride_PressureCoefficientOfLinearSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_PressureCoefficientOfExponentialSpeed = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed = { "bOverride_PressureCoefficientOfExponentialSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_PressureAngularDependence = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence = { "bOverride_PressureAngularDependence", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_SuctionCoefficientOfLinearSpeed = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed = { "bOverride_SuctionCoefficientOfLinearSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_SuctionCoefficientOfExponentialSpeed = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed = { "bOverride_SuctionCoefficientOfExponentialSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_SuctionAngularDependence = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence = { "bOverride_SuctionAngularDependence", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DragReferenceSpeed = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed = { "bOverride_DragReferenceSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_MaxSlammingForceAtAcceleration = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration = { "bOverride_MaxSlammingForceAtAcceleration", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_SlammingForceExponent = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent = { "bOverride_SlammingForceExponent", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_bEnableBuoyancyForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce = { "bOverride_bEnableBuoyancyForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_bEnableViscousFluidResistance = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance = { "bOverride_bEnableViscousFluidResistance", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_bEnablePressureDragForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce = { "bOverride_bEnablePressureDragForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_bEnableSlammingForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce = { "bOverride_bEnableSlammingForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_bEnableForceClamping = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping = { "bOverride_bEnableForceClamping", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugSubmersion = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion = { "bOverride_DebugSubmersion", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugTriangleData = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData = { "bOverride_DebugTriangleData", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugBuoyancyForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce = { "bOverride_DebugBuoyancyForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugViscousFluidResistance = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance = { "bOverride_DebugViscousFluidResistance", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugPressureDragForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce = { "bOverride_DebugPressureDragForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugSlammingForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce = { "bOverride_DebugSlammingForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity_MetaData[] = {
		{ "Category", "Overrides" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "PinHiddenByDefault", "" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bOverride_DebugFluidVelocity = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity = { "bOverride_DebugFluidVelocity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool , RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(uint8), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidDensity_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "ClampMin", "0.001" },
		{ "Comment", "/* \n\x09\x09""Fluid Density measured in kg/m3\n\n\x09\x09Primarily affects strength of buoyancy.\n\x09*/" },
		{ "EditCondition", "bOverride_FluidDensity" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Fluid Density measured in kg/m3\n\nPrimarily affects strength of buoyancy." },
		{ "UIMax", "10000" },
		{ "UIMin", "0.001" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidDensity = { "FluidDensity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, FluidDensity), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidDensity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidDensity_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidKinematicViscocity_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "ClampMin", "0.00001" },
		{ "Comment", "/* \n\x09\x09Kinematic Viscocity measured in centistokes (cSt)\n\n\x09\x09""Affects the strength of the viscous fluid resistance. Think honey (2000-3000 cSt) vs water (~1 cSt).\n\x09*/" },
		{ "EditCondition", "bOverride_FluidKinematicViscocity" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Kinematic Viscocity measured in centistokes (cSt)\n\nAffects the strength of the viscous fluid resistance. Think honey (2000-3000 cSt) vs water (~1 cSt)." },
		{ "UIMax", "10" },
		{ "UIMin", "0.00001" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidKinematicViscocity = { "FluidKinematicViscocity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, FluidKinematicViscocity), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidKinematicViscocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidKinematicViscocity_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "Comment", "/*\n\x09\x09Water Info Fetching Method\n\n\x09\x09""Determines how the water surface information will be fetched. By default this uses a water surface fetching algorithm which is \n\x09\x09optimized for precision and speed. If your objects do not require an accurate water surface you could the \"PerObject\" option \n\x09\x09which only fetch the water surface once per object. This will greatly improve performance at the cost of wave accuracy.\x09The per vertex \n\x09\x09option is not recommended unless you know what you are doing.\n\x09*/" },
		{ "EditCondition", "bOverride_WaterInfoFetchingMethod" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Water Info Fetching Method\n\nDetermines how the water surface information will be fetched. By default this uses a water surface fetching algorithm which is\noptimized for precision and speed. If your objects do not require an accurate water surface you could the \"PerObject\" option\nwhich only fetch the water surface once per object. This will greatly improve performance at the cost of wave accuracy. The per vertex\noption is not recommended unless you know what you are doing." },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod = { "WaterInfoFetchingMethod", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, WaterInfoFetchingMethod), Z_Construct_UEnum_WaterPhysics_EWaterInfoFetchingMethod, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubdivisionSettings_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "Comment", "/*\n\x09\x09Subdivision Settings\n\n\x09\x09When generating the underlying triangulated mesh used for water physics calculations, how many times should the triangles for each\n\x09\x09""collider primitive type be split. A higher value can improve simulation stability at the cost of some performance.\n\x09*/" },
		{ "EditCondition", "bOverride_SubdivisionSettings" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Subdivision Settings\n\nWhen generating the underlying triangulated mesh used for water physics calculations, how many times should the triangles for each\ncollider primitive type be split. A higher value can improve simulation stability at the cost of some performance." },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubdivisionSettings = { "SubdivisionSettings", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, SubdivisionSettings), Z_Construct_UScriptStruct_FTriangleSubdivisionSettings, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubdivisionSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubdivisionSettings_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubmergedTessellationSettings_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "Comment", "/*\n\x09\x09Submerged Tessellation Settings\n\n\x09\x09How to tessellate the submerged triangles. Increasing this number will improve the accuracy of the calculations at the cost of some performance.\n\x09*/" },
		{ "EditCondition", "bOverride_SubmergedTessellationSettings" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Submerged Tessellation Settings\n\nHow to tessellate the submerged triangles. Increasing this number will improve the accuracy of the calculations at the cost of some performance." },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubmergedTessellationSettings = { "SubmergedTessellationSettings", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, SubmergedTessellationSettings), Z_Construct_UScriptStruct_FTessellationSettings, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubmergedTessellationSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubmergedTessellationSettings_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfLinearSpeed_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "Comment", "/* \n\x09\x09Pressure Coefficient Of Linear Speed\n\n\x09\x09""Controls the linear drag component of the pressure-drag equation.\n\x09\x09""Example: PressureCoefficientOfLinearSpeed * Speed + PressureCoefficientOfExponentialSpeed * Pow(Speed, 2)\n\x09*/" },
		{ "EditCondition", "bOverride_PressureCoefficientOfLinearSpeed" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Pressure Coefficient Of Linear Speed\n\nControls the linear drag component of the pressure-drag equation.\nExample: PressureCoefficientOfLinearSpeed * Speed + PressureCoefficientOfExponentialSpeed * Pow(Speed, 2)" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfLinearSpeed = { "PressureCoefficientOfLinearSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, PressureCoefficientOfLinearSpeed), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfLinearSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfLinearSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfExponentialSpeed_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "Comment", "/* \n\x09\x09Pressure Coefficient Of Exponential Speed\n\n\x09\x09""Controls the exponential drag component of the pressure-drag equation.\n\x09\x09""Example: PressureCoefficientOfLinearSpeed * Speed + PressureCoefficientOfExponentialSpeed * Pow(Speed, 2)\n\x09*/" },
		{ "EditCondition", "bOverride_PressureCoefficientOfExponentialSpeed" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Pressure Coefficient Of Exponential Speed\n\nControls the exponential drag component of the pressure-drag equation.\nExample: PressureCoefficientOfLinearSpeed * Speed + PressureCoefficientOfExponentialSpeed * Pow(Speed, 2)" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfExponentialSpeed = { "PressureCoefficientOfExponentialSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, PressureCoefficientOfExponentialSpeed), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfExponentialSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfExponentialSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureAngularDependence_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "ClampMax", "1.0" },
		{ "ClampMin", "0.0" },
		{ "Comment", "/* \n\x09\x09Pressure Angular Dependence\n\n\x09\x09The falloff rate of the pressure force in relation to force angle.\n\x09\x09""Example: Force *= Pow(ForceAngle, PressureAngularDependence)\n\x09*/" },
		{ "EditCondition", "bOverride_PressureAngularDependence" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Pressure Angular Dependence\n\nThe falloff rate of the pressure force in relation to force angle.\nExample: Force *= Pow(ForceAngle, PressureAngularDependence)" },
		{ "UIMax", "1.0" },
		{ "UIMin", "0.0" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureAngularDependence = { "PressureAngularDependence", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, PressureAngularDependence), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureAngularDependence_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureAngularDependence_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfLinearSpeed_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "Comment", "/* \n\x09\x09Suction Coefficient Of Linear Speed\n\n\x09\x09""Controls the linear drag component of the suction-drag equation.\n\x09\x09""Example: SuctionCoefficientOfLinearSpeed * Speed + SuctionCoefficientOfExponentialSpeed * Pow(Speed, 2)\n\x09*/" },
		{ "EditCondition", "bOverride_SuctionCoefficientOfLinearSpeed" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Suction Coefficient Of Linear Speed\n\nControls the linear drag component of the suction-drag equation.\nExample: SuctionCoefficientOfLinearSpeed * Speed + SuctionCoefficientOfExponentialSpeed * Pow(Speed, 2)" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfLinearSpeed = { "SuctionCoefficientOfLinearSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, SuctionCoefficientOfLinearSpeed), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfLinearSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfLinearSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfExponentialSpeed_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "Comment", "/* \n\x09\x09Suction Coefficient Of Exponential Speed\n\n\x09\x09""Controls the exponential drag component of the suction-drag equation.\n\x09\x09""Example: SuctionCoefficientOfLinearSpeed * Speed + SuctionCoefficientOfExponentialSpeed * Pow(Speed, 2)\n\x09*/" },
		{ "EditCondition", "bOverride_SuctionCoefficientOfExponentialSpeed" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Suction Coefficient Of Exponential Speed\n\nControls the exponential drag component of the suction-drag equation.\nExample: SuctionCoefficientOfLinearSpeed * Speed + SuctionCoefficientOfExponentialSpeed * Pow(Speed, 2)" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfExponentialSpeed = { "SuctionCoefficientOfExponentialSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, SuctionCoefficientOfExponentialSpeed), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfExponentialSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfExponentialSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionAngularDependence_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "ClampMax", "1.0" },
		{ "ClampMin", "0.0" },
		{ "Comment", "/* \n\x09\x09Suction Angular Dependence\n\n\x09\x09The falloff rate of the suction force in relation to force angle.\n\x09\x09""Example: Force *= Pow(ForceAngle, SuctionAngularDependence)\n\x09*/" },
		{ "EditCondition", "bOverride_SuctionAngularDependence" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Suction Angular Dependence\n\nThe falloff rate of the suction force in relation to force angle.\nExample: Force *= Pow(ForceAngle, SuctionAngularDependence)" },
		{ "UIMax", "1.0" },
		{ "UIMin", "0.0" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionAngularDependence = { "SuctionAngularDependence", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, SuctionAngularDependence), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionAngularDependence_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionAngularDependence_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DragReferenceSpeed_MetaData[] = {
		{ "Category", "Water Physics Drag" },
		{ "ClampMin", "0.001" },
		{ "Comment", "/* \n\x09\x09""Drag Reference Speed\n\n\x09\x09The speed at which exponential component of the pressure/suction drag equation will begin to increase faster than the linear component.\n\x09\x09In layman terms: The speed at which the drag will start to increase exponentially.\n\x09*/" },
		{ "EditCondition", "bOverride_DragReferenceSpeed" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Drag Reference Speed\n\nThe speed at which exponential component of the pressure/suction drag equation will begin to increase faster than the linear component.\nIn layman terms: The speed at which the drag will start to increase exponentially." },
		{ "UIMax", "1000.0" },
		{ "UIMin", "0.001" },
		{ "Units", "m/s" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DragReferenceSpeed = { "DragReferenceSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DragReferenceSpeed), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DragReferenceSpeed_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DragReferenceSpeed_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_MaxSlammingForceAtAcceleration_MetaData[] = {
		{ "Category", "Water Physics Slamming" },
		{ "ClampMin", "0.001" },
		{ "Comment", "/* \n\x09\x09Max Slamming Force At Acceleration\n\n\x09\x09The acceleration at which the body would stop instantly if accelerating at, or faster, than this value into the water.\n\x09*/" },
		{ "EditCondition", "bOverride_MaxSlammingForceAtAcceleration" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Max Slamming Force At Acceleration\n\nThe acceleration at which the body would stop instantly if accelerating at, or faster, than this value into the water." },
		{ "UIMax", "1000.0" },
		{ "UIMin", "0.001" },
		{ "Units", "m/s" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_MaxSlammingForceAtAcceleration = { "MaxSlammingForceAtAcceleration", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, MaxSlammingForceAtAcceleration), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_MaxSlammingForceAtAcceleration_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_MaxSlammingForceAtAcceleration_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SlammingForceExponent_MetaData[] = {
		{ "Category", "Water Physics Slamming" },
		{ "ClampMin", "0.001" },
		{ "Comment", "/* \n\x09\x09Slamming Force Exponent\n\n\x09\x09""Exponent of the slamming force gradient e.g. Pow(amount of slamming force(0 - 1), SlammingForceExponent).\n\x09\x09""A lower exponent will increase the \"stiffness\" of the slamming force, making it skipp more on the surface of the water.\n\x09*/" },
		{ "EditCondition", "bOverride_SlammingForceExponent" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Slamming Force Exponent\n\nExponent of the slamming force gradient e.g. Pow(amount of slamming force(0 - 1), SlammingForceExponent).\nA lower exponent will increase the \"stiffness\" of the slamming force, making it skipp more on the surface of the water." },
		{ "UIMax", "10.0" },
		{ "UIMin", "0.001" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SlammingForceExponent = { "SlammingForceExponent", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, SlammingForceExponent), METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SlammingForceExponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SlammingForceExponent_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce_MetaData[] = {
		{ "Category", "Water Physics Forces" },
		{ "EditCondition", "bOverride_bEnableBuoyancyForce" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bEnableBuoyancyForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce = { "bEnableBuoyancyForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance_MetaData[] = {
		{ "Category", "Water Physics Forces" },
		{ "EditCondition", "bOverride_bEnableViscousFluidResistance" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bEnableViscousFluidResistance = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance = { "bEnableViscousFluidResistance", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce_MetaData[] = {
		{ "Category", "Water Physics Forces" },
		{ "EditCondition", "bOverride_bEnablePressureDragForce" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bEnablePressureDragForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce = { "bEnablePressureDragForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce_MetaData[] = {
		{ "Category", "Water Physics Forces" },
		{ "EditCondition", "bOverride_bEnableSlammingForce" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bEnableSlammingForce = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce = { "bEnableSlammingForce", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping_MetaData[] = {
		{ "Category", "Water Physics Forces" },
		{ "EditCondition", "bOverride_bEnableForceClamping" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping_SetBit(void* Obj)
	{
		((FWaterPhysicsSettings*)Obj)->bEnableForceClamping = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping = { "bEnableForceClamping", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterPhysicsSettings), &Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugSubmersion" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion = { "DebugSubmersion", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugSubmersion), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugTriangleData" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData = { "DebugTriangleData", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugTriangleData), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugBuoyancyForce" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce = { "DebugBuoyancyForce", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugBuoyancyForce), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugViscousFluidResistance" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance = { "DebugViscousFluidResistance", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugViscousFluidResistance), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugPressureDragForce" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce = { "DebugPressureDragForce", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugPressureDragForce), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugSlammingForce" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce = { "DebugSlammingForce", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugSlammingForce), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "EditCondition", "bOverride_DebugFluidVelocity" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity = { "DebugFluidVelocity", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsSettings, DebugFluidVelocity), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsDebugLevel, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidDensity,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_FluidKinematicViscocity,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_WaterInfoFetchingMethod,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubdivisionSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SubmergedTessellationSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfLinearSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureCoefficientOfExponentialSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_PressureAngularDependence,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfLinearSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionCoefficientOfExponentialSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SuctionAngularDependence,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DragReferenceSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_MaxSlammingForceAtAcceleration,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_SlammingForceExponent,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableBuoyancyForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableViscousFluidResistance,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnablePressureDragForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableSlammingForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_bEnableForceClamping,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSubmersion,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugTriangleData,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugBuoyancyForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugViscousFluidResistance,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugPressureDragForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugSlammingForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bOverride_DebugFluidVelocity,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidDensity,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_FluidKinematicViscocity,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_WaterInfoFetchingMethod,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubdivisionSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SubmergedTessellationSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfLinearSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureCoefficientOfExponentialSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_PressureAngularDependence,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfLinearSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionCoefficientOfExponentialSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SuctionAngularDependence,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DragReferenceSpeed,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_MaxSlammingForceAtAcceleration,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_SlammingForceExponent,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableBuoyancyForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableViscousFluidResistance,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnablePressureDragForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableSlammingForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_bEnableForceClamping,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSubmersion,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugTriangleData,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugBuoyancyForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugViscousFluidResistance,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugPressureDragForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugSlammingForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::NewProp_DebugFluidVelocity,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"WaterPhysicsSettings",
		sizeof(FWaterPhysicsSettings),
		alignof(FWaterPhysicsSettings),
		Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000201),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsSettings()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsSettings_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("WaterPhysicsSettings"), sizeof(FWaterPhysicsSettings), Get_Z_Construct_UScriptStruct_FWaterPhysicsSettings_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FWaterPhysicsSettings_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsSettings_Hash() { return 1206262784U; }
class UScriptStruct* FTriangleSubdivisionSettings::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("TriangleSubdivisionSettings"), sizeof(FTriangleSubdivisionSettings), Get_Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FTriangleSubdivisionSettings>()
{
	return FTriangleSubdivisionSettings::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FTriangleSubdivisionSettings(FTriangleSubdivisionSettings::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("TriangleSubdivisionSettings"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFTriangleSubdivisionSettings
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFTriangleSubdivisionSettings()
	{
		UScriptStruct::DeferCppStructOps<FTriangleSubdivisionSettings>(FName(TEXT("TriangleSubdivisionSettings")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFTriangleSubdivisionSettings;
	struct Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Box_MetaData[];
#endif
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_Box;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Convex_MetaData[];
#endif
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_Convex;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Sphere_MetaData[];
#endif
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_Sphere;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Capsule_MetaData[];
#endif
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_Capsule;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FTriangleSubdivisionSettings>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Box_MetaData[] = {
		{ "Category", "Subdivision Settings" },
		{ "ClampMin", "0" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "UIMax", "5" },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Box = { "Box", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTriangleSubdivisionSettings, Box), METADATA_PARAMS(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Box_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Box_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Convex_MetaData[] = {
		{ "Category", "Subdivision Settings" },
		{ "ClampMin", "0" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "UIMax", "5" },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Convex = { "Convex", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTriangleSubdivisionSettings, Convex), METADATA_PARAMS(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Convex_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Convex_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Sphere_MetaData[] = {
		{ "Category", "Subdivision Settings" },
		{ "ClampMin", "0" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "UIMax", "5" },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Sphere = { "Sphere", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTriangleSubdivisionSettings, Sphere), METADATA_PARAMS(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Sphere_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Sphere_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Capsule_MetaData[] = {
		{ "Category", "Subdivision Settings" },
		{ "ClampMin", "0" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "UIMax", "5" },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Capsule = { "Capsule", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTriangleSubdivisionSettings, Capsule), METADATA_PARAMS(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Capsule_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Capsule_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Box,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Convex,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Sphere,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::NewProp_Capsule,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"TriangleSubdivisionSettings",
		sizeof(FTriangleSubdivisionSettings),
		alignof(FTriangleSubdivisionSettings),
		Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000201),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FTriangleSubdivisionSettings()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("TriangleSubdivisionSettings"), sizeof(FTriangleSubdivisionSettings), Get_Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FTriangleSubdivisionSettings_Hash() { return 4039241530U; }
class UScriptStruct* FTessellationSettings::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FTessellationSettings_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FTessellationSettings, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("TessellationSettings"), sizeof(FTessellationSettings), Get_Z_Construct_UScriptStruct_FTessellationSettings_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FTessellationSettings>()
{
	return FTessellationSettings::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FTessellationSettings(FTessellationSettings::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("TessellationSettings"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFTessellationSettings
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFTessellationSettings()
	{
		UScriptStruct::DeferCppStructOps<FTessellationSettings>(FName(TEXT("TessellationSettings")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFTessellationSettings;
	struct Z_Construct_UScriptStruct_FTessellationSettings_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_TessellationMode_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_TessellationMode_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_TessellationMode;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_MaxArea_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_MaxArea;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Levels_MetaData[];
#endif
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_Levels;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTessellationSettings_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FTessellationSettings>();
	}
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode_MetaData[] = {
		{ "Category", "Tessellation Settings" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode = { "TessellationMode", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTessellationSettings, TessellationMode), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsTessellationMode, METADATA_PARAMS(Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_MaxArea_MetaData[] = {
		{ "Category", "Tessellation Settings" },
		{ "ClampMin", "0.01" },
		{ "Comment", "// Minimum area (m^2) to subdivide the triangle to\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Minimum area (m^2) to subdivide the triangle to" },
		{ "UIMax", "5" },
		{ "UIMin", "0.1" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_MaxArea = { "MaxArea", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTessellationSettings, MaxArea), METADATA_PARAMS(Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_MaxArea_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_MaxArea_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_Levels_MetaData[] = {
		{ "Category", "Tessellation Settings" },
		{ "ClampMin", "0" },
		{ "Comment", "// Nr of times to subdived all triangles\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
		{ "ToolTip", "Nr of times to subdived all triangles" },
		{ "UIMax", "5" },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_Levels = { "Levels", nullptr, (EPropertyFlags)0x0010000000000015, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FTessellationSettings, Levels), METADATA_PARAMS(Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_Levels_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_Levels_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FTessellationSettings_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_TessellationMode,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_MaxArea,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FTessellationSettings_Statics::NewProp_Levels,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FTessellationSettings_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"TessellationSettings",
		sizeof(FTessellationSettings),
		alignof(FTessellationSettings),
		Z_Construct_UScriptStruct_FTessellationSettings_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTessellationSettings_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FTessellationSettings_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FTessellationSettings_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FTessellationSettings()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FTessellationSettings_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("TessellationSettings"), sizeof(FTessellationSettings), Get_Z_Construct_UScriptStruct_FTessellationSettings_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FTessellationSettings_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FTessellationSettings_Hash() { return 2593663504U; }
class UScriptStruct* FGetWaterInfoResult::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FGetWaterInfoResult_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FGetWaterInfoResult, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("GetWaterInfoResult"), sizeof(FGetWaterInfoResult), Get_Z_Construct_UScriptStruct_FGetWaterInfoResult_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FGetWaterInfoResult>()
{
	return FGetWaterInfoResult::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FGetWaterInfoResult(FGetWaterInfoResult::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("GetWaterInfoResult"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFGetWaterInfoResult
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFGetWaterInfoResult()
	{
		UScriptStruct::DeferCppStructOps<FGetWaterInfoResult>(FName(TEXT("GetWaterInfoResult")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFGetWaterInfoResult;
	struct Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterSurfaceLocation_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterSurfaceLocation;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterSurfaceNormal_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterSurfaceNormal;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterVelocity_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterVelocity;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FGetWaterInfoResult>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceLocation_MetaData[] = {
		{ "Category", "Water Info" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceLocation = { "WaterSurfaceLocation", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FGetWaterInfoResult, WaterSurfaceLocation), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceLocation_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceLocation_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceNormal_MetaData[] = {
		{ "Category", "Water Info" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceNormal = { "WaterSurfaceNormal", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FGetWaterInfoResult, WaterSurfaceNormal), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceNormal_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceNormal_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterVelocity_MetaData[] = {
		{ "Category", "Water Info" },
		{ "ModuleRelativePath", "Public/WaterPhysicsTypes.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterVelocity = { "WaterVelocity", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FGetWaterInfoResult, WaterVelocity), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterVelocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterVelocity_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceLocation,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterSurfaceNormal,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::NewProp_WaterVelocity,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"GetWaterInfoResult",
		sizeof(FGetWaterInfoResult),
		alignof(FGetWaterInfoResult),
		Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FGetWaterInfoResult()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FGetWaterInfoResult_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("GetWaterInfoResult"), sizeof(FGetWaterInfoResult), Get_Z_Construct_UScriptStruct_FGetWaterInfoResult_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FGetWaterInfoResult_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FGetWaterInfoResult_Hash() { return 3874735558U; }
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
