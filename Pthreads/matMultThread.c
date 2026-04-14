#include <stdio.h>
#include <stdlib.h>
#include "pthread.h"
#include <time.h>
typedef struct matrix
{
    pthread_t id;
    short row,column,size,col2;
    int *arr1,*arr2,*result;
}matrix;
void print(int n,int m,int *arr)
{
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++)
            printf("%d ",arr[i*m+j]);
        puts("");
    }
}
void * multiplyE(void *data)
{
    int element=0;
    matrix* mat=(matrix*)data;
    for(int i=0;i<mat->size;i++)
        element+=mat->arr1[mat->size*mat->row+i]*mat->arr2[i*(mat->col2)+mat->column];
    pthread_exit(element);
}
void * multiplyR(void *data)
{   int element;
    matrix* mat=(matrix*)data;
    for(int i=0;i<mat->col2;i++)
    {
        element=0;
        for(int j=0;j<mat->size;j++)
            element+=mat->arr1[mat->size*mat->row+j]*mat->arr2[j*(mat->col2)+i];
        mat->result[mat->row*(mat->col2)+i]=element;
    }
    pthread_exit(NULL);
}
void multEl(int n1,int m1,int m2,int*arr1,int* arr2)
{
    clock_t start_t=clock();
    void *ret;
    int result[n1*m2],check;
    matrix arr[n1*m2];
    for(int i=0;i<n1;i++)
        for(int j=0;j<m2;j++)
        {
            arr[i*m2+j].arr1=arr1;
            arr[i*m2+j].arr2=arr2;
            arr[i*m2+j].size=m1;
            arr[i*m2+j].column=j;
            arr[i*m2+j].row=i;
            arr[i*m2+j].col2=m2;
            check= pthread_create(&(arr[i*m2+j].id), NULL,multiplyE, (void*)&arr[i*m2+j]);
            if(check) perror("could not create a thread");
    }
    for(int i=0;i<n1;i++)
        for(int j=0;j<m2;j++)
        {   pthread_join(arr[i*m2+j].id, &ret);
            result[i*m2+j]=ret;
        }
        print(n1,m2,result);
        printf("Time taken by first procedure is= %f\n", (double)(clock()-start_t)/CLOCKS_PER_SEC);
}
void multRow(int n1,int m1,int m2,int*arr1,int* arr2)
{
    clock_t start_t=clock();
    int result[n1*m2],check;
    matrix arr[n1];
    for(int i=0;i<n1;i++)
        {
            arr[i].arr1=arr1;
            arr[i].arr2=arr2;
            arr[i].size=m1;
            arr[i].row=i;
            arr[i].col2=m2;
            arr[i].result=result;
            check= pthread_create(&(arr[i].id), NULL,multiplyR, (void*)&arr[i]);
            if(check) perror("could not create a thread");
        }
    for(int i=0;i<n1;i++)
        pthread_join(arr[i].id, NULL);
    print(n1,m2,result);
        printf("Time taken by second procedure is= %f\n", (double)(clock()-start_t)/CLOCKS_PER_SEC);
}
int main(int argc, char *argv[] )
{
    FILE *f=freopen(argv[1], "r", stdin);
    if(!f) perror("can not read the file");
    int n1,m1,n2,m2;
    while (!feof(f))
    {
        fscanf(f, "%d %d",&n1,&m1);
        int arr1[n1][m1];
        for(int i=0;i<n1;i++)
            for(int j=0;j<m1;j++)
                fscanf(f, "%d ",&arr1[i][j]);
        fscanf(f, "%d %d",&n2,&m2);
        int arr2[n2][m2];
        for(int i=0;i<n2;i++)
            for(int j=0;j<m2;j++)
                fscanf(f, "%d ",&arr2[i][j]);
        multEl(n1,m1,m2,(int*)arr1,(int*)arr2);
        multRow(n1,m1,m2,(int*)arr1,(int*)arr2);
    }
    fclose(f);
    return 0;
}