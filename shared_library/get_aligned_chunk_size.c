#include<stdio.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
    int i;
    unsigned long total_size = 0;
    unsigned long total_pages = 0;
    unsigned long size;

    if(argc < 2){
        printf("You should pass the parameters (ed. ./get_aligned_chunk_size size_in_MB) \n");
        return -1;
    }else{
        sscanf(argv[1], "%lu", &size);
    }

    while(total_size < size){
        total_size +=4096;
        total_pages++;
    }
    printf("Count pages:%ld, total_size:%ld\n", total_pages, total_size);
    return 0;
}
