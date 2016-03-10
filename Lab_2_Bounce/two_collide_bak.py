
import pygame
import RPi.GPIO as GPIO
import time
import subprocess
import sys
import os
os.putenv('SDL_FBDEV', '/dev/fb0') 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# GPIO.cleanup()
GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering 

# GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def GPIO17_callback(channel):
	print "exiting"
	GPIO.cleanup() 
	sys.exit("Quiting bounce program")


GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)




pygame.init()
size = width, height = 320, 240
speed1 = [2,2]
speed2 = [1,1]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("image/magic_ball.png")
ball2 = pygame.image.load("image/soccer_ball.png")
ball1rect = ball1.get_rect()
ball2rect = ball2.get_rect()
d1=ball1rect.right-ball1rect.left
d2=ball2rect.right-ball2rect.left

colliding=True


while 1:
	ball1rect = ball1rect.move(speed1)
	ball2rect = ball2rect.move(speed2)
	
	c21=ball2rect.left+ball2rect.right
	c22=ball2rect.top+ball2rect.bottom
	c11=ball1rect.left+ball1rect.right
	c12=ball1rect.top+ball1rect.bottom


	if (ball2rect.left+ball2rect.right-ball1rect.left-ball1rect.right)**2+\
	(ball2rect.top+ball2rect.bottom-ball1rect.top-ball1rect.bottom)**2<=\
	d1**2+d2**2:
	    if not colliding:
	    	coeff = ((speed1[0]-speed2[0])*(c11-c21)+(speed1[1]-speed2[1])*(c12-c22))*1.0/((c11-c21)**2+(c12-c22)**2)
	    	dvx=coeff*(c11-c21)
	    	dvy=coeff*(c12-c22)
	    	speed1[0]=speed1[0]-dvx
	    	speed1[1]=speed1[1]-dvy
	    	speed2[0]+=dvx
	    	speed2[1]+=dvy
	    	colliding = True

	else:
		colliding = False



	if ball1rect.left < 0 or ball1rect.right > width: speed1[0] = -speed1[0]
	if ball1rect.top < 0 or ball1rect.bottom > height: speed1[1] = -speed1[1]

	if ball2rect.left < 0 or ball2rect.right > width: speed2[0] = -speed2[0]
	if ball2rect.top < 0 or ball2rect.bottom > height: speed2[1] = -speed2[1]

	screen.fill(black)
	screen.blit(ball1, ball1rect)
	screen.blit(ball2, ball2rect)
	pygame.display.flip()



# import pygame
# import os
# os.putenv('SDL_FBDEV', '/dev/fb1') 
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
# pygame.init()
# pygame.mouse.set_visible(False)
# screen = pygame.display.set_mode((320, 240))
# my_font = pygame.font.Font(None, 50)
# my_buttons = { 'button1':(80,180), 'button2':(240,180)}
# for my_text, text_pos in my_buttons.items():
# 	text_surface = my_font.render(my_text, True, WHITE)
# 	rect = text_surface.get_rect(center=text_pos)
# 	screen.blit(text_surface, rect)
# Pygame.display.flip()

# while True:
# 	for event in pygame.event.get():
# 		if(event.type is MOUSEBUTTONDOWN):
# 			pos = pygame.mouse.get_pos()
# 		elif(event.type is MOUSEBUTTONUP):
# 			pos = pygame.mouse.get_pos()
# 	x,y = pos
# 	if y > 120:
# 		if x < 160:
# 			print "button1 pressed"
# 		else:
# 			print "button2 pressed"