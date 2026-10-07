[Setup]
AppName=Img2PDF
AppVersion=1.0
DefaultDirName={pf}\Img2PDF
DefaultGroupName=Img2PDF
UninstallDisplayIcon={app}\Img2PDF.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.\Output
OutputBaseFilename=Img2Pdf_Installer
SetupIconFile=resources\icon.ico
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\Img2PDF\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "resources\icon.ico"; DestDir: "{app}\resources"; Flags: ignoreversion

[Icons]
Name: "{group}\Img2PDF"; Filename: "{app}\Img2PDF.exe"; IconFilename: "{app}\resources\icon.ico"
Name: "{commondesktop}\Img2PDF"; Filename: "{app}\Img2PDF.exe"; Tasks: desktopicon; IconFilename: "{app}\resources\icon.ico"

[Run]
Filename: "{app}\Img2PDF.exe"; Description: "Launch Img2PDF"; Flags: nowait postinstall skipifsilent
