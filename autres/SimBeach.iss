[Setup]
AppName=SimBeach
AppVersion=1.0
DefaultDirName={commonpf}\SimBeach
OutputDir=.
OutputBaseFilename=SimBeachSetup
SetupIconFile=robot.ico

[Files]
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\dist\SimBeach.exe"; DestDir: "{app}"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\robot.ico"; DestDir: "{app}"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\ecrans\*"; DestDir: "{app}\ecrans"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\structure\*"; DestDir: "{app}\structure"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\assets\backgrounds\*"; DestDir: "{app}\assets\backgrounds"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\assets\dechets\*"; DestDir: "{app}\assets\dechets"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\assets\icones\*"; DestDir: "{app}\assets\icones"
Source: "C:\Users\jeanp\Documents\UDM_Year2\PTuto\assets\robot\*"; DestDir: "{app}\assets\robot"

[Dirs]
Name: "{app}\variables"; Permissions: users-modify

[Icons]
Name: "{group}\SimBeach"; Filename: "{app}\SimBeach.exe"; IconFilename: "{app}\robot.ico"
Name: "{userdesktop}\SimBeach"; Filename: "{app}\SimBeach.exe"; WorkingDir: "{app}"; IconFilename: "{app}\robot.ico"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"