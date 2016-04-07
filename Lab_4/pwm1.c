#include <stdio.h>
#include <wiringPi.h>

// LED Pin - wiringPi pin 0 is BCM_GPIO 17.
#define LED 21

int main (void)
{
  printf ("Blinking\n");

  wiringPiSetup();

  pinMode(LED, OUTPUT);

  for (int i = 0;i<2;i++)
  {
    digitalWrite (LED, 1);     // On
    delay (1);               // mS
    printf ("Blinking\n");
    digitalWrite (LED, 0);     // Off
    delay (1);
    delay (30000);
  }
  return 0 ;
}
