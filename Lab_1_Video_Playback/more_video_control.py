import RPi.GPIO as GPIO
import time
import subprocess
import sys
import os
GPIO.cleanup()
GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering 

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

f='/home/pi/fifo'
if (len(sys.argv)<=1):
    print 'No mplayer FIFO path specified. Using default {0}'.format(f)
else:
    f=sys.argv[1]
    print 'Using {0} as mplayer FIFO path'.format(f)

def GPIO27_callback(channel):
	cmd = 'echo "pause" > {0}'.format(f)
	print "GPIO27 pressed"
	# os.system('echo  hello?')
	# print subprocess.check_output('echo  hello?', shell=True)
	print subprocess.check_output(cmd, shell=True)
	print "pause sent"



def GPIO23_callback(channel):
	cmd = 'echo "seek 10 0" > {0}'.format(f)
	print "GPIO23 pressed"
	# os.system('echo "asdfasdf" > /home/pi/fifo')
	print subprocess.check_output(cmd, shell=True)
	print "fast forward 10 seconds"

def GPIO22_callback(channel):
	cmd = 'echo "seek -10 0" > {0}'.format(f)
	print "GPIO22 pressed"
	print subprocess.check_output(cmd, shell=True)
	print "rewind 10 seconds"

# def GPIO17_callback(channel):
	# 

def GPIO26_callback(channel):
	print "GPIO26 pressed"
	cmd = 'echo "seek 30 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	print "forward 30 seconds"

def GPIO19_callback(channel):
	print "GPIO19 pressed"
	cmd = 'echo "seek -30 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	print "rewind 30 seconds"

GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)

try:
	print "Waiting for falling edge on port 17"
	GPIO.wait_for_edge(17, GPIO.FALLING)

	print "Falling edge detected on port 17"
	cmd = 'echo "quit 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	GPIO.cleanup()
	exit
except KeyboardInterrupt:
	GPIO.cleanup() # clean up GPIO on CTRL+C exit
 # clean up GPIO on normal exit
# while 1:
# 	try:
# 		pass
# 	except KeyboardInterrupt:
# 		GPIO.cleanup()
# GPIO.cleanup()


# while True:
# 	time.sleep(0.2) # short sleep for screen output if ( not GPIO.input(26)) ):

# 	if not GPIO.input(27):
# 		cmd = 'echo "pause" > {0}'.format(f)
# 		print subprocess.check_output(cmd, shell=True)
# 	if not GPIO.input(23):
# 		cmd = 'echo "seek 10 0" > {0}'.format(f)
# 		print subprocess.check_output(cmd, shell=True)
# 	if not GPIO.input(22):
# 		cmd = 'echo "seek -10 0" > {0}'.format(f)
# 		print subprocess.check_output(cmd, shell=True)
# 	if not GPIO.input(17):
# 		cmd = 'echo "quit 0" > {0}'.format(f)
# 		print subprocess.check_output(cmd, shell=True)
# 		break
# 	