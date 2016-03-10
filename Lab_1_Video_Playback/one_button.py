import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering 

# setup a GPIO for an input button...
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	time.sleep(0.2) # short sleep for screen output 
	if ( not GPIO.input(27)) :
		print ('Button 13 hass been pressed!')
	else:
		print('')
