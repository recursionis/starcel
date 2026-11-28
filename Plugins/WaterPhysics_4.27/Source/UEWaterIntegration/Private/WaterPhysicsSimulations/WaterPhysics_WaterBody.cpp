// Copyright Mans Isaksson 2021. All Rights Reserved.

#include "WaterPhysicsSimulations/WaterPhysics_WaterBody.h"
#include "WaterPhysicsCompatibilityLayer.h"
#if ENGINE_VERSION_LESS_THAN(5, 0)
#include "WaterBodyActor_PublicHack.h"
#include "WaterSplineComponent.h"
#include "LandscapeProxy.h"
#endif
#include "WaterPhysicsSettingsComponent.h"
#include "WaterPhysicsSceneComponent.h"
#include "WaterPhysicsSimulations/WaterPhysics_WaterVolume.h"
#include "Components/BillboardComponent.h"
#include "WaterBodyActor.h"
#include "UObject/ConstructorHelpers.h"

// This entire class is just a huge hack such that we can override UWaterSubsystem::GetWaterTimeSeconds() as that function has a GetValueOnGameThread() call
// which crashes if we run the water information fetching in parallel.
// 
// This has been fixed in UE5 so kept for backwards compatibility
class FWaterBodyHack
{
public:
#if ENGINE_VERSION_LESS_THAN(5, 0)
	static float LazilyComputeSplineKey(FWaterBodyQueryResult& QueryResult, const AWaterBody& InWaterBody, const FVector& InWorldLocation)
	{
		// only compute if not done (or set) before : 
		if (!QueryResult.SplineInputKey.IsSet())
		{
			QueryResult.SplineInputKey = TOptional<float>(InWaterBody.FindInputKeyClosestToWorldLocation(InWorldLocation));
		}
		return QueryResult.SplineInputKey.GetValue();
	}

	static float GetWaterOceanFallbackDepth()
	{
		static IConsoleVariable* ConsoleVariable = nullptr;
		static FCriticalSection CriticalSection;
		if (ConsoleVariable == nullptr)
		{
			FScopeLock Lock(&CriticalSection);
			if (ConsoleVariable == nullptr)
				ConsoleVariable = IConsoleManager::Get().FindConsoleVariable(TEXT("r.Water.OceanFallbackDepth"));
		}

		check(ConsoleVariable != nullptr);
		return ConsoleVariable->GetFloat();
	}

	static int32 GetOverrideWavesTime()
	{
		static IConsoleVariable* ConsoleVariable = nullptr;
		static FCriticalSection CriticalSection;
		if (ConsoleVariable == nullptr)
		{
			FScopeLock Lock(&CriticalSection);
			if (ConsoleVariable == nullptr)
				ConsoleVariable = IConsoleManager::Get().FindConsoleVariable(TEXT("r.Water.OverrideWavesTime"));
		}

		check(ConsoleVariable != nullptr);
		return ConsoleVariable->GetInt();
	}

	static float GetWaveReferenceTime(AWaterBody* WaterBody)
	{
		if (WaterBody->HasWaves())
		{
			UWorld* World = WaterBody->GetWorld();
			if (UWaterSubsystem* WaterSubsystem = UWaterSubsystem::GetWaterSubsystem(World))
			{
				float ForceWavesTimeValue = GetOverrideWavesTime();
				if (ForceWavesTimeValue >= 0.0f)
				{
					return ForceWavesTimeValue;
				}

				if (World->IsGameWorld() && WaterSubsystem->bUsingSmoothedTime)
				{
					return WaterSubsystem->GetSmoothedWorldTimeSeconds();
				}

				return WaterSubsystem->NonSmoothedWorldTimeSeconds;
			}
		}
		return 0.0f;
	}

	static bool GetWaveInfoAtPosition(AWaterBody* WaterBody, const FVector& InPosition, float InWaterDepth, bool bInSimpleWaves, FWaveInfo& InOutWaveInfo)
	{
		if (!WaterBody->HasWaves())
		{
			return false; //Collision needs to be fixed for rivers
		}

		float MaxWaveHeight = WaterBody->GetMaxWaveHeight();

		InOutWaveInfo.ReferenceTime = GetWaveReferenceTime(WaterBody);
		InOutWaveInfo.AttenuationFactor *= WaterBody->GetWaveAttenuationFactor(InPosition, InWaterDepth);

		// No need to perform computation if we're going to cancel it out afterwards :
		if (InOutWaveInfo.AttenuationFactor > 0.0f)
		{
			// Maximum amplitude that the wave can reach at this location : 
			InOutWaveInfo.MaxHeight = MaxWaveHeight * InOutWaveInfo.AttenuationFactor;

			float WaveHeight;
			if (bInSimpleWaves)
			{
				WaveHeight = WaterBody->GetSimpleWaveHeightAtPosition(InPosition, InWaterDepth, InOutWaveInfo.ReferenceTime);
			}
			else
			{
				FVector ComputedNormal;
				WaveHeight = WaterBody->GetWaveHeightAtPosition(InPosition, InWaterDepth, InOutWaveInfo.ReferenceTime, ComputedNormal);
				// Attenuate the normal :
				ComputedNormal = FMath::Lerp(InOutWaveInfo.Normal, ComputedNormal, InOutWaveInfo.AttenuationFactor);
				if (!ComputedNormal.IsZero())
				{
					InOutWaveInfo.Normal = ComputedNormal;
				}
			}

			// Attenuate the wave amplitude :
			InOutWaveInfo.Height = WaveHeight * InOutWaveInfo.AttenuationFactor;
		}

		return true;
	}

	static EWaterBodyQueryFlags CheckAndAjustQueryFlags(AWaterBody* WaterBody, EWaterBodyQueryFlags InQueryFlags)
	{
		EWaterBodyQueryFlags Result = InQueryFlags;

		// Waves only make sense for the following queries : 
		check(!EnumHasAnyFlags(Result, EWaterBodyQueryFlags::IncludeWaves)
			|| EnumHasAnyFlags(Result, EWaterBodyQueryFlags::ComputeLocation | EWaterBodyQueryFlags::ComputeNormal | EWaterBodyQueryFlags::ComputeDepth | EWaterBodyQueryFlags::ComputeImmersionDepth));

		// Simple waves only make sense when computing waves : 
		check(!EnumHasAnyFlags(Result, EWaterBodyQueryFlags::SimpleWaves)
			|| EnumHasAnyFlags(Result, EWaterBodyQueryFlags::IncludeWaves));

		if (EnumHasAnyFlags(InQueryFlags, EWaterBodyQueryFlags::ComputeDepth | EWaterBodyQueryFlags::ComputeImmersionDepth))
		{
			// We need location when querying depth : 
			Result |= EWaterBodyQueryFlags::ComputeLocation;
		}

		if (EnumHasAnyFlags(InQueryFlags, EWaterBodyQueryFlags::IncludeWaves) && WaterBody->HasWaves())
		{
			// We need location and water depth when computing waves :
			Result |= EWaterBodyQueryFlags::ComputeLocation | EWaterBodyQueryFlags::ComputeDepth;
		}

		return Result;
	}

	static FWaterBodyQueryResult QueryWaterInfoClosestToWorldLocation(AWaterBody* WaterBody, const FVector& InWorldLocation, EWaterBodyQueryFlags InQueryFlags, const TOptional<float>& InSplineInputKey)
	{
		QUICK_SCOPE_CYCLE_COUNTER(STAT_Custom_WaterBody_ComputeWaterInfo);

		// Use the (optional) input spline input key if it has already been computed: 
		FWaterBodyQueryResult Result(InSplineInputKey);
		Result.SetQueryFlags(CheckAndAjustQueryFlags(WaterBody, InQueryFlags));

		if (!EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::IgnoreExclusionVolumes))
		{
			// No early-out, so that the requested information is still set. It is expected for the caller to check for IsInExclusionVolume() because technically, the returned information will be invalid :
			Result.SetIsInExclusionVolume(WaterBody->IsWorldLocationInExclusionVolume(InWorldLocation));
		}

		// Lakes and oceans have surfaces aligned with the XY plane
		const bool bFlatSurface = WaterBody->IsFlatSurface();

		// Compute water plane location :
		if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeLocation))
		{
			FVector WaterPlaneLocation = InWorldLocation;
			// If in exclusion volume, force the water plane location at the query location. It is technically invalid, but it's up to the caller to check whether we're in an exclusion volume. 
			//  If the user fails to do so, at least it allows immersion depth to be 0.0f, which means the query location is NOT in water :
			if (!Result.IsInExclusionVolume())
			{
				WaterPlaneLocation.Z = bFlatSurface ? WaterBody->GetActorLocation().Z : WaterBody->GetWaterSpline()->GetLocationAtSplineInputKey(LazilyComputeSplineKey(Result, *WaterBody, InWorldLocation), ESplineCoordinateSpace::World).Z;

				// Apply body height offset if applicable (ocean)
				if (WaterBody->IsHeightOffsetSupported())
				{
					WaterPlaneLocation.Z += WaterBody->GetHeightOffset();
				}
			}

			Result.SetWaterPlaneLocation(WaterPlaneLocation);
			// When not including waves, water surface == water plane : 
			Result.SetWaterSurfaceLocation(WaterPlaneLocation);
		}

		// Compute water plane normal :
		FVector WaterPlaneNormal = FVector::UpVector;
		if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeNormal))
		{
			// Default to Z up for the normal
			if (!bFlatSurface)
			{
				// For rivers default to using spline up vector to account for sloping rivers
				WaterPlaneNormal = WaterBody->GetWaterSpline()->GetUpVectorAtSplineInputKey(LazilyComputeSplineKey(Result, *WaterBody, InWorldLocation), ESplineCoordinateSpace::World);
			}

			Result.SetWaterPlaneNormal(WaterPlaneNormal);
			// When not including waves, water surface == water plane : 
			Result.SetWaterSurfaceNormal(WaterPlaneNormal);
		}

		// Compute water plane depth : 
		float WaveAttenuationFactor = 1.0f;
		if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeDepth))
		{
			QUICK_SCOPE_CYCLE_COUNTER(STAT_WaterBody_ComputeWaterDepth);

			check(EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeLocation));
			float WaterPlaneDepth = 0.0f;

			// The better option for computing water depth for ocean and lake is landscape : 
			const bool bTryUseLandscape = (WaterBody->GetWaterBodyType() == EWaterBodyType::Ocean || WaterBody->GetWaterBodyType() == EWaterBodyType::Lake);
			if (bTryUseLandscape)
			{
				TOptional<float> LandscapeHeightOptional;
				if (ALandscapeProxy* LandscapePtr = WaterBody->FindLandscape())
				{
					QUICK_SCOPE_CYCLE_COUNTER(STAT_WaterBody_ComputeLandscapeDepth);
					LandscapeHeightOptional = LandscapePtr->GetHeightAtLocation(InWorldLocation);
				}

				bool bValidLandscapeData = LandscapeHeightOptional.IsSet();
				if (bValidLandscapeData)
				{
					WaterPlaneDepth = Result.GetWaterPlaneLocation().Z - LandscapeHeightOptional.GetValue();
					// Special case : cancel out waves for under-landscape ocean
					if ((WaterPlaneDepth < 0.0f) && (WaterBody->GetWaterBodyType() == EWaterBodyType::Ocean))
					{
						WaveAttenuationFactor = 0.0f;
					}
				}

				// If the height is invalid, we either have invalid landscape data or we're under the landscape
				if (!bValidLandscapeData || (WaterPlaneDepth < 0.0f))
				{
					if (WaterBody->GetWaterBodyType() == EWaterBodyType::Ocean)
					{
						// Fallback value when landscape is not found under the ocean water.
						WaterPlaneDepth = FWaterBodyHack::GetWaterOceanFallbackDepth();
					}
					else
					{
						check(WaterBody->GetWaterBodyType() == EWaterBodyType::Lake);
						// For an underwater lake, consider an uniform depth across the projection segment on the lake spline :
						WaterPlaneDepth = WaterBody->WaterSplineMetadata->Depth.Eval(LazilyComputeSplineKey(Result, *WaterBody, InWorldLocation), 0.f);
					}
				}
			}
			else
			{
				// For rivers and transitions, depth always come from the spline :
				WaterPlaneDepth = WaterBody->WaterSplineMetadata->Depth.Eval(LazilyComputeSplineKey(Result, *WaterBody, InWorldLocation), 0.f);
			}

			WaterPlaneDepth = FMath::Max(WaterPlaneDepth, 0.0f);
			Result.SetWaterPlaneDepth(WaterPlaneDepth);

			// When not including waves, water surface == water plane : 
			Result.SetWaterSurfaceDepth(WaterPlaneDepth);
		}

		// Optionally compute water surface location/normal/depth for waves : 
		if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::IncludeWaves) && WaterBody->HasWaves())
		{
			QUICK_SCOPE_CYCLE_COUNTER(STAT_WaterBody_ComputeWaveHeight);
			FWaveInfo WaveInfo;

			if (!Result.IsInExclusionVolume())
			{
				WaveInfo.AttenuationFactor = WaveAttenuationFactor;
				WaveInfo.Normal = WaterPlaneNormal;
				const bool bSimpleWaves = EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::SimpleWaves);
				FWaterBodyHack::GetWaveInfoAtPosition(WaterBody, Result.GetWaterPlaneLocation(), Result.GetWaterSurfaceDepth(), bSimpleWaves, WaveInfo);
			}

			Result.SetWaveInfo(WaveInfo);

			if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeLocation))
			{
				FVector WaterSurfaceLocation = Result.GetWaterSurfaceLocation();
				WaterSurfaceLocation.Z += WaveInfo.Height;
				Result.SetWaterSurfaceLocation(WaterSurfaceLocation);
			}

			if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeNormal))
			{
				Result.SetWaterSurfaceNormal(WaveInfo.Normal);
			}

			if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeDepth))
			{
				Result.SetWaterSurfaceDepth(Result.GetWaterSurfaceDepth() + WaveInfo.Height);
			}
		}

		if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeImmersionDepth))
		{
			check(EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeLocation));

			// Immersion depth indicates how much under the water surface is the world location. 
			//  therefore, it takes into account the waves if IncludeWaves is passed :
			Result.SetImmersionDepth(Result.GetWaterSurfaceLocation().Z - InWorldLocation.Z);
			// When in an exclusion volume, the queried location is considered out of water (immersion depth == 0.0f)
			check(!Result.IsInExclusionVolume() || (Result.GetImmersionDepth() == 0.0f));
		}

		// Compute velocity : 
		if (EnumHasAnyFlags(Result.GetQueryFlags(), EWaterBodyQueryFlags::ComputeVelocity))
		{
			FVector Velocity = FVector::ZeroVector;
			if (!Result.IsInExclusionVolume())
			{
				Velocity = WaterBody->GetWaterVelocityVectorAtSplineInputKey(LazilyComputeSplineKey(Result, *WaterBody, InWorldLocation));
			}

			Result.SetVelocity(Velocity);
		}

		return Result;
	}
#else
	static FWaterBodyQueryResult QueryWaterInfoClosestToWorldLocation(AWaterBody* WaterBody, const FVector& InWorldLocation, EWaterBodyQueryFlags InQueryFlags, const TOptional<float>& InSplineInputKey)
	{
		return WaterBody->GetWaterBodyComponent()->QueryWaterInfoClosestToWorldLocation(InWorldLocation, InQueryFlags, InSplineInputKey);
	}
#endif
};

int32 AWaterPhysics_WaterBody::GetWaterBodyPriority(AActor* InWaterBody) const
{
	return WaterBodies.IndexOfByPredicate([&](const FWaterBodySetup& X) { return X.WaterBody == InWaterBody; });
}

TArray<AActor*> AWaterPhysics_WaterBody::GetWaterBodies() const
{
	TArray<AActor*> OutActors;
	OutActors.Reserve(WaterBodies.Num());
	for (const FWaterBodySetup& WaterBodySetup : WaterBodies)
	{
		OutActors.Add(WaterBodySetup.WaterBody);
	}
	return OutActors;
}

FGetWaterInfoResult AWaterPhysics_WaterBody::CalculateWaterBodyWaterInfo(AActor* InWaterBody, const UActorComponent* Component, const FVector& Location) const
{
	check(IsValid(Component));
	AWaterBody* WaterBody = static_cast<AWaterBody*>(InWaterBody);

	EWaterBodyQueryFlags QueryFlags = EWaterBodyQueryFlags::ComputeLocation | EWaterBodyQueryFlags::ComputeNormal;

	const FWaterBodySetup* WaterBodySetup = WaterBodies.FindByPredicate([&](const auto& X) { return X.WaterBody == WaterBody; });
	check(WaterBodySetup);

	if (WaterBodySetup->bIncludeWaves)
		QueryFlags |= EWaterBodyQueryFlags::IncludeWaves;
	if (WaterBodySetup->bIncludeWaves && WaterBodySetup->bUseSimpleWaves)
		QueryFlags |= EWaterBodyQueryFlags::SimpleWaves;
	if (WaterBodySetup->bIncludeVelocity)
		QueryFlags |= EWaterBodyQueryFlags::ComputeVelocity;

	const FWaterBodyQueryResult QueryResult = FWaterBodyHack::QueryWaterInfoClosestToWorldLocation(WaterBody, Location, QueryFlags, TOptional<float>());

	return FGetWaterInfoResult{
		QueryResult.GetWaterSurfaceLocation(),
		QueryResult.GetWaterSurfaceNormal(),
		(int32)(QueryResult.GetQueryFlags() & EWaterBodyQueryFlags::ComputeVelocity) ? QueryResult.GetVelocity() : FVector::ZeroVector
	};
}