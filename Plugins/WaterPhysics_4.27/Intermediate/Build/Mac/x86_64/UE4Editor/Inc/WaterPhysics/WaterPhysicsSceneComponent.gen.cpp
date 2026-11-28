// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsSceneComponent.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysicsSceneComponent() {}
// Cross Module References
	WATERPHYSICS_API UFunction* Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	WATERPHYSICS_API UFunction* Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature();
	ENGINE_API UClass* Z_Construct_UClass_UActorComponent_NoRegister();
	COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FGetWaterInfoResult();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsActingForces();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsSceneComponent_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsSceneComponent();
	ENGINE_API UClass* Z_Construct_UClass_UActorComponent();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsSettings();
// End Cross Module References
	struct Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature_Statics::FuncParams = { (UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics, nullptr, "K2_PreStepWaterPhysicsScene__DelegateSignature", nullptr, nullptr, 0, nullptr, 0, RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00130000, 0, 0, METADATA_PARAMS(Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics
	{
		struct _Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms
		{
			const UActorComponent* Component;
			FVector Location;
			FGetWaterInfoResult ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Location_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_Location;
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080082, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(_Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Component_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Location_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Location = { "Location", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(_Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms, Location), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Location_MetaData, UE_ARRAY_COUNT(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Location_MetaData)) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(_Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms, ReturnValue), Z_Construct_UScriptStruct_FGetWaterInfoResult, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_Location,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::FuncParams = { (UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics, nullptr, "BlueprintGetWaterInfoAtLocation__DelegateSignature", nullptr, nullptr, sizeof(_Script_WaterPhysics_eventBlueprintGetWaterInfoAtLocation_Parms), Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00120000, 0, 0, METADATA_PARAMS(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature_Statics::FuncParams);
		}
		return ReturnFunction;
	}
class UScriptStruct* FWaterPhysicsActingForces::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FWaterPhysicsActingForces, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("WaterPhysicsActingForces"), sizeof(FWaterPhysicsActingForces), Get_Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FWaterPhysicsActingForces>()
{
	return FWaterPhysicsActingForces::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FWaterPhysicsActingForces(FWaterPhysicsActingForces::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("WaterPhysicsActingForces"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsActingForces
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsActingForces()
	{
		UScriptStruct::DeferCppStructOps<FWaterPhysicsActingForces>(FName(TEXT("WaterPhysicsActingForces")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFWaterPhysicsActingForces;
	struct Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_BuoyancyForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_BuoyancyForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_BuoyancyTorque_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_BuoyancyTorque;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ViscousFluidResistanceForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ViscousFluidResistanceForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ViscousFluidResistanceTorque_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ViscousFluidResistanceTorque;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_PressureDragForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_PressureDragForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_PressureDragTorque_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_PressureDragTorque;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SlammingForce_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_SlammingForce;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SlammingTorque_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_SlammingTorque;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FWaterPhysicsActingForces>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyForce_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyForce = { "BuoyancyForce", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, BuoyancyForce), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyTorque_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyTorque = { "BuoyancyTorque", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, BuoyancyTorque), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyTorque_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyTorque_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceForce_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceForce = { "ViscousFluidResistanceForce", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, ViscousFluidResistanceForce), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceTorque_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceTorque = { "ViscousFluidResistanceTorque", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, ViscousFluidResistanceTorque), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceTorque_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceTorque_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragForce_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragForce = { "PressureDragForce", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, PressureDragForce), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragTorque_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragTorque = { "PressureDragTorque", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, PressureDragTorque), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragTorque_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragTorque_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingForce_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingForce = { "SlammingForce", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, SlammingForce), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingForce_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingForce_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingTorque_MetaData[] = {
		{ "Category", "Water Physics Acting Forces" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingTorque = { "SlammingTorque", nullptr, (EPropertyFlags)0x0010000000000004, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterPhysicsActingForces, SlammingTorque), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingTorque_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingTorque_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_BuoyancyTorque,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_ViscousFluidResistanceTorque,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_PressureDragTorque,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingForce,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::NewProp_SlammingTorque,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"WaterPhysicsActingForces",
		sizeof(FWaterPhysicsActingForces),
		alignof(FWaterPhysicsActingForces),
		Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsActingForces()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("WaterPhysicsActingForces"), sizeof(FWaterPhysicsActingForces), Get_Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FWaterPhysicsActingForces_Hash() { return 1325210048U; }
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execK2_SetWaterInfoGetter)
	{
		P_GET_PROPERTY_REF(FDelegateProperty,Z_Param_Out_InWaterInfoGetter);
		P_GET_UBOOL(Z_Param_bThreadSafe);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->K2_SetWaterInfoGetter(FBlueprintGetWaterInfoAtLocation(Z_Param_Out_InWaterInfoGetter),Z_Param_bThreadSafe);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execGetComponentBodySubmergedArea)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_GET_PROPERTY(FNameProperty,Z_Param_BodyName);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(float*)Z_Param__Result=P_THIS->GetComponentBodySubmergedArea(Z_Param_Component,Z_Param_BodyName);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execGetComponentSubmergedArea)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(float*)Z_Param__Result=P_THIS->GetComponentSubmergedArea(Z_Param_Component);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execGetComponentBodyActingWaterPhysicsForces)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_GET_PROPERTY(FNameProperty,Z_Param_BodyName);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(FWaterPhysicsActingForces*)Z_Param__Result=P_THIS->GetComponentBodyActingWaterPhysicsForces(Z_Param_Component,Z_Param_BodyName);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execGetComponentActingWaterPhysicsForces)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(FWaterPhysicsActingForces*)Z_Param__Result=P_THIS->GetComponentActingWaterPhysicsForces(Z_Param_Component);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execContainsComponentBody)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_GET_PROPERTY(FNameProperty,Z_Param_BodyName);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(bool*)Z_Param__Result=P_THIS->ContainsComponentBody(Z_Param_Component,Z_Param_BodyName);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execContainsComponent)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(bool*)Z_Param__Result=P_THIS->ContainsComponent(Z_Param_Component);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execSetComponentWaterPhysicsSettings)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_GET_STRUCT_REF(FWaterPhysicsSettings,Z_Param_Out_WaterPhysicsSettings);
		P_GET_UBOOL(Z_Param_bAllBodies);
		P_GET_PROPERTY(FNameProperty,Z_Param_BodyName);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->SetComponentWaterPhysicsSettings(Z_Param_Component,Z_Param_Out_WaterPhysicsSettings,Z_Param_bAllBodies,Z_Param_BodyName);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execRemoveComponentFromWaterPhysics)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_GET_UBOOL(Z_Param_bAllBodies);
		P_GET_PROPERTY(FNameProperty,Z_Param_BodyName);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(bool*)Z_Param__Result=P_THIS->RemoveComponentFromWaterPhysics(Z_Param_Component,Z_Param_bAllBodies,Z_Param_BodyName);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execAddComponentToWaterPhysics)
	{
		P_GET_OBJECT(UActorComponent,Z_Param_Component);
		P_GET_STRUCT_REF(FWaterPhysicsSettings,Z_Param_Out_WaterPhysicsSettings);
		P_GET_UBOOL(Z_Param_bAllBodies);
		P_GET_PROPERTY(FNameProperty,Z_Param_BodyName);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->AddComponentToWaterPhysics(Z_Param_Component,Z_Param_Out_WaterPhysicsSettings,Z_Param_bAllBodies,Z_Param_BodyName);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execRemoveActorsFromWaterPhysics)
	{
		P_GET_TARRAY_REF(AActor*,Z_Param_Out_Actors);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(bool*)Z_Param__Result=P_THIS->RemoveActorsFromWaterPhysics(Z_Param_Out_Actors);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execAddActorsToWaterPhysics)
	{
		P_GET_TARRAY_REF(AActor*,Z_Param_Out_Actors);
		P_GET_STRUCT_REF(FWaterPhysicsSettings,Z_Param_Out_WaterPhysicsSettings);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->AddActorsToWaterPhysics(Z_Param_Out_Actors,Z_Param_Out_WaterPhysicsSettings);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execRemoveActorFromWaterPhysics)
	{
		P_GET_OBJECT(AActor,Z_Param_Actor);
		P_FINISH;
		P_NATIVE_BEGIN;
		*(bool*)Z_Param__Result=P_THIS->RemoveActorFromWaterPhysics(Z_Param_Actor);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(UWaterPhysicsSceneComponent::execAddActorToWaterPhysics)
	{
		P_GET_OBJECT(AActor,Z_Param_Actor);
		P_GET_STRUCT_REF(FWaterPhysicsSettings,Z_Param_Out_WaterPhysicsSettings);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->AddActorToWaterPhysics(Z_Param_Actor,Z_Param_Out_WaterPhysicsSettings);
		P_NATIVE_END;
	}
	void UWaterPhysicsSceneComponent::StaticRegisterNativesUWaterPhysicsSceneComponent()
	{
		UClass* Class = UWaterPhysicsSceneComponent::StaticClass();
		static const FNameNativePtrPair Funcs[] = {
			{ "AddActorsToWaterPhysics", &UWaterPhysicsSceneComponent::execAddActorsToWaterPhysics },
			{ "AddActorToWaterPhysics", &UWaterPhysicsSceneComponent::execAddActorToWaterPhysics },
			{ "AddComponentToWaterPhysics", &UWaterPhysicsSceneComponent::execAddComponentToWaterPhysics },
			{ "ContainsComponent", &UWaterPhysicsSceneComponent::execContainsComponent },
			{ "ContainsComponentBody", &UWaterPhysicsSceneComponent::execContainsComponentBody },
			{ "GetComponentActingWaterPhysicsForces", &UWaterPhysicsSceneComponent::execGetComponentActingWaterPhysicsForces },
			{ "GetComponentBodyActingWaterPhysicsForces", &UWaterPhysicsSceneComponent::execGetComponentBodyActingWaterPhysicsForces },
			{ "GetComponentBodySubmergedArea", &UWaterPhysicsSceneComponent::execGetComponentBodySubmergedArea },
			{ "GetComponentSubmergedArea", &UWaterPhysicsSceneComponent::execGetComponentSubmergedArea },
			{ "K2_SetWaterInfoGetter", &UWaterPhysicsSceneComponent::execK2_SetWaterInfoGetter },
			{ "RemoveActorFromWaterPhysics", &UWaterPhysicsSceneComponent::execRemoveActorFromWaterPhysics },
			{ "RemoveActorsFromWaterPhysics", &UWaterPhysicsSceneComponent::execRemoveActorsFromWaterPhysics },
			{ "RemoveComponentFromWaterPhysics", &UWaterPhysicsSceneComponent::execRemoveComponentFromWaterPhysics },
			{ "SetComponentWaterPhysicsSettings", &UWaterPhysicsSceneComponent::execSetComponentWaterPhysicsSettings },
		};
		FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics
	{
		struct WaterPhysicsSceneComponent_eventAddActorsToWaterPhysics_Parms
		{
			TArray<AActor*> Actors;
			FWaterPhysicsSettings WaterPhysicsSettings;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actors_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Actors_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_Actors;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterPhysicsSettings;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors_Inner = { "Actors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors = { "Actors", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddActorsToWaterPhysics_Parms, Actors), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_WaterPhysicsSettings = { "WaterPhysicsSettings", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddActorsToWaterPhysics_Parms, WaterPhysicsSettings), Z_Construct_UScriptStruct_FWaterPhysicsSettings, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_Actors,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::NewProp_WaterPhysicsSettings,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Overload of AddActorToWaterPhysics which takes an array of actors.\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Overload of AddActorToWaterPhysics which takes an array of actors." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "AddActorsToWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventAddActorsToWaterPhysics_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics
	{
		struct WaterPhysicsSceneComponent_eventAddActorToWaterPhysics_Parms
		{
			AActor* Actor;
			FWaterPhysicsSettings WaterPhysicsSettings;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterPhysicsSettings;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddActorToWaterPhysics_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_WaterPhysicsSettings = { "WaterPhysicsSettings", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddActorToWaterPhysics_Parms, WaterPhysicsSettings), Z_Construct_UScriptStruct_FWaterPhysicsSettings, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_Actor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::NewProp_WaterPhysicsSettings,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09""Adds all components on the actor which can simulate water physics to the water physics simulation scene.\n\x09\x09WaterPhysicsSettings: Settings used for this actors components.\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Adds all components on the actor which can simulate water physics to the water physics simulation scene.\nWaterPhysicsSettings: Settings used for this actors components." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "AddActorToWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventAddActorToWaterPhysics_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics
	{
		struct WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms
		{
			UActorComponent* Component;
			FWaterPhysicsSettings WaterPhysicsSettings;
			bool bAllBodies;
			FName BodyName;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterPhysicsSettings;
		static void NewProp_bAllBodies_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bAllBodies;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_BodyName;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_Component_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_WaterPhysicsSettings = { "WaterPhysicsSettings", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms, WaterPhysicsSettings), Z_Construct_UScriptStruct_FWaterPhysicsSettings, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_WaterPhysicsSettings_MetaData)) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_bAllBodies_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms*)Obj)->bAllBodies = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_bAllBodies = { "bAllBodies", nullptr, (EPropertyFlags)0x0010040000000080, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_bAllBodies_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_BodyName = { "BodyName", nullptr, (EPropertyFlags)0x0010040000000080, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms, BodyName), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_WaterPhysicsSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_bAllBodies,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::NewProp_BodyName,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "AdvancedDisplay", "bAllBodies,BodyName" },
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09""Adds the components physics bodies to the water physics simulation scene.\n\x09\x09""bAllBodies: Add all physics bodies on the component to the water physics simulation.\n\x09\x09""BodyName: if bAllBodies is false, only add the specified body to the the water physics simulation.\n\x09*/" },
		{ "CPP_Default_bAllBodies", "true" },
		{ "CPP_Default_BodyName", "None" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Adds the components physics bodies to the water physics simulation scene.\nbAllBodies: Add all physics bodies on the component to the water physics simulation.\nBodyName: if bAllBodies is false, only add the specified body to the the water physics simulation." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "AddComponentToWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventAddComponentToWaterPhysics_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics
	{
		struct WaterPhysicsSceneComponent_eventContainsComponent_Parms
		{
			UActorComponent* Component;
			bool ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static void NewProp_ReturnValue_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventContainsComponent_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_Component_MetaData)) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_ReturnValue_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventContainsComponent_Parms*)Obj)->ReturnValue = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventContainsComponent_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09""Checks if the water physics simulation contains any body associated with the component\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Checks if the water physics simulation contains any body associated with the component" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "ContainsComponent", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventContainsComponent_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics
	{
		struct WaterPhysicsSceneComponent_eventContainsComponentBody_Parms
		{
			UActorComponent* Component;
			FName BodyName;
			bool ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_BodyName;
		static void NewProp_ReturnValue_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventContainsComponentBody_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_Component_MetaData)) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_BodyName = { "BodyName", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventContainsComponentBody_Parms, BodyName), METADATA_PARAMS(nullptr, 0) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_ReturnValue_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventContainsComponentBody_Parms*)Obj)->ReturnValue = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventContainsComponentBody_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_BodyName,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09""Checks if the water physics simulation contains a specific body on the component\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Checks if the water physics simulation contains a specific body on the component" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "ContainsComponentBody", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventContainsComponentBody_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics
	{
		struct WaterPhysicsSceneComponent_eventGetComponentActingWaterPhysicsForces_Parms
		{
			UActorComponent* Component;
			FWaterPhysicsActingForces ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentActingWaterPhysicsForces_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_Component_MetaData)) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentActingWaterPhysicsForces_Parms, ReturnValue), Z_Construct_UScriptStruct_FWaterPhysicsActingForces, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Returns the current water physics forces currently acting on all the component bodies\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Returns the current water physics forces currently acting on all the component bodies" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "GetComponentActingWaterPhysicsForces", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventGetComponentActingWaterPhysicsForces_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics
	{
		struct WaterPhysicsSceneComponent_eventGetComponentBodyActingWaterPhysicsForces_Parms
		{
			UActorComponent* Component;
			FName BodyName;
			FWaterPhysicsActingForces ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_BodyName;
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentBodyActingWaterPhysicsForces_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_Component_MetaData)) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_BodyName = { "BodyName", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentBodyActingWaterPhysicsForces_Parms, BodyName), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentBodyActingWaterPhysicsForces_Parms, ReturnValue), Z_Construct_UScriptStruct_FWaterPhysicsActingForces, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_BodyName,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Returns the current water physics forces currently acting on the component body\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Returns the current water physics forces currently acting on the component body" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "GetComponentBodyActingWaterPhysicsForces", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventGetComponentBodyActingWaterPhysicsForces_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics
	{
		struct WaterPhysicsSceneComponent_eventGetComponentBodySubmergedArea_Parms
		{
			UActorComponent* Component;
			FName BodyName;
			float ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_BodyName;
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentBodySubmergedArea_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_Component_MetaData)) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_BodyName = { "BodyName", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentBodySubmergedArea_Parms, BodyName), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentBodySubmergedArea_Parms, ReturnValue), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_BodyName,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Returns the total submerged area of this component body\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Returns the total submerged area of this component body" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "GetComponentBodySubmergedArea", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventGetComponentBodySubmergedArea_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics
	{
		struct WaterPhysicsSceneComponent_eventGetComponentSubmergedArea_Parms
		{
			UActorComponent* Component;
			float ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentSubmergedArea_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_Component_MetaData)) };
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventGetComponentSubmergedArea_Parms, ReturnValue), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Returns the total submerged area of this component\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Returns the total submerged area of this component" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "GetComponentSubmergedArea", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventGetComponentSubmergedArea_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics
	{
		struct WaterPhysicsSceneComponent_eventK2_SetWaterInfoGetter_Parms
		{
			FScriptDelegate InWaterInfoGetter;
			bool bThreadSafe;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_InWaterInfoGetter_MetaData[];
#endif
		static const UE4CodeGen_Private::FDelegatePropertyParams NewProp_InWaterInfoGetter;
		static void NewProp_bThreadSafe_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bThreadSafe;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_InWaterInfoGetter_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FDelegatePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_InWaterInfoGetter = { "InWaterInfoGetter", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Delegate, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventK2_SetWaterInfoGetter_Parms, InWaterInfoGetter), Z_Construct_UDelegateFunction_WaterPhysics_BlueprintGetWaterInfoAtLocation__DelegateSignature, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_InWaterInfoGetter_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_InWaterInfoGetter_MetaData)) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_bThreadSafe_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventK2_SetWaterInfoGetter_Parms*)Obj)->bThreadSafe = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_bThreadSafe = { "bThreadSafe", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventK2_SetWaterInfoGetter_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_bThreadSafe_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_InWaterInfoGetter,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::NewProp_bThreadSafe,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09WARNING: Implementing this function in Blueprint is highly discouraged due to the high potential performance impact.\n\n\x09\x09Set the delegate used to calculate the water-surface.\n\x09\x09""bThreadSafe: Is this surface getter safe to call outside of GameThread?\n\x09*/" },
		{ "DisplayName", "Set Water Info Getter" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "WARNING: Implementing this function in Blueprint is highly discouraged due to the high potential performance impact.\n\nSet the delegate used to calculate the water-surface.\nbThreadSafe: Is this surface getter safe to call outside of GameThread?" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "K2_SetWaterInfoGetter", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventK2_SetWaterInfoGetter_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics
	{
		struct WaterPhysicsSceneComponent_eventRemoveActorFromWaterPhysics_Parms
		{
			AActor* Actor;
			bool ReturnValue;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
		static void NewProp_ReturnValue_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventRemoveActorFromWaterPhysics_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventRemoveActorFromWaterPhysics_Parms*)Obj)->ReturnValue = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventRemoveActorFromWaterPhysics_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::NewProp_Actor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Removes all components on the actor to from water physics simulation scene.\n\x09\x09Returns true if any component was removed.\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Removes all components on the actor to from water physics simulation scene.\nReturns true if any component was removed." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "RemoveActorFromWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventRemoveActorFromWaterPhysics_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics
	{
		struct WaterPhysicsSceneComponent_eventRemoveActorsFromWaterPhysics_Parms
		{
			TArray<AActor*> Actors;
			bool ReturnValue;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actors_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Actors_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_Actors;
		static void NewProp_ReturnValue_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors_Inner = { "Actors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors = { "Actors", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventRemoveActorsFromWaterPhysics_Parms, Actors), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors_MetaData)) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventRemoveActorsFromWaterPhysics_Parms*)Obj)->ReturnValue = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventRemoveActorsFromWaterPhysics_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_Actors,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Overload of RemoveActorFromWaterPhysics which takes an array of actors.\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Overload of RemoveActorFromWaterPhysics which takes an array of actors." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "RemoveActorsFromWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventRemoveActorsFromWaterPhysics_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics
	{
		struct WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms
		{
			UActorComponent* Component;
			bool bAllBodies;
			FName BodyName;
			bool ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
		static void NewProp_bAllBodies_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bAllBodies;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_BodyName;
		static void NewProp_ReturnValue_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_Component_MetaData)) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_bAllBodies_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms*)Obj)->bAllBodies = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_bAllBodies = { "bAllBodies", nullptr, (EPropertyFlags)0x0010040000000080, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_bAllBodies_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_BodyName = { "BodyName", nullptr, (EPropertyFlags)0x0010040000000080, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms, BodyName), METADATA_PARAMS(nullptr, 0) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms*)Obj)->ReturnValue = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_bAllBodies,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_BodyName,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "AdvancedDisplay", "bAllBodies,BodyName" },
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Removes the components physics bodies from the water physics simulation scene.\n\x09\x09""bAllBodies: Remove all physics bodies on the component from the water physics simulation.\n\x09\x09""BodyName: if bAllBodies is false, only remove the specified body from the the water physics simulation.\n\x09*/" },
		{ "CPP_Default_bAllBodies", "true" },
		{ "CPP_Default_BodyName", "None" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Removes the components physics bodies from the water physics simulation scene.\nbAllBodies: Remove all physics bodies on the component from the water physics simulation.\nBodyName: if bAllBodies is false, only remove the specified body from the the water physics simulation." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "RemoveComponentFromWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventRemoveComponentFromWaterPhysics_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics
	{
		struct WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms
		{
			UActorComponent* Component;
			FWaterPhysicsSettings WaterPhysicsSettings;
			bool bAllBodies;
			FName BodyName;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Component_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Component;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterPhysicsSettings;
		static void NewProp_bAllBodies_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bAllBodies;
		static const UE4CodeGen_Private::FNamePropertyParams NewProp_BodyName;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_Component_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_WaterPhysicsSettings_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_WaterPhysicsSettings = { "WaterPhysicsSettings", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms, WaterPhysicsSettings), Z_Construct_UScriptStruct_FWaterPhysicsSettings, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_WaterPhysicsSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_WaterPhysicsSettings_MetaData)) };
	void Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_bAllBodies_SetBit(void* Obj)
	{
		((WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms*)Obj)->bAllBodies = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_bAllBodies = { "bAllBodies", nullptr, (EPropertyFlags)0x0010040000000080, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms), &Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_bAllBodies_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FNamePropertyParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_BodyName = { "BodyName", nullptr, (EPropertyFlags)0x0010040000000080, UE4CodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms, BodyName), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_WaterPhysicsSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_bAllBodies,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::NewProp_BodyName,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::Function_MetaDataParams[] = {
		{ "AdvancedDisplay", "bAllBodies,BodyName" },
		{ "Category", "Water Physics" },
		{ "Comment", "/*\n\x09\x09Update the water physics settings on a components physics bodies.\n\x09\x09""bAllBodies: Update the settings on all the components bodies.\n\x09\x09""BodyName: if bAllBodies is false, only updated the settings on the specified body.\n\x09*/" },
		{ "CPP_Default_bAllBodies", "true" },
		{ "CPP_Default_BodyName", "None" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Update the water physics settings on a components physics bodies.\nbAllBodies: Update the settings on all the components bodies.\nBodyName: if bAllBodies is false, only updated the settings on the specified body." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UWaterPhysicsSceneComponent, nullptr, "SetComponentWaterPhysicsSettings", nullptr, nullptr, sizeof(WaterPhysicsSceneComponent_eventSetComponentWaterPhysicsSettings_Parms), Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	UClass* Z_Construct_UClass_UWaterPhysicsSceneComponent_NoRegister()
	{
		return UWaterPhysicsSceneComponent::StaticClass();
	}
	struct Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics
	{
		static UObject* (*const DependentSingletons[])();
		static const FClassFunctionLinkInfo FuncInfo[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_DefaultWaterPhysicsSettings_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_DefaultWaterPhysicsSettings;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bDrawWaterInfoDebug_MetaData[];
#endif
		static void NewProp_bDrawWaterInfoDebug_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bDrawWaterInfoDebug;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_K2_PreStepWaterPhysicsScene_MetaData[];
#endif
		static const UE4CodeGen_Private::FMulticastDelegatePropertyParams NewProp_K2_PreStepWaterPhysicsScene;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_UActorComponent,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
	const FClassFunctionLinkInfo Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::FuncInfo[] = {
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorsToWaterPhysics, "AddActorsToWaterPhysics" }, // 3699670351
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddActorToWaterPhysics, "AddActorToWaterPhysics" }, // 2663644762
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_AddComponentToWaterPhysics, "AddComponentToWaterPhysics" }, // 2672324894
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponent, "ContainsComponent" }, // 2880047013
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_ContainsComponentBody, "ContainsComponentBody" }, // 3868425236
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentActingWaterPhysicsForces, "GetComponentActingWaterPhysicsForces" }, // 3720154008
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodyActingWaterPhysicsForces, "GetComponentBodyActingWaterPhysicsForces" }, // 3928088324
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentBodySubmergedArea, "GetComponentBodySubmergedArea" }, // 3247593905
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_GetComponentSubmergedArea, "GetComponentSubmergedArea" }, // 2962863533
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_K2_SetWaterInfoGetter, "K2_SetWaterInfoGetter" }, // 3635091608
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorFromWaterPhysics, "RemoveActorFromWaterPhysics" }, // 2069112204
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveActorsFromWaterPhysics, "RemoveActorsFromWaterPhysics" }, // 1265441219
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_RemoveComponentFromWaterPhysics, "RemoveComponentFromWaterPhysics" }, // 2715215574
		{ &Z_Construct_UFunction_UWaterPhysicsSceneComponent_SetComponentWaterPhysicsSettings, "SetComponentWaterPhysicsSettings" }, // 1384709574
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::Class_MetaDataParams[] = {
		{ "BlueprintSpawnableComponent", "" },
		{ "ClassGroupNames", "Physics" },
		{ "Comment", "/* Advanced: Use this component to create custom water physics implementations */" },
		{ "DisplayName", "Water Physics Scene" },
		{ "HideCategories", "ComponentReplication Collision" },
		{ "IncludePath", "WaterPhysicsSceneComponent.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ToolTip", "Advanced: Use this component to create custom water physics implementations" },
	};
#endif
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_DefaultWaterPhysicsSettings_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
		{ "ShowOnlyInnerProperties", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_DefaultWaterPhysicsSettings = { "DefaultWaterPhysicsSettings", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsSceneComponent, DefaultWaterPhysicsSettings), Z_Construct_UScriptStruct_FWaterPhysicsSettings, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_DefaultWaterPhysicsSettings_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_DefaultWaterPhysicsSettings_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug_MetaData[] = {
		{ "Category", "Water Physics Settings" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	void Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug_SetBit(void* Obj)
	{
		((UWaterPhysicsSceneComponent*)Obj)->bDrawWaterInfoDebug = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug = { "bDrawWaterInfoDebug", nullptr, (EPropertyFlags)0x0010040000000005, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(UWaterPhysicsSceneComponent), &Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug_SetBit, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_K2_PreStepWaterPhysicsScene_MetaData[] = {
		{ "Category", "Water Physics Events" },
		{ "DisplayName", "Pre Step Water Physics Scene" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSceneComponent.h" },
	};
#endif
	const UE4CodeGen_Private::FMulticastDelegatePropertyParams Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_K2_PreStepWaterPhysicsScene = { "K2_PreStepWaterPhysicsScene", nullptr, (EPropertyFlags)0x0010000010080000, UE4CodeGen_Private::EPropertyGenFlags::InlineMulticastDelegate, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsSceneComponent, K2_PreStepWaterPhysicsScene), Z_Construct_UDelegateFunction_WaterPhysics_K2_PreStepWaterPhysicsScene__DelegateSignature, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_K2_PreStepWaterPhysicsScene_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_K2_PreStepWaterPhysicsScene_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_DefaultWaterPhysicsSettings,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_bDrawWaterInfoDebug,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::NewProp_K2_PreStepWaterPhysicsScene,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UWaterPhysicsSceneComponent>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::ClassParams = {
		&UWaterPhysicsSceneComponent::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		FuncInfo,
		Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		UE_ARRAY_COUNT(FuncInfo),
		UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::PropPointers),
		0,
		0x00B000A4u,
		METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_UWaterPhysicsSceneComponent()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_UWaterPhysicsSceneComponent_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(UWaterPhysicsSceneComponent, 2420240078);
	template<> WATERPHYSICS_API UClass* StaticClass<UWaterPhysicsSceneComponent>()
	{
		return UWaterPhysicsSceneComponent::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_UWaterPhysicsSceneComponent(Z_Construct_UClass_UWaterPhysicsSceneComponent, &UWaterPhysicsSceneComponent::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("UWaterPhysicsSceneComponent"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(UWaterPhysicsSceneComponent);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
