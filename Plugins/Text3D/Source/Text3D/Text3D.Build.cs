// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Text3D : ModuleRules
{
	public Text3D(ReadOnlyTargetRules Target) : base(Target)
	{
		bEnableExceptions = true;
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
		});

		PrivateDependencyModuleNames.AddRange(new string[] {
           "FreeType2",
            "GeometricObjects",
			"GeometryAlgorithms",
            "HarfBuzz",
            "ICU",
            "MeshDescription",
			"SlateCore",
			"StaticMeshDescription",
		});

		// The engine's FreeType2 2.10 lib needs libpng + zlib for bitmap fonts, but FreeType2.Build.cs
		// only adds them when the engine is built from source/monolithic. With an installed (launcher)
		// engine, a project-side copy of Text3D has to link them itself or it fails with png_*/inflate
		// unresolved externals.
		AddEngineThirdPartyPrivateStaticDependencies(Target, "zlib", "UElibPNG");
	}
}
