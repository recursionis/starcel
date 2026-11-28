// Copyright Mans Isaksson 2021. All Rights Reserved.

#include "WaterPhysicsSimulations/WaterPhysics_Riverology.h"
#include "RiverologyIntegrationModule.h"
#include "WaterPhysicsSettingsComponent.h"
#include "WaterPhysicsSceneComponent.h"
#include "WaterPhysicsCompatibilityLayer.h"
#include "Components/SplineComponent.h"

void AWaterPhysics_Riverology::BeginPlay()
{
	for (const FRiverologyWaterBodySetup& WaterBodySetup : RiverologyWaterBodies)
	{
		if (IsValid(WaterBodySetup.RiverologyWater))
		{
			FProperty* EnableBuoyancyProperty = FRiverologyIntegrationModule::GetEnableBuoyancyProperty();
			check(EnableBuoyancyProperty);

			bool* EnableBuoyancyBooleanValue = EnableBuoyancyProperty->ContainerPtrToValuePtr<bool>(WaterBodySetup.RiverologyWater);
			check(EnableBuoyancyBooleanValue);

			*EnableBuoyancyBooleanValue = false;
		}
	}

	Super::BeginPlay();
}

int32 AWaterPhysics_Riverology::GetWaterBodyPriority(AActor* InWaterBody) const
{
	return RiverologyWaterBodies.IndexOfByPredicate([&](const auto& X) { return X.RiverologyWater == InWaterBody; });
}

TArray<AActor*> AWaterPhysics_Riverology::GetWaterBodies() const
{
	TArray<AActor*> OutActors;
	OutActors.Reserve(RiverologyWaterBodies.Num());
	for (const FRiverologyWaterBodySetup& RiverologyWater : RiverologyWaterBodies)
	{
		OutActors.Add(RiverologyWater.RiverologyWater);
	}
	return OutActors;
}

FGetWaterInfoResult AWaterPhysics_Riverology::CalculateWaterBodyWaterInfo(AActor* InWaterBody, const UActorComponent* Component, const FVector& Location) const
{
	QUICK_SCOPE_CYCLE_COUNTER(STAT_CalculateRiverologyWaterHeight);

	const FRiverologyWaterBodySetup* RiverologySetup = RiverologyWaterBodies.FindByPredicate([&](const auto& X) { return X.RiverologyWater == InWaterBody; });
	check(RiverologySetup);

	USplineComponent* SplineComponent = FRiverologyIntegrationModule::FastGetRiverologySplineComponentChecked(InWaterBody);

	const FTransform SplineTransform = SplineComponent->FindTransformClosestToWorldLocation(Location, ESplineCoordinateSpace::World, false);
	const FVector WaterSurfaceNormal = FVector::UpVector; // NOTE: Riverology does not support rotating the spline, if this changes then we should update this
	const FVector WaterSurfaceLocation = FVector::PointPlaneProject(Location, SplineTransform.GetLocation(), WaterSurfaceNormal);

	FVector WaterVelocity = FVector::ZeroVector;

	if (RiverologySetup->bIncludeVelocity)
	{
		const FVector SplineForwardVector = SplineTransform.GetRotation().GetForwardVector();
		WaterVelocity = SplineForwardVector * RiverologySetup->WaterVelocity;
	}

	return FGetWaterInfoResult{ WaterSurfaceLocation, WaterSurfaceNormal, WaterVelocity };
}