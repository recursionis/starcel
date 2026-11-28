// Copyright Mans Isaksson 2021. All Rights Reserved.

#pragma once
#include "DrawDebugHelpers.h"
#include "WaterPhysicsTypes.h"
#include "Core/Public/Stats/Stats2.h"

#if WITH_WATER_PHYS_DEBUG
#define EXEC_WITH_WATER_PHYS_DEBUG(Block) Block
#define EXEC_WITH_WATER_PHYS_DEBUG_ON_GAME_THREAD(Func) FFunctionGraphTask::CreateAndDispatchWhenReady(Func, TStatId(), nullptr, ENamedThreads::GameThread);
#else
#define EXEC_WITH_WATER_PHYS_DEBUG(Block)
#define EXEC_WITH_WATER_PHYS_DEBUG_ON_GAME_THREAD(Block)
#endif

#define USE_CUSTOM_DYNAMIC_EVENTS 0

#if STATS || ENABLE_STATNAMEDEVENTS

#if USE_CUSTOM_DYNAMIC_EVENTS
#define DYNAMIC_SCOPE_CYCLE_COUNTER(Stat, StatGroup, Format, ...) \
	FScopeCycleCounter ScopeCycleCounter_##Stat(FDynamicStats::CreateStatId<FStatGroup_##StatGroup>(FString(TEXT(#Stat)) + FString::Printf(TEXT(Format), __VA_ARGS__)));

#define DYNAMIC_QUICK_SCOPE_CYCLE_COUNTER(Stat, Format, ...) \
	DYNAMIC_SCOPE_CYCLE_COUNTER(Stat, STATGROUP_Quick, Format, __VA_ARGS__)
#else
#define DYNAMIC_SCOPE_CYCLE_COUNTER(Stat, StatGroup, Format, ...) SCOPE_CYCLE_COUNTER(Stat, StatGroup)
#define DYNAMIC_QUICK_SCOPE_CYCLE_COUNTER(Stat, Format, ...) QUICK_SCOPE_CYCLE_COUNTER(Stat)
#endif

#else
#define DYNAMIC_SCOPE_CYCLE_COUNTER(Stat, StatGroup, Format, ...)
#define DYNAMIC_QUICK_SCOPE_CYCLE_COUNTER(Stat, Format, ...)
#endif

template<typename TTriangle>
void DrawDebugTriangle(UWorld* World, const TTriangle &Triangle, bool bDrawNormal = false, const FColor& Color = FColor::Red, bool bPersistentLines = false, float LifeTime = -1.f, uint8 DepthPriority = 0, float Thickness = 0.f)
{
	DrawDebugLine(World, Triangle[0], Triangle[1], Color, bPersistentLines, LifeTime, DepthPriority, Thickness);
	DrawDebugLine(World, Triangle[1], Triangle[2], Color, bPersistentLines, LifeTime, DepthPriority, Thickness);
	DrawDebugLine(World, Triangle[2], Triangle[0], Color, bPersistentLines, LifeTime, DepthPriority, Thickness);

	if (bDrawNormal) 
	{
		const auto TriangleCenter = CalcTriangleCentroid(Triangle);
		const auto TriangleNormal = CalcTriangleNormal(Triangle);
		DrawDebugLine(World, TriangleCenter, TriangleCenter + TriangleNormal * 15.f, FColor::Blue, bPersistentLines, LifeTime, DepthPriority, Thickness);
	}
};