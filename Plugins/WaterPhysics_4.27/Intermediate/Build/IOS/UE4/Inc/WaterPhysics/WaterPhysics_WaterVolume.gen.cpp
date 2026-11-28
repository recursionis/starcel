// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysics_WaterVolume() {}
// Cross Module References
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterVolume_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysics_WaterVolume();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysicsActor();
	ENGINE_API UClass* Z_Construct_UClass_UBoxComponent_NoRegister();
	ENGINE_API UClass* Z_Construct_UClass_UPrimitiveComponent_NoRegister();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	ENGINE_API UScriptStruct* Z_Construct_UScriptStruct_FHitResult();
// End Cross Module References
	static UEnum* EWaterVolumeOverlapMethod_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterVolumeOverlapMethod"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterVolumeOverlapMethod>()
	{
		return EWaterVolumeOverlapMethod_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterVolumeOverlapMethod(EWaterVolumeOverlapMethod_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterVolumeOverlapMethod"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod_Hash() { return 2274502206U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterVolumeOverlapMethod"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterVolumeOverlapMethod::Overlap", (int64)EWaterVolumeOverlapMethod::Overlap },
				{ "EWaterVolumeOverlapMethod::Trace", (int64)EWaterVolumeOverlapMethod::Trace },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "BlueprintType", "true" },
				{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
				{ "Overlap.DisplayName", "On Overlap Event" },
				{ "Overlap.Name", "EWaterVolumeOverlapMethod::Overlap" },
				{ "Trace.Comment", "// Use unreals built-in overlap events to detect overlapping physics bodes\n" },
				{ "Trace.DisplayName", "Trace" },
				{ "Trace.Name", "EWaterVolumeOverlapMethod::Trace" },
				{ "Trace.ToolTip", "Use unreals built-in overlap events to detect overlapping physics bodes" },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterVolumeOverlapMethod",
				"EWaterVolumeOverlapMethod",
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
	DEFINE_FUNCTION(AWaterPhysics_WaterVolume::execOnVolumeEndOverlap)
	{
		P_GET_OBJECT(UPrimitiveComponent,Z_Param_OverlappedComponent);
		P_GET_OBJECT(AActor,Z_Param_OtherActor);
		P_GET_OBJECT(UPrimitiveComponent,Z_Param_OtherComp);
		P_GET_PROPERTY(FIntProperty,Z_Param_OtherBodyIndex);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->OnVolumeEndOverlap(Z_Param_OverlappedComponent,Z_Param_OtherActor,Z_Param_OtherComp,Z_Param_OtherBodyIndex);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysics_WaterVolume::execOnVolumeBeginOverlap)
	{
		P_GET_OBJECT(UPrimitiveComponent,Z_Param_OverlappedComponent);
		P_GET_OBJECT(AActor,Z_Param_OtherActor);
		P_GET_OBJECT(UPrimitiveComponent,Z_Param_OtherComp);
		P_GET_PROPERTY(FIntProperty,Z_Param_OtherBodyIndex);
		P_GET_UBOOL(Z_Param_bFromSweep);
		P_GET_STRUCT_REF(FHitResult,Z_Param_Out_SweepResult);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->OnVolumeBeginOverlap(Z_Param_OverlappedComponent,Z_Param_OtherActor,Z_Param_OtherComp,Z_Param_OtherBodyIndex,Z_Param_bFromSweep,Z_Param_Out_SweepResult);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysics_WaterVolume::execSetOverlapMethod)
	{
		P_GET_ENUM(EWaterVolumeOverlapMethod,Z_Param_NewOverlapMethod);
		P_GET_UBOOL(Z_Param_ResetOverlaps);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->SetOverlapMethod(EWaterVolumeOverlapMethod(Z_Param_NewOverlapMethod),Z_Param_ResetOverlaps);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysics_WaterVolume::execGetBoxComponent)
	{
		P_FINISH;
		P_NATIVE_BEGIN;
		*(UBoxComponent**)Z_Param__Result=P_THIS->GetBoxComponent();
		P_NATIVE_END;
	}
	void AWaterPhysics_WaterVolume::StaticRegisterNativesAWaterPhysics_WaterVolume()
	{
		UClass* Class = AWaterPhysics_WaterVolume::StaticClass();
		static const FNameNativePtrPair Funcs[] = {
			{ "GetBoxComponent", &AWaterPhysics_WaterVolume::execGetBoxComponent },
			{ "OnVolumeBeginOverlap", &AWaterPhysics_WaterVolume::execOnVolumeBeginOverlap },
			{ "OnVolumeEndOverlap", &AWaterPhysics_WaterVolume::execOnVolumeEndOverlap },
			{ "SetOverlapMethod", &AWaterPhysics_WaterVolume::execSetOverlapMethod },
		};
		FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics
	{
		struct WaterPhysics_WaterVolume_eventGetBoxComponent_Parms
		{
			UBoxComponent* ReturnValue;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ReturnValue_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::NewProp_ReturnValue_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000080588, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventGetBoxComponent_Parms, ReturnValue), Z_Construct_UClass_UBoxComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::NewProp_ReturnValue_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::NewProp_ReturnValue_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Volume" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterVolume, nullptr, "GetBoxComponent", nullptr, nullptr, sizeof(WaterPhysics_WaterVolume_eventGetBoxComponent_Parms), Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics
	{
		struct WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms
		{
			UPrimitiveComponent* OverlappedComponent;
			AActor* OtherActor;
			UPrimitiveComponent* OtherComp;
			int32 OtherBodyIndex;
			bool bFromSweep;
			FHitResult SweepResult;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OverlappedComponent_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OverlappedComponent;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OtherActor;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OtherComp_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OtherComp;
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_OtherBodyIndex;
		static void NewProp_bFromSweep_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bFromSweep;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SweepResult_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_SweepResult;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OverlappedComponent_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OverlappedComponent = { "OverlappedComponent", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms, OverlappedComponent), Z_Construct_UClass_UPrimitiveComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OverlappedComponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OverlappedComponent_MetaData)) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherComp_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherComp = { "OtherComp", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms, OtherComp), Z_Construct_UClass_UPrimitiveComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherComp_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherComp_MetaData)) };
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherBodyIndex = { "OtherBodyIndex", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms, OtherBodyIndex), METADATA_PARAMS(nullptr, 0) };
	void Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_bFromSweep_SetBit(void* Obj)
	{
		((WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms*)Obj)->bFromSweep = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_bFromSweep = { "bFromSweep", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms), &Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_bFromSweep_SetBit, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_SweepResult_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_SweepResult = { "SweepResult", nullptr, (EPropertyFlags)0x0010008008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms, SweepResult), Z_Construct_UScriptStruct_FHitResult, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_SweepResult_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_SweepResult_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OverlappedComponent,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherActor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherComp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_OtherBodyIndex,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_bFromSweep,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::NewProp_SweepResult,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterVolume, nullptr, "OnVolumeBeginOverlap", nullptr, nullptr, sizeof(WaterPhysics_WaterVolume_eventOnVolumeBeginOverlap_Parms), Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00420401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics
	{
		struct WaterPhysics_WaterVolume_eventOnVolumeEndOverlap_Parms
		{
			UPrimitiveComponent* OverlappedComponent;
			AActor* OtherActor;
			UPrimitiveComponent* OtherComp;
			int32 OtherBodyIndex;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OverlappedComponent_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OverlappedComponent;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OtherActor;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OtherComp_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OtherComp;
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_OtherBodyIndex;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OverlappedComponent_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OverlappedComponent = { "OverlappedComponent", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeEndOverlap_Parms, OverlappedComponent), Z_Construct_UClass_UPrimitiveComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OverlappedComponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OverlappedComponent_MetaData)) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeEndOverlap_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherComp_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherComp = { "OtherComp", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeEndOverlap_Parms, OtherComp), Z_Construct_UClass_UPrimitiveComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherComp_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherComp_MetaData)) };
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherBodyIndex = { "OtherBodyIndex", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventOnVolumeEndOverlap_Parms, OtherBodyIndex), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OverlappedComponent,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherActor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherComp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::NewProp_OtherBodyIndex,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterVolume, nullptr, "OnVolumeEndOverlap", nullptr, nullptr, sizeof(WaterPhysics_WaterVolume_eventOnVolumeEndOverlap_Parms), Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics
	{
		struct WaterPhysics_WaterVolume_eventSetOverlapMethod_Parms
		{
			EWaterVolumeOverlapMethod NewOverlapMethod;
			bool ResetOverlaps;
		};
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_NewOverlapMethod_Underlying;
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_NewOverlapMethod;
		static void NewProp_ResetOverlaps_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ResetOverlaps;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_NewOverlapMethod_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_NewOverlapMethod = { "NewOverlapMethod", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysics_WaterVolume_eventSetOverlapMethod_Parms, NewOverlapMethod), Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod, METADATA_PARAMS(nullptr, 0) };
	void Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_ResetOverlaps_SetBit(void* Obj)
	{
		((WaterPhysics_WaterVolume_eventSetOverlapMethod_Parms*)Obj)->ResetOverlaps = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_ResetOverlaps = { "ResetOverlaps", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysics_WaterVolume_eventSetOverlapMethod_Parms), &Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_ResetOverlaps_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_NewOverlapMethod_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_NewOverlapMethod,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::NewProp_ResetOverlaps,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Volume" },
		{ "CPP_Default_ResetOverlaps", "false" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysics_WaterVolume, nullptr, "SetOverlapMethod", nullptr, nullptr, sizeof(WaterPhysics_WaterVolume_eventSetOverlapMethod_Parms), Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	UClass* Z_Construct_UClass_AWaterPhysics_WaterVolume_NoRegister()
	{
		return AWaterPhysics_WaterVolume::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics
	{
		static UObject* (*const DependentSingletons[])();
		static const FClassFunctionLinkInfo FuncInfo[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_OverlappingActors_ElementProp;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OverlappingActors_MetaData[];
#endif
		static const UE4CodeGen_Private::FSetPropertyParams NewProp_OverlappingActors;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_NewOverlappingActors_ElementProp;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_NewOverlappingActors_MetaData[];
#endif
		static const UE4CodeGen_Private::FSetPropertyParams NewProp_NewOverlappingActors;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_BoxComponent_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_BoxComponent;
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_OverlapMethod_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_OverlapMethod_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_OverlapMethod;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AWaterPhysicsActor,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
	const FClassFunctionLinkInfo Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::FuncInfo[] = {
		{ &Z_Construct_UFunction_AWaterPhysics_WaterVolume_GetBoxComponent, "GetBoxComponent" }, // 1501952683
		{ &Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeBeginOverlap, "OnVolumeBeginOverlap" }, // 1240872934
		{ &Z_Construct_UFunction_AWaterPhysics_WaterVolume_OnVolumeEndOverlap, "OnVolumeEndOverlap" }, // 1637003087
		{ &Z_Construct_UFunction_AWaterPhysics_WaterVolume_SetOverlapMethod, "SetOverlapMethod" }, // 116029296
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "DisplayName", "Water Physics - Water Volume" },
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors_ElementProp = { "OverlappingActors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FSetPropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors = { "OverlappingActors", nullptr, (EPropertyFlags)0x0040000000002000, UE4CodeGen_Private::EPropertyGenFlags::Set, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_WaterVolume, OverlappingActors), METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors_MetaData)) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors_ElementProp = { "NewOverlappingActors", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors_MetaData[] = {
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FSetPropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors = { "NewOverlappingActors", nullptr, (EPropertyFlags)0x0040000000002000, UE4CodeGen_Private::EPropertyGenFlags::Set, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_WaterVolume, NewOverlappingActors), METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_BoxComponent_MetaData[] = {
		{ "AllowPrivateAccess", "true" },
		{ "Category", "Water Volume" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_BoxComponent = { "BoxComponent", nullptr, (EPropertyFlags)0x00400000000a001d, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_WaterVolume, BoxComponent), Z_Construct_UClass_UBoxComponent_NoRegister, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_BoxComponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_BoxComponent_MetaData)) };
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod_MetaData[] = {
		{ "Category", "Water Volume" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysics_WaterVolume.h" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod = { "OverlapMethod", nullptr, (EPropertyFlags)0x0020080000000015, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysics_WaterVolume, OverlapMethod), Z_Construct_UEnum_WaterPhysics_EWaterVolumeOverlapMethod, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors_ElementProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlappingActors,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors_ElementProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_NewOverlappingActors,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_BoxComponent,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::NewProp_OverlapMethod,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysics_WaterVolume>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::ClassParams = {
		&AWaterPhysics_WaterVolume::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		FuncInfo,
		Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		UE_ARRAY_COUNT(FuncInfo),
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::PropPointers),
		0,
		0x009000A4u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysics_WaterVolume()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysics_WaterVolume_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysics_WaterVolume, 3459966109);
	template<> WATERPHYSICS_API UClass* StaticClass<AWaterPhysics_WaterVolume>()
	{
		return AWaterPhysics_WaterVolume::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysics_WaterVolume(Z_Construct_UClass_AWaterPhysics_WaterVolume, &AWaterPhysics_WaterVolume::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("AWaterPhysics_WaterVolume"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysics_WaterVolume);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
