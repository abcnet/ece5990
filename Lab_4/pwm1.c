#include <stdio.h>
#include <wiringPi.h>

// LED Pin - wiringPi pin 0 is BCM_GPIO 17.
#define LED 21

int main (void)
{
  printf ("Blinking\n");

  wiringPiSetup();

  pinMode(LED, OUTPUT);

  for (int i = 0;i<10;i++)
  {
    digitalWrite (LED, 1);     // On
    delay (500);               // mS
    printf ("Blinking\n");
    digitalWrite (LED, 0);     // Off
    delay (500);
    //delay (30000);
  }
  return 0 ;
}
