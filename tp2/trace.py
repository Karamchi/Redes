#! /usr/bin/env python
import logging
import sys
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

h = sys.argv[1]
last_src = None
lines=[]
mediciones=[[]]*65

for i in range(1,100):

	lines = []

	for ttl in range(1,65):
		
		pk = IP(dst=h, ttl = ttl) / ICMP()		#Arma paquete
		ans, unans= sr(pk, timeout = 5, verbose=False)	#Manda paquete
		if(len(ans) > 0):
			snd, rcv = ans[0]
			if last_src == rcv.src:	break
			last_src = rcv.src
			mediciones[ttl].append((rcv.time-snd.time)*2)
			lines.append([ttl, rcv.src, sum(mediciones[ttl])/len(mediciones[ttl])])

	print lines[0][0], lines[0][1] , '\t', lines[0][2]
	for i in range(1,len(lines)): 
		a = lines[i][2] - lines[i-1][2]
		print lines[i][0], lines[i][1], '\t', a if a>0 else 0
