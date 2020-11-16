import struct
import random
import string

class Package(object):
    def __init__(self, filename, fn):
        self.filename = fn
        self.fakepath = 'C:\\Intel\\{}'.format(self.filename)

        self.orgpath = self.fakepath
        self.datapath = self.fakepath

        with open(filename,'rb') as f:
            self.data = f.read()

        self.OBJ_HEAD = r""
        self.OBJ_TAIL = r"0105000000000000"

    def get_object_header(self):
        OLEVersion = '01050000'
        FormatID = '02000000'
        ClassName = 'Package'
        szClassName = struct.pack("<I", len(ClassName) + 1).encode('hex')
        szPackageData = struct.pack("<I", len(self.get_package_data())/2).encode('hex')

        return ''.join([
            OLEVersion,
            FormatID,
            szClassName,
            ClassName.encode('hex') + '00',
            '00000000',
            '00000000',
            szPackageData,
        ])

    def get_package_data(self):  
        StreamHeader = '0200'
        Label = self.filename.encode('hex') + '00'
        OrgPath = self.orgpath.encode('hex') + '00'
        UType = '00000300'
        DataPath = self.datapath.encode('hex') + '00'
        DataPathLen = struct.pack("<I", len(self.datapath)+1).encode('hex')
        DataLen = struct.pack("<I", len(self.data)).encode('hex')
        Data = self.data.encode('hex')
        OrgPathWLen = struct.pack("<I", len(self.datapath)).encode('hex')
        OrgPathW = self.datapath.encode('utf-16le').encode('hex')
        LabelLen = struct.pack("<I", len(self.filename)).encode('hex')
        LabelW = self.filename.encode('utf-16le').encode('hex')
        DefPathWLen = struct.pack("<I", len(self.orgpath)).encode('hex')
        DefPathW = self.orgpath.encode('utf-16le').encode('hex')

        return ''.join([
            StreamHeader,
            Label,
            OrgPath,
            UType,
            DataPathLen,
            DataPath,
            DataLen,
            Data,
            OrgPathWLen,
            OrgPathW,
            LabelLen,
            LabelW,
            DefPathWLen,
            DefPathW,
        ])

    def build_package(self):
        return self.OBJ_HEAD + self.get_object_header() + self.get_package_data() + self.OBJ_TAIL

def get_package_bytes(sct,fn):
    p = Package(sct,fn)
    package = p.build_package()
    return package
