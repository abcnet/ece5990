import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time

#dc_max = 8.5
#dc_min = 6.5
dc=7.5
dc_var = 7.5
CHANNEL = 19
freq=46.51
inc = 0.1

GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

# GPIO pin setup
GPIO.setup(CHANNEL, GPIO.OUT)

# To create a PWM instance:
p = GPIO.PWM(CHANNEL, freq)
# Initialize servo to not moving
p.start(dc)

# To change the frequency:
# p.ChangeFrequency(freq) # where freq is the new frequency in Hz
# To change the duty cycle:
# p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0

time.sleep(3)
x = 1
while True:
	while x<=10:
		dc_var += inc
		p.start(dc_var)
		print dc_var
		ts = time.time()
		while (time.time() - ts <= 3.0):
			pass		
		x +=1
	dc_var = dc
	p.start(dc)
	print dc_var
	print "Done counter-clockwise"
	x = 1	
	while x<=10:
		dc_var -= inc
		p.start(dc_var)
		print dc_var
		ts = time.time()	
		while (time.time() - ts <= 3.0):
			pass
		x+=1
	print "Done clockwise"
	p.start(dc)
	redo = input('Redo Run?(y/n): ')
	if (redo == 'n'):
		sys.exit("quitting")
	else:
		pass
