// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsCollisionInterface.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysicsCollisionInterface() {}
// Cross Module References
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsCollisionInterface_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsCollisionInterface();
	COREUOBJECT_API UClass* Z_Construct_UClass_UInterface();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
// End Cross Module References
	void UWaterPhysicsCollisionInterface::StaticRegisterNativesUWaterPhysicsCollisionInterface()
	{
	}
	UClass* Z_Construct_UClass_UWaterPhysicsCollisionInterface_NoRegister()
	{
		return UWaterPhysicsCollisionInterface::StaticClass();
	}
	struct Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics
	{
		static UObject* (*const DependentSingletons[])();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_UInterface,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::Class_MetaDataParams[] = {
		{ "CannotImplementInterfaceInBlueprint", "" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionInterface.h" },
	};
#endif
	const FCppClassTypeInfoStatic Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<IWaterPhysicsCollisionInterface>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::ClassParams = {
		&UWaterPhysicsCollisionInterface::StaticClass,
		nullptr,
		&StaticCppClassTypeInfo,
		DependentSingletons,
		nullptr,
		nullptr,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		0,
		0,
		0,
		0x000840A1u,
		METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_UWaterPhysicsCollisionInterface()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_UWaterPhysicsCollisionInterface_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(UWaterPhysicsCollisionInterface, 1582358474);
	template<> WATERPHYSICS_API UClass* StaticClass<UWaterPhysicsCollisionInterface>()
	{
		return UWaterPhysicsCollisionInterface::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_UWaterPhysicsCollisionInterface(Z_Construct_UClass_UWaterPhysicsCollisionInterface, &UWaterPhysicsCollisionInterface::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("UWaterPhysicsCollisionInterface"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(UWaterPhysicsCollisionInterface);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
