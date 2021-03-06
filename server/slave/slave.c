//gcc -o slave slave.c -I../src -L.. -liniparser
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <errno.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include "iniparser.h"

#define MSG_SIZE 255

void create_example_ini_file(void);
int parse_ini_file(char * ini_name, char * bufferIn, char * bufferOut);
int process_request(char *request, char *data );

void main(int argc, char * argv[])
{
  int sockfd, bind_return, rcv_return, snd_return;
	int port = 1026;
	int size = sizeof(struct sockaddr_in);
	struct sockaddr_in *server_addr_in;
	server_addr_in = (struct sockaddr_in*)malloc(sizeof(*server_addr_in));
	struct sockaddr_in *initiator;
	initiator = (struct sockaddr_in *) malloc(sizeof(*initiator));
	char *buffer = (char *) malloc(MSG_SIZE * sizeof(char));
  char *dataObject = (char *) malloc(MSG_SIZE * sizeof(char));
  char *data = (char *) malloc(MSG_SIZE * sizeof(char));
  u_long fromaddr;


	//Initialise le serveur en identifiant la connexion à travers un port donné en argument
	memset(server_addr_in, 0, (size_t)sizeof(server_addr_in));
	server_addr_in->sin_family = AF_INET;
	server_addr_in->sin_port = htons(port);
	server_addr_in->sin_addr.s_addr = INADDR_ANY; //inet_addr("192.168.23.12"); //"192.168.23.12"; //INADDR_ANY;

	//Fonction socket
	if ((sockfd = socket (PF_INET, SOCK_DGRAM, 0)) < 0) { //ou IPPROTO_UDP à la place de 0
			perror("socket");
			exit(EXIT_FAILURE);
	}
	else {
		perror("socket");
	}

	//Fonction bind
	if ((bind_return = bind (sockfd, (struct sockaddr *)server_addr_in, sizeof(*server_addr_in))) <0) {
		perror("bind");
		exit(EXIT_FAILURE);
	}
	else {
		perror("bind");
	}

	fprintf(stdout,"\nReady to receive..\n");
int val=1;
	while (1) {
		//Fonction receive
    //memset(buffer, 0, (size_t)sizeof(buffer));
		if(rcv_return = recvfrom (sockfd, buffer, MSG_SIZE,0, (struct sockaddr *) initiator, (socklen_t *) &size) == -1){
			fprintf(stderr,"Error %d in recvfrom: %s\n", errno,sys_errlist[errno]);
			exit(errno);
		}
    //Cette variable doit être après le "rcvfrom"
    //fromaddr = initiator -> sin_addr.s_addr;
    //fprintf(stdout, "From : %s:%d : %s\n", (gethostbyaddr((char*)&fromaddr, sizeof(fromaddr), AF_INET)) -> h_name, initiator->sin_port,buffer);
    //memset(data, 0, (size_t)sizeof(data));
    printf("Ok\n");
    if(process_request((char *)buffer, data ) == 0){//succeed
      printf("Success\n");
      //sprintf(dataObject,"{\"ip\":\"%s\",\"data\":\"%s\"}",(gethostbyaddr((char*)&fromaddr, sizeof(fromaddr), AF_INET)) -> h_name,data);
      //Fonction send : envoi le retour de la commande contenu dans tmp.txt au master
      if(snd_return = sendto(sockfd,data,(int)strlen(data),0,(struct sockaddr *)initiator, sizeof(*server_addr_in)) == -1) {
        fprintf(stderr,"Error %d in sendto: %s\n", errno,sys_errlist[errno]);
        exit(errno);
      }
      printf("%s\n",dataObject);
    }else{//failed
      printf("Error");
      printf("%s\n",data);
    }
    val = 0;
	}
	//Fonction close
	close(sockfd);
}


int parse_ini_file(char * ini_name, char * bufferIn, char * bufferOut)
{
    dictionary  *   ini ;
    const char  *   s;

    ini = iniparser_load(ini_name);
    if (ini==NULL) {
        fprintf(stderr, "cannot parse file: %s\n", ini_name);
        return -1 ;
    }
    printf("%s\n", bufferIn);
    s = iniparser_getstring(ini, bufferIn, NULL);
    printf("%s\n",s);
    sprintf(bufferOut,"%s",s);
    iniparser_freedict(ini);
    return 0 ;
}

int process_request(char *request, char *data ){
  char *s = (char *) malloc(MSG_SIZE * sizeof(char));
  char *commandLine = (char *) malloc(MSG_SIZE * sizeof(char));
  char *commandLineData = (char *) malloc(MSG_SIZE * sizeof(char));
  int commandLineStatus;
  FILE* dataFile = NULL;
  parse_ini_file("configuration.ini", request,s);
  sprintf(commandLine, "%s > data191215.txt", s);
  commandLineStatus = system(commandLine);
  dataFile = fopen("data191215.txt" , "r+");
  if(dataFile != NULL){
		fgets(commandLineData, MSG_SIZE, dataFile);
  }
  strncpy(data, commandLineData, strlen(commandLineData)-2);
  fclose(dataFile);
  remove("data191215.txt");
  if(commandLineStatus == 0){
    return 0;
  }else{
    return -1;
  }
}
