@echo off
REM Setup script: create venv, install pyinstaller, build single exe (windowed)

REM Create virtual environment if it doesn't exist
if not exist .venv (
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install pyinstaller
python -m pip install pyinstaller
python -m pip install PyQt6 cryptography reportlab

REM Remove old build/dist/spec files
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
REM if exist Billtracker_qt.spec del /q Billtracker_qt.spec

REM Build the exe (windowed, no console)
pyinstaller --onefile --windowed --noupx --add-data "billtracker.ico;." --add-data "billtracker.png;." --add-data "tray.ico;." --add-data "README.md;." --add-data "README_GE.md;." --icon="billtracker.ico" Billtracker_qt.py

REM Show result
if exist dist\Billtracker_qt.exe (
    echo Build successful! EXE is in the dist folder.
) else (
    echo Build failed. Check the output above for errors.
)

REM pause
