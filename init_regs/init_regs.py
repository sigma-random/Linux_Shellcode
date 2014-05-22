from struct import pack
import sys 
import binascii

##########################################################
#
#  init_regs
#
#	                         random	     2014-04-21
##########################################################


##########################################################
des_format = 'shellcode: init_regs' 

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
	print des


def init_regs_shellcode():
	shellcode = ''
	#init
	shellcode += '\x31\xc0\x31\xd2\x31\xdb\x31\xc9'			#xor eax,eax#xor edx,edx#xor ebx,ebx#xor ecx,ecx
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
	shellcode = init_regs_shellcode()
	out_format(language)
	getshellcode(language, shellcode)
	



