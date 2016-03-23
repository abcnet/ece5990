import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time

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


# GPIO pin setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#define interrupt handlers
def GPIO17_callback(channel):
	GPIO.cleanup()
	sys.exit("Quitting Bounce Program")

#interrupt detection
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)


#initialize pygame
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))
black = 0, 0, 0
my_font = pygame.font.Font(None, 50)

resume_button = ('Resume', (160,120),(0,255,0))
panic_button = ('Panic stop', (160,120),(255,0,0))
quit_button = ('Quit', (160,200), (255,255,255))

def place_button(b):
	text_surface = my_font.render(b[0], True, b[2])
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




panic=False
while True:
	screen.fill(black)
	place_buttons(panic)
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
				sys.exit("Quitting Program")
			if 0<x<240 and 80<y<160:
				panic = not panic
	if panic:
		pass
		
	pygame.display.flip()

