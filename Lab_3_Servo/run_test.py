import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time
import threading
# code for setting up two threads from http://stackoverflow.com/questions/6286235/terminate-multiple-threads-when-any-thread-completes-a-task

#setup touchscreen io
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


CHANNEL1 = 19
CHANNEL2 = 16
freq = 46.51
cw=1.3
no=1.5
ccw=1.7
# GPIO.cleanup()
GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

# GPIO pin setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CHANNEL1, GPIO.OUT)
GPIO.setup(CHANNEL2, GPIO.OUT)
# GPIO.cleanup()




#define interrupt handlers
def GPIO17_callback(channel):
	GPIO.cleanup()
	sys.exit("Quitting Bounce Program")

#interrupt detection
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
# cw_char = u"\u21BB"
ccw_char = u"\u21BA"

#initialize pygame
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))
black = 0, 0, 0
my_font = pygame.font.Font(None, 50)

resume_button = ('Resume', (160,120),(0,255,0))
panic_button = ('Panic stop', (160,120),(255,0,0))
quit_button = ('Quit', (160,200), (255,255,255))

p1 = GPIO.PWM(CHANNEL1, freq)
p2 = GPIO.PWM(CHANNEL2, freq)
pulses=[no,no]
d=['STOP','STOP']
def drive_servo(servo_number, direction):
	if servo_number==1:
		p=p1
	elif servo_number==2:
		p=p2
	else:
		print "error"
		return
	if direction==0:
		if servo_number==1:
			pulses[0]=no
			d[0]='STOP'
		else:
			pulses[1]=no
			d[1]='STOP'
		p.start(no/(20+no)*100.0)
		p.ChangeFrequency(1000.0/(20+no))
	elif direction<0:
		if servo_number==1:
			pulses[0]=ccw
			d[0]='<==='
		else:
			pulses[1]=ccw
			d[1]='<==='
		p.start(ccw/(20+ccw)*100.0)
		p.ChangeFrequency(1000.0/(20+ccw))
		# p.ChangeDutyCycle(1.7/21.7)
	elif direction>0:
		if servo_number==1:
			pulses[0]=cw
			d[0]='===>'
		else:
			pulses[1]=cw
			d[1]='===>'
		p.start(cw/(20+cw)*100.0)
		p.ChangeFrequency(1000.0/(20+cw))
		# p.ChangeDutyCycle(1.3/21.3)
	else:
		print "error"

def place_button(b, font=my_font):
	text_surface = font.render(b[0], True, b[2])
	rect = text_surface.get_rect(center=b[1])
	screen.blit(text_surface, rect)

def place_buttons(panicked=False):
	place_button(quit_button)
	if panicked:
		place_button(resume_button)
	else:
		place_button(panic_button)

place_buttons()

pygame.display.flip()



size = width, height = 320, 240


black = 0, 0, 0
kill = False
def func():
	drive_servo(1, -1)
	drive_servo(2, 1)
	time.sleep(5)

	drive_servo(1,0)
	drive_servo(2,0)
	time.sleep(3)

	drive_servo(1, 1)
	drive_servo(2, -1)
	time.sleep(5)

	drive_servo(1,0)
	drive_servo(2,0)
	time.sleep(3)

	drive_servo(1, 1)
	drive_servo(2, 1)
	time.sleep(5)

	drive_servo(1,0)
	drive_servo(2,0)
	time.sleep(3)

	drive_servo(1, -1)
	drive_servo(2, -1)
	time.sleep(5)

	drive_servo(1,0)
	drive_servo(2,0)
	kill=True
	



thread = threading.Thread(target=func)
thread.start()

panic=False
while not kill:
	screen.fill(black)
	place_buttons(panic)
	place_button(('Servo 1: {0}, Servo 2: {1}'.format(d[0],d[1]), (160,40), (255,255,255)),\
	 font=pygame.font.Font(None, 30))
	for event in pygame.event.get():
		
		if(event.type == pygame.MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
			print pos
			# screen.fill(black)
			# text_surface = my_font.render('Hit at '+str(pos), True, (255,255,255))
			# # subprocess.check_output('echo "{0}" >> log'.format(str(pos)), shell=True)
			# screen.blit(text_surface,text_surface.get_rect(center=(160,120)))
			
			# pygame.display.flip()
			x,y=pos
			if 80<x<240 and y>180:
				GPIO.cleanup()
				kill = True
				subprocess.check_output("kill -9 {0}".format(os.getpid()), shell=True)
				sys.exit("Quitting Program")
			if 0<x<240 and 80<y<160:
				panic = not panic
			if panic:
				p1.stop()
				p2.stop()
			else:
				
				p1.start(pulses[0]/(20+pulses[0])*100.0)
				p1.ChangeFrequency(1000.0/(20+pulses[0]))
				p2.start(pulses[1]/(20+pulses[1])*100.0)
				p2.ChangeFrequency(1000.0/(20+pulses[1]))
		
	pygame.display.flip()

