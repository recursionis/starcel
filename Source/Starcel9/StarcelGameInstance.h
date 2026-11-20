#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "StarcelGameInstance.generated.h"

/**
 * Game instance that spawns a "main" PyActor into every game world that loads
 * (initial map, OpenLevel / ServerTravel, PIE).
 *
 * Defaults: BP_PyActor with PythonModule="main", PythonClass="Main".
 * All three are config properties, so they can be overridden in DefaultGame.ini under
 * [/Script/Starcel9.StarcelGameInstance] or in a Blueprint subclass.
 */
UCLASS(Config = Game)
class STARCEL9_API UStarcelGameInstance : public UGameInstance
{
	GENERATED_BODY()

public:
	UStarcelGameInstance();

	virtual void Init() override;
	virtual void Shutdown() override;

	/** Master switch: when false, no main actor is spawned on map load. */
	UPROPERTY(Config, EditDefaultsOnly, BlueprintReadOnly, Category = "Starcel|Main Actor")
	bool bSpawnMainActor;

	/** Actor class to spawn on every map load. Must be (a subclass of) APyActor. */
	UPROPERTY(Config, EditDefaultsOnly, BlueprintReadOnly, Category = "Starcel|Main Actor")
	TSoftClassPtr<AActor> MainActorClass;

	UPROPERTY(Config, EditDefaultsOnly, BlueprintReadOnly, Category = "Starcel|Main Actor")
	FString MainPythonModule;

	UPROPERTY(Config, EditDefaultsOnly, BlueprintReadOnly, Category = "Starcel|Main Actor")
	FString MainPythonClass;

	/** If a PyActor with the same module/class is already placed in the map, don't spawn another. */
	UPROPERTY(Config, EditDefaultsOnly, BlueprintReadOnly, Category = "Starcel|Main Actor")
	bool bSkipIfAlreadyPresent;

	/** The main actor spawned for the current map (null between maps). */
	UFUNCTION(BlueprintPure, Category = "Starcel|Main Actor")
	AActor* GetMainActor() const { return MainActor.Get(); }

private:
	void HandleWorldInitializedActors(const UWorld::FActorsInitializedParams& Params);
	AActor* SpawnMainActor(UWorld* World);

	FDelegateHandle WorldInitHandle;
	TWeakObjectPtr<AActor> MainActor;
};
