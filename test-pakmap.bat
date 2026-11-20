@echo off
rem Launches the packaged game straight into a map from a mod .pak.
rem -ModPak mounts the pak before the startup map loads; a short map name
rem (e.g. SunTemple) is resolved to its full path inside the pak.

set "GAME=C:\Users\Nick\Desktop\WindowsNoEditor\WindowsNoEditor\Starcel9.exe"
set "PAK=C:\Users\Nick\Desktop\StarcelMapTest1-WindowsNoEditor.pak"
set "MAP=SunTemple"

start "" "%GAME%" "%MAP%" -ModPak="%PAK%" -windowed -ResX=1280 -ResY=720 -log
