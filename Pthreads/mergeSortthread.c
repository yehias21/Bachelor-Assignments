//in linux add this line to makefiles set(CMAKE_CXX_FLAGS "-pthread")
//todo ask the TA about pthread_detach and &attr in pthreadcreate (void*) casting
#include <stdio.h>
#include <stdlib.h>
#include "pthread.h"
typedef struct arg
{
    int *arr;
    int start;
    int end;
}arg;
void merge(int data[], int left, int right)
{
    int count = 0;
    int i = left;
    int mid = left + ((right - left) / 2);
    int j = mid + 1;
    int buff[right-left+1];
    while (i <= mid && j <= right) {
        if (data[i] <= data[j]) {
            buff[count++] =  data[i++];
        } else {
            buff[count++] =  data[j++];
        }
    }
    if (i == mid + 1) {
        while (j <= right) {
            buff[count++] = data[j++];
        }
    } else {
        while (i <= mid) {
            buff[count++] = data[i++];
        }
    }
    i = left;
    count = 0;
    while (i <= right) {
        data[i++] = buff[count++];
    }
}
void* mergeSort(void* data)
{
    arg *args=(arg*) data;
    if (args->start < args->end) {
        arg arrL,arrR;
        pthread_t idL,idR;
        int m = args->start +( args->end-args->start) / 2;
        arrL.arr=arrR.arr=args->arr;
        arrL.start=args->start;
        arrL.end=m;
        arrR.start=m+1;
        arrR.end=args->end;
        int check= pthread_create(&idL, NULL,mergeSort, (void*)&arrL);
        int check2=pthread_create(&idR, NULL,mergeSort, (void*)&arrR);
        if(check&&check2) fprintf(stderr,"%s","creationof threads failed");
        pthread_join(idL, NULL);
        pthread_join(idR, NULL);
        merge(args->arr, args->start,args->end);
    }
    pthread_exit(NULL);
}
void print(int *arr,int n)
{
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    puts("");
}
int main(int argc, char *argv[] )
{
    FILE *f=freopen(argv[1],"r", stdin);
    if(!f) perror("can not read the file");
    int n;
    arg data;
    while (!feof(f))
    {
        fscanf(f,"%d",&n);
        int arr[n];
        for(int i=0;i<n;i++)
            fscanf(f, "%d ",&arr[i]);
        pthread_t id;
        data.arr=arr;
        data.start=0;
        data.end=n;
        int check=pthread_create(&id, NULL,mergeSort, (void*)&data);
        if(check) fprintf(stderr,"%s","creation of threads failed");
        pthread_join(id, NULL);
        print(arr,n);
    }
    fclose(f);
    return 0;
}