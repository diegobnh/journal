//#include <libsyscall_intercept_hook_point.h>
#include "/ihome/dmosse/dmoura/0_tools/syscall/syscall_intercept/include/libsyscall_intercept_hook_point.h"
#include <syscall.h>
#include <errno.h>
#include <stdio.h>
#include <execinfo.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#define _GNU_SOURCE
#include <pthread.h>
#define SIZE 2048
#include <sys/resource.h>
#include <numaif.h>


#define CHUNK_SIZE 500002816UL
#define N 50
FILE *g_fp=NULL;
FILE *fp_bind=NULL;
char *g_line = NULL;
size_t len = 0;

pthread_mutex_t count_mutex;

unsigned long g_call_stack_vector[N];

void read_parameters_for_binding(void){
    int call_stack_size;
    int i;

    fp_bind=fopen("static_mapping.txt", "r");
    if(fp_bind == NULL){
      fprintf(stderr, "Error open bind text!\n");
    }
    fscanf(fp_bind, "%d\n",&call_stack_size);
    for(i=0; i<call_stack_size; i++){
       fscanf(fp_bind, "%lu\n", &g_call_stack_vector[i]);
    }
    g_call_stack_vector[i]=-1;
    fclose(fp_bind);
}

int check_address(unsigned long call_stack_hash)
{
    int i=0;
    while(g_call_stack_vector[i] != -1){
       if(g_call_stack_vector[i] == call_stack_hash){
          return 1;
       }
       i++;
    }
    return 0;
}

long int hash (char* word)
{
    unsigned int hash = 0;
    for (int i = 0 ; word[i] != '\0' ; i++)
    {
        hash = 31*hash + word[i];
    }
    //return hash % TABLE_SIZE;
    return abs(hash) ;
}

void redirect_stdout(char *filename)
{
    int fd;
    if ((fd = open(filename,O_CREAT|O_WRONLY,0666)) < 0){
       perror(filename);
       exit(1);
    }
    close(1);
    if (dup(fd) !=1){
       fprintf(stderr,"Unexpected dup failure\n");
       exit(1);
    }
    close(fd);

    g_fp = fopen("call_stack.txt", "w+");
    if(g_fp==NULL){
       printf("Error when try to use fopen!!\n");
    }
}

void get_call_stack(char *call_stack) {
    int static mmap_id=0;
    int nptrs;
    void *buffer[SIZE];
    ssize_t read;
    char *addr;
    int j;
    char **strings;

    nptrs = backtrace(buffer, SIZE);
    backtrace_symbols_fd(buffer, nptrs,STDOUT_FILENO);
    fflush(stdout);

    int i; // callstack_line_index;
    int k=0;
    const char* substring = getenv("APP");


    char *p;
    //while ((read = getline(&g_line, &len, g_fp)) != -1) {
    for(int callstack_line_index=0; callstack_line_index < nptrs; callstack_line_index++){
        read = getline(&g_line, &len, g_fp);
        p = strstr(g_line,substring);
        if(p){
          for(i=0;i<len;i++)
          {
	  	if(g_line[i] == '[')
		{
		     break;
		}
          }
          for(i=i+1; i<len;i++)
          {
		if(g_line[i] ==']')
                    break;
                call_stack[k] = g_line[i];
                k++;
	  }
          call_stack[k] = ':';
          k++;
       }
    }
    call_stack[k-1] = '\0';
}


static int
hook(long syscall_number,
			long arg0, long arg1,
			long arg2, long arg3,
			long arg4, long arg5,
			long *result)
{

        int static mmap_id=0;
        int i;
        struct timespec ts;
        char size[SIZE];
        char chunk_index[3];
        char temp_call_stack[SIZE];
        char call_stack[SIZE]="";
        unsigned long long remnant_size;
        int total_obj;
        unsigned long call_stack_hash;
        unsigned long g_nodemask;

	if (syscall_number == SYS_mmap) {

	       *result = syscall_no_intercept(syscall_number, arg0, arg1, arg2, arg3, arg4, arg5);

	       pthread_mutex_lock(&count_mutex);
	       clock_gettime(CLOCK_MONOTONIC, &ts);
               get_call_stack(call_stack);
               fprintf(stderr,"%s,%d\n",temp_call_stack, hash(temp_call_stack));

               if(arg1 > CHUNK_SIZE){
                    i = 0;
		    total_obj = arg1/CHUNK_SIZE;
		    remnant_size = arg1 - (total_obj * CHUNK_SIZE);

		    while(i < total_obj){
                         strcat(temp_call_stack,call_stack);
                         sprintf(size, ":%d", CHUNK_SIZE);
                         strcat(temp_call_stack, size);
                         sprintf(chunk_index, ":%d", i);
                         strcat(temp_call_stack, chunk_index);

                         if(check_address(hash(temp_call_stack))){
                             //fprintf(stderr,"binding to dram :%d\n",hash(temp_call_stack));
                             g_nodemask = 1;
                         }else{
                             g_nodemask = 4;
                         }
                         if(mbind((void *)*result + (i * CHUNK_SIZE), (unsigned long)CHUNK_SIZE, MPOL_BIND, &g_nodemask, 64, MPOL_MF_MOVE) == -1)
                         {
                             fprintf(stderr,"Error:%d\n",errno);
                             perror("Error description");
                         }

		         i++;

                         memset(&temp_call_stack[0], 0, sizeof(temp_call_stack));
                         memset(&size[0], 0, sizeof(size));
                         memset(&chunk_index[0], 0, sizeof(chunk_index));
		    }
		    if(remnant_size > 0){
                         strcat(temp_call_stack,call_stack);
                         sprintf(size, ":%d", remnant_size);
                         strcat(temp_call_stack, size);
                         sprintf(chunk_index, ":%d", i);
                         strcat(temp_call_stack, chunk_index);

                         if(check_address(hash(temp_call_stack))){
                             //fprintf(stderr,"binding to dram :%d\n",hash(temp_call_stack));
                             g_nodemask = 1;
                         }else{
                             g_nodemask = 4;
                         }
                         if(mbind((void *)*result + (i * CHUNK_SIZE), (unsigned long)remnant_size, MPOL_BIND, &g_nodemask, 64, MPOL_MF_MOVE) == -1)
                         {
                             fprintf(stderr,"Error:%d\n",errno);
                             perror("Error description");
                         }

		    }else{
                         strcat(temp_call_stack,call_stack);
                         sprintf(size, ":%d", CHUNK_SIZE);
                         strcat(temp_call_stack, size);
                         sprintf(chunk_index, ":%d", i);
                         strcat(temp_call_stack, chunk_index);

                         if(check_address(hash(temp_call_stack))){
                             //fprintf(stderr,"binding to dram :%d\n",hash(temp_call_stack));
                             g_nodemask = 1;
                         }else{
                             g_nodemask = 4;
                         }
                         if(mbind((void *)*result + (i * CHUNK_SIZE), (unsigned long)CHUNK_SIZE, MPOL_BIND, &g_nodemask, 64, MPOL_MF_MOVE) == -1)
                         {
                             fprintf(stderr,"Error:%d\n",errno);
                             perror("Error description");
                         }

		    }
	       }else{
                     strcat(temp_call_stack,call_stack);
                     sprintf(size, ":%d", arg1);
                     strcat(temp_call_stack, size);
                     sprintf(chunk_index, ":%d", i);
                     strcat(temp_call_stack, chunk_index);

                     if(check_address(hash(temp_call_stack))){
                         //fprintf(stderr,"binding to dram :%d\n",hash(temp_call_stack));
                         g_nodemask = 1;
                     }else{
                         g_nodemask = 4;
                     }
                     if(mbind((void *)*result, (unsigned long)arg1, MPOL_BIND, &g_nodemask, 64, MPOL_MF_MOVE) == -1)
                     {
                         fprintf(stderr,"Error:%d\n",errno);
                         perror("Error description");
                     }

	       }

   	       pthread_mutex_unlock(&count_mutex);

	       return 0;
	}else if(syscall_number == SYS_munmap){
		/* pass it on to the kernel */
		*result = syscall_no_intercept(syscall_number, arg0, arg1, arg2, arg3, arg4, arg5);
		clock_gettime(CLOCK_MONOTONIC, &ts);

		return 0;
	}else {
		/*
		 * Ignore any other syscalls
		 * i.e.: pass them on to the kernel
		 * as would normally happen.
		 */
		return 1;
	}
}

static __attribute__((constructor)) void
init(int argc, char * argv[])
{
    setvbuf(stdout, NULL, _IONBF, 0);  //avoid buffer from printf
    redirect_stdout("call_stack.txt");
    read_parameters_for_binding();
    intercept_hook_point = hook;
}
