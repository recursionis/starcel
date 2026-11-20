#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "StarcelPakLoader.generated.h"

/**
 * Loads maps from .pak files at runtime, including paks that were packaged
 * from a *different* project (e.g. a full "StarcelMapTest1-WindowsNoEditor.pak").
 *
 * Such a pak stores its files as "<OtherProject>/Content/...", but its assets
 * reference each other as /Game/..., which in this game resolves to
 * "Starcel9/Content/...". To bridge that, the pak is mounted at a private,
 * hidden root and a small platform-file layer redirects any /Game (and /Engine)
 * file that the base game does NOT have to the matching file inside the pak.
 * Base-game files always win.
 *
 * Only works in a packaged (cooked) build - the editor cannot load cooked content.
 */
UCLASS()
class STARCEL9_API UStarcelPakLoader : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/**
	 * Mount a pak so its content becomes loadable under /Game/.
	 * @param PakFilePath           Absolute path to the .pak file.
	 * @param OutMapPackageNames    Maps found in the pak, as package names like "/Game/MapTest1".
	 * @return true if the pak is mounted (also true if it was already mounted).
	 */
	UFUNCTION(BlueprintCallable, Category = "Starcel|Pak")
	static bool MountMapPak(const FString& PakFilePath, TArray<FString>& OutMapPackageNames);

	/**
	 * Mount a pak (if needed) and travel to one of its maps.
	 * @param MapName   "MapTest1", "/Game/MapTest1" or "/Game/Maps/SunTemple". Empty = first map found.
	 */
	UFUNCTION(BlueprintCallable, Category = "Starcel|Pak", meta = (WorldContext = "WorldContextObject"))
	static bool MountPakAndOpenMap(UObject* WorldContextObject, const FString& PakFilePath, const FString& MapName);
};
