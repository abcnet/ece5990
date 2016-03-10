
prompt_text = "Enter a command (e.g. pause, quit): "
import subprocess

# Use a python subprocess to execute some 'echo' commands...
# cmd = 'echo "Hello There!" > /home/jfs9/py_tests_v2/test_file'
# print subprocess.check_output(cmd, shell=True)
import sys

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
f='/home/pi/fifo'
if (len(sys.argv)<=1):
    print 'No mplayer FIFO path specified. Using default {0}'.format(f)
else:
    f=sys.argv[1]
    print 'Using {0} as mplayer FIFO path'.format(f)
# subprocess.check_output("rm {0}".format(f), shell=True)
# subprocess.check_output("mkfifo {0}".format(f), shell=True)

while True:
    user_in = raw_input(prompt_text)
    if user_in=='quit':
    	break
    cmd = 'echo "{1}" > {0}'.format(f,user_in)
    print subprocess.check_output(cmd, shell=True)
    # call(c.split())

    