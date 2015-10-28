#! /usr/bin/env python
import logging
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

h = "mit.edu"
ansv=[]
last_src = None

for ttl in range(1,65):
	
	pk = IP(dst=h, ttl = ttl) / ICMP()
	ans, unans= sr(pk, timeout = 5, verbose=False)
	#if(len(ans) > 0):
	
#	for i in unans:
#		print i
        if len(ans) == 0:
               print ttl, "***"
	else:
		snd, rcv = ans[0]
		snd.show()
		if last_src == rcv.src:
			break
		last_src = rcv.src
		print ttl, rcv.src
		
		
   

#for i in range(0, 11):
#	for snd, rcv in ansv[i]:
#		print i+1, rcv.src
#	if len(ansv[i]) == 0:
 #               print i+1, "*"
	# else:
	# 	print("timeout")
