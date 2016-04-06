import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time

#GPIO.cleanup()
dc=50
CHANNEL=5
freq=1

GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

# GPIO pin setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CHANNEL, GPIO.OUT)



# To create a PWM instance:
p = GPIO.PWM(CHANNEL, freq)
# To start PWM:
p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)
# To change the frequency:
# p.ChangeFrequency(freq) # where freq is the new frequency in Hz
# To change the duty cycle:
# p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0
# To stop PWM:




#define interrupt handlers
def GPIO17_callback(channel):
	p.stop()
	GPIO.cleanup()
	sys.exit("Quitting PWM Program")

def GPIO22_callback(channel):
	p.start(dc)

def GPIO23_callback(channel):
	p.stop()


#interrupt detection
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)


while True:
	pass
