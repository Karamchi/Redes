#! /usr/bin/env python
import logging
import sys
import numpy
import math
logging.getLogger("scapy").setLevel(1)

from scapy.all import *
from scipy import stats as st
import csv

if (len(sys.argv)!=4): print "Uso: iteraciones destino salida"
else: 
	h = sys.argv[2]
	last_src = None
	rtt=[[]]*65
	salida = open(sys.argv[3]+".csv","w")
	csvsalida = csv.writer(salida)

	for i in range(int(sys.argv[1])):

		lines = []
	#	drtt=[]

		for ttl in range(1,65):
		
			pk = IP(dst=h, ttl = ttl) / ICMP()
			ans, unans= sr(pk, timeout = 5, verbose=False)
			if(len(ans) > 0):
				snd, rcv = ans[0]
				if last_src == rcv.src:	break
				last_src = rcv.src
				time=(rcv.time-snd.time)*2
				rtt[ttl].append(time)
				csvsalida.writerow((ttl, rcv.src, time))
				lines.append([ttl, rcv.src, sum(rtt[ttl])/len(rtt[ttl]), numpy.std(rtt[ttl])])

		print lines[0][0], lines[0][1] , '\t', lines[0][2], lines[0][3] #Soy un cabeza
		for i in range(1,len(lines)): 
			a = lines[i][2] - lines[i-1][2]
			a = 0 if a<0 else 0
	#		drtt.append(a)
			print lines[i][0], lines[i][1], '\t', a, lines[i][3]
		print " " 
