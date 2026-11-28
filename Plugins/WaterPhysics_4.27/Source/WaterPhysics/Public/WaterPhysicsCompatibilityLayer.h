// Copyright Mans Isaksson 2021. All Rights Reserved.

#pragma once
#include "Runtime/Launch/Resources/Version.h"

#define ENGINE_VERSION_HIGHER_THAN(Major, Minor) ENGINE_MAJOR_VERSION > Major || (ENGINE_MAJOR_VERSION == Major && ENGINE_MINOR_VERSION > Minor)

#define ENGINE_VERSION_LESS_THAN(Major, Minor) ENGINE_MAJOR_VERSION < Major || (ENGINE_MAJOR_VERSION == Major && ENGINE_MINOR_VERSION < Minor)

class UStaticMesh;
class UBodySetup;
class FStaticMeshRenderData;

namespace WaterPhysicsCompat
{
	WATERPHYSICS_API UBodySetup* GetStaticMeshBodySetup(UStaticMesh* Mesh);
	
	WATERPHYSICS_API FStaticMeshRenderData* GetStaticMeshRenderData(UStaticMesh* Mesh);

	template<typename T>
	void MarkObjectPendingKill(T* Object)
	{
#if ENGINE_VERSION_LESS_THAN(5, 0)
		Object->MarkPendingKill();
#else
		Object->MarkAsGarbage();
#endif
	}
};
