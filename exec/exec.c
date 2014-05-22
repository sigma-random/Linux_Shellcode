#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

char *cmd[] = {"/bin/ls","-al","/root/"};

int main( ) {

	execve(cmd[0],cmd,NULL);

}