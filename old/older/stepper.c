/************

Raspberry Pi Micro-stepping demo
using GPIO connected to a L298 I.C.

Author: Daniel Perron
Date:   7 Septembre 2014

External library  :
   PIGPIO    http://abyz.co.uk/rpi/pigpio/download.html

How to compile :

gcc -o stepper stepper.c  -lm -lpthread -lpigpio -lrt


GPL License

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

*******************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sched.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <pthread.h>
#include <pigpio.h>
#include <signal.h>


// =========   GPIO  IO DEFINITION

#define STEP_A  17
#define STEP_AN 18 
#define STEP_B  22
#define STEP_BN 25


#define PWM_A  23
#define PWM_B  24

#define MICROSTEP   10

long  StepperDelay = 50000/MICROSTEP;

#define STEP_PER_REVOLUTION 200



// BCM2708 DEFINITION  FOR MEMORY ACCESS



#define BCM2708_PERI_BASE        0x20000000
#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */

#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

int  mem_fd;
void *gpio_map;

// I/O access
volatile unsigned long *gpio;

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

// 32bit parallel mode  gpio handling

#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0
#define GPIO_READ  *(gpio + 13)



// ===========   STEPPER  DEFINITION



#define MICROSTEP_PER_REVOLUTION (STEP_PER_REVOLUTION * MICROSTEP)
#define CoilTableSize  (4 * MICROSTEP)



unsigned long StepperCoil[CoilTableSize];
unsigned char StepperAPWM[CoilTableSize];
unsigned char StepperBPWM[CoilTableSize];

unsigned long StepperMask = (1<<STEP_A) | (1<<STEP_AN) | (1<<STEP_B) | ( 1<<STEP_BN);

volatile long StepperPosition = 0;
volatile long TargetPosition = 0;
volatile int  StepperReadyFlag = 1;

pthread_mutex_t StepperThread_mutex;
pthread_mutex_t Stepper_mutex;
pthread_t StepperThreadId;

// ============   FUNCTION

void set_max_priority(void) {
  struct sched_param sched;
  memset(&sched, 0, sizeof(sched));
  // Use FIFO scheduler with highest priority for the lowest chance of the kernel context switching.
  sched.sched_priority = sched_get_priority_max(SCHED_FIFO);
  sched_setscheduler(0, SCHED_FIFO, &sched);
}

void set_default_priority(void) {
  struct sched_param sched;
  memset(&sched, 0, sizeof(sched));
  // Go back to default scheduler with default 0 priority.
  sched.sched_priority = 0;
  sched_setscheduler(0, SCHED_OTHER, &sched);
}



// ======= stepper thread



void SetStepper(unsigned long  StepperMicroStep)
{
  int  index = StepperMicroStep % CoilTableSize;

  GPIO_CLR= StepperMask & ~ StepperCoil[index];
  GPIO_SET= StepperCoil[index];
  gpioPWM(PWM_A, StepperAPWM[index]);
  gpioPWM(PWM_B, StepperBPWM[index]);
/*  printf("Position = %d Index = %d  PWA:%d PWB:%d",StepperMicroStep,index,StepperAPWM[index],StepperBPWM[index]);
  if(StepperCoil[index] & (1 << STEP_A)) printf(" A+ ");
  if(StepperCoil[index] & (1 << STEP_AN)) printf(" A- ");
  if(StepperCoil[index] & (1 << STEP_B)) printf(" B+ ");
  if(StepperCoil[index] & (1 << STEP_BN)) printf(" B- ");
  printf("\n");
*/
}


int exitFlag=0;
int ThreadReturn;
void*  StepperThreadFunction(void  * arg )
{
  long ltemp;
  
  set_max_priority();

  while(!exitFlag)
  {

   // Lock  position
   pthread_mutex_lock(&Stepper_mutex);

   if(TargetPosition == StepperPosition)
     {
        StepperReadyFlag=1;
        pthread_mutex_unlock(&Stepper_mutex);
        break;
      }
   StepperReadyFlag=0;
   if(TargetPosition < StepperPosition)
      StepperPosition--;
    else
      StepperPosition++;
    ltemp = StepperPosition;
    pthread_mutex_unlock(&Stepper_mutex);
    SetStepper(ltemp);
    // Set Current Position
    usleep(StepperDelay);
   }

//   printf("Thread close \n");
   set_default_priority();
   pthread_mutex_unlock(&StepperThread_mutex);
   pthread_exit(&ThreadReturn);
  return NULL;
}

//  FUNCTION


long GetStepperPosition(void)
{
  long ltemp;
  pthread_mutex_lock(&Stepper_mutex);
    ltemp = StepperPosition;
  pthread_mutex_unlock(&Stepper_mutex);
  return ltemp;
}


void MoveStepper(long value)
{
  // Lock mutex to  create Thread
  pthread_mutex_lock(&StepperThread_mutex);

  // Set  new Target position
  TargetPosition += value;

   // create the thread to move stepper
    int err = pthread_create(&StepperThreadId, NULL, &StepperThreadFunction, NULL);
        if (err != 0)
           {
             printf("\ncan't create thread :[%s]", strerror(err));
             pthread_mutex_unlock(&StepperThread_mutex);
           }
}



void BuildCoilTable(void)
{
  int loop;

  // Set first coil
  for(loop=0;loop<(CoilTableSize/2);loop++)
     StepperCoil[loop]= 1 << STEP_A;
  for(;loop<CoilTableSize;loop++)
     StepperCoil[loop]= 1 << STEP_AN;

  // Set second coil
  for(loop=0;loop<(CoilTableSize/2);loop++)
     StepperCoil[(loop + CoilTableSize/4) % CoilTableSize]|= 1 << STEP_B;
  for(;loop<CoilTableSize;loop++)
     StepperCoil[(loop + CoilTableSize/4) % CoilTableSize]|= 1 << STEP_BN;


   // Set Power to coil
   for(loop=0;loop<CoilTableSize;loop++)
    {
      unsigned char _temp;
      double sinV = fabs(sin(M_PI * loop / (CoilTableSize/2.0)));
      _temp= (unsigned char) floor( 255.0 * sqrt(sinV));
      StepperAPWM[loop]= _temp;
      StepperBPWM[(loop + MICROSTEP) % CoilTableSize]= _temp;
    }
}


void setup_io()
{
   /* open /dev/mem */
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
      printf("can't open /dev/mem \n");
      exit(-1);
   }

   /* mmap GPIO */
   gpio_map = mmap(
      NULL,             //Any adddress in our space will do
      BLOCK_SIZE,       //Map length
      PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
      MAP_SHARED,       //Shared with other processes
      mem_fd,           //File to map
      GPIO_BASE         //Offset to GPIO peripheral
   );

   close(mem_fd); //No need to keep mem_fd open after mmap

   if (gpio_map == MAP_FAILED) {
      printf("mmap error %d\n", (int)gpio_map);//errno also set!
      exit(-1);
   }

   // Always use volatile pointer!
   gpio = (volatile unsigned long *)gpio_map;

} // setup_io

// exit handler.  Just kill the thread 
void   bye(void)
     {
       exitFlag=1;
       puts ("\nGoodbye, cruel world....");
       usleep(100000);
     }

// Control-C handler.  Somehow the pigpio unhandle it properly
void MyCtrlC(int sig)
{
  exitFlag=1;
}


int main(void)
{
   int loop;

   printf("Raspberry Pi micro-stepping demo with L298 driver\n");
   printf("(c) Daniel Perron Sept.2014\n");
   printf("Micro-step= %d  (%d steps/turn)\n\n",MICROSTEP, MICROSTEP * STEP_PER_REVOLUTION );


   // initialize pigpio
   gpioInitialise();

   // create exit handler
   atexit(bye);
   signal(SIGINT, MyCtrlC);


   //  memory map GPIO. This way I could use GPIO in Parallel  mode.
   setup_io();

   //  Create Stepper table
   BuildCoilTable();

//   printf("GPIO Mask : %08lX\n", StepperMask);
//   for(loop=0;loop< CoilTableSize; loop++)
//    printf("%d: %08lX %03d %03d\n", loop, StepperCoil[loop], StepperAPWM[loop],StepperBPWM[loop]);


   // set PWM

   gpioSetMode(PWM_A, PI_OUTPUT);
   gpioSetMode(PWM_B, PI_OUTPUT);
   gpioSetPWMfrequency(PWM_A, 100000);
   gpioSetPWMfrequency(PWM_B, 100000);
   gpioSetPWMrange(PWM_A,255);
   gpioSetPWMrange(PWM_B,255);


   // set GPIO OUTPUT

   INP_GPIO(STEP_A);
   OUT_GPIO(STEP_A);
   INP_GPIO(STEP_AN);
   OUT_GPIO(STEP_AN);
   INP_GPIO(STEP_B);
   OUT_GPIO(STEP_B);
   INP_GPIO(STEP_BN);
   OUT_GPIO(STEP_BN);

   // put all Coil to 0
   GPIO_CLR=StepperMask;



   int p;
   while(!exitFlag)
   {

     printf("Stepper position %ld.   Number of step to move (0=exit) ?",GetStepperPosition());

     if(scanf("%d",&p)==1)
      {
         if(p==0) break;
        MoveStepper(p);

        MoveStepper(0); // this will just wait until is done.
      }
   }

   usleep(100000);
   GPIO_CLR=StepperMask;

   return 0;
}
