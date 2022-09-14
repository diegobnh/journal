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
#include <signal.h>
#include <sys/time.h>
#define _GNU_SOURCE
#include <pthread.h>
#define SIZE 4096
#include <sys/resource.h> 
#include <numaif.h>
#include <sys/types.h>


static unsigned long g_nodemask;
static sig_atomic_t g_running = 1;
pthread_t thread_test;

static void __attribute__ ((constructor)) init_lib(void);
static void __attribute__((destructor)) exit_lib(void);


void init_lib(void)
{
	fprintf(stderr, "init_lib()\n");
}


void exit_lib(void)
{
        g_running=0;

        fprintf(stderr, "exit_lib()\n");
}

static int
hook(long syscall_number,
			long arg0, long arg1,
			long arg2, long arg3,
			long arg4, long arg5,
			long *result)
{
	if (syscall_number == SYS_mmap) {

		*result = syscall_no_intercept(syscall_number, arg0, arg1, arg2, arg3, arg4, arg5);
		if(arg1 > 100000000000){
			g_nodemask = 4;
			fprintf(stderr,"Bind to PMEM\n");
                }else{
			g_nodemask = 1;
			fprintf(stderr,"Bind to DRAM\n");
                }
		if(mbind((void *)*result, (unsigned long)arg1, MPOL_BIND, &g_nodemask, 64, MPOL_MF_MOVE) == -1)
                {
                      fprintf(stderr,"Error:%d\n",errno);
                      perror("Error description");
                 }
		return 0;
	}else if(syscall_number == SYS_munmap){
		*result = syscall_no_intercept(syscall_number, arg0, arg1, arg2, arg3, arg4, arg5);

		return 0;
	}else {
		return 1;
	}
}

void *thread_test_function(void * _args)
{
	while(g_running){
		fprintf(stderr, "Cleaning page cache!!\n");
		sync();
		int fd = open("/proc/sys/vm/drop_caches", O_WRONLY);
		write(fd, "1", 1);
		close(fd);
		sleep(10);
	}

}

static __attribute__((constructor)) void
init(int argc, char * argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);  //avoid buffer from printf
	intercept_hook_point = hook;
	//pthread_create(&thread_test, NULL, thread_test_function, NULL);
}

