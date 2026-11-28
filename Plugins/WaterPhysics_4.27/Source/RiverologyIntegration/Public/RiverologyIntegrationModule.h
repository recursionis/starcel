// Copyright Mans Isaksson 2021. All Rights Reserved.

#pragma once
#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

DECLARE_LOG_CATEGORY_EXTERN(LogRiverologyIntegration, Log, All);

class FRiverologyIntegrationModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;

	static class USplineComponent* FastGetRiverologySplineComponentChecked(class AActor* InRiverologySplineComponent);

	static FProperty* GetEnableBuoyancyProperty();
};