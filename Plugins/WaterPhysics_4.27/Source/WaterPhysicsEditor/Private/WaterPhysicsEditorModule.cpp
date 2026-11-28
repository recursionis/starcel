// Copyright Mans Isaksson 2021. All Rights Reserved.

#include "WaterPhysicsEditorModule.h"
#include "WaterPhysicsTypes.h"
#include "WaterPhysicsApp.h"
#include "WaterPhysicsCollisionComponent.h"
#include "WaterPhysicsCollisionComponentVisualizer.h"
#include "ActorComponentsSelectionCustomization.h"
#include "WaterPhysicsFilterCustomization.h"
#include "Editor.h"
#include "UnrealEdGlobals.h"
#include "Editor/UnrealEdEngine.h"
#include "Misc/MessageDialog.h"

DEFINE_LOG_CATEGORY(LogWaterPhysicsEd);

namespace WaterPhysicsEditorModule
{
	void OnMapChanged(const FString& Filename, bool bAsTemplate)
	{
		static bool bHasShownTrialVersionModal = false;
		if (!bHasShownTrialVersionModal)
		{
			const static FText DialogTitle = NSLOCTEXT("WaterPhysicsEd", "TrialVersionNoticeTitle", "Dynamic Water Physics - Trial Version");
			const static FText DialogMessage = NSLOCTEXT("WaterPhysicsEd", "TrialVersionNoticeMsh", "You are using a trial version of Dynamic Water Physics. To use this plugin in a released product you must purchase a full license at:\n\nhttps://www.unrealengine.com/marketplace/en-US/product/2d8710643bcf4e2b94a9154d0732b4af");
			FMessageDialog::Open(EAppMsgType::Ok, DialogMessage, &DialogTitle);
			bHasShownTrialVersionModal = true;
		}
	}
}

void FWaterPhysicsEditorModule::StartupModule()
{
	RegisterDetailsCustomization();
	RegisterEditorDelegates();
	RegisterVisualizers();
}

void FWaterPhysicsEditorModule::ShutdownModule()
{
	UnregisterDetailsCustomization();
	UnregisterEditorDelegates();
	UnregisterVisualizers();
}

void FWaterPhysicsEditorModule::RegisterDetailsCustomization()
{
	FPropertyEditorModule& PropertyEditorModule = FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");
	
	PropertyEditorModule.RegisterCustomPropertyTypeLayout(
		FActorComponentsSelection::StaticStruct()->GetFName(),
		FOnGetPropertyTypeCustomizationInstance::CreateLambda([]() { return MakeShareable(new FActorComponentsSelectionCustomization); })
	);

	PropertyEditorModule.RegisterCustomPropertyTypeLayout(
		FWaterPhysicsFilter::StaticStruct()->GetFName(),
		FOnGetPropertyTypeCustomizationInstance::CreateLambda([]() { return MakeShareable(new FWaterPhysicsFilterCustomization); })
	);
}

void FWaterPhysicsEditorModule::UnregisterDetailsCustomization()
{
	if (FPropertyEditorModule* PropertyEditorModule = FModuleManager::GetModulePtr<FPropertyEditorModule>("PropertyEditor"))
	{
		PropertyEditorModule->UnregisterCustomPropertyTypeLayout(FActorComponentsSelection::StaticStruct()->GetFName());

		PropertyEditorModule->UnregisterCustomPropertyTypeLayout(FWaterPhysicsFilter::StaticStruct()->GetFName());
	}
}

void FWaterPhysicsEditorModule::RegisterEditorDelegates()
{
	if (FWaterPhysicsApp::IsTrialVersion())
	{
		FEditorDelegates::OnMapOpened.AddStatic(WaterPhysicsEditorModule::OnMapChanged);
	}
}

void FWaterPhysicsEditorModule::UnregisterEditorDelegates()
{
	if (FWaterPhysicsApp::IsTrialVersion())
	{
		FEditorDelegates::OnMapOpened.Remove(OnMapOpenedHandle);
	}
}

void FWaterPhysicsEditorModule::RegisterVisualizers()
{
	if (GUnrealEd != NULL)
	{
		TSharedPtr<FComponentVisualizer> WaterPhysicsCollisionComponentVisualizer = MakeShared<FWaterPhysicsCollisionComponentVisualizer>();
		GUnrealEd->RegisterComponentVisualizer(UWaterPhysicsCollisionComponent::StaticClass()->GetFName(), WaterPhysicsCollisionComponentVisualizer);
		WaterPhysicsCollisionComponentVisualizer->OnRegister();
	}
}

void FWaterPhysicsEditorModule::UnregisterVisualizers()
{
	if (GUnrealEd != NULL)
	{
		GUnrealEd->UnregisterComponentVisualizer(UWaterPhysicsCollisionComponent::StaticClass()->GetFName());
	}
}

IMPLEMENT_MODULE(FWaterPhysicsEditorModule, WaterPhysicsEditor);