#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

char * buf[1024];

int main (int argc, char** argv) {

	int fd;
	int r_cnt;
	if(argc != 2) {
		printf("usage : %s filename\n",argv[0]);
		return -1;
	}
	if( -1 == (fd = open(argv[1],O_RDONLY))) {
		perror("open");
		exit(-1);
	}
	r_cnt = read(fd,buf,1024);
	write(STDOUT_FILENO,buf,r_cnt);
	return 0;
}
