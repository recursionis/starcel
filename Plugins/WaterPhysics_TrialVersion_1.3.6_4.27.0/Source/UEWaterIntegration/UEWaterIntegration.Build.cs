// Copyright Mans Isaksson 2021. All Rights Reserved.

using UnrealBuildTool;

public class UEWaterIntegration : ModuleRules
{
    public UEWaterIntegration(ReadOnlyTargetRules Target) : base(Target)
    {
        bUsePrecompiled = true; // trial ships binaries only, no Private source
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "WaterPhysics",
            "Water",
            "Landscape"
        });
    }
}
