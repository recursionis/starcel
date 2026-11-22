# Build StarcelInstaller.exe via PyInstaller.
# Run from the starcel/ repo root.

$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

# Ensure pyinstaller is available
python -m pip show pyinstaller *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing pyinstaller..."
    python -m pip install pyinstaller
}

# Clean previous build output
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build, dist

# Build
python -m PyInstaller bootstrap.spec

if (Test-Path "dist\StarcelInstaller.exe") {
    Write-Host ""
    Write-Host "Built: $(Resolve-Path 'dist\StarcelInstaller.exe')"
    Get-Item "dist\StarcelInstaller.exe" | Select-Object Name, Length, LastWriteTime
} else {
    Write-Error "Build failed — dist\StarcelInstaller.exe not found."
    exit 1
}
