@echo off
REM Install boost-multiprecision + mpfr via vcpkg with a properly-set MSVC env.
REM Uses our pinned _setupenv.bat (since vswhere isn't on this machine's PATH).

call "%~dp0_setupenv.bat"

REM Tell vcpkg + CMake where the compiler is.
set "CC=cl.exe"
set "CXX=cl.exe"

echo === PATH includes MSVC?
where cl.exe
echo === Running C:\vcpkg\vcpkg.exe install ===
C:\vcpkg\vcpkg.exe install boost-multiprecision:x64-windows mpfr:x64-windows
exit /b %ERRORLEVEL%
