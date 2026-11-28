// Copyright Mans Isaksson 2021. All Rights Reserved.

#include "RiverologyIntegrationModule.h"
#include "UObject/Class.h"
#include "GameFramework/Actor.h"

DEFINE_LOG_CATEGORY(LogRiverologyIntegration);

namespace Riverology
{
	const static TCHAR* RiverologyClassName = TEXT("/Riverology_Plugin/Advanced/Blueprints/BP_Riverology.BP_Riverology_C");
	const static TCHAR* RiverologySplineComponentName = TEXT("SplineComponent");
	const static TCHAR* RiverologyEnableBuoyancyPropertyName = TEXT("Enable Buoyancy");

	UClass* GetRiverologyClass()
	{
		return LoadClass<UObject>(nullptr, RiverologyClassName);
	}

	UClass* StaticRiverologyClass = nullptr;
	FProperty* StaticRiverologySplineComponentProperty = nullptr;
	FProperty* StaticRiverologyEnableBuoyancyProperty = nullptr;
};

void FRiverologyIntegrationModule::StartupModule()
{
	Riverology::StaticRiverologyClass = Riverology::GetRiverologyClass();
	Riverology::StaticRiverologySplineComponentProperty = Riverology::StaticRiverologyClass->FindPropertyByName(Riverology::RiverologySplineComponentName);
	Riverology::StaticRiverologyEnableBuoyancyProperty = Riverology::StaticRiverologyClass->FindPropertyByName(Riverology::RiverologyEnableBuoyancyPropertyName);
}

class USplineComponent* FRiverologyIntegrationModule::FastGetRiverologySplineComponentChecked(AActor* InRiverologySplineComponent)
{
	check(Riverology::StaticRiverologyClass != nullptr);
	check(Riverology::StaticRiverologySplineComponentProperty != nullptr);
	check(InRiverologySplineComponent->GetClass()->IsChildOf(Riverology::StaticRiverologyClass));

	return *Riverology::StaticRiverologySplineComponentProperty->ContainerPtrToValuePtr<USplineComponent*>((void*)InRiverologySplineComponent);
}

FProperty* FRiverologyIntegrationModule::GetEnableBuoyancyProperty()
{
	return Riverology::StaticRiverologyEnableBuoyancyProperty;
}

IMPLEMENT_MODULE(FRiverologyIntegrationModule, RiverologyIntegration);