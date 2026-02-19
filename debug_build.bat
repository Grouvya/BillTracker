@echo off
REM Debug build script: console enabled
if not exist .venv ( python -m venv .venv )
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install pyinstaller PyQt6 cryptography reportlab
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Billtracker_qt.spec del /q Billtracker_qt.spec

REM Build WITHOUT --windowed to see errors
pyinstaller --onefile --add-data "billtracker.ico;." --add-data "billtracker.png;." --add-data "tray.ico;." --add-data "README.md;." --add-data "README_GE.md;." --icon="billtracker.ico" Billtracker_qt.py

if exist dist\Billtracker_qt.exe ( echo Build successful! ) else ( echo Build failed. )
