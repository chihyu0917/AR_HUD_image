import time
import socket
import os
import datetime
import json

ip="127.0.0.1"
port=17414

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


# csv_path='1711944888.csv'
csv_path = '2023-05-18-09-10-10_23.csv'


lines=[]
if os.path.isfile(csv_path):
    fp = open(csv_path, "r")
    lines = lines+fp.readlines()
    fp.close()


timestamp_video_start=(json.loads(lines[0]))['Time']

line_count=0

#---------------find can head--------------------
while line_count<len(lines):
    line=lines[line_count]
    dict_this_line=json.loads(line)
    timestamp=dict_this_line['Time']
    if timestamp>=timestamp_video_start:
        break
    line_count=line_count+1
#------------------------------------------------

start_time_dif=time.time()-timestamp

#time.sleep(6)

while line_count<len(lines):
    line=lines[line_count]
    
    dict_this_line=json.loads(line)
    timestamp=dict_this_line.pop('Time',None)
    if timestamp>time.time()-start_time_dif:
        continue
    out_string=json.dumps(dict_this_line)
    sock.sendto(out_string.encode(), (ip, port))


    line_count=line_count+1
