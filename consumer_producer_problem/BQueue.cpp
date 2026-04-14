#include <iostream>
#include "BQueue.h"
BQueue::BQueue(int size)
{
    try{
        if(size<=0) throw "non positive size";
        else{
            sem_init(&empty,0,size);
            sem_init(&full,0,0);
            buffer= new int[size];
            this->size=size;
        }
    }
    catch(...)
    {
        std::fprintf(stderr,"Can not create the queue - Size must be bigger than 0");
    }
}
void BQueue::enqueue(int temp) {
    if(sem_trywait(&empty)==-1)
    {
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Monitor thread: Buffer full!!"<<std::endl;
        pthread_mutex_unlock(&lockPrint);
    }
    else{
        pthread_mutex_lock(&qLck);
        buffer[in] = temp;
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Monitor thread: writing to the buffer value "<<buffer[in]<<" at position "<< in<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        in = (in+1)%size;
        pthread_mutex_unlock(&qLck);
        sem_post(&full);
    }
}
int BQueue::dequeue(void)
{
    if(sem_trywait(&full)==-1)
    {
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Collector thread: nothing is in the buffer!"<<std::endl;
        pthread_mutex_unlock(&lockPrint);
    }
    else{
        pthread_mutex_lock(&qLck);
        pthread_mutex_lock(&lockPrint);
        std::cout<<"Collector thread: reading from the buffer value "<<buffer[out]<<" at position "<< out<<std::endl;
        pthread_mutex_unlock(&lockPrint);
        out = (out+1)%size;
        pthread_mutex_unlock(&qLck);
        sem_post(&empty);
    }
}

