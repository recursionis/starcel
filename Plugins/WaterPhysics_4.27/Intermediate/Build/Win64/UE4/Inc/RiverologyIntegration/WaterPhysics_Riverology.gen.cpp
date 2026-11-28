// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "RiverologyIntegration/Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysics_Riverology() {}
// Cross Module References
	RIVEROLOGYINTEGRATION_API UScriptStruct* Z_Construct_UScriptStruct_FRiverologyWaterBodySetup();
	UPackage* Z_Construct_UPackage__Script_RiverologyIntegration();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	RIVEROLOGYINTEGRATION_API UClass* Z_Construct_UClass_AWaterPhysics_Riverology_NoRegister();
	RIVEROLOGYINTEGRATION_API UClass* Z_Construct_UClass_AWaterPhysics_Riverology();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase();
// End Cross Module References
class UScriptStruct* FRiverologyWaterBodySetup::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern RIVEROLOGYINTEGRATION_API uint32 Get_Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup, Z_Construct_UPackage__Script_RiverologyIntegration(), TEXT("RiverologyWaterBodySetup"), sizeof(FRiverologyWaterBodySetup), Get_Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Hash());
	}
	return Singleton;
}
template<> RIVEROLOGYINTEGRATION_API UScriptStruct* StaticStruct<FRiverologyWaterBodySetup>()
{
	return FRiverologyWaterBodySetup::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FRiverologyWaterBodySetup(FRiverologyWaterBodySetup::StaticStruct, TEXT("/Script/RiverologyIntegration"), TEXT("RiverologyWaterBodySetup"), false, nullptr, nullptr);
static struct FScriptStruct_RiverologyIntegration_StaticRegisterNativesFRiverologyWaterBodySetup
{
	FScriptStruct_RiverologyIntegration_StaticRegisterNativesFRiverologyWaterBodySetup()
	{
		UScriptStruct::DeferCppStructOps<FRiverologyWaterBodySetup>(FName(TEXT("RiverologyWaterBodySetup")));
	}
} ScriptStruct_RiverologyIntegration_StaticRegisterNativesFRiverologyWaterBodySetup;
	struct Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_RiverologyWater_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_RiverologyWater;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bIncludeVelocity_MetaData[];
#endif
		static void NewProp_bIncludeVelocity_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bIncludeVelocity;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterVelocity_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_WaterVelocity;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FRiverologyWaterBodySetup>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_RiverologyWater_MetaData[] = {
		{ "AllowedClasses", "Riverology" },
		{ "Category", "Water Physics" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_RiverologyWater = { "RiverologyWater", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FRiverologyWaterBodySetup, RiverologyWater), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_RiverologyWater_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_RiverologyWater_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity_SetBit(void* Obj)
	{
		((FRiverologyWaterBodySetup*)Obj)->bIncludeVelocity = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity = { "bIncludeVelocity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FRiverologyWaterBodySetup), &Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_WaterVelocity_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "EditCondition", "bIncludeVelocity" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_WaterVelocity = { "WaterVelocity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FRiverologyWaterBodySetup, WaterVelocity), METADATA_PARAMS(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_WaterVelocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_WaterVelocity_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_RiverologyWater,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_bIncludeVelocity,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::NewProp_WaterVelocity,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_RiverologyIntegration,
		nullptr,
		&NewStructOps,
		"RiverologyWaterBodySetup",
		sizeof(FRiverologyWaterBodySetup),
		alignof(FRiverologyWaterBodySetup),
		Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FRiverologyWaterBodySetup()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_RiverologyIntegration();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("RiverologyWaterBodySetup"), sizeof(FRiverologyWaterBodySetup), Get_Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FRiverologyWaterBodySetup_Hash() { return 1037697853U; }
	void AWaterPhysics_Riverology::StaticRegisterNativesAWaterPhysics_Riverology()
	{
	}
	UClass* Z_Construct_UClass_AWaterPhysics_Riverology_NoRegister()
	{
		return AWaterPhysics_Riverology::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysics_Riverology_Statics
	{
		static UObject* (*const DependentSingletons[])();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_RiverologyWaterBodies_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_RiverologyWaterBodies_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_RiverologyWaterBodies;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysics_Riverology_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AWaterPhysics_WaterBodyBase,
		(UObject* (*)())Z_Construct_UPackage__Script_RiverologyIntegration,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Riverology_Statics::Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "DisplayName", "Water Physics - Riverology" },
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies_Inner = { "RiverologyWaterBodies", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UScriptStruct_FRiverologyWaterBodySetup, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "// List of Riverology water bodies which should be included in the water physics simulation.\n// If you have overlapping rivers they will be prioritized in the order they appear in this list (Lower index equals more important).\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Riverology.h" },
		{ "ToolTip", "List of Riverology water bodies which should be included in the water physics simulation.\nIf you have overlapping rivers they will be prioritized in the order they appear in this list (Lower index equals more important)." },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies = { "RiverologyWaterBodies", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Riverology, RiverologyWaterBodies), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysics_Riverology_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Riverology_Statics::NewProp_RiverologyWaterBodies,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysics_Riverology_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysics_Riverology>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysics_Riverology_Statics::ClassParams = {
		&AWaterPhysics_Riverology::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		nullptr,
		Z_Construct_UClass_AWaterPhysics_Riverology_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		0,
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Riverology_Statics::PropPointers),
		0,
		0x009000A4u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Riverology_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Riverology_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysics_Riverology()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysics_Riverology_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysics_Riverology, 1761869157);
	template<> RIVEROLOGYINTEGRATION_API UClass* StaticClass<AWaterPhysics_Riverology>()
	{
		return AWaterPhysics_Riverology::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysics_Riverology(Z_Construct_UClass_AWaterPhysics_Riverology, &AWaterPhysics_Riverology::StaticClass, TEXT("/Script/RiverologyIntegration"), TEXT("AWaterPhysics_Riverology"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysics_Riverology);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
