// Fill out your copyright notice in the Description page of Project Settings.


#include "HandDriverBPLibrary.h"
#include "ILiveLinkClient.h"
#include "LiveLinkClient.h"
#include "LiveLinkClientReference.h"
#include "HandDriverSourceFactory.h"

void UHandDriverBPLibrary::CreateSourceRuntime( const FString& ConnectionString, FLiveLinkSourceHandle& Handle )
{
	// Was: while(true){...} with no exit condition -> hung the editor whenever the
	// connection string failed to parse. Now we bail out cleanly instead.
	TSharedPtr<ILiveLinkSource> NewSource = UHandDriverSourceFactory::CreateSourceAtRuntime( ConnectionString );
	if (!NewSource.IsValid())
	{
		UE_LOG(LogTemp, Warning, TEXT("[HandDriver] CreateSourceRuntime: invalid connection string '%s' (expected e.g. 0.0.0.0:5555)"), *ConnectionString);
		return;
	}
	FLiveLinkClientReference ClientRef;
	if (ILiveLinkClient* Client = ClientRef.GetClient())
	{
		Client->AddSource( NewSource );
	}
	Handle = FLiveLinkSourceHandle();
	Handle.SetSourcePointer( NewSource );
}
