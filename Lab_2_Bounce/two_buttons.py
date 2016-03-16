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

my_buttons = {'Start':(60,200),'Quit':(260,200)}
def place_buttons():
	for my_text, text_pos in my_buttons.items():
		text_surface = my_font.render(my_text, True, (255,255,255))
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
place_buttons()

pygame.display.flip()



size = width, height = 320, 240

speed1 = [5.0,5.0]
speed2 = [3.0,3.0]
black = 0, 0, 0

ball1 = pygame.image.load("image/magic_ball.png")
ball2 = pygame.image.load("image/soccer_ball.png")
ball1rect = ball1.get_rect()
ball2rect = ball2.get_rect()
d1=ball1rect.right-ball1rect.left
d2=ball2rect.right-ball2rect.left

# colliding=True
newspeed1=[2.0,2.0]
newspeed2=[1.0,1.0]



start=False
while True:
	screen.fill(black)
	place_buttons()
	for event in pygame.event.get():
		

		if(event.type == pygame.MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
			print pos
			# screen.fill(black)
			# text_surface = my_font.render('Hit at '+str(pos), True, (255,255,255))
			# # subprocess.check_output('echo "{0}" >> log'.format(str(pos)), shell=True)
			# screen.blit(text_surface,text_surface.get_rect(center=(160,120)))
			place_buttons()
			# pygame.display.flip()
			x,y=pos
			if x>200 and y>180:
				GPIO.cleanup()
				sys.exit("Quitting Bounce Program")
			if x<120 and y>180:
				start = True
	if start:
		ball1rect = ball1rect.move(speed1)
		ball2rect = ball2rect.move(speed2)
		newspeed1[0]=speed1[0]
		newspeed1[1]=speed1[1]
		newspeed2[0]=speed2[0]
		newspeed2[1]=speed2[1]
		c21=ball2rect.left+ball2rect.right
		c22=ball2rect.top+ball2rect.bottom
		c11=ball1rect.left+ball1rect.right
		c12=ball1rect.top+ball1rect.bottom
		collide = (ball2rect.left+ball2rect.right-ball1rect.left-ball1rect.right)**2+\
		(ball2rect.top+ball2rect.bottom-ball1rect.top-ball1rect.bottom)**2<=\
		d1**2+d2**2


		if collide:
		    # if not colliding:
			coeff = ((speed1[0]-speed2[0])*(c11-c21)+(speed1[1]-speed2[1])*(c12-c22))*1.0/((c11-c21)**2+(c12-c22)**2)
			dvx=coeff*(c11-c21)
			dvy=coeff*(c12-c22)
			newspeed1[0]=speed1[0]-dvx*2*d2*1.0/(d1+d2)
			newspeed1[1]=speed1[1]-dvy*2*d2*1.0/(d1+d2)
			newspeed2[0]=speed2[0]+dvx*2*d1*1.0/(d1+d2)
	    	newspeed2[1]=speed2[1]+dvy*2*d1*1.0/(d1+d2)
		    	# colliding = True

		# else:
		# 	colliding = False



		if ball1rect.left < 0 or ball1rect.right > width: 
			speed1[0] = -speed1[0]
			newspeed1[0] = -newspeed1[0]
		if ball1rect.top < 0 or ball1rect.bottom > height: 
			speed1[1] = -speed1[1]
			newspeed1[1] = -newspeed1[1]

		if ball2rect.left < 0 or ball2rect.right > width: 
			speed2[0] = -speed2[0]
			newspeed2[0] = -newspeed2[0]
		if ball2rect.top < 0 or ball2rect.bottom > height: 
			speed2[1] = -speed2[1]
			newspeed2[1] = -newspeed2[1]
		distance_no = (c11+speed1[0]-c21-speed2[0])**2+(c12+speed1[1]-c22-speed2[1])**2
		distance_yes = (c11+newspeed1[0]-c21-newspeed2[0])**2+(c12+newspeed1[1]-c22-newspeed2[1])**2
		if collide and distance_yes > distance_no:
			speed1[0]=newspeed1[0]
			speed1[1]=newspeed1[1]

			speed2[0]=newspeed2[0]
			speed2[1]=newspeed2[1]

		# screen.fill(black)
		screen.blit(ball1, ball1rect)
		screen.blit(ball2, ball2rect)
		
		pygame.display.flip()
