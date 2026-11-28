// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "OceanologyIntegration/Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysics_Oceanology() {}
// Cross Module References
	OCEANOLOGYINTEGRATION_API UScriptStruct* Z_Construct_UScriptStruct_FOceanologyThreadCopy();
	UPackage* Z_Construct_UPackage__Script_OceanologyIntegration();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	OCEANOLOGYINTEGRATION_API UScriptStruct* Z_Construct_UScriptStruct_FActorArray();
	OCEANOLOGYINTEGRATION_API UClass* Z_Construct_UClass_AWaterPhysics_Oceanology_NoRegister();
	OCEANOLOGYINTEGRATION_API UClass* Z_Construct_UClass_AWaterPhysics_Oceanology();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysicsActor();
	COREUOBJECT_API UClass* Z_Construct_UClass_UFunction();
// End Cross Module References
class UScriptStruct* FOceanologyThreadCopy::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern OCEANOLOGYINTEGRATION_API uint32 Get_Z_Construct_UScriptStruct_FOceanologyThreadCopy_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FOceanologyThreadCopy, Z_Construct_UPackage__Script_OceanologyIntegration(), TEXT("OceanologyThreadCopy"), sizeof(FOceanologyThreadCopy), Get_Z_Construct_UScriptStruct_FOceanologyThreadCopy_Hash());
	}
	return Singleton;
}
template<> OCEANOLOGYINTEGRATION_API UScriptStruct* StaticStruct<FOceanologyThreadCopy>()
{
	return FOceanologyThreadCopy::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FOceanologyThreadCopy(FOceanologyThreadCopy::StaticStruct, TEXT("/Script/OceanologyIntegration"), TEXT("OceanologyThreadCopy"), false, nullptr, nullptr);
static struct FScriptStruct_OceanologyIntegration_StaticRegisterNativesFOceanologyThreadCopy
{
	FScriptStruct_OceanologyIntegration_StaticRegisterNativesFOceanologyThreadCopy()
	{
		UScriptStruct::DeferCppStructOps<FOceanologyThreadCopy>(FName(TEXT("OceanologyThreadCopy")));
	}
} ScriptStruct_OceanologyIntegration_StaticRegisterNativesFOceanologyThreadCopy;
	struct Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ThreadCopy_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_ThreadCopy;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::Struct_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	void* Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FOceanologyThreadCopy>();
	}
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::NewProp_ThreadCopy_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::NewProp_ThreadCopy = { "ThreadCopy", nullptr, (EPropertyFlags)0x0010000000002000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FOceanologyThreadCopy, ThreadCopy), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::NewProp_ThreadCopy_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::NewProp_ThreadCopy_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::NewProp_ThreadCopy,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_OceanologyIntegration,
		nullptr,
		&NewStructOps,
		"OceanologyThreadCopy",
		sizeof(FOceanologyThreadCopy),
		alignof(FOceanologyThreadCopy),
		Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FOceanologyThreadCopy()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FOceanologyThreadCopy_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_OceanologyIntegration();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("OceanologyThreadCopy"), sizeof(FOceanologyThreadCopy), Get_Z_Construct_UScriptStruct_FOceanologyThreadCopy_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FOceanologyThreadCopy_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FOceanologyThreadCopy_Hash() { return 684867268U; }
class UScriptStruct* FActorArray::StaticStruct()
{
	static class UScriptStruct* Singleton = NULL;
	if (!Singleton)
	{
		extern OCEANOLOGYINTEGRATION_API uint32 Get_Z_Construct_UScriptStruct_FActorArray_Hash();
		Singleton = GetStaticStruct(Z_Construct_UScriptStruct_FActorArray, Z_Construct_UPackage__Script_OceanologyIntegration(), TEXT("ActorArray"), sizeof(FActorArray), Get_Z_Construct_UScriptStruct_FActorArray_Hash());
	}
	return Singleton;
}
template<> OCEANOLOGYINTEGRATION_API UScriptStruct* StaticStruct<FActorArray>()
{
	return FActorArray::StaticStruct();
}
static FCompiledInDeferStruct Z_CompiledInDeferStruct_UScriptStruct_FActorArray(FActorArray::StaticStruct, TEXT("/Script/OceanologyIntegration"), TEXT("ActorArray"), false, nullptr, nullptr);
static struct FScriptStruct_OceanologyIntegration_StaticRegisterNativesFActorArray
{
	FScriptStruct_OceanologyIntegration_StaticRegisterNativesFActorArray()
	{
		UScriptStruct::DeferCppStructOps<FActorArray>(FName(TEXT("ActorArray")));
	}
} ScriptStruct_OceanologyIntegration_StaticRegisterNativesFActorArray;
	struct Z_Construct_UScriptStruct_FActorArray_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[];
#endif
		static void* NewStructOps();
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actors_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Actors_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_Actors;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const UE4CodeGen_Private::FStructParams ReturnStructParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FActorArray_Statics::Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "Comment", "// UE4 Reflection cannot handle nested containers, so we wrap this array with a struct\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
		{ "ToolTip", "UE4 Reflection cannot handle nested containers, so we wrap this array with a struct" },
	};
#endif
	void* Z_Construct_UScriptStruct_FActorArray_Statics::NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FActorArray>();
	}
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors_Inner = { "Actors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors = { "Actors", nullptr, (EPropertyFlags)0x0010000000002000, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(FActorArray, Actors), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors_MetaData, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FActorArray_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FActorArray_Statics::NewProp_Actors,
	};
	const UE4CodeGen_Private::FStructParams Z_Construct_UScriptStruct_FActorArray_Statics::ReturnStructParams = {
		(UObject* (*)())Z_Construct_UPackage__Script_OceanologyIntegration,
		nullptr,
		&NewStructOps,
		"ActorArray",
		sizeof(FActorArray),
		alignof(FActorArray),
		Z_Construct_UScriptStruct_FActorArray_Statics::PropPointers,
		UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorArray_Statics::PropPointers),
		RF_Public|RF_Transient|RF_MarkAsNative,
		EStructFlags(0x00000001),
		METADATA_PARAMS(Z_Construct_UScriptStruct_FActorArray_Statics::Struct_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FActorArray_Statics::Struct_MetaDataParams))
	};
	UScriptStruct* Z_Construct_UScriptStruct_FActorArray()
	{
#if WITH_HOT_RELOAD
		extern uint32 Get_Z_Construct_UScriptStruct_FActorArray_Hash();
		UPackage* Outer = Z_Construct_UPackage__Script_OceanologyIntegration();
		static UScriptStruct* ReturnStruct = FindExistingStructIfHotReloadOrDynamic(Outer, TEXT("ActorArray"), sizeof(FActorArray), Get_Z_Construct_UScriptStruct_FActorArray_Hash(), false);
#else
		static UScriptStruct* ReturnStruct = nullptr;
#endif
		if (!ReturnStruct)
		{
			UE4CodeGen_Private::ConstructUScriptStruct(ReturnStruct, Z_Construct_UScriptStruct_FActorArray_Statics::ReturnStructParams);
		}
		return ReturnStruct;
	}
	uint32 Get_Z_Construct_UScriptStruct_FActorArray_Hash() { return 3732516504U; }
	DEFINE_FUNCTION(AWaterPhysics_Oceanology::execOnActorEndOverlapBoundsActor)
	{
		P_GET_OBJECT(AActor,Z_Param_OverlappedActor);
		P_GET_OBJECT(AActor,Z_Param_OtherActor);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->OnActorEndOverlapBoundsActor(Z_Param_OverlappedActor,Z_Param_OtherActor);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysics_Oceanology::execOnActorBeginOverlapBoundsActor)
	{
		P_GET_OBJECT(AActor,Z_Param_OverlappedActor);
		P_GET_OBJECT(AActor,Z_Param_OtherActor);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->OnActorBeginOverlapBoundsActor(Z_Param_OverlappedActor,Z_Param_OtherActor);
		P_NATIVE_END;
	}
	void AWaterPhysics_Oceanology::StaticRegisterNativesAWaterPhysics_Oceanology()
	{
		UClass* Class = AWaterPhysics_Oceanology::StaticClass();
		static const FNameNativePtrPair Funcs[] = {
			{ "OnActorBeginOverlapBoundsActor", &AWaterPhysics_Oceanology::execOnActorBeginOverlapBoundsActor },
			{ "OnActorEndOverlapBoundsActor", &AWaterPhysics_Oceanology::execOnActorEndOverlapBoundsActor },
		};
		FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
	}
	struct Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics
	{
		struct WaterPhysics_Oceanology_eventOnActorBeginOverlapBoundsActor_Parms
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
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::NewProp_OverlappedActor = { "OverlappedActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_Oceanology_eventOnActorBeginOverlapBoundsActor_Parms, OverlappedActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_Oceanology_eventOnActorBeginOverlapBoundsActor_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::NewProp_OverlappedActor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::NewProp_OtherActor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_Oceanology, nullptr, "OnActorBeginOverlapBoundsActor", nullptr, nullptr, sizeof(WaterPhysics_Oceanology_eventOnActorBeginOverlapBoundsActor_Parms), Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00040401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics
	{
		struct WaterPhysics_Oceanology_eventOnActorEndOverlapBoundsActor_Parms
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
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::NewProp_OverlappedActor = { "OverlappedActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_Oceanology_eventOnActorEndOverlapBoundsActor_Parms, OverlappedActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_Oceanology_eventOnActorEndOverlapBoundsActor_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::NewProp_OverlappedActor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::NewProp_OtherActor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_Oceanology, nullptr, "OnActorEndOverlapBoundsActor", nullptr, nullptr, sizeof(WaterPhysics_Oceanology_eventOnActorEndOverlapBoundsActor_Parms), Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00040401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	UClass* Z_Construct_UClass_AWaterPhysics_Oceanology_NoRegister()
	{
		return AWaterPhysics_Oceanology::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysics_Oceanology_Statics
	{
		static UObject* (*const DependentSingletons[])();
		static const FClassFunctionLinkInfo FuncInfo[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_GetWaveHightFunction_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_GetWaveHightFunction;
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_OceanologyThreadCopies_ValueProp;
		static const UE4CodeGen_Private::FUInt32PropertyParams NewProp_OceanologyThreadCopies_Key_KeyProp;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OceanologyThreadCopies_MetaData[];
#endif
		static const UE4CodeGen_Private::FMapPropertyParams NewProp_OceanologyThreadCopies;
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ActorOverlapTracker_ValueProp;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_ActorOverlapTracker_Key_KeyProp;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ActorOverlapTracker_MetaData[];
#endif
		static const UE4CodeGen_Private::FMapPropertyParams NewProp_ActorOverlapTracker;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OceanologyWater_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OceanologyWater;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_InitiallySimulatedActors_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_InitiallySimulatedActors_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_InitiallySimulatedActors;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OceanBoundsActors_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OceanBoundsActors_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_OceanBoundsActors;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AWaterPhysicsActor,
		(UObject* (*)())Z_Construct_UPackage__Script_OceanologyIntegration,
	};
	const FClassFunctionLinkInfo Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::FuncInfo[] = {
		{ &Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorBeginOverlapBoundsActor, "OnActorBeginOverlapBoundsActor" }, // 1960917628
		{ &Z_Construct_UFunction_AWaterPhysics_Oceanology_OnActorEndOverlapBoundsActor, "OnActorEndOverlapBoundsActor" }, // 2515641214
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "DisplayName", "Water Physics - Oceanology" },
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_GetWaveHightFunction_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_GetWaveHightFunction = { "GetWaveHightFunction", nullptr, (EPropertyFlags)0x0040000000002000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Oceanology, GetWaveHightFunction), Z_Construct_UClass_UFunction, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_GetWaveHightFunction_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_GetWaveHightFunction_MetaData)) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_ValueProp = { "OceanologyThreadCopies", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, 1, Z_Construct_UScriptStruct_FOceanologyThreadCopy, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FUInt32PropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_Key_KeyProp = { "OceanologyThreadCopies_Key", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::UInt32, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FMapPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies = { "OceanologyThreadCopies", nullptr, (EPropertyFlags)0x0040000000002000, UE4CodeGen_Private::EPropertyGenFlags::Map, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Oceanology, OceanologyThreadCopies), EMapPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_MetaData)) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_ValueProp = { "ActorOverlapTracker", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, 1, Z_Construct_UScriptStruct_FActorArray, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_Key_KeyProp = { "ActorOverlapTracker_Key", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
	};
#endif
	const UE4CodeGen_Private::FMapPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker = { "ActorOverlapTracker", nullptr, (EPropertyFlags)0x0040000000002000, UE4CodeGen_Private::EPropertyGenFlags::Map, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Oceanology, ActorOverlapTracker), EMapPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyWater_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "// A reference to the oceanology water which should have water physics added to it\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
		{ "ToolTip", "A reference to the oceanology water which should have water physics added to it" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyWater = { "OceanologyWater", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Oceanology, OceanologyWater), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyWater_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyWater_MetaData)) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors_Inner = { "InitiallySimulatedActors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "// Actors which should float on the Oceanology water. To dynamically add/remove actors from the water physics simulation,\n// call the AddActorToWater and RemoveActorFromWater functions on this actor.\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
		{ "ToolTip", "Actors which should float on the Oceanology water. To dynamically add/remove actors from the water physics simulation,\ncall the AddActorToWater and RemoveActorFromWater functions on this actor." },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors = { "InitiallySimulatedActors", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Oceanology, InitiallySimulatedActors), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors_MetaData)) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors_Inner = { "OceanBoundsActors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors_MetaData[] = {
		{ "Category", "Water Physics" },
		{ "Comment", "// When these actors generate OnActorBegin/End overlap events, the overlapped actor will be automatically added/removed from the water physics\n// simulation. As long as the actor overlaps any of the actors in this list it will be part of the water physics simulation.\n// \n// Usefull to define the bounds of the ocean as Oceanology does not generate overlap events.\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_Oceanology.h" },
		{ "ToolTip", "When these actors generate OnActorBegin/End overlap events, the overlapped actor will be automatically added/removed from the water physics\nsimulation. As long as the actor overlaps any of the actors in this list it will be part of the water physics simulation.\n\nUsefull to define the bounds of the ocean as Oceanology does not generate overlap events." },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors = { "OceanBoundsActors", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_Oceanology, OceanBoundsActors), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_GetWaveHightFunction,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_ValueProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies_Key_KeyProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyThreadCopies,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_ValueProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker_Key_KeyProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_ActorOverlapTracker,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanologyWater,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_InitiallySimulatedActors,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::NewProp_OceanBoundsActors,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysics_Oceanology>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::ClassParams = {
		&AWaterPhysics_Oceanology::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		FuncInfo,
		Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		UE_ARRAY_COUNT(FuncInfo),
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::PropPointers),
		0,
		0x009000A4u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysics_Oceanology()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysics_Oceanology_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysics_Oceanology, 440094846);
	template<> OCEANOLOGYINTEGRATION_API UClass* StaticClass<AWaterPhysics_Oceanology>()
	{
		return AWaterPhysics_Oceanology::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysics_Oceanology(Z_Construct_UClass_AWaterPhysics_Oceanology, &AWaterPhysics_Oceanology::StaticClass, TEXT("/Script/OceanologyIntegration"), TEXT("AWaterPhysics_Oceanology"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysics_Oceanology);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
