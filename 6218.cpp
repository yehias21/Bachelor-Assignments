#include <iostream>
#include "semaphore.h"
#include "pthread.h"
#include<time.h>
#include <unistd.h>
#define MAXTHREADS 5
#define SLEEP 10
#define QUEMAX 5
int mcount=0;
sem_t empty;
sem_t full;
int in = 0;
int out = 0;
int arr[QUEMAX];
pthread_mutex_t mutex;
pthread_mutex_t lockC=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lockPrint=PTHREAD_MUTEX_INITIALIZER;
void * counter(void* id);
void * monitor(void *);
void * collector(void *);

//todo: print medium print ( check lock )
int main() {
    srand(time(NULL));
    sem_init(&empty,0,QUEMAX);
    sem_init(&full,0,NULL);
    pthread_t tid[MAXTHREADS];
    pthread_t mmonitorID;
    pthread_t mcollectorID;
    for(int i=0;i<MAXTHREADS;i++)
    {
        pthread_create(&tid[i],NULL,counter,(void*)&tid[i]);
    }
    pthread_create(&mmonitorID,NULL,monitor,NULL);
    pthread_create(&mcollectorID,NULL,collector,NULL);
    pthread_join(tid[0],NULL);
}
void * counter(void* id)
{
    pthread_t * ID=(pthread_t*)id;
    while(true){
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Counter thread "<< *ID<<" received a message"<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        if(pthread_mutex_trylock(&lockC)!=0){
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Counter thread "<< *ID<<": waiting to write"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            pthread_mutex_lock(&lockC);
        }
        mcount+=1;
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Counter thread "<< *ID<<" now adding to counter, counter value = "<<mcount<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        pthread_mutex_unlock(&lockC);
        sleep(rand()%10+1);
    }
}
void * monitor(void* )
{
    int countT;
    while(true){
        if(pthread_mutex_trylock(&lockC)!=0){
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Monitor thread: waiting to read counter"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            pthread_mutex_lock(&lockC);
        }
        countT=mcount;
        mcount=0;
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Monitor thread: reading a count value of "<<countT<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        pthread_mutex_unlock(&lockC);
        if(sem_trywait(&empty)==-1)
        {
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Monitor thread: buffer full!!"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
        }
        else{
            pthread_mutex_lock(&mutex);
            arr[in] = countT;
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Monitor thread: writing to the buffer value "<<arr[in]<<" at position "<< in<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            in = (in+1)%QUEMAX;
            pthread_mutex_unlock(&mutex);
            sem_post(&full);
        }
        sleep(rand()%SLEEP+1);
    }
}
void * collector(void* )
{
    int temp;
    while(true){
        sem_getvalue(&empty,&temp);
        if(temp==QUEMAX)
        {
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Collector thread: nothing is in the buffer!"<<std::endl;
            pthread_mutex_unlock(&lockPrint);
        }
        else{
            sem_wait(&full);
            pthread_mutex_lock(&mutex);
            pthread_mutex_lock(&lockPrint);
            std::cout<<"Collector thread: reading from the buffer value "<<arr[out]<<" at position "<< out<<std::endl;
            pthread_mutex_unlock(&lockPrint);
            out = (out+1)%QUEMAX;
            pthread_mutex_unlock(&mutex);
            sem_post(&empty);
        }
        sleep(rand()%SLEEP+1);
    }
}