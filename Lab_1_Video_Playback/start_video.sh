#! /bin/bash

python /home/pi/Desktop/more_video_control_cb.py &
sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -slave -quiet -vo sdl -framedrop -input file=/home/pi/fifo /home/pi/Desktop/Lab_1_Video_Playback/vid.h264
