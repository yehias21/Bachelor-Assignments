#ifndef SEMAPHORES_BQUEUE_H
#define SEMAPHORES_BQUEUE_H
#include "semaphore.h"
class BQueue {
    private:
        sem_t empty;
        sem_t full;
        int in = 0;
        int out = 0;
        int* buffer;
        pthread_mutex_t qLck;
        int size;
    public:
        BQueue(int size);
        void enqueue(int temp);
        int dequeue(void);
};


#endif //SEMAPHORES_BQUEUE_H

#include<stdio.h>
#include<time.h>
#include "pthread.h"
#include "semaphore.h"
#include <stdarg.h>
#include <unistd.h>
#include <stdlib.h>
int counter=0;
static pthread_mutex_t count,print_mut,buff;
static sem_t produced,consumed;
#define TSLEEP 5
#define CAPACITY 7
typedef struct queue{
    int * arr;
    short enqueue;
    short dequeue;
}queue;
#define INIT_QUEUE(X) queue X = {.enqueue = -1, .dequeue =-1,.arr=(int*)malloc(sizeof(int)*CAPACITY)}
//must flush the buffer
void print(const char *format,...)
{
    va_list args;
    va_start(args,format);
    pthread_mutex_lock(&print_mut);
    vprintf(format,args);
    pthread_mutex_unlock(&print_mut);
    va_end(args);
    fflush(stdout);
}
void mmonitor(void *args){
    queue*buffer=(void *)args;
    int temp;
    while(1){
        sleep(rand()%(2*TSLEEP));
        if(pthread_mutex_trylock(&count)){
            print("Monitor thread: waiting to read counter\n");
            pthread_mutex_lock(&count);
        }
        temp=counter;
        counter=0;
        pthread_mutex_unlock(&count);
        print("Monitor thread: reading a count value of %d\n",temp);
        if(sem_trywait(&consumed))
        {
            print("Monitor thread: Buffer full!\n");
            sem_wait(&consumed);
        }
        pthread_mutex_lock(&buff);
        buffer->arr[++(buffer->enqueue)%CAPACITY]=temp;
        print("monitor thread: writing to the buffer value %d at position at position %d\n",temp,buffer->enqueue);
        pthread_mutex_unlock(&buff);
        sem_post(&produced);
    }
}
void mcounter(void *args){
    int *id=(int *)args;
    while(1){
        sleep(rand()%TSLEEP);
        print("Counter thread %d received a message\n",*id);
        if(pthread_mutex_trylock(&count)){
            print("Counter thread %d: waiting to write\n",*id);
            pthread_mutex_lock(&count);
        }
        counter++;
        pthread_mutex_unlock(&count);
        print("Counter thread %d now adding to counter, counter value = %d\n",*id,counter);
    }
}
void mcollector(void *args){
    queue*buffer=(void *)args;
    while(1){
        sleep(rand()%(TSLEEP*3));
        if(sem_trywait(&produced)){
            print("Collector thread: nothing is in the buffer!!\n");
            sem_wait(&produced);
        }
        pthread_mutex_lock(&buff);
        print("Collector thread: reading from the buffer value %d at position at position %d\n",buffer->arr[++(buffer->dequeue)%CAPACITY],buffer->dequeue);
        pthread_mutex_unlock(&buff);
        sem_post(&consumed);
    }
}
int main(void){
    //    number of cores
    int t_num=8;
    pthread_mutex_init(&print_mut,NULL);
    pthread_mutex_init(&count,NULL);
    pthread_mutex_init(&buff,NULL);
    sem_init(&produced,0,0);
    sem_init(&consumed,0,CAPACITY);
    INIT_QUEUE(buffer);
    queue *buffer_ptr=&buffer;
    srand(time(0));
    pthread_t id[t_num+2];
    int ids[t_num];
    int ret;
    for(int i=0;i<t_num;i++)
    {
        ids[i]=i+1;
        ret=pthread_create(&id[i],NULL,mcounter,i+1);
        if(ret) fprintf(stderr,"failed to create thread n: %d\n",(void *)&ids[i]);
    }
    ret=pthread_create(&id[t_num],NULL,mmonitor,(void*)buffer_ptr);
    if(ret) fprintf(stderr,"failed to create producer thread\n");
    ret=pthread_create(&id[t_num+1],NULL,mcollector,(void*)buffer_ptr);
    if(ret) fprintf(stderr,"failed to create consumer thread\n");
    for(int i=0;i<t_num+2;i++)
        pthread_join(id[i],NULL);
    free(buffer.arr);
}