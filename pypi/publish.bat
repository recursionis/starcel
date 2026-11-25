@echo off
REM Build and upload the starcel package to PyPI.
REM
REM   publish.bat            uses the VERSION already in src\starcel\config.py
REM   publish.bat 0.2.0a4    sets VERSION to 0.2.0a4 first
REM
REM PyPI rejects re-uploads of an existing version, so bump it each release.

setlocal
cd /d "%~dp0.."

if not "%~1"=="" (
    echo Setting version to %~1
    powershell -NoProfile -Command "$p = (Resolve-Path 'pypi\src\starcel\config.py').Path; $t = [IO.File]::ReadAllText($p) -replace '(?m)^VERSION = \".*\"', 'VERSION = \"%~1\"'; [IO.File]::WriteAllText($p, $t)"
    if errorlevel 1 goto :fail
)

for /f "tokens=3 delims= " %%v in ('findstr /b "VERSION =" pypi\src\starcel\config.py') do set VER=%%~v
echo Publishing starcel %VER%

if exist pypi\dist rmdir /s /q pypi\dist

python pypi\build.py
if errorlevel 1 goto :fail

python -m twine upload pypi\dist\*
if errorlevel 1 goto :fail

echo.
echo Published starcel %VER%
pause
exit /b 0

:fail
echo.
echo Publish failed.
pause
exit /b 1
