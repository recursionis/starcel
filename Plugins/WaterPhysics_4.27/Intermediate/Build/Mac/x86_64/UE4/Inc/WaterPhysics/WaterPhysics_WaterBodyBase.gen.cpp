// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysics_WaterBodyBase() {}
// Cross Module References
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FWaterBodyArray();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysicsActor();
	ENGINE_API UClass* Z_Construct_UClass_UActorComponent_NoRegister();
	COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FGetWaterInfoResult();
// End Cross Module References
class UScriptStruct* FWaterBodyArray::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern WATERPHYSICS_API uint32 Get_Z_Construct_UScriptStruct_FWaterBodyArray_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FWaterBodyArray, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("WaterBodyArray"), sizeof(FWaterBodyArray), Get_Z_Construct_UScriptStruct_FWaterBodyArray_Hash());
	}
	return Singleton;
}
template<> WATERPHYSICS_API UScriptStruct* StaticStruct<FWaterBodyArray>()
{
	return FWaterBodyArray::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FWaterBodyArray(FWaterBodyArray::StaticStruct, TEXT("/Script/WaterPhysics"), TEXT("WaterBodyArray"), false, nullptr, nullptr);
static struct FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterBodyArray
{
	FScriptStruct_WaterPhysics_StaticRegisterNativesFWaterBodyArray()
	{
		UScriptStruct::DeferCppStructOps<FWaterBodyArray>(FName(TEXT("WaterBodyArray")));
	}
} ScriptStruct_WaterPhysics_StaticRegisterNativesFWaterBodyArray;
	struct Z_Construct_UScriptStruct_FWaterBodyArray_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_WaterBodies_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterBodies_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_WaterBodies;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodyArray_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "Comment", "// UE4 Reflection cannot handle nested containers, so we wrap this array with a struct\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
		{ "ToolTip", "UE4 Reflection cannot handle nested containers, so we wrap this array with a struct" },
	};
#endif
	void* Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FWaterBodyArray>();
	}
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies_Inner = { "WaterBodies", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies = { "WaterBodies", nullptr, (EPropertyFlags)0x0010000000002000, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FWaterBodyArray, WaterBodies), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FWaterBodyArray_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FWaterBodyArray_Statics::NewProp_WaterBodies,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FWaterBodyArray_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
		nullptr,
		&NewStructOps,
		"WaterBodyArray",
		sizeof(FWaterBodyArray),
		alignof(FWaterBodyArray),
		Z_Construct_UScriptStruct_FWaterBodyArray_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodyArray_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FWaterBodyArray_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FWaterBodyArray_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FWaterBodyArray()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FWaterBodyArray_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("WaterBodyArray"), sizeof(FWaterBodyArray), Get_Z_Construct_UScriptStruct_FWaterBodyArray_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FWaterBodyArray_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FWaterBodyArray_Hash() { return 2498719963U; }
	DEFINE_FUNCTION(AWaterPhysics_WaterBodyBase::execOnActorEndOverlapWaterBody)
	{
		P_GET_OBJECT(AActor,Z_Param_OverlappedActor);
		P_GET_OBJECT(AActor,Z_Param_OtherActor);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->OnActorEndOverlapWaterBody(Z_Param_OverlappedActor,Z_Param_OtherActor);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysics_WaterBodyBase::execOnActorBeginOverlapWaterBody)
	{
		P_GET_OBJECT(AActor,Z_Param_OverlappedActor);
		P_GET_OBJECT(AActor,Z_Param_OtherActor);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->OnActorBeginOverlapWaterBody(Z_Param_OverlappedActor,Z_Param_OtherActor);
		P_NATIVE_END;
	}
	static FName NAME_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody = FName(TEXT("ReceiveCalculateWaterInfoForWaterBody"));
	FGetWaterInfoResult AWaterPhysics_WaterBodyBase::ReceiveCalculateWaterInfoForWaterBody(AActor* WaterBody, const UActorComponent* Component, FVector const& Location) const
	{
		WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms Parms;
		Parms.WaterBody=WaterBody;
		Parms.Component=Component;
		Parms.Location=Location;
		const_cast<AWaterPhysics_WaterBodyBase*>(this)->ProcessEvent(FindFunctionChecked(NAME_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody),&Parms);
		return Parms.ReturnValue;
	}
	void AWaterPhysics_WaterBodyBase::StaticRegisterNativesAWaterPhysics_WaterBodyBase()
	{
		UClass* Class = AWaterPhysics_WaterBodyBase::StaticClass();
		static const FNameNativePtrPair Funcs[] = {
			{ "OnActorBeginOverlapWaterBody", &AWaterPhysics_WaterBodyBase::execOnActorBeginOverlapWaterBody },
			{ "OnActorEndOverlapWaterBody", &AWaterPhysics_WaterBodyBase::execOnActorEndOverlapWaterBody },
		};
		FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics
	{
		struct WaterPhysics_WaterBodyBase_eventOnActorBeginOverlapWaterBody_Parms
		{
			AActor* OverlappedActor;
			AActor* OtherActor;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OverlappedActor;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OtherActor;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::NewProp_OverlappedActor = { "OverlappedActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventOnActorBeginOverlapWaterBody_Parms, OverlappedActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventOnActorBeginOverlapWaterBody_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::NewProp_OverlappedActor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::NewProp_OtherActor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterBodyBase, nullptr, "OnActorBeginOverlapWaterBody", nullptr, nullptr, sizeof(WaterPhysics_WaterBodyBase_eventOnActorBeginOverlapWaterBody_Parms), Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics
	{
		struct WaterPhysics_WaterBodyBase_eventOnActorEndOverlapWaterBody_Parms
		{
			AActor* OverlappedActor;
			AActor* OtherActor;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OverlappedActor;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OtherActor;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::NewProp_OverlappedActor = { "OverlappedActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventOnActorEndOverlapWaterBody_Parms, OverlappedActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventOnActorEndOverlapWaterBody_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::NewProp_OverlappedActor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::NewProp_OtherActor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterBodyBase, nullptr, "OnActorEndOverlapWaterBody", nullptr, nullptr, sizeof(WaterPhysics_WaterBodyBase_eventOnActorEndOverlapWaterBody_Parms), Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics
	{
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_WaterBody;
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
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_WaterBody = { "WaterBody", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms, WaterBody), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080082, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Component_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Location_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Location = { "Location", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms, Location), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Location_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Location_MetaData)) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms, ReturnValue), Z_Construct_UScriptStruct_FGetWaterInfoResult, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_WaterBody,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_Location,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "// Blueprint overridable function for calculating the water surface location for a given water body and location.\n" },
		{ "DisplayName", "Calculate Water Info For Water Body" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
		{ "ToolTip", "Blueprint overridable function for calculating the water surface location for a given water body and location." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterBodyBase, nullptr, "ReceiveCalculateWaterInfoForWaterBody", nullptr, nullptr, sizeof(WaterPhysics_WaterBodyBase_eventReceiveCalculateWaterInfoForWaterBody_Parms), Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x48C80800, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase_NoRegister()
	{
		return AWaterPhysics_WaterBodyBase::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics
	{
		static UObject* (*const DependentSingletons[])();
		static const FClassFunctionLinkInfo FuncInfo[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ActorCurrentWaterBodies_ValueProp;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_ActorCurrentWaterBodies_Key_KeyProp;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ActorCurrentWaterBodies_MetaData[];
#endif
		static const UE4CodeGen_Private::FMapPropertyParams NewProp_ActorCurrentWaterBodies;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AWaterPhysicsActor,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
	const FClassFunctionLinkInfo Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::FuncInfo[] = {
		{ &Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorBeginOverlapWaterBody, "OnActorBeginOverlapWaterBody" }, // 170571110
		{ &Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_OnActorEndOverlapWaterBody, "OnActorEndOverlapWaterBody" }, // 1687057533
		{ &Z_Construct_UFunction_AWaterPhysics_WaterBodyBase_ReceiveCalculateWaterInfoForWaterBody, "ReceiveCalculateWaterInfoForWaterBody" }, // 1675136017
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::Class_MetaDataParams[] = {
		{ "Comment", "// Base implementation for adding water physics simulation to any set of actors which can generate overlap events.\n" },
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
		{ "ToolTip", "Base implementation for adding water physics simulation to any set of actors which can generate overlap events." },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_ValueProp = { "ActorCurrentWaterBodies", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, 1, Z_Construct_UScriptStruct_FWaterBodyArray, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_Key_KeyProp = { "ActorCurrentWaterBodies_Key", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterBodyBase.h" },
	};
#endif
	const UE4CodeGen_Private::FMapPropertyParams Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies = { "ActorCurrentWaterBodies", nullptr, (EPropertyFlags)0x0040000000002000, UE4CodeGen_Private::EPropertyGenFlags::Map, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_WaterBodyBase, ActorCurrentWaterBodies), EMapPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_ValueProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies_Key_KeyProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::NewProp_ActorCurrentWaterBodies,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysics_WaterBodyBase>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::ClassParams = {
		&AWaterPhysics_WaterBodyBase::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		FuncInfo,
		Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		UE_ARRAY_COUNT(FuncInfo),
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::PropPointers),
		0,
		0x009000A5u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysics_WaterBodyBase()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysics_WaterBodyBase_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysics_WaterBodyBase, 471372213);
	template<> WATERPHYSICS_API UClass* StaticClass<AWaterPhysics_WaterBodyBase>()
	{
		return AWaterPhysics_WaterBodyBase::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysics_WaterBodyBase(Z_Construct_UClass_AWaterPhysics_WaterBodyBase, &AWaterPhysics_WaterBodyBase::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("AWaterPhysics_WaterBodyBase"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysics_WaterBodyBase);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
