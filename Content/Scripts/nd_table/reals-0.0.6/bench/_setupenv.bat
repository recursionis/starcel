@echo off
REM Reusable MSVC env block — works without vswhere.exe by pinning known paths.
REM Adjust toolset / SDK versions here if your install differs.

set "MSVC=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.29.30133"
set "SDK=C:\Program Files (x86)\Windows Kits\10"
set "SDKV=10.0.19041.0"

set "PATH=%MSVC%\bin\HostX64\x64;%SDK%\bin\%SDKV%\x64;%PATH%"
set "INCLUDE=%MSVC%\include;%SDK%\Include\%SDKV%\ucrt;%SDK%\Include\%SDKV%\shared;%SDK%\Include\%SDKV%\um;%SDK%\Include\%SDKV%\winrt"
set "LIB=%MSVC%\lib\x64;%SDK%\Lib\%SDKV%\ucrt\x64;%SDK%\Lib\%SDKV%\um\x64"
