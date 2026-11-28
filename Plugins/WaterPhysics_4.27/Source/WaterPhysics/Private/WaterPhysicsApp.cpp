// Copyright Mans Isaksson 2021. All Rights Reserved.

#include "WaterPhysicsApp.h"
#include "Misc/App.h"

static int32 GIsTrialVersion = {
	#include "WaterPhysicsTrialVersion.inl"
};

bool FWaterPhysicsApp::IsTrialVersion()
{
	return GIsTrialVersion == 1;
}

bool FWaterPhysicsApp::CanUseWaterPhysicsPlugin()
{
	if (UNLIKELY(IsTrialVersion()))
		return FApp::GetBuildTargetType() == EBuildTargetType::Editor;
	else
		return true;
}