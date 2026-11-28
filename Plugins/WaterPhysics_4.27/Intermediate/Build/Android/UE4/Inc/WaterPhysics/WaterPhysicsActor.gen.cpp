// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsSimulations/WaterPhysicsActor.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysicsActor() {}
// Cross Module References
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysicsActor_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_AWaterPhysicsActor();
	ENGINE_API UClass* Z_Construct_UClass_AActor();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsSceneComponent_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsSettingsComponent_NoRegister();
	ENGINE_API UClass* Z_Construct_UClass_UActorComponent_NoRegister();
	COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FGetWaterInfoResult();
	WATERPHYSICS_API UScriptStruct* Z_Construct_UScriptStruct_FWaterPhysicsFilter();
// End Cross Module References
	DEFINE_FUNCTION(AWaterPhysicsActor::execNotifyWaterPhysicsSettingsChanged)
	{
		P_GET_OBJECT(UWaterPhysicsSettingsComponent,Z_Param_WaterPhysicsSettingsComponent);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->NotifyWaterPhysicsSettingsChanged(Z_Param_WaterPhysicsSettingsComponent);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysicsActor::execRemoveActorFromWater)
	{
		P_GET_OBJECT(AActor,Z_Param_Actor);
		P_GET_PROPERTY(FFloatProperty,Z_Param_RemoveDelay);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->RemoveActorFromWater(Z_Param_Actor,Z_Param_RemoveDelay);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysicsActor::execAddActorToWater)
	{
		P_GET_OBJECT(AActor,Z_Param_Actor);
		P_FINISH;
		P_NATIVE_BEGIN;
		P_THIS->AddActorToWater(Z_Param_Actor);
		P_NATIVE_END;
	}
	DEFINE_FUNCTION(AWaterPhysicsActor::execGetWaterPhysicsSceneComponent)
	{
		P_FINISH;
		P_NATIVE_BEGIN;
		*(UWaterPhysicsSceneComponent**)Z_Param__Result=P_THIS->GetWaterPhysicsSceneComponent();
		P_NATIVE_END;
	}
	static FName NAME_AWaterPhysicsActor_ReceiveCalculateWaterInfo = FName(TEXT("ReceiveCalculateWaterInfo"));
	FGetWaterInfoResult AWaterPhysicsActor::ReceiveCalculateWaterInfo(const UActorComponent* Component, FVector const& Location)
	{
		WaterPhysicsActor_eventReceiveCalculateWaterInfo_Parms Parms;
		Parms.Component=Component;
		Parms.Location=Location;
		ProcessEvent(FindFunctionChecked(NAME_AWaterPhysicsActor_ReceiveCalculateWaterInfo),&Parms);
		return Parms.ReturnValue;
	}
	static FName NAME_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics = FName(TEXT("ReceiveFilterActorFromWaterPhysics"));
	bool AWaterPhysicsActor::ReceiveFilterActorFromWaterPhysics(AActor* Actor)
	{
		WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms Parms;
		Parms.Actor=Actor;
		ProcessEvent(FindFunctionChecked(NAME_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics),&Parms);
		return !!Parms.ReturnValue;
	}
	static FName NAME_AWaterPhysicsActor_ReceiveOnActorAddedToWater = FName(TEXT("ReceiveOnActorAddedToWater"));
	void AWaterPhysicsActor::ReceiveOnActorAddedToWater(AActor* Actor)
	{
		WaterPhysicsActor_eventReceiveOnActorAddedToWater_Parms Parms;
		Parms.Actor=Actor;
		ProcessEvent(FindFunctionChecked(NAME_AWaterPhysicsActor_ReceiveOnActorAddedToWater),&Parms);
	}
	static FName NAME_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater = FName(TEXT("ReceiveOnActorRemovedFromWater"));
	void AWaterPhysicsActor::ReceiveOnActorRemovedFromWater(AActor* Actor)
	{
		WaterPhysicsActor_eventReceiveOnActorRemovedFromWater_Parms Parms;
		Parms.Actor=Actor;
		ProcessEvent(FindFunctionChecked(NAME_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater),&Parms);
	}
	static FName NAME_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick = FName(TEXT("ReceivePreWaterPhysicsSceneTick"));
	void AWaterPhysicsActor::ReceivePreWaterPhysicsSceneTick()
	{
		ProcessEvent(FindFunctionChecked(NAME_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick),NULL);
	}
	void AWaterPhysicsActor::StaticRegisterNativesAWaterPhysicsActor()
	{
		UClass* Class = AWaterPhysicsActor::StaticClass();
		static const FNameNativePtrPair Funcs[] = {
			{ "AddActorToWater", &AWaterPhysicsActor::execAddActorToWater },
			{ "GetWaterPhysicsSceneComponent", &AWaterPhysicsActor::execGetWaterPhysicsSceneComponent },
			{ "NotifyWaterPhysicsSettingsChanged", &AWaterPhysicsActor::execNotifyWaterPhysicsSettingsChanged },
			{ "RemoveActorFromWater", &AWaterPhysicsActor::execRemoveActorFromWater },
		};
		FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics
	{
		struct WaterPhysicsActor_eventAddActorToWater_Parms
		{
			AActor* Actor;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventAddActorToWater_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::NewProp_Actor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/* Adds the actor to this water physics simulations */" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Adds the actor to this water physics simulations" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "AddActorToWater", nullptr, nullptr, sizeof(WaterPhysicsActor_eventAddActorToWater_Parms), Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics
	{
		struct WaterPhysicsActor_eventGetWaterPhysicsSceneComponent_Parms
		{
			UWaterPhysicsSceneComponent* ReturnValue;
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
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::NewProp_ReturnValue_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000080588, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventGetWaterPhysicsSceneComponent_Parms, ReturnValue), Z_Construct_UClass_UWaterPhysicsSceneComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::NewProp_ReturnValue_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::NewProp_ReturnValue_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "GetWaterPhysicsSceneComponent", nullptr, nullptr, sizeof(WaterPhysicsActor_eventGetWaterPhysicsSceneComponent_Parms), Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics
	{
		struct WaterPhysicsActor_eventNotifyWaterPhysicsSettingsChanged_Parms
		{
			UWaterPhysicsSettingsComponent* WaterPhysicsSettingsComponent;
		};
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsSettingsComponent_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_WaterPhysicsSettingsComponent;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::NewProp_WaterPhysicsSettingsComponent_MetaData[] = {
		{ "EditInline", "true" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::NewProp_WaterPhysicsSettingsComponent = { "WaterPhysicsSettingsComponent", nullptr, (EPropertyFlags)0x0010000000080080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventNotifyWaterPhysicsSettingsChanged_Parms, WaterPhysicsSettingsComponent), Z_Construct_UClass_UWaterPhysicsSettingsComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::NewProp_WaterPhysicsSettingsComponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::NewProp_WaterPhysicsSettingsComponent_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::NewProp_WaterPhysicsSettingsComponent,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/*\n\x09\x09Notifies the water physics simulation that a setting on the supplied WaterPhysicsSettingsComponent has been changed. \n\x09\x09""Causing the owning actor to have its water physics settings updated, if it exists in the water physics simulation.\n\x09*/" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Notifies the water physics simulation that a setting on the supplied WaterPhysicsSettingsComponent has been changed.\nCausing the owning actor to have its water physics settings updated, if it exists in the water physics simulation." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "NotifyWaterPhysicsSettingsChanged", nullptr, nullptr, sizeof(WaterPhysicsActor_eventNotifyWaterPhysicsSettingsChanged_Parms), Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics
	{
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
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Component_MetaData[] = {
		{ "EditInline", "true" },
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Component = { "Component", nullptr, (EPropertyFlags)0x0010000000080082, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventReceiveCalculateWaterInfo_Parms, Component), Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Component_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Component_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Location_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Location = { "Location", nullptr, (EPropertyFlags)0x0010000008000182, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventReceiveCalculateWaterInfo_Parms, Location), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Location_MetaData, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Location_MetaData)) };
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventReceiveCalculateWaterInfo_Parms, ReturnValue), Z_Construct_UScriptStruct_FGetWaterInfoResult, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Component,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_Location,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/*\n\x09\x09""Blueprint implementable interface for calculating water surface information.\n\x09*/" },
		{ "DisplayName", "Calculate Water Info" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Blueprint implementable interface for calculating water surface information." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "ReceiveCalculateWaterInfo", nullptr, nullptr, sizeof(WaterPhysicsActor_eventReceiveCalculateWaterInfo_Parms), Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x08C20800, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics
	{
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
		static void NewProp_ReturnValue_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	void Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit(void* Obj)
	{
		((WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms*)Obj)->ReturnValue = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms), &Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::NewProp_Actor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::NewProp_ReturnValue,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/*\n\x09\x09""Blueprint implementable event for filtering actors from this water physics simulation. \n\x09\x09Return true to prevent the actor from being added to the water physics simulation.\n\x09*/" },
		{ "DisplayName", "Filter Actor From Water Physics" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Blueprint implementable event for filtering actors from this water physics simulation.\nReturn true to prevent the actor from being added to the water physics simulation." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "ReceiveFilterActorFromWaterPhysics", nullptr, nullptr, sizeof(WaterPhysicsActor_eventReceiveFilterActorFromWaterPhysics_Parms), Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x08020800, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics
	{
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventReceiveOnActorAddedToWater_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::NewProp_Actor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/*\n\x09\x09""Blueprint implementable event for when an actor gets added to the water physics simulation.\n\x09*/" },
		{ "DisplayName", "On Actor Added To Water" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Blueprint implementable event for when an actor gets added to the water physics simulation." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "ReceiveOnActorAddedToWater", nullptr, nullptr, sizeof(WaterPhysicsActor_eventReceiveOnActorAddedToWater_Parms), Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x08020800, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics
	{
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventReceiveOnActorRemovedFromWater_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::NewProp_Actor,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/*\n\x09\x09""Blueprint implementable event for when an actor gets removed from the water physics simulation.\n\x09*/" },
		{ "DisplayName", "On Actor Removed From Water" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Blueprint implementable event for when an actor gets removed from the water physics simulation." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "ReceiveOnActorRemovedFromWater", nullptr, nullptr, sizeof(WaterPhysicsActor_eventReceiveOnActorRemovedFromWater_Parms), Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x08020800, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick_Statics
	{
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/*\n\x09\x09""Blueprint implementable event called before the water physics scene is ticked.\n\x09*/" },
		{ "DisplayName", "Pre Water Physics Scene Tick" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Blueprint implementable event called before the water physics scene is ticked." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "ReceivePreWaterPhysicsSceneTick", nullptr, nullptr, 0, nullptr, 0, RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x08020800, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	struct Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics
	{
		struct WaterPhysicsActor_eventRemoveActorFromWater_Parms
		{
			AActor* Actor;
			float RemoveDelay;
		};
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Actor;
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_RemoveDelay;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Function_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FFunctionParams FuncParams;
	};
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::NewProp_Actor = { "Actor", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventRemoveActorFromWater_Parms, Actor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::NewProp_RemoveDelay = { "RemoveDelay", nullptr, (EPropertyFlags)0x0010000000000080, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(WaterPhysicsActor_eventRemoveActorFromWater_Parms, RemoveDelay), METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::NewProp_Actor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::NewProp_RemoveDelay,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::Function_MetaDataParams[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "/* \n\x09\x09Removes the actor from this water physics simulations.\n\n\x09\x09RemoveDelay: Delay before removing the actor. \n\x09\x09\x09""A RemoveDelay of 0 leads to a one frame delay.\n\x09\x09\x09""A RemoveDelay of > 0 leads to instant removal.\n\x09\x09\x09""Calling AddActorToWater will remove the actor from pending removal.\n\x09*/" },
		{ "CPP_Default_RemoveDelay", "-1.000000" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Removes the actor from this water physics simulations.\n\nRemoveDelay: Delay before removing the actor.\n        A RemoveDelay of 0 leads to a one frame delay.\n        A RemoveDelay of > 0 leads to instant removal.\n        Calling AddActorToWater will remove the actor from pending removal." },
	};
#endif
	const UE4CodeGen_Private::FFunctionParams Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_AWaterPhysicsActor, nullptr, "RemoveActorFromWater", nullptr, nullptr, sizeof(WaterPhysicsActor_eventRemoveActorFromWater_Parms), Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::PropPointers), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::Function_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::Function_MetaDataParams)) };
	UFunction* Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater()
	{
		static UFunction* ReturnFunction = nullptr;
		if (!ReturnFunction)
		{
			UE4CodeGen_Private::ConstructUFunction(ReturnFunction, Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater_Statics::FuncParams);
		}
		return ReturnFunction;
	}
	UClass* Z_Construct_UClass_AWaterPhysicsActor_NoRegister()
	{
		return AWaterPhysicsActor::StaticClass();
	}
	struct Z_Construct_UClass_AWaterPhysicsActor_Statics
	{
		static UObject* (*const DependentSingletons[])();
		static const FClassFunctionLinkInfo FuncInfo[];
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsSceneComponent_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_WaterPhysicsSceneComponent;
#if WITH_EDITORONLY_DATA
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_EditorComponentValidationTable_ValueProp;
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_EditorComponentValidationTable_Key_KeyProp;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_EditorComponentValidationTable_MetaData[];
#endif
		static const UE4CodeGen_Private::FMapPropertyParams NewProp_EditorComponentValidationTable;
#endif // WITH_EDITORONLY_DATA
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_WaterPhysicsFilter_Inner;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_WaterPhysicsFilter_MetaData[];
#endif
		static const UE4CodeGen_Private::FArrayPropertyParams NewProp_WaterPhysicsFilter;
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_EDITORONLY_DATA
#endif // WITH_EDITORONLY_DATA
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_AWaterPhysicsActor_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AActor,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
	const FClassFunctionLinkInfo Z_Construct_UClass_AWaterPhysicsActor_Statics::FuncInfo[] = {
		{ &Z_Construct_UFunction_AWaterPhysicsActor_AddActorToWater, "AddActorToWater" }, // 3541824091
		{ &Z_Construct_UFunction_AWaterPhysicsActor_GetWaterPhysicsSceneComponent, "GetWaterPhysicsSceneComponent" }, // 2023799694
		{ &Z_Construct_UFunction_AWaterPhysicsActor_NotifyWaterPhysicsSettingsChanged, "NotifyWaterPhysicsSettingsChanged" }, // 2540072585
		{ &Z_Construct_UFunction_AWaterPhysicsActor_ReceiveCalculateWaterInfo, "ReceiveCalculateWaterInfo" }, // 1170713329
		{ &Z_Construct_UFunction_AWaterPhysicsActor_ReceiveFilterActorFromWaterPhysics, "ReceiveFilterActorFromWaterPhysics" }, // 1981662529
		{ &Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorAddedToWater, "ReceiveOnActorAddedToWater" }, // 2602170584
		{ &Z_Construct_UFunction_AWaterPhysicsActor_ReceiveOnActorRemovedFromWater, "ReceiveOnActorRemovedFromWater" }, // 1368508987
		{ &Z_Construct_UFunction_AWaterPhysicsActor_ReceivePreWaterPhysicsSceneTick, "ReceivePreWaterPhysicsSceneTick" }, // 433629599
		{ &Z_Construct_UFunction_AWaterPhysicsActor_RemoveActorFromWater, "RemoveActorFromWater" }, // 1600061283
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysicsActor_Statics::Class_MetaDataParams[] = {
		{ "IncludePath", "WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
	};
#endif
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsSceneComponent_MetaData[] = {
		{ "AllowPrivateAccess", "true" },
		{ "Category", "Water Volume" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsSceneComponent = { "WaterPhysicsSceneComponent", nullptr, (EPropertyFlags)0x00200800000a001d, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysicsActor, WaterPhysicsSceneComponent), Z_Construct_UClass_UWaterPhysicsSceneComponent_NoRegister, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsSceneComponent_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsSceneComponent_MetaData)) };
#if WITH_EDITORONLY_DATA
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_ValueProp = { "EditorComponentValidationTable", nullptr, (EPropertyFlags)0x0000000800080008, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 1, Z_Construct_UClass_UActorComponent_NoRegister, METADATA_PARAMS(nullptr, 0) };
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_Key_KeyProp = { "EditorComponentValidationTable_Key", nullptr, (EPropertyFlags)0x0000000800080008, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_MetaData[] = {
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
	};
#endif
	const UE4CodeGen_Private::FMapPropertyParams Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable = { "EditorComponentValidationTable", nullptr, (EPropertyFlags)0x0020088800002008, UE4CodeGen_Private::EPropertyGenFlags::Map, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysicsActor, EditorComponentValidationTable), EMapPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_MetaData)) };
#endif // WITH_EDITORONLY_DATA
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter_Inner = { "WaterPhysicsFilter", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, Z_Construct_UScriptStruct_FWaterPhysicsFilter, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter_MetaData[] = {
		{ "Category", "Water Physics Actor" },
		{ "Comment", "// Only include actors which satisfies this filter. Leave empty for no filter.\n// For more advanced filtering, look at overriding \"Filter Actor From Water Physics\" on this actor.\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsSimulations/WaterPhysicsActor.h" },
		{ "ToolTip", "Only include actors which satisfies this filter. Leave empty for no filter.\nFor more advanced filtering, look at overriding \"Filter Actor From Water Physics\" on this actor." },
	};
#endif
	const UE4CodeGen_Private::FArrayPropertyParams Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter = { "WaterPhysicsFilter", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(AWaterPhysicsActor, WaterPhysicsFilter), EArrayPropertyFlags::None, METADATA_PARAMS(Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter_MetaData)) };
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_AWaterPhysicsActor_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsSceneComponent,
#if WITH_EDITORONLY_DATA
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_ValueProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable_Key_KeyProp,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_EditorComponentValidationTable,
#endif // WITH_EDITORONLY_DATA
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter_Inner,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_AWaterPhysicsActor_Statics::NewProp_WaterPhysicsFilter,
	};
	const FCppClassTypeInfoStatic Z_Construct_UClass_AWaterPhysicsActor_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<AWaterPhysicsActor>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_AWaterPhysicsActor_Statics::ClassParams = {
		&AWaterPhysicsActor::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		FuncInfo,
		Z_Construct_UClass_AWaterPhysicsActor_Statics::PropPointers,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		UE_ARRAY_COUNT(FuncInfo),
		UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysicsActor_Statics::PropPointers),
		0,
		0x009000A5u,
		METADATA_PARAMS(Z_Construct_UClass_AWaterPhysicsActor_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_AWaterPhysicsActor_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_AWaterPhysicsActor()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_AWaterPhysicsActor_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(AWaterPhysicsActor, 1493781390);
	template<> WATERPHYSICS_API UClass* StaticClass<AWaterPhysicsActor>()
	{
		return AWaterPhysicsActor::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_AWaterPhysicsActor(Z_Construct_UClass_AWaterPhysicsActor, &AWaterPhysicsActor::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("AWaterPhysicsActor"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(AWaterPhysicsActor);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
