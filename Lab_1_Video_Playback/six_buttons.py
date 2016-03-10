import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Set for broad com numbering not board numbering


#setup for 6 buttons
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        time.sleep(0.2) # short sleep for screen output 
	if ( not GPIO.input(27)):
        	print ('Button 13 has been pressed!')
        if ( not GPIO.input(23)):
		print ('Button 16 has been pressed!')
	if ( not GPIO.input(22)):
		print ('Button 15 has been pressed!')
	if ( not GPIO.input(17)):
		print ('Button 11 has been pressed!')
	if ( GPIO.input(19)):
		print ('Button L has been pressed!')
	if ( GPIO.input(26)):
		print ('Button R has been pressed!')
	else:
		print('')
