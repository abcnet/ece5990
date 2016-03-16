import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time

GPIO.cleanup()
dc_max = 8.5
dc_min = 6.5
dc=7.5
dc_var = 7.5
CHANNEL = 19
freq=46.51
inc = 0.1


GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

# GPIO pin setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CHANNEL, GPIO.OUT)



# To create a PWM instance:
p = GPIO.PWM(CHANNEL, freq)
# Initialize servo to not moving
p.start(dc)



# To change the frequency:
# p.ChangeFrequency(freq) # where freq is the new frequency in Hz
# To change the duty cycle:
# p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0
# To stop PWM:




#define interrupt handlers
def GPIO17_callback(channel):
	p.stop()
	GPIO.cleanup()
	sys.exit("Quitting Bounce Program")

def GPIO22_callback(channel):
	p.stop()

def GPIO23_callback(channel):
	p.start(dc)
	p.ChangeFrequency(freq)


#interrupt detection
#GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)

time.sleep(5)
while True:
	for x in range(1,11):
		time.sleep(1)
		dc_var += inc
		p.ChangeDutyCycle(dc_var)
		print x
		ts = time.time()
		p.start(dc_var)
		while (time.time() - ts <= 3.0):
			pass
		p.stop()
	dc_var = dc
	print "Done counter-clockwise"
	for x in range(1,10):
		time.sleep(1)
		dc_var -= inc
		p.ChangeDutyCycle(dc_var)
		ts = time.time()	
		p.start(dc_var)
		while (time.time() - ts <= 3.0):
			pass
		p.stop()
	print "Done clockwise"
	break
