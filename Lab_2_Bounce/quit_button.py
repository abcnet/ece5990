import pygame
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import time

# GPIO.cleanup()
GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

# GPIO pin setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#define interrupt handlers
def GPIO17_callback(channel):
	GPIO.cleanup()
        sys.exit("Quitting Bounce Program")

#interrupt detection
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

#setup touchscreen io
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#initialize pygame
pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))
black = 0,0,0

my_font = pygame.font.Font(None, 50)

my_buttons = {'Quit':(250,190)}
WHITE = (255,255,255)

screen.fill(black)	#fill screen empty

for my_text, text_pos in my_buttons.items():
	text_surface = my_font.render(my_text, True, WHITE)
	rect = text_surface.get_rect(center=text_pos)
	screen.blit(text_surface, rect)
	
pygame.display.flip()

pos = 0;
while True:
	screen.fill(black)	#fill screen empty

	for my_text, text_pos in my_buttons.items():
		text_surface = my_font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
	
	pygame.display.flip()

	for event in pygame.event.get():
		if(event.type == pygame.MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
		elif(event.type == pygame.MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
	x = pos(0)
	y = pos(1)
	if (y > 120):
		if (x > 160):
			sys.exit("quitting")

print "done"
