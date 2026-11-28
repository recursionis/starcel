// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsSimulations/WaterPhysics_GenericWaterBody.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysics_GenericWaterBody() {}
// Cross Module References
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_GenericWaterBody_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_GenericWaterBody();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
// End Cross Module References
	void AWaterPhysics_GenericWaterBody::StaticRegisterNativesAWaterPhysics_GenericWaterBody()
	{
	}
	UClass* Z_Construct_UClass_AWaterPhysics_GenericWaterBody_NoRegister()
	{
		return AWaterPhysics_GenericWaterBody::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics
	{
		static UObject* (*const DependentSingletons[])();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_WaterBodies_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterBodies_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_WaterBodies;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AWaterPhysics_WaterBodyBase,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "Comment", "// A class for adding water physics simulation to any actor which can generate overlap events.\n// The surface of the water is assumed to be at the center of the actor included as a water body.\n// \n// To manually specify the location of the water surface, override the CalculateWaterInfoForWaterBody function either in C++ or in Blueprint.\n// IMPORTANT: By default parallell fetching of water surface info is enabled, if your water surface calculation is not thread safe then this needs to be disabled!!!\n" },
		{ "DisplayName", "Water Physics - Generic Water Body" },
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysics_GenericWaterBody.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_GenericWaterBody.h" },
		{ "ToolTip", "A class for adding water physics simulation to any actor which can generate overlap events.\nThe surface of the water is assumed to be at the center of the actor included as a water body.\n\nTo manually specify the location of the water surface, override the CalculateWaterInfoForWaterBody function either in C++ or in Blueprint.\nIMPORTANT: By default parallell fetching of water surface info is enabled, if your water surface calculation is not thread safe then this needs to be disabled!!!" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies_Inner = { "WaterBodies", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies_MetaData[] = {
		{ "Category", "Generic Water Volume" },
		{ "Comment", "// List of actors which should be included as a water body in the water physics simulation.\n// If you have overlapping actors they will be prioritized in the order they appear in this list (Lower index equals more important).\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_GenericWaterBody.h" },
		{ "ToolTip", "List of actors which should be included as a water body in the water physics simulation.\nIf you have overlapping actors they will be prioritized in the order they appear in this list (Lower index equals more important)." },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies = { "WaterBodies", nullptr, (EPropertyFlags)0x0020080000000015, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_GenericWaterBody, WaterBodies), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::NewProp_WaterBodies,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysics_GenericWaterBody>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::ClassParams = {
		&AWaterPhysics_GenericWaterBody::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		nullptr,
		Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		0,
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::PropPointers),
		0,
		0x009000A4u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysics_GenericWaterBody()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysics_GenericWaterBody_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysics_GenericWaterBody, 1545916702);
	template<> WATERPHYSICS_API UClass* StaticClass<AWaterPhysics_GenericWaterBody>()
	{
		return AWaterPhysics_GenericWaterBody::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysics_GenericWaterBody(Z_Construct_UClass_AWaterPhysics_GenericWaterBody, &AWaterPhysics_GenericWaterBody::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("AWaterPhysics_GenericWaterBody"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysics_GenericWaterBody);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
