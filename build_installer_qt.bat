@echo off
REM Build NSIS installer for Billtracker_qt.exe



REM Build the installer using the NSIS script
makensis Billtracker_qt_installer.nsi

REM Show result
if exist Billtracker_qt_Installer.exe (
    echo Installer built successfully: Billtracker_qt_Installer.exe
) else (
    echo Installer build failed. Check the output above for errors.
)

pause
