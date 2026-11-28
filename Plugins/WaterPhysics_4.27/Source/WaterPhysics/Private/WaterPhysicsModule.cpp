// Copyright Mans Isaksson 2021. All Rights Reserved.

#include "WaterPhysicsModule.h"
#include "Modules/ModuleManager.h"
#include "WaterPhysicsApp.h"

DEFINE_LOG_CATEGORY(LogWaterPhysics);

static FName WaterIntegrationModuleName = TEXT("UEWaterIntegration");
static FName OceanologyIntegrationModuleName = TEXT("OceanologyIntegration");
static FName RiverologyIntegrationModuleName = TEXT("RiverologyIntegration");

void FWaterPhysicsModule::StartupModule()
{
	if (!FWaterPhysicsApp::CanUseWaterPhysicsPlugin())
	{
		UE_LOG(LogWaterPhysics, Error, TEXT("YOU ARE USING A TRIAL VERSION OF DYNAMIC WATER PHYSICS IN A RELEASED GAME"));
		UE_LOG(LogWaterPhysics, Error, TEXT("Water Physics features have been disabled, to purchase full version visit: https://www.unrealengine.com/marketplace/en-US/product/2d8710643bcf4e2b94a9154d0732b4af"));
	}

	// IMPORTANT: This assumes the Water module is loaded before us,
	// right now the water module is loaded in PostConfigInit, which is before us.
	if (FModuleManager::Get().IsModuleLoaded(TEXT("Water")))
	{
		FModuleManager::Get().LoadModule(WaterIntegrationModuleName);
	}

	// IMPORTANT: This assumes the Oceanology module is loaded before us,
	// right now the oceanology module is loaded in Default, which is before us.
	if (FModuleManager::Get().IsModuleLoaded(TEXT("Oceanology_Plugin")))
	{
		FModuleManager::Get().LoadModule(OceanologyIntegrationModuleName);
	}

	// IMPORTANT: This assumes the Riverology module is loaded before us,
	// right now the oceanology module is loaded in PreDefault, which is before us.
	if (FModuleManager::Get().IsModuleLoaded(TEXT("Riverology_Plugin")))
	{
		FModuleManager::Get().LoadModule(RiverologyIntegrationModuleName);
	}
}

void FWaterPhysicsModule::ShutdownModule()
{
	if (FModuleManager::Get().IsModuleLoaded(WaterIntegrationModuleName))
	{
		// bIsShutdown true to prevent ModulesChangedEvent from firing.
		// This event is for unreal to update UI, which is not necessary with this module.
		FModuleManager::Get().UnloadModule(WaterIntegrationModuleName, true);
	}

	if (FModuleManager::Get().IsModuleLoaded(OceanologyIntegrationModuleName))
	{
		// bIsShutdown true to prevent ModulesChangedEvent from firing.
		// This event is for unreal to update UI, which is not necessary with this module.
		FModuleManager::Get().UnloadModule(OceanologyIntegrationModuleName, true);
	}

	if (FModuleManager::Get().IsModuleLoaded(RiverologyIntegrationModuleName))
	{
		// bIsShutdown true to prevent ModulesChangedEvent from firing.
		// This event is for unreal to update UI, which is not necessary with this module.
		FModuleManager::Get().UnloadModule(RiverologyIntegrationModuleName, true);
	}
}

IMPLEMENT_MODULE(FWaterPhysicsModule, WaterPhysics);