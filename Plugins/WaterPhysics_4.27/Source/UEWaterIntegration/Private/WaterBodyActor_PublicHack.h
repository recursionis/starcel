// Copyright Mans Isaksson 2021. All Rights Reserved.

// HUGE HACK: Epic's implementation of QueryWaterInfoClosestToWorldLocation is increadibly slow
// and doesn't support parallel queries. However, most functions required to create our own implmentation are private/protected inside AWaterBody.
// This is a terrible soulution and would normally be unacceptable, however the difference in performance is staggering and leads me to make the
// difficult choice of including this hack in the final product.

// We first include the includes of WaterBodyActor and WaterSubsystem manually to ensure they are not affected
// by our inclusion hack

// WaterBodyActor.h Includes
#include "GameFramework/Actor.h"
#include "Engine/Scene.h"
#include "TerrainCarvingSettings.h"
#include "WaterBrushActorInterface.h"
#include "WaterBodyWeightmapSettings.h"
#include "WaterBodyHeightmapSettings.h"
#include "WaterCurveSettings.h"
#include "WaterSplineMetadata.h"
#include "NavAreas/NavArea.h"
#include "AI/Navigation/NavRelevantInterface.h"
#include "Interfaces/Interface_PostProcessVolume.h"
#include "WaterWaves.h"

// WaterSubsystem.h Includes
#include "UObject/ObjectMacros.h"
#include "Subsystems/WorldSubsystem.h"
#include "Engine/EngineTypes.h"
#include "Engine/Public/Tickable.h"
#include "Interfaces/Interface_PostProcessVolume.h"
#include "WaterBodyManager.h"

#define private friend class FWaterBodyHack; private
#define protected friend class FWaterBodyHack; protected
#include "WaterBodyActor.h"
#include "WaterSubsystem.h"
#undef private
#undef protected