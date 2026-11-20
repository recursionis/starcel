#include "StarcelGameInstance.h"

#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/UnrealType.h"

DEFINE_LOG_CATEGORY_STATIC(LogStarcelGameInstance, Log, All);

namespace
{
	// PyActor lives in the UnrealEnginePython plugin. Its properties are set through reflection
	// so this module does not need to link against the plugin or include the Python headers.
	FStrProperty* FindStrProp(UClass* Class, const TCHAR* Name)
	{
		return FindFProperty<FStrProperty>(Class, Name);
	}

	FString GetStrProp(UObject* Obj, const TCHAR* Name)
	{
		if (FStrProperty* Prop = FindStrProp(Obj->GetClass(), Name))
		{
			return Prop->GetPropertyValue_InContainer(Obj);
		}
		return FString();
	}
}

UStarcelGameInstance::UStarcelGameInstance()
	: bSpawnMainActor(true)
	, MainActorClass(FSoftObjectPath(TEXT("/Game/Blueprints/Assets/BP_PyActor.BP_PyActor_C")))
	, MainPythonModule(TEXT("main"))
	, MainPythonClass(TEXT("Main"))
	, bSkipIfAlreadyPresent(true)
{
}

void UStarcelGameInstance::Init()
{
	Super::Init();

	// Fires for every world after its actors are initialized and before BeginPlay is dispatched:
	// the startup map, every OpenLevel/ServerTravel, and PIE sessions.
	WorldInitHandle = FWorldDelegates::OnWorldInitializedActors.AddUObject(
		this, &UStarcelGameInstance::HandleWorldInitializedActors);
}

void UStarcelGameInstance::Shutdown()
{
	FWorldDelegates::OnWorldInitializedActors.Remove(WorldInitHandle);
	WorldInitHandle.Reset();
	Super::Shutdown();
}

void UStarcelGameInstance::HandleWorldInitializedActors(const UWorld::FActorsInitializedParams& Params)
{
	if (!bSpawnMainActor)
	{
		return;
	}

	UWorld* World = Params.World;

	// Only worlds owned by this game instance (ignores editor preview worlds, other PIE instances, etc.)
	if (!World || !World->IsGameWorld() || World->GetGameInstance() != this)
	{
		return;
	}

	SpawnMainActor(World);
}

AActor* UStarcelGameInstance::SpawnMainActor(UWorld* World)
{
	UClass* Class = MainActorClass.LoadSynchronous();
	if (!Class)
	{
		UE_LOG(LogStarcelGameInstance, Error, TEXT("MainActorClass '%s' could not be loaded"),
			*MainActorClass.ToString());
		return nullptr;
	}

	FStrProperty* ModuleProp = FindStrProp(Class, TEXT("PythonModule"));
	FStrProperty* ClassProp = FindStrProp(Class, TEXT("PythonClass"));
	if (!ModuleProp || !ClassProp)
	{
		UE_LOG(LogStarcelGameInstance, Error, TEXT("%s has no PythonModule/PythonClass properties (not a PyActor?)"),
			*Class->GetName());
		return nullptr;
	}

	if (bSkipIfAlreadyPresent)
	{
		// Scene maps (StaringAtSky, PineTree, RiceMap, ...) are driven by a placed
		// BP_PyActorEmpty running their own maps.<scene>.pyactor_main module. Those
		// maps don't have the main level's sky/fog/lights, so main.Main stays out.
		static const TSoftClassPtr<AActor> MapControllerClassPtr(
			FSoftObjectPath(TEXT("/Game/Blueprints/Assets/BP_PyActorEmpty.BP_PyActorEmpty_C")));
		UClass* MapControllerClass = MapControllerClassPtr.LoadSynchronous();

		// Check every actor, not just MainActorClass: BP_PyActorEmpty is not a
		// subclass of BP_PyActor, but it is still a PyActor.
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!FindStrProp(It->GetClass(), TEXT("PythonModule")))
			{
				continue;  // not a PyActor
			}

			const FString Module = GetStrProp(*It, TEXT("PythonModule"));
			const FString PyClass = GetStrProp(*It, TEXT("PythonClass"));

			if (Module == MainPythonModule && PyClass == MainPythonClass)
			{
				UE_LOG(LogStarcelGameInstance, Log, TEXT("Map %s already has %s.%s actor (%s), not spawning"),
					*World->GetMapName(), *MainPythonModule, *MainPythonClass, *It->GetName());
				MainActor = *It;
				return *It;
			}

			if (MapControllerClass && It->IsA(MapControllerClass) && !Module.IsEmpty())
			{
				UE_LOG(LogStarcelGameInstance, Log, TEXT("Map %s has its own controller %s (%s.%s), not spawning %s.%s"),
					*World->GetMapName(), *It->GetName(), *Module, *PyClass, *MainPythonModule, *MainPythonClass);
				return nullptr;
			}
		}
	}

	// Deferred spawn: PyActor imports its Python module in PreInitializeComponents(),
	// so PythonModule/PythonClass must be set before FinishSpawning.
	AActor* Actor = World->SpawnActorDeferred<AActor>(Class, FTransform::Identity, nullptr, nullptr,
		ESpawnActorCollisionHandlingMethod::AlwaysSpawn);
	if (!Actor)
	{
		UE_LOG(LogStarcelGameInstance, Error, TEXT("Failed to spawn %s in %s"), *Class->GetName(), *World->GetMapName());
		return nullptr;
	}

	ModuleProp->SetPropertyValue_InContainer(Actor, MainPythonModule);
	ClassProp->SetPropertyValue_InContainer(Actor, MainPythonClass);
	UGameplayStatics::FinishSpawningActor(Actor, FTransform::Identity);

	UE_LOG(LogStarcelGameInstance, Log, TEXT("Spawned %s (%s.%s) in %s"),
		*Actor->GetName(), *MainPythonModule, *MainPythonClass, *World->GetMapName());

	MainActor = Actor;
	return Actor;
}
