#!/bin/bash

CLIP_NAME=2022-09-19-12-53-54_62_0155-0249

gnome-terminal --tab -e "sh -c 'sleep 2 ; python3 deepstream_detection_udp.py -s=file:///home/nvidia/test_all/video/${CLIP_NAME}_30FPS.mp4 -c=/home/nvidia/test_all/config_infer_primary_yoloV8_thermal.txt -w=900 -e=720 --window_x=190 --window_y=200;sleep 10' "
gnome-terminal --tab -e "sh -c 'sleep 5 ; python3 udp_sender.py --csv_name=csv/${CLIP_NAME}.csv' "
python3 receive_detection_fcw.py
