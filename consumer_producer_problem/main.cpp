#include <iostream>
#include<time.h>
#include <unistd.h>
#include "pthread.h"
#include "BQueue.h"
#define MAXTHREADS 5
#define SLEEP 10
//todo: mimize the dependencies
//todo:implement error protocols
//todo:organize the code (use the inline operations)
//todo: print medium print ( check lock )
int counter=0;
pthread_mutex_t lockC=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lockPrint=PTHREAD_MUTEX_INITIALIZER;
void * mcounter(void* id);
void * mmonitor(void *);
void * mcollector(void *);
int main() {
    BQueue jobs(-1);
//    srand(time(0));
//    pthread_t ids[MAXTHREADS],mmonitorID,mcollectorID;
//    int args[MAXTHREADS];
//    for(int i=0;i<MAXTHREADS;i++)
//    {
//        args[i]=i+1;
//        pthread_create(&ids[i],NULL,mcounter,(void*)&args[i]);
//    }
//    pthread_create(&mmonitorID,NULL,mmonitor,NULL);
//    pthread_create(&mcollectorID,NULL,mcollector,NULL);
//    pthread_join(ids[0],NULL);
}
void * mcounter(void* id)
{
    int * ID=(int*)id;
    while(1){
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Counter thread "<< *ID<<" received a message"<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        if(pthread_mutex_trylock(&lockC)!=0){
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Counter thread "<< *ID<<": waiting to write"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            pthread_mutex_lock(&lockC);
        }
        counter+=1;
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Counter thread "<< *ID<<" now adding to counter, counter value = "<<counter<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        pthread_mutex_unlock(&lockC);
        sleep(rand()%10+1);
    }
}
void * mmonitor(void* )
{
    int temp;
    while(true){
        if(pthread_mutex_trylock(&lockC)!=0){
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Monitor thread: waiting to read counter"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            pthread_mutex_lock(&lockC);
        }
        temp=counter;
        counter=0;
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Monitor thread: reading a count value of "<<temp<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        pthread_mutex_unlock(&lockC);
        sleep(rand()%SLEEP+1);
    }
}
void * mcollector(void* )
{
    while(true){
        sleep(rand()%SLEEP+1);
    }
}
