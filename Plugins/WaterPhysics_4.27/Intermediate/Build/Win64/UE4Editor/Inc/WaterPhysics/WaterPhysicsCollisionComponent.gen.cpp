// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "WaterPhysics/Public/WaterPhysicsCollisionComponent.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeWaterPhysicsCollisionComponent() {}
// Cross Module References
	WATERPHYSICS_API UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsCollisionType();
	UPackage* Z_Construct_UPackage__Script_WaterPhysics();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsCollisionComponent_NoRegister();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsCollisionComponent();
	ENGINE_API UClass* Z_Construct_UClass_USceneComponent();
	ENGINE_API UClass* Z_Construct_UClass_UStaticMesh_NoRegister();
	COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector();
	COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FColor();
	WATERPHYSICS_API UClass* Z_Construct_UClass_UWaterPhysicsCollisionInterface_NoRegister();
// End Cross Module References
	static UEnum* EWaterPhysicsCollisionType_StaticEnum()
	{
		static UEnum* Singleton = nullptr;
		if (!Singleton)
		{
			Singleton = GetStaticEnum(Z_Construct_UEnum_WaterPhysics_EWaterPhysicsCollisionType, Z_Construct_UPackage__Script_WaterPhysics(), TEXT("EWaterPhysicsCollisionType"));
		}
		return Singleton;
	}
	template<> WATERPHYSICS_API UEnum* StaticEnum<EWaterPhysicsCollisionType>()
	{
		return EWaterPhysicsCollisionType_StaticEnum();
	}
	static FCompiledInDeferEnum Z_CompiledInDeferEnum_UEnum_EWaterPhysicsCollisionType(EWaterPhysicsCollisionType_StaticEnum, TEXT("/Script/WaterPhysics"), TEXT("EWaterPhysicsCollisionType"), false, nullptr, nullptr);
	uint32 Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsCollisionType_Hash() { return 2612049276U; }
	UEnum* Z_Construct_UEnum_WaterPhysics_EWaterPhysicsCollisionType()
	{
#if WITH_HOT_RELOAD
		UPackage* Outer = Z_Construct_UPackage__Script_WaterPhysics();
		static UEnum* ReturnEnum = FindExistingEnumIfHotReloadOrDynamic(Outer, TEXT("EWaterPhysicsCollisionType"), 0, Get_Z_Construct_UEnum_WaterPhysics_EWaterPhysicsCollisionType_Hash(), false);
#else
		static UEnum* ReturnEnum = nullptr;
#endif // WITH_HOT_RELOAD
		if (!ReturnEnum)
		{
			static const UE4CodeGen_Private::FEnumeratorParam Enumerators[] = {
				{ "EWaterPhysicsCollisionType::Mesh", (int64)EWaterPhysicsCollisionType::Mesh },
				{ "EWaterPhysicsCollisionType::MeshCollision", (int64)EWaterPhysicsCollisionType::MeshCollision },
				{ "EWaterPhysicsCollisionType::Box", (int64)EWaterPhysicsCollisionType::Box },
				{ "EWaterPhysicsCollisionType::Sphere", (int64)EWaterPhysicsCollisionType::Sphere },
				{ "EWaterPhysicsCollisionType::Capsule", (int64)EWaterPhysicsCollisionType::Capsule },
			};
#if WITH_METADATA
			const UE4CodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
				{ "Box.Name", "EWaterPhysicsCollisionType::Box" },
				{ "Capsule.Name", "EWaterPhysicsCollisionType::Capsule" },
				{ "Mesh.Name", "EWaterPhysicsCollisionType::Mesh" },
				{ "MeshCollision.Name", "EWaterPhysicsCollisionType::MeshCollision" },
				{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
				{ "Sphere.Name", "EWaterPhysicsCollisionType::Sphere" },
			};
#endif
			static const UE4CodeGen_Private::FEnumParams EnumParams = {
				(UObject*(*)())Z_Construct_UPackage__Script_WaterPhysics,
				nullptr,
				"EWaterPhysicsCollisionType",
				"EWaterPhysicsCollisionType",
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
	void UWaterPhysicsCollisionComponent::StaticRegisterNativesUWaterPhysicsCollisionComponent()
	{
	}
	UClass* Z_Construct_UClass_UWaterPhysicsCollisionComponent_NoRegister()
	{
		return UWaterPhysicsCollisionComponent::StaticClass();
	}
	struct Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics
	{
		static UObject* (*const DependentSingletons[])();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const UE4CodeGen_Private::FBytePropertyParams NewProp_CollisionType_Underlying;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_CollisionType_MetaData[];
#endif
		static const UE4CodeGen_Private::FEnumPropertyParams NewProp_CollisionType;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_Mesh_MetaData[];
#endif
		static const UE4CodeGen_Private::FObjectPropertyParams NewProp_Mesh;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_LOD_MetaData[];
#endif
		static const UE4CodeGen_Private::FIntPropertyParams NewProp_LOD;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_BoxExtent_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_BoxExtent;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_SphereRadius_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_SphereRadius;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_CapsuleHalfHeight_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_CapsuleHalfHeight;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_CapsuleRadius_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_CapsuleRadius;
#if WITH_EDITORONLY_DATA
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_LineThickness_MetaData[];
#endif
		static const UE4CodeGen_Private::FFloatPropertyParams NewProp_LineThickness;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_ShapeColor_MetaData[];
#endif
		static const UE4CodeGen_Private::FStructPropertyParams NewProp_ShapeColor;
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam NewProp_bVisibleOnlyWithShowCollision_MetaData[];
#endif
		static void NewProp_bVisibleOnlyWithShowCollision_SetBit(void* Obj);
		static const UE4CodeGen_Private::FBoolPropertyParams NewProp_bVisibleOnlyWithShowCollision;
#endif // WITH_EDITORONLY_DATA
		static const UE4CodeGen_Private::FPropertyParamsBase* const PropPointers[];
#if WITH_EDITORONLY_DATA
#endif // WITH_EDITORONLY_DATA
		static const UE4CodeGen_Private::FImplementedInterfaceParams InterfaceParams[];
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_USceneComponent,
		(UObject* (*)())Z_Construct_UPackage__Script_WaterPhysics,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::Class_MetaDataParams[] = {
		{ "BlueprintSpawnableComponent", "" },
		{ "ClassGroupNames", "Physics" },
		{ "Comment", "/*\n* This component will add additional collision for the water physics system (This collision is purely logical and will not create an actual collider).\n* Needs to be attached to a PrimitiveComponent which is simulating physics (Or which is welded to a simulating component).\n*/" },
		{ "DisplayName", "Water Physics Collision" },
		{ "HideCategories", "ComponentReplication Collision ComponentTick Activation Events Physics LOD Trigger PhysicsVolume" },
		{ "IncludePath", "WaterPhysicsCollisionComponent.h" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "* This component will add additional collision for the water physics system (This collision is purely logical and will not create an actual collider).\n* Needs to be attached to a PrimitiveComponent which is simulating physics (Or which is welded to a simulating component)." },
	};
#endif
	const UE4CodeGen_Private::FBytePropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UE4CodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, 1, 0, nullptr, METADATA_PARAMS(nullptr, 0) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "Comment", "// The type of collision which should be used for this component\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The type of collision which should be used for this component" },
	};
#endif
	const UE4CodeGen_Private::FEnumPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType = { "CollisionType", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, CollisionType), Z_Construct_UEnum_WaterPhysics_EWaterPhysicsCollisionType, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_Mesh_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "Comment", "/**\n\x09 *\x09The mesh asset used for Mesh/MeshCollision. \n\x09 *\x09When using Mesh option, the StaticMesh asset must enable \"Allow CPU Access\"\n\x09 */" },
		{ "EditCondition", "CollisionType==EWaterPhysicsCollisionType::Mesh||CollisionType==EWaterPhysicsCollisionType::MeshCollision" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The mesh asset used for Mesh/MeshCollision.\nWhen using Mesh option, the StaticMesh asset must enable \"Allow CPU Access\"" },
	};
#endif
	const UE4CodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_Mesh = { "Mesh", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, Mesh), Z_Construct_UClass_UStaticMesh_NoRegister, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_Mesh_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_Mesh_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LOD_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "Comment", "// The LOD to use when sourcing the mesh used for water physics simulation\n" },
		{ "EditCondition", "CollisionType==EWaterPhysicsCollisionType::Mesh" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The LOD to use when sourcing the mesh used for water physics simulation" },
	};
#endif
	const UE4CodeGen_Private::FIntPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LOD = { "LOD", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, LOD), METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LOD_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LOD_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_BoxExtent_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "Comment", "// The extents of the box (Used with collision type Box)\n" },
		{ "EditCondition", "CollisionType==EWaterPhysicsCollisionType::Box" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The extents of the box (Used with collision type Box)" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_BoxExtent = { "BoxExtent", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, BoxExtent), Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_BoxExtent_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_BoxExtent_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_SphereRadius_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "ClampMin", "0" },
		{ "Comment", "// The radius of the sphere (Used with collision type Sphere)\n" },
		{ "EditCondition", "CollisionType==EWaterPhysicsCollisionType::Sphere" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The radius of the sphere (Used with collision type Sphere)" },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_SphereRadius = { "SphereRadius", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, SphereRadius), METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_SphereRadius_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_SphereRadius_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleHalfHeight_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "ClampMin", "0" },
		{ "Comment", "/** \n\x09 *\x09""Capsule Half-height, from center of capsule to the end of top or bottom hemisphere.\n\x09 *\x09This cannot be less than CapsuleRadius.\n\x09 */" },
		{ "EditCondition", "CollisionType==EWaterPhysicsCollisionType::Capsule" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "Capsule Half-height, from center of capsule to the end of top or bottom hemisphere.\nThis cannot be less than CapsuleRadius." },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleHalfHeight = { "CapsuleHalfHeight", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, CapsuleHalfHeight), METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleHalfHeight_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleHalfHeight_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleRadius_MetaData[] = {
		{ "Category", "Water Physics Collision" },
		{ "ClampMin", "0" },
		{ "Comment", "/** \n\x09 *\x09Radius of cap hemispheres and center cylinder.\n\x09 *\x09This cannot be more than CapsuleHalfHeight.\n\x09 */" },
		{ "EditCondition", "CollisionType==EWaterPhysicsCollisionType::Capsule" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "Radius of cap hemispheres and center cylinder.\nThis cannot be more than CapsuleHalfHeight." },
		{ "UIMin", "0" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleRadius = { "CapsuleRadius", nullptr, (EPropertyFlags)0x0010000000000005, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, CapsuleRadius), METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleRadius_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleRadius_MetaData)) };
#if WITH_EDITORONLY_DATA
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LineThickness_MetaData[] = {
		{ "Category", "Rendering" },
		{ "Comment", "// The line thickness to use during component visualization\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The line thickness to use during component visualization" },
	};
#endif
	const UE4CodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LineThickness = { "LineThickness", nullptr, (EPropertyFlags)0x0010040800000001, UE4CodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, LineThickness), METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LineThickness_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LineThickness_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_ShapeColor_MetaData[] = {
		{ "Category", "Rendering" },
		{ "Comment", "// The color to use during component visualization\n" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "The color to use during component visualization" },
	};
#endif
	const UE4CodeGen_Private::FStructPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_ShapeColor = { "ShapeColor", nullptr, (EPropertyFlags)0x0010040800000001, UE4CodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, 1, STRUCT_OFFSET(UWaterPhysicsCollisionComponent, ShapeColor), Z_Construct_UScriptStruct_FColor, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_ShapeColor_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_ShapeColor_MetaData)) };
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision_MetaData[] = {
		{ "Category", "Rendering" },
		{ "Comment", "// If this component should only be visible during \"Show Collision\"\n" },
		{ "EditCondition", "bVisible" },
		{ "ModuleRelativePath", "Public/WaterPhysicsCollisionComponent.h" },
		{ "ToolTip", "If this component should only be visible during \"Show Collision\"" },
	};
#endif
	void Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision_SetBit(void* Obj)
	{
		((UWaterPhysicsCollisionComponent*)Obj)->bVisibleOnlyWithShowCollision = 1;
	}
	const UE4CodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision = { "bVisibleOnlyWithShowCollision", nullptr, (EPropertyFlags)0x0010040800000001, UE4CodeGen_Private::EPropertyGenFlags::Bool | UE4CodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, 1, sizeof(bool), sizeof(UWaterPhysicsCollisionComponent), &Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision_SetBit, METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision_MetaData, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision_MetaData)) };
#endif // WITH_EDITORONLY_DATA
	const UE4CodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::PropPointers[] = {
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType_Underlying,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CollisionType,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_Mesh,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LOD,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_BoxExtent,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_SphereRadius,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleHalfHeight,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_CapsuleRadius,
#if WITH_EDITORONLY_DATA
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_LineThickness,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_ShapeColor,
		(const UE4CodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::NewProp_bVisibleOnlyWithShowCollision,
#endif // WITH_EDITORONLY_DATA
	};
		const UE4CodeGen_Private::FImplementedInterfaceParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::InterfaceParams[] = {
			{ Z_Construct_UClass_UWaterPhysicsCollisionInterface_NoRegister, (int32)VTABLE_OFFSET(UWaterPhysicsCollisionComponent, IWaterPhysicsCollisionInterface), false },
		};
	const FCppClassTypeInfoStatic Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UWaterPhysicsCollisionComponent>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::ClassParams = {
		&UWaterPhysicsCollisionComponent::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		nullptr,
		Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::PropPointers,
		InterfaceParams,
		UE_ARRAY_COUNT(DependentSingletons),
		0,
		UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::PropPointers),
		UE_ARRAY_COUNT(InterfaceParams),
		0x00B000A4u,
		METADATA_PARAMS(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_UWaterPhysicsCollisionComponent()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_UWaterPhysicsCollisionComponent_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(UWaterPhysicsCollisionComponent, 2635751281);
	template<> WATERPHYSICS_API UClass* StaticClass<UWaterPhysicsCollisionComponent>()
	{
		return UWaterPhysicsCollisionComponent::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_UWaterPhysicsCollisionComponent(Z_Construct_UClass_UWaterPhysicsCollisionComponent, &UWaterPhysicsCollisionComponent::StaticClass, TEXT("/Script/WaterPhysics"), TEXT("UWaterPhysicsCollisionComponent"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(UWaterPhysicsCollisionComponent);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
