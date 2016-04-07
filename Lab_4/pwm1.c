#include <stdio.h>
#include <wiringPi.h>

// LED Pin - wiringPi pin 0 is BCM_GPIO 17.
#define LED 21

int main (void)
{
  printf ("Blinking\n") ;

  wiringPiSetup();

  pinMode(LED, OUTPUT) ;

  for (;;)
  {
    digitalWrite (LED, 1) ;     // On
    delay (1) ;               // mS
    digitalWrite (LED, 0) ;     // Off
    delay (1) ;
  }
  return 0 ;
}
