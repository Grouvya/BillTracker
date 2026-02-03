; Billtracker_qt_installer.nsi
; NSIS script for Billtracker_qt

;--------------------------------
;General

  ;Name and file
  Name "Billtracker"
  OutFile "Billtracker_qt_Installer.exe"
  Unicode True
  VIProductVersion "5.5.0.0"
  VIAddVersionKey "FileVersion" "5.5.0 Cross-Platform"

  ;Default Installation Directory
  InstallDir "$PROGRAMFILES\Billtracker"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Billtracker" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin

;--------------------------------
;Interface Settings

  !include "MUI2.nsh"
  !include "LogicLib.nsh"
  !include "LogicLib.nsh"

  !define MUI_ABORTWARNING
  !define MUI_ICON "calc.ico"
  !define MUI_UNICON "calc.ico"

;--------------------------------
;Functions

  Function .onInit
    UserInfo::GetAccountType
    Pop $0
    ${If} $0 != "admin"
      MessageBox MB_OK|MB_ICONSTOP "You need administrator rights to install Billtracker."
      SetErrorLevel 740 ; ERROR_ELEVATION_REQUIRED
      Quit
    ${EndIf}
  FunctionEnd

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "LICENSE" ; Ensure you have a LICENSE file or comment this out if not
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Billtracker" SecDummy

  SetOutPath "$INSTDIR"
  
  ;ADD YOUR OWN FILES HERE...
  File "dist\Billtracker_qt.exe"
  ; If there are other dependencies in dist, include them here. 
  ; For a single-file exe from PyInstaller, usually just the exe is enough.
  
  ;Store installation folder
  WriteRegStr HKCU "Software\Billtracker" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ;Create Shortcuts
  CreateDirectory "$SMPROGRAMS\Billtracker"
  CreateShortcut "$SMPROGRAMS\Billtracker\Billtracker.lnk" "$INSTDIR\Billtracker_qt.exe"
  CreateShortcut "$SMPROGRAMS\Billtracker\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Desktop Shortcut" SecDesktop
  CreateShortcut "$DESKTOP\Billtracker.lnk" "$INSTDIR\Billtracker_qt.exe"
SectionEnd

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  Delete "$INSTDIR\Billtracker_qt.exe"
  Delete "$INSTDIR\Uninstall.exe"

  Delete "$SMPROGRAMS\Billtracker\Billtracker.lnk"
  Delete "$SMPROGRAMS\Billtracker\Uninstall.lnk"
  Delete "$DESKTOP\Billtracker.lnk"
  RMDir "$SMPROGRAMS\Billtracker"

  DeleteRegKey /ifempty HKCU "Software\Billtracker"

  RMDir "$INSTDIR"

SectionEnd
