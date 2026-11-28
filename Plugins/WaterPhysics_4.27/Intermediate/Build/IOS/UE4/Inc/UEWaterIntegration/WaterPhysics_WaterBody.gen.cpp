// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "UEWaterIntegration/Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysics_WaterBody() {}
// Cross Module References
	UEWATERINTEGRATION_API UScriptStruct* Z_Construct_UScriptStruct_FWaterBodySetup();
	UPackage* Z_Construct_UPackage__Script_UEWaterIntegration();
	WATER_API UClass* Z_Construct_UClass_AWaterBody_NoRegister();
	UEWATERINTEGRATION_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBody_NoRegister();
	UEWATERINTEGRATION_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBody();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase();
// End Cross Module References
class UScriptStruct* FWaterBodySetup::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern UEWATERINTEGRATION_API uint32 Get_Z_Construct_UScriptStruct_FWaterBodySetup_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FWaterBodySetup, Z_Construct_UPackage__Script_UEWaterIntegration(), TEXT("WaterBodySetup"), sizeof(FWaterBodySetup), Get_Z_Construct_UScriptStruct_FWaterBodySetup_Hash());
	}
	return Singleton;
}
template<> UEWATERINTEGRATION_API UScriptStruct* StaticStruct<FWaterBodySetup>()
{
	return FWaterBodySetup::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FWaterBodySetup(FWaterBodySetup::StaticStruct, TEXT("/Script/UEWaterIntegration"), TEXT("WaterBodySetup"), false, nullptr, nullptr);
static struct FScriptStruct_UEWaterIntegration_StaticRegisterNativesFWaterBodySetup
{
	FScriptStruct_UEWaterIntegration_StaticRegisterNativesFWaterBodySetup()
	{
		UScriptStruct::DeferCppStructOps<FWaterBodySetup>(FName(TEXT("WaterBodySetup")));
	}
} ScriptStruct_UEWaterIntegration_StaticRegisterNativesFWaterBodySetup;
	struct Z_Construct_UScriptStruct_FWaterBodySetup_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterBody_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_WaterBody;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bIncludeWaves_MetaData[];
#endif
		static void NewProp_bIncludeWaves_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bIncludeWaves;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bUseSimpleWaves_MetaData[];
#endif
		static void NewProp_bUseSimpleWaves_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bUseSimpleWaves;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bIncludeVelocity_MetaData[];
#endif
		static void NewProp_bIncludeVelocity_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bIncludeVelocity;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodySetup_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FWaterBodySetup>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_WaterBody_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_WaterBody = { "WaterBody", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterBodySetup, WaterBody), Z_Construct_UClass_AWaterBody_NoRegister, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_WaterBody_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_WaterBody_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves_SetBit(void* Obj)
	{
		((FWaterBodySetup*)Obj)->bIncludeWaves = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves = { "bIncludeWaves", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterBodySetup), &Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "EditCondition", "bIncludeWaves" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves_SetBit(void* Obj)
	{
		((FWaterBodySetup*)Obj)->bUseSimpleWaves = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves = { "bUseSimpleWaves", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterBodySetup), &Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
	};
#endif
	void Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity_SetBit(void* Obj)
	{
		((FWaterBodySetup*)Obj)->bIncludeVelocity = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity = { "bIncludeVelocity", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(FWaterBodySetup), &Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity_SetBit, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FWaterBodySetup_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_WaterBody,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeWaves,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bUseSimpleWaves,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterBodySetup_Statics::NewProp_bIncludeVelocity,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FWaterBodySetup_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_UEWaterIntegration,
		nullptr,
		&NewStructOps,
		"WaterBodySetup",
		sizeof(FWaterBodySetup),
		alignof(FWaterBodySetup),
		Z_Construct_UScriptStruct_FWaterBodySetup_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodySetup_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FWaterBodySetup()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FWaterBodySetup_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_UEWaterIntegration();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("WaterBodySetup"), sizeof(FWaterBodySetup), Get_Z_Construct_UScriptStruct_FWaterBodySetup_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FWaterBodySetup_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FWaterBodySetup_Hash() { return 3032979195U; }
	void AWaterPhysics_WaterBody::StaticRegisterNativesAWaterPhysics_WaterBody()
	{
	}
	UClass* Z_Construct_UClass_AWaterPhysics_WaterBody_NoRegister()
	{
		return AWaterPhysics_WaterBody::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysics_WaterBody_Statics
	{
		static UObject* (*const DependentSingletons[])();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterBodies_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterBodies_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_WaterBodies;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AWaterPhysics_WaterBodyBase,
		(UObject* (*)())Z_Construct_UPackage__Script_UEWaterIntegration,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "Comment", "// A class for adding water physics simulation Unreal's built in water system. \n// This class uses overlapping with the water surface to automatically add/remove actors from the water physics simulation.\n// To manually add/remove actors to the water physics simulation, use the AddActorToWater and RemoveActorFromWater functions on this actor.\n" },
		{ "DisplayName", "Water Physics - UE4 Water Body" },
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
		{ "ToolTip", "A class for adding water physics simulation Unreal's built in water system.\nThis class uses overlapping with the water surface to automatically add/remove actors from the water physics simulation.\nTo manually add/remove actors to the water physics simulation, use the AddActorToWater and RemoveActorFromWater functions on this actor." },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies_Inner = { "WaterBodies", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UScriptStruct_FWaterBodySetup, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "// List of UE4 water bodies which should be included in the water physics simulation.\n// If you have overlapping water bodies they will be prioritized in the order they appear in this list (Lower index equals more important).\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBody.h" },
		{ "ToolTip", "List of UE4 water bodies which should be included in the water physics simulation.\nIf you have overlapping water bodies they will be prioritized in the order they appear in this list (Lower index equals more important)." },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies = { "WaterBodies", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_WaterBody, WaterBodies), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::NewProp_WaterBodies,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysics_WaterBody>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::ClassParams = {
		&AWaterPhysics_WaterBody::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		nullptr,
		Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		0,
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::PropPointers),
		0,
		0x009000A4u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysics_WaterBody()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysics_WaterBody_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysics_WaterBody, 3716893647);
	template<> UEWATERINTEGRATION_API UClass* StaticClass<AWaterPhysics_WaterBody>()
	{
		return AWaterPhysics_WaterBody::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysics_WaterBody(Z_Construct_UClass_AWaterPhysics_WaterBody, &AWaterPhysics_WaterBody::StaticClass, TEXT("/Script/UEWaterIntegration"), TEXT("AWaterPhysics_WaterBody"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysics_WaterBody);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
