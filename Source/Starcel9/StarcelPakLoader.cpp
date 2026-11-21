#include "StarcelPakLoader.h"

#include "HAL/PlatformFilemanager.h"
#include "IPlatformFilePak.h"
#include "Misc/Paths.h"
#include "Misc/ScopeRWLock.h"
#include "ShaderCodeLibrary.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "HAL/IConsoleManager.h"
#include "Misc/CoreDelegates.h"
#include "Misc/CommandLine.h"
#include "Misc/DelayedAutoRegister.h"

DEFINE_LOG_CATEGORY_STATIC(LogStarcelPak, Log, All);

namespace StarcelPak
{
	static FString Normalize(const TCHAR* In)
	{
		FString P(In);
		FPaths::NormalizeFilename(P);
		return P;
	}

	/** Strips Prefix (relative or absolute form) from Path. */
	static bool StripPrefix(const FString& Path, const FString& RelPrefix, const FString& FullPrefix, FString& OutRest)
	{
		if (Path.StartsWith(RelPrefix, ESearchCase::IgnoreCase))
		{
			OutRest = Path.RightChop(RelPrefix.Len());
			return true;
		}
		if (Path.StartsWith(FullPrefix, ESearchCase::IgnoreCase))
		{
			OutRest = Path.RightChop(FullPrefix.Len());
			return true;
		}
		return false;
	}

	static FString FullDir(const FString& RelDir)
	{
		FString Full = FPaths::ConvertRelativePathToFull(RelDir);
		FPaths::NormalizeDirectoryName(Full);
		return Full + TEXT("/");
	}

	/**
	 * Sits on top of the platform-file chain. Paks are mounted at a hidden root
	 * ("../../../_StarcelMods/<PakName>/") so they can never shadow base-game files.
	 * Requests for base-game content dirs that the base game lacks are redirected
	 * into the matching folder inside the hidden root.
	 */
	class FStarcelModPlatformFile : public IPlatformFile
	{
	public:
		struct FRedirect
		{
			FString From;     // e.g. "../../../Starcel9/Content/"
			FString FromFull; // absolute form of From
			FString To;       // e.g. "../../../_StarcelMods/X/StarcelMapTest1/Content/"
		};

		IPlatformFile* Lower = nullptr;
		FPakPlatformFile* Pak = nullptr;
		IPlatformFile* PakIF = nullptr; // same object, via the interface (avoids overload hiding)
		bool bOwnsPak = false;
		FString HiddenRoot;     // "../../../_StarcelMods/"
		FString HiddenRootFull;

		void AddRedirect(const FString& From, const FString& To)
		{
			FWriteScopeLock Lock(RedirectLock);
			Redirects.Add({ From, FullDir(From), To });
		}

		// --- resolution ---------------------------------------------------------

		/** Returns true (and the in-pak path) if Filename should be served from a mod pak. */
		bool Resolve(const TCHAR* Filename, FString& Out, bool bDirectory = false)
		{
			const FString P = Normalize(Filename);
			FString Rest;
			if (StripPrefix(P, HiddenRoot, HiddenRootFull, Rest))
			{
				Out = HiddenRoot + Rest;
				return true;
			}

			FReadScopeLock Lock(RedirectLock);
			// Newest mods first.
			for (int32 i = Redirects.Num() - 1; i >= 0; --i)
			{
				const FRedirect& R = Redirects[i];
				if (!StripPrefix(P, R.From, R.FromFull, Rest))
				{
					continue;
				}
				const FString Candidate = R.To + Rest;
				const bool bInPak = bDirectory ? PakIF->DirectoryExists(*Candidate) : Pak->FindFileInPakFiles(*Candidate);
				if (!bInPak)
				{
					continue;
				}
				// Base game always wins.
				if (bDirectory ? Lower->DirectoryExists(Filename) : Lower->FileExists(Filename))
				{
					return false;
				}
				Out = Candidate;
				return true;
			}
			return false;
		}

		// --- IPlatformFile ------------------------------------------------------

		virtual bool Initialize(IPlatformFile* Inner, const TCHAR* CmdLine) override { Lower = Inner; return Lower != nullptr; }
		virtual IPlatformFile* GetLowerLevel() override { return Lower; }
		virtual void SetLowerLevel(IPlatformFile* NewLowerLevel) override { Lower = NewLowerLevel; }
		virtual const TCHAR* GetName() const override { return TEXT("StarcelModRedirect"); }

		virtual void Tick() override
		{
			Lower->Tick();
			if (bOwnsPak) { PakIF->Tick(); }
		}
		virtual void SetAsyncMinimumPriority(EAsyncIOPriorityAndFlags MinPriority) override
		{
			Lower->SetAsyncMinimumPriority(MinPriority);
			if (bOwnsPak) { PakIF->SetAsyncMinimumPriority(MinPriority); }
		}
		virtual void BypassSecurity(bool bInBypass) override { Lower->BypassSecurity(bInBypass); }
		virtual void AddLocalDirectories(TArray<FString>& LocalDirectories) override { Lower->AddLocalDirectories(LocalDirectories); }
		virtual bool SendMessageToServer(const TCHAR* Message, IFileServerMessageHandler* Handler) override { return Lower->SendMessageToServer(Message, Handler); }
		virtual bool DoesCreatePublicFiles() override { return Lower->DoesCreatePublicFiles(); }
		virtual void SetCreatePublicFiles(bool bCreatePublicFiles) override { Lower->SetCreatePublicFiles(bCreatePublicFiles); }


		virtual bool FileExists(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->FileExists(*R); } return Lower->FileExists(Filename);
		}
		virtual int64 FileSize(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->FileSize(*R); } return Lower->FileSize(Filename);
		}
		virtual bool IsReadOnly(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return true; } return Lower->IsReadOnly(Filename);
		}
		virtual FDateTime GetTimeStamp(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->GetTimeStamp(*R); } return Lower->GetTimeStamp(Filename);
		}
		virtual FDateTime GetAccessTimeStamp(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->GetAccessTimeStamp(*R); } return Lower->GetAccessTimeStamp(Filename);
		}
		virtual FString GetFilenameOnDisk(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return Filename; } return Lower->GetFilenameOnDisk(Filename);
		}
		virtual IFileHandle* OpenRead(const TCHAR* Filename, bool bAllowWrite) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->OpenRead(*R, false); } return Lower->OpenRead(Filename, bAllowWrite);
		}
		virtual IFileHandle* OpenReadNoBuffering(const TCHAR* Filename, bool bAllowWrite) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->OpenReadNoBuffering(*R, false); } return Lower->OpenReadNoBuffering(Filename, bAllowWrite);
		}
		virtual IAsyncReadFileHandle* OpenAsyncRead(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->OpenAsyncRead(*R); } return Lower->OpenAsyncRead(Filename);
		}
		virtual IMappedFileHandle* OpenMapped(const TCHAR* Filename) override
		{
			FString R; if (Resolve(Filename, R)) { return PakIF->OpenMapped(*R); } return Lower->OpenMapped(Filename);
		}
		virtual FFileStatData GetStatData(const TCHAR* FilenameOrDirectory) override
		{
			FString R;
			if (Resolve(FilenameOrDirectory, R) || Resolve(FilenameOrDirectory, R, true)) { return PakIF->GetStatData(*R); }
			return Lower->GetStatData(FilenameOrDirectory);
		}
		virtual bool DirectoryExists(const TCHAR* Directory) override
		{
			FString R; if (Resolve(Directory, R, true)) { return PakIF->DirectoryExists(*R); } return Lower->DirectoryExists(Directory);
		}
		virtual bool IterateDirectory(const TCHAR* Directory, FDirectoryVisitor& Visitor) override
		{
			FString R; if (Resolve(Directory, R, true)) { return PakIF->IterateDirectory(*R, Visitor); } return Lower->IterateDirectory(Directory, Visitor);
		}
		virtual bool IterateDirectoryStat(const TCHAR* Directory, FDirectoryStatVisitor& Visitor) override
		{
			FString R; if (Resolve(Directory, R, true)) { return PakIF->IterateDirectoryStat(*R, Visitor); } return Lower->IterateDirectoryStat(Directory, Visitor);
		}
		virtual bool IterateDirectoryRecursively(const TCHAR* Directory, FDirectoryVisitor& Visitor) override
		{
			FString R; if (Resolve(Directory, R, true)) { return PakIF->IterateDirectoryRecursively(*R, Visitor); } return Lower->IterateDirectoryRecursively(Directory, Visitor);
		}
		virtual bool IterateDirectoryStatRecursively(const TCHAR* Directory, FDirectoryStatVisitor& Visitor) override
		{
			FString R; if (Resolve(Directory, R, true)) { return PakIF->IterateDirectoryStatRecursively(*R, Visitor); } return Lower->IterateDirectoryStatRecursively(Directory, Visitor);
		}

		// Writes always go to the real file system.
		virtual bool DeleteFile(const TCHAR* Filename) override { return Lower->DeleteFile(Filename); }
		virtual bool MoveFile(const TCHAR* To, const TCHAR* From) override { return Lower->MoveFile(To, From); }
		virtual bool SetReadOnly(const TCHAR* Filename, bool bNewReadOnlyValue) override { return Lower->SetReadOnly(Filename, bNewReadOnlyValue); }
		virtual void SetTimeStamp(const TCHAR* Filename, FDateTime DateTime) override { Lower->SetTimeStamp(Filename, DateTime); }
		virtual IFileHandle* OpenWrite(const TCHAR* Filename, bool bAppend, bool bAllowRead) override { return Lower->OpenWrite(Filename, bAppend, bAllowRead); }
		virtual bool CreateDirectory(const TCHAR* Directory) override { return Lower->CreateDirectory(Directory); }
		virtual bool DeleteDirectory(const TCHAR* Directory) override { return Lower->DeleteDirectory(Directory); }


	private:
		FRWLock RedirectLock;
		TArray<FRedirect> Redirects;
	};

	static FStarcelModPlatformFile* GModFile = nullptr;
	static TMap<FString, TArray<FString>> GMountedPaks; // pak path -> map package names

	/** Installs the redirect layer (and a pak reader if the game has none). */
	static FStarcelModPlatformFile* GetOrCreateModFile()
	{
		if (GModFile)
		{
			return GModFile;
		}

		FPlatformFileManager& Manager = FPlatformFileManager::Get();
		IPlatformFile* Top = &Manager.GetPlatformFile();

		FPakPlatformFile* Pak = static_cast<FPakPlatformFile*>(Manager.FindPlatformFile(FPakPlatformFile::GetTypeName()));
		bool bOwnsPak = false;
		if (!Pak)
		{
			// The game is packaged as loose files (UsePakFile=False), so there is no pak reader.
			// Create a private one that is NOT inserted into the chain: once it has a pak mounted
			// it would block loose .uasset/.umap reads for the whole game.
			Pak = new FPakPlatformFile();
			if (!Pak->Initialize(Top, TEXT("")))
			{
				UE_LOG(LogStarcelPak, Error, TEXT("Failed to initialize pak platform file."));
				delete Pak;
				return nullptr;
			}
			Pak->InitializeNewAsyncIO();
			bOwnsPak = true;
		}

		FStarcelModPlatformFile* ModFile = new FStarcelModPlatformFile();
		ModFile->Initialize(Top, TEXT(""));
		ModFile->Pak = Pak;
		ModFile->PakIF = Pak;
		ModFile->bOwnsPak = bOwnsPak;

		// Parent of Engine/, e.g. "../../../". (CollapseRelativeDirectories can't be used: it rejects
		// paths starting with "..", and an uncollapsed mount point never matches the pak's
		// normalized directory lookups.)
		FString EngineDir = FPaths::EngineDir();
		FPaths::NormalizeDirectoryName(EngineDir); // strips trailing '/'
		const FString Root = FPaths::GetPath(EngineDir);
		ModFile->HiddenRoot = Root + TEXT("/_StarcelMods/");
		ModFile->HiddenRootFull = FullDir(ModFile->HiddenRoot);

		Manager.SetPlatformFile(*ModFile);
		GModFile = ModFile;
		UE_LOG(LogStarcelPak, Log, TEXT("Installed mod redirect layer (own pak reader: %d)."), bOwnsPak ? 1 : 0);
		return GModFile;
	}

	static FString ToMapPackageName(const FString& MapName, const TArray<FString>& Maps)
	{
		if (MapName.IsEmpty())
		{
			return Maps.Num() > 0 ? Maps[0] : FString();
		}
		if (MapName.StartsWith(TEXT("/")))
		{
			return MapName;
		}
		for (const FString& M : Maps)
		{
			if (FPackageName::GetShortName(M).Equals(MapName, ESearchCase::IgnoreCase))
			{
				return M;
			}
		}
		return TEXT("/Game/") + MapName;
	}
}

bool UStarcelPakLoader::MountMapPak(const FString& PakFilePath, TArray<FString>& OutMapPackageNames)
{
	using namespace StarcelPak;
	OutMapPackageNames.Reset();

#if WITH_EDITOR
	if (GIsEditor)
	{
		UE_LOG(LogStarcelPak, Error, TEXT("MountMapPak only works in a packaged build; the editor can't load cooked content."));
		return false;
	}
#endif

	FString PakPath = FPaths::ConvertRelativePathToFull(PakFilePath);
	FPaths::NormalizeFilename(PakPath);

	if (const TArray<FString>* Existing = GMountedPaks.Find(PakPath))
	{
		OutMapPackageNames = *Existing;
		return true;
	}

	if (!FPaths::FileExists(PakPath))
	{
		UE_LOG(LogStarcelPak, Error, TEXT("Pak not found: %s"), *PakPath);
		return false;
	}

	FStarcelModPlatformFile* ModFile = GetOrCreateModFile();
	if (!ModFile)
	{
		return false;
	}

	// Each pak gets its own hidden mount point so its Engine/ and Config/ files never shadow ours.
	const FString PakId = FPaths::GetBaseFilename(PakPath);
	const FString MountPoint = ModFile->HiddenRoot + PakId + TEXT("/");
	if (!ModFile->Pak->Mount(*PakPath, 1000, *MountPoint))
	{
		UE_LOG(LogStarcelPak, Error, TEXT("Failed to mount pak: %s"), *PakPath);
		return false;
	}
	UE_LOG(LogStarcelPak, Log, TEXT("Mounted %s at %s"), *PakPath, *MountPoint);

	// Find the project folder inside the pak: the top-level dir with a Content/ folder that isn't Engine/.
	TArray<FString> ProjectDirs;
	ModFile->PakIF->IterateDirectory(*MountPoint, [&ProjectDirs](const TCHAR* Path, bool bIsDir)
	{
		if (bIsDir)
		{
			ProjectDirs.Add(Normalize(Path));
		}
		return true;
	});

	// Fallback: "<Project>-WindowsNoEditor.pak" -> "<Project>".
	FString NameFromPak = PakId;
	int32 DashIdx;
	if (NameFromPak.FindLastChar(TEXT('-'), DashIdx))
	{
		NameFromPak = NameFromPak.Left(DashIdx);
	}
	ProjectDirs.Add(MountPoint + NameFromPak);

	FString ModProjectDir;
	for (FString Dir : ProjectDirs)
	{
		FPaths::NormalizeDirectoryName(Dir);
		const FString Name = FPaths::GetCleanFilename(Dir);
		if (!Name.Equals(TEXT("Engine"), ESearchCase::IgnoreCase) && ModFile->PakIF->DirectoryExists(*(Dir / TEXT("Content"))))
		{
			ModProjectDir = Dir + TEXT("/");
			break;
		}
	}

	if (ModProjectDir.IsEmpty())
	{
		UE_LOG(LogStarcelPak, Error, TEXT("No <Project>/Content folder found in %s (looked at:%s)"), *PakPath,
			*FString::JoinBy(ProjectDirs, TEXT(""), [](const FString& D) { return TEXT(" ") + D; }));
		ModFile->Pak->Unmount(*PakPath); // so a retry starts clean
		return false;
	}
	UE_LOG(LogStarcelPak, Log, TEXT("Pak content folder: %s"), *ModProjectDir);

	const FString ModContentDir = ModProjectDir + TEXT("Content/");
	const FString ModProjectName = FPaths::GetCleanFilename(ModProjectDir.LeftChop(1));

	// /Game/... -> <ModProject>/Content/..., and /Engine/... -> pak's Engine/Content/... (only for files we lack).
	ModFile->AddRedirect(FPaths::ProjectContentDir(), ModContentDir);
	ModFile->AddRedirect(FPaths::EngineContentDir(), MountPoint + TEXT("Engine/Content/"));

	// Materials in the pak need its shader library.
	if (!FShaderCodeLibrary::OpenLibrary(ModProjectName, ModContentDir))
	{
		UE_LOG(LogStarcelPak, Warning, TEXT("No shader library '%s' in pak (materials may render with default shaders)."), *ModProjectName);
	}

	// List maps.
	TArray<FString> MapFiles;
	ModFile->PakIF->FindFilesRecursively(MapFiles, *ModContentDir, TEXT(".umap"));
	for (FString MapFile : MapFiles)
	{
		FPaths::NormalizeFilename(MapFile);
		if (MapFile.StartsWith(ModContentDir, ESearchCase::IgnoreCase))
		{
			const FString Rel = FPaths::ChangeExtension(MapFile.RightChop(ModContentDir.Len()), TEXT(""));
			OutMapPackageNames.Add(TEXT("/Game/") + Rel);
		}
	}
	OutMapPackageNames.Sort();

	UE_LOG(LogStarcelPak, Log, TEXT("Pak project '%s' has %d map(s):"), *ModProjectName, OutMapPackageNames.Num());
	for (const FString& M : OutMapPackageNames)
	{
		UE_LOG(LogStarcelPak, Log, TEXT("  %s"), *M);
	}

	GMountedPaks.Add(PakPath, OutMapPackageNames);
	return true;
}

bool UStarcelPakLoader::MountPakAndOpenMap(UObject* WorldContextObject, const FString& PakFilePath, const FString& MapName)
{
	TArray<FString> Maps;
	if (!MountMapPak(PakFilePath, Maps))
	{
		return false;
	}

	const FString MapPackage = StarcelPak::ToMapPackageName(MapName, Maps);
	if (MapPackage.IsEmpty() || !FPackageName::DoesPackageExist(MapPackage))
	{
		UE_LOG(LogStarcelPak, Error, TEXT("Map '%s' not found in mounted content."), *MapPackage);
		return false;
	}

	UE_LOG(LogStarcelPak, Log, TEXT("Opening %s"), *MapPackage);
	UGameplayStatics::OpenLevel(WorldContextObject, FName(*MapPackage));
	return true;
}

// Command line: Starcel9.exe [MapName] -ModPak="C:/path/to/File.pak"
// Mounts the pak before the startup map loads. If the first argument is a short map name
// that exists in the pak (e.g. "SunTemple"), it is rewritten to its full path ("/Game/Maps/SunTemple").
namespace StarcelPak
{
	static void MountFromCommandLine()
	{
		if (GIsEditor)
		{
			return;
		}

		FString PakPath;
		if (!FParse::Value(FCommandLine::Get(), TEXT("ModPak="), PakPath, false))
		{
			return;
		}
		PakPath = PakPath.TrimQuotes();

		TArray<FString> Maps;
		if (!UStarcelPakLoader::MountMapPak(PakPath, Maps))
		{
			return;
		}

		// First token is the startup map, unless it's a switch.
		const TCHAR* Cmd = FCommandLine::Get();
		const TCHAR* Rest = Cmd;
		FString FirstToken;
		if (!FParse::Token(Rest, FirstToken, false) || FirstToken.IsEmpty() || FirstToken[0] == TEXT('-'))
		{
			return;
		}

		FString MapPart = FirstToken;
		FString Options;
		int32 OptIdx;
		if (MapPart.FindChar(TEXT('?'), OptIdx))
		{
			Options = MapPart.Mid(OptIdx);
			MapPart = MapPart.Left(OptIdx);
		}
		if (MapPart.StartsWith(TEXT("/")))
		{
			return; // already a long package name
		}

		for (const FString& M : Maps)
		{
			if (FPackageName::GetShortName(M).Equals(MapPart, ESearchCase::IgnoreCase))
			{
				const FString NewCmd = M + Options + Rest;
				UE_LOG(LogStarcelPak, Log, TEXT("Startup map '%s' -> '%s'"), *MapPart, *M);
				FCommandLine::Set(*NewCmd);
				return;
			}
		}
		UE_LOG(LogStarcelPak, Warning, TEXT("Startup map '%s' is not in the mod pak; leaving it unchanged."), *MapPart);
	}
}

// Runs after GEngine->Init() and before GEngine->Start() loads the startup map.
static FDelayedAutoRegisterHelper GStarcelModPakStartup(EDelayedRegisterRunPhase::ObjectSystemReady, []
{
	FCoreDelegates::OnPostEngineInit.AddStatic(&StarcelPak::MountFromCommandLine);
});

// Console: Starcel.LoadPakMap "C:/path/to/File.pak" [MapName]
static FAutoConsoleCommandWithWorldAndArgs GStarcelLoadPakMapCmd(
	TEXT("Starcel.LoadPakMap"),
	TEXT("Mount a .pak and open a map from it. Usage: Starcel.LoadPakMap <PakPath> [MapName]"),
	FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args, UWorld* World)
	{
		if (Args.Num() < 1)
		{
			UE_LOG(LogStarcelPak, Warning, TEXT("Usage: Starcel.LoadPakMap <PakPath> [MapName]"));
			return;
		}
		UStarcelPakLoader::MountPakAndOpenMap(World, Args[0].TrimQuotes(), Args.Num() > 1 ? Args[1] : FString());
	}));
