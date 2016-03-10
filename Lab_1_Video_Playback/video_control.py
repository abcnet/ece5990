import RPi.GPIO as GPIO
import time
import subprocess
import sys

#setup runtime only for 10 seconds
maxTime = 10
startTime = time.time()


GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering 

# setup a GPIO for an input button...
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

f='/home/pi/fifo'
if (len(sys.argv)<=1):
    print 'No mplayer FIFO path specified. Using default {0}'.format(f)
else:
    f=sys.argv[1]
    print 'Using {0} as mplayer FIFO path'.format(f)

while ((time.time() - startTime) < maxTime):
	#time.sleep(0.00002) # short sleep for screen output if ( not GPIO.input(26)) ):


	# print GPIO.input(27), GPIO.input(23), GPIO.input(22), GPIO.input(17)

	if not GPIO.input(27):
		cmd = 'echo "pause" > {0}'.format(f)
		print subprocess.check_output(cmd, shell=True)
		print 'Pressed Pause Button'

	if not GPIO.input(23):
		cmd = 'echo "seek 10 0" > {0}'.format(f)
		print subprocess.check_output(cmd, shell=True)
		print 'Pressed FF button for 10 seconds'

	if not GPIO.input(22):
		cmd = 'echo "seek -10 0" > {0}'.format(f)
		print subprocess.check_output(cmd, shell=True)
		print 'Pressed RW 10 seconds button'

	if not GPIO.input(17):
		print 'Pressed Quit button'
		cmd = 'echo "quit 0" > {0}'.format(f)
		print subprocess.check_output(cmd, shell=True)
		break
