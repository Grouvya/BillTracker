@echo off
REM Add NSIS (makensis.exe) directory to the user PATH environment variable

set "NSIS_PATH=C:\Program Files (x86)\NSIS"

REM Check if the directory exists
if not exist "%NSIS_PATH%\makensis.exe" (
    echo NSIS not found in the default location: %NSIS_PATH%\makensis.exe
    echo Please check your NSIS installation path and update this script if needed.
    pause
    exit /b 1
)

REM Add to user PATH if not already present
setx PATH "%PATH%;%NSIS_PATH%"

if %ERRORLEVEL% EQU 0 (
    echo NSIS path added to user PATH. Please restart your terminal or computer for changes to take effect.
) else (
    echo Failed to update PATH. Try running this script as administrator.
)

pause
