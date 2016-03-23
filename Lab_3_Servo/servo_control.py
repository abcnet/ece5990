import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time

#dc_max = 8.5
#dc_min = 6.5
cw=1.3
no=1.5
ccw=1.7

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


# To change the frequency:
# p.ChangeFrequency(freq) # where freq is the new frequency in Hz
# To change the duty cycle:
# p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0


while True:
	for i in range(10):
		pulse = no-0.02*i
		p.start(pulse/(20+pulse)*100.0)
		p.ChangeFrequency(1000.0/(20+pulse))
		print "Clockwise speed {0}/10".format(i+1)
		time.sleep(3)
	# dc_var = dc
	# p.start(dc)
	# print dc_var
	print "Done clockwise"
	# x = 1	
	for i in range(10):
		pulse = no+0.02*i
		p.start(pulse/(20+pulse)*100.0)
		p.ChangeFrequency(1000.0/(20+pulse))
		print "Counter-lockwise speed {0}/10".format(i+1)
		time.sleep(3)
	print "Done coutner-clockwise"
	p.start(dc)
	redo = raw_input('Redo Run?(y/n): ')
	if (redo == 'n'):
		p.stop()
		sys.exit("quitting")
	else:
		pass
