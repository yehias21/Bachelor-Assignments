#include <iostream>
#include "semaphore.h"
#include "pthread.h"
#include<time.h>
#include <unistd.h>
#define MAXTHREADS 5
#define SLEEP 10
#define QUEMAX 5
int counter=0;
sem_t empty;
sem_t full;
int in = 0;
int out = 0;
int buffer[QUEMAX];
pthread_mutex_t mutex;
pthread_mutex_t lockC=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lockPrint=PTHREAD_MUTEX_INITIALIZER;
void * mcounter(void* id);
void * mmonitor(void *);
void * mcollector(void *);

//todo: print medium print ( check lock )
int main() {
    srand(time(0));
    sem_init(&empty,0,QUEMAX);
    sem_init(&full,0,0);pthread_t ids[MAXTHREADS];
    pthread_t mmonitorID;
    pthread_t mcollectorID;
    int args[MAXTHREADS];
    for(int i=0;i<MAXTHREADS;i++)
    {
        args[i]=i+1;
        pthread_create(&ids[i],NULL,mcounter,(void*)&args[i]);
    }
    pthread_create(&mmonitorID,NULL,mmonitor,NULL);
    pthread_create(&mcollectorID,NULL,mcollector,NULL);
    pthread_join(ids[0],NULL);
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
    while(1){
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
        if(sem_trywait(&empty)==-1)
        {
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Monitor thread: Buffer full!!"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
        }
        else{
            pthread_mutex_lock(&mutex);
            buffer[in] = temp;
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Monitor thread: writing to the buffer value "<<buffer[in]<<" at position "<< in<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            in = (in+1)%QUEMAX;
            pthread_mutex_unlock(&mutex);
            sem_post(&full);
        }
        sleep(rand()%SLEEP+1);
    }
}
void * mcollector(void* )
{
    while(1){
        if(sem_trywait(&full)==-1)
        {
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Collector thread: nothing is in the buffer!"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
        }
        else{
            pthread_mutex_lock(&mutex);
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Collector thread: reading from the buffer value "<<buffer[out]<<" at position "<< out<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            out = (out+1)%QUEMAX;
            pthread_mutex_unlock(&mutex);
            sem_post(&empty);
        }
        sleep(rand()%SLEEP+1);
    }
}
