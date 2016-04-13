#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sched.h>
#include <sys/mman.h>
#include <string.h>
#include <wiringPi.h>

//LED pin - wiringPi pin 0 is BCM_GPIO_17
#define LED 21


#define MY_PRIORITY (49) /* we use 49 as the PRREMPT_RT use 50
                            as the priority of kernel tasklets
                            and interrupt handler by default */

#define MAX_SAFE_STACK (8*1024) /* The maximum stack size which is
                                   guaranteed safe to access without
                                   faulting */

#define NSEC_PER_SEC    (1000000000) /* The number of nsecs per sec. */

void stack_prefault(void) {

        unsigned char dummy[MAX_SAFE_STACK];

        memset(dummy, 0, MAX_SAFE_STACK);
        return;
}

int main(int argc, char* argv[])
{
        struct timespec t;
        struct sched_param param;
        int interval = 500000000; /* 500ms*/

        /* Declare ourself as a real time task */

        param.sched_priority = MY_PRIORITY;
        if(sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
                perror("sched_setscheduler failed");
                exit(-1);
        }

        /* Lock memory */

        if(mlockall(MCL_CURRENT|MCL_FUTURE) == -1) {
                perror("mlockall failed");
                exit(-2);
        }

        /* Pre-fault our stack */

        stack_prefault();

	clock_gettime(CLOCK_MONOTONIC ,&t);
        /* start after one second */
        t.tv_sec++;

	wiringPiSetup();
	pinMode(LED, OUTPUT);
	int on = 0;        

	while(1) {
                /* wait until next shot */
                clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &t, NULL);

                /* do the stuff */
		on ^= 1;
		digitalWrite (LED, on);     // On or off
			
                /* calculate next shot */
                t.tv_nsec += interval;

                while (t.tv_nsec >= NSEC_PER_SEC) {
                       t.tv_nsec -= NSEC_PER_SEC;
                        t.tv_sec++;
                }
   }
}
