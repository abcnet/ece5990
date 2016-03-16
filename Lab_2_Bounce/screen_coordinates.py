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


#initialize pygame
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))
black = 0, 0, 0
my_font = pygame.font.Font(None, 50)

my_buttons = {'Quit':(260,200)}
def place_buttons():
	for my_text, text_pos in my_buttons.items():
		text_surface = my_font.render(my_text, True, (255,255,255))
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
place_buttons()

pygame.display.flip()

while True:
	for event in pygame.event.get():
		

		if(event.type == pygame.MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
			print pos
			screen.fill(black)
			text_surface = my_font.render('Hit at '+str(pos), True, (255,255,255))
			subprocess.check_output('echo "{0}" >> hit_log'.format(str(pos)), shell=True)
			screen.blit(text_surface,text_surface.get_rect(center=(160,120)))
			place_buttons()
			pygame.display.flip()
			x,y=pos
			if x>200 and y>180:
				GPIO.cleanup()
				sys.exit("Quitting Bounce Program")

		# elif(event.type == pygame.MOUSEBUTTONUP):
		# 	pos = pygame.mouse.get_pos()
		# 	print pos
		# 	screen.fill(black)
		# 	screen.blit(my_font.render('Hit at '+str(pos), True, (255,255,255)),text_surface.get_rect(center=(100,120)))
		# 	place_buttons()
		# 	pygame.display.flip()
		

	# if y < 110:
	# 	if x < 160:
	# 		pause()
	# 	else:
	# 		quit()
	# elif y < 210:
	# 	if x < 160:
	# 		fast10()
	# 	else:
	# 		rewind10()
	# else:
	# 	if x < 160:
	# 		fast30()
	# 	else:
	# 		rewind30()
