import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time



CHANNEL1 = 19
CHANNEL2 = 16
freq = 46.51

GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

# GPIO pin setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CHANNEL1, GPIO.OUT)



# To create a PWM instance:
p1 = GPIO.PWM(CHANNEL1, freq)
p2 = GPIO.PWM(CHANNEL2, freq)
# To start PWM:
# p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)
# To change the frequency:
# p.ChangeFrequency(freq) # where freq is the new frequency in Hz
# To change the duty cycle:
# p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0
# To stop PWM:

def drive_servo(servo_number, direction):
	if servo_number==1:
		p=p1
	elif servo_number==2:
		p=p2
	else:
		print "error"
		return
	if direction==0:
		p.stop()
	elif direction<0:
		p.start()
		p.ChangeFrequency(1000.0/21.7)
		p.ChangeDutyCycle(1.7/21.7)
	elif direction>0:
		p.start()
		p.ChangeFrequency(1000.0/21.3)
		p.ChangeDutyCycle(1.3/21.3)
	else:
		print "error"


#define interrupt handlers
def GPIO17_callback(channel):
	p1.stop()
	p2.stop()
	GPIO.cleanup()
	sys.exit("Quitting Program")

def GPIO22_callback(channel):
	p1.stop()
	p2.stop()

# def GPIO23_callback(channel):
# 	p.start(dc)
# 	p.ChangeFrequency(freq)


#interrupt detection
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)


while True:
	servo_number = raw_input("Chooese server (1 or 2): ")
	direction = raw_input("Chooese direction (-1, 0 or 1): ")
	drive_servo(servo_number, direction)