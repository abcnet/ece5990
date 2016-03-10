import RPi.GPIO as GPIO
import time
import subprocess
import sys

maxTime = 10
startTime = time.time()

#while((time.time() - startTime) < maxTime):
#Setup Broadcom numbering NOT BOARD NUMBERING
GPIO.setmode(GPIO.BCM)

#Setup GPIO buttons as inputs
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# pause
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# ff10 seconds
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# rw10 seconds
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# quit
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# ff30 seconds
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# rw30 seconds

#setup FIFO file
f='/home/pi/fifo'
if (len(sys.argv)<=1):
    print 'No mplayer FIFO path specified. Using default {0}'.format(f)
else:
    f=sys.argv[1]
    print 'Using {0} as mplayer FIFO path'.format(f)

#Define GPIO interrupt handlers
def GPIO27_callback(channel):
	cmd = 'echo "pause" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	#print "GPIO27 pressed"

def GPIO23_callback(channel):
	cmd = 'echo "seek 10 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	#print "GPIO23 pressed"

def GPIO22_callback(channel):
	cmd = 'echo "seek -10 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	#print "GPIO22 pressed"

# def GPIO17_callback(channel):
# 	print "GPIO17 pressed"	
	
def GPIO19_callback(channel):
	cmd = 'echo "seek -30 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)
	#print "GPIO19 pressed"

def GPIO26_callback(channel):
	#print "GPIO25 pressed"
	cmd = 'echo "seek 30 0" > {0}'.format(f)
	print subprocess.check_output(cmd, shell=True)


GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)

#try:
#	print "Waiting for falling edge on port 17"
#	GPIO.wait_for_edge(17, GPIO.FALLING)
#	cmd = 'echo "quit 0" > {0}'.format(f)
#	print subprocess.check_output(cmd, shell=True)
#	print "Falling edge on port 17 captured"
#
#except KeyboardInterrupt:
#	GPIO.cleanup()

while(time.time() - startTime < maxTime):
	print "running for 10 seconds"

GPIO.cleanup()
sys.exit("Finished Time")
