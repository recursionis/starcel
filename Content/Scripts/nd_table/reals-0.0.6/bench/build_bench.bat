@echo off
REM Build bench_boost_mpfr.exe with MSVC + vcpkg-installed Boost/MPFR.
REM Prereqs:
REM   - VS 2022 with C++ workload
REM   - install_via_vcpkg.bat already run successfully (Boost + MPFR installed)
REM Usage:
REM   build_bench.bat

cd /d "%~dp0"
call "%~dp0_setupenv.bat"

if not exist C:\vcpkg\installed\x64-windows\include\boost\multiprecision\mpfr.hpp (
    echo Boost+MPFR headers not found at C:\vcpkg\installed\x64-windows\.
    echo Run install_via_vcpkg.bat first ^(from a Developer Command Prompt^).
    exit /b 1
)

echo === Compiling bench_boost_mpfr.cpp ===
cl /nologo /O2 /EHsc /std:c++17 /MD ^
   /I C:\vcpkg\installed\x64-windows\include ^
   bench_boost_mpfr.cpp ^
   /Fe:bench_boost_mpfr.exe ^
   /link /LIBPATH:C:\vcpkg\installed\x64-windows\lib mpfr.lib gmp.lib
if errorlevel 1 (
    echo Compile failed.
    exit /b 1
)

REM Copy runtime DLLs next to the exe.
if exist C:\vcpkg\installed\x64-windows\bin\mpfr-*.dll copy /Y C:\vcpkg\installed\x64-windows\bin\mpfr-*.dll . >nul
if exist C:\vcpkg\installed\x64-windows\bin\gmp-*.dll copy /Y C:\vcpkg\installed\x64-windows\bin\gmp-*.dll . >nul

echo === Build OK. Run: bench_boost_mpfr.exe
