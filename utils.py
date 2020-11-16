import re
import os
import subprocess
import sys
import random
import string
import binascii

# utils
def basedir(append=''):
    return os.path.realpath(os.path.dirname(__file__)) + '/' + append

def capture(command, stdin=None):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return proc.communicate(input=stdin)[0]

def randstr(minsize=4, maxsize=8):
    size = random.randint(minsize, maxsize + 1)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))

wordlist = basedir('resources/wordlist.txt')
words = None

def randhuman(minnumber=1, maxnumber=3, title_case=True):
    # read in wordlist
    global words
    if not words:
        with open(wordlist, 'r') as fp:
            words = [
                        ''.join(c for c in s if c.isalpha()) for s in fp.readlines()
                    ]

    # generate them
    num_choices = random.randint(minnumber, maxnumber + 1)
    choices = [random.choice(words) for _ in range(num_choices)]

    # make title case
    if title_case and len(choices) > 1:
        choices = [choices[0]] + [s.title() for s in choices[1:]]

    return ''.join(choices)

def chunkup(s, size=75):
    chunks = [s[i:i + size] for i in range(0, len(s), size)]
    return chunks

# obfuscation
def vba_split_string(string):
    quoted = ['"{}"'.format(c) for c in string]
    return ' & '.join(quoted)

def obfuscate_tokens(data):
    # get tokens
    matches = re.finditer('%%[^%]+%%', data)
    tokens = [m.group(0) for m in matches]
    unique = set(tokens)

    def gentokens(human=True, factor=5):
        while True:
            if human:
                yield randhuman(factor - 2, factor - 1)
            else:
                yield randstr(3 * factor, 5 * factor)

    token_iter = iter(unique)
    replace_iter = gentokens()
    for token, replace in zip(token_iter, replace_iter):
        debug('replacing {} with {}'.format(token, replace))
        while replace in data:
            replace = next(replace_iter)
        data = data.replace(token, replace)

    return data

def mask_buffer(buf, mask):
    masked = b''
    for b in buf:
        masked += bytes([b ^ mask])
    return masked

def encode_string(string, mask):
    """
    Mask and hex encode a string
    """
    masked = mask_buffer(string.encode(), mask)
    return binascii.hexlify(masked).decode()

def vba_encode(string):
    """
    Mask and encode string. Returns it wrapped in a decoder function (must be named %%DECODE%%)
    """
    mask = random.randint(1, 255)
    encoded = encode_string(string, mask)
    return '%%DECODE%%("{}", {})'.format(encoded, mask)

# print
enable_debug = False

def debug(s):
    global enable_debug
    if enable_debug:
        print('[D] ' + s, file=sys.stderr)

def ok(s):
    print('[.] ' + s, file=sys.stderr)

def yes(s):
    print('[+] ' + s, file=sys.stderr)

def no(s):
    print('[!] ' + s, file=sys.stderr)

def bye(s):
    no(s)
    sys.exit(1)
