#! /usr/bin/env python
import logging
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

h = "www.dc.uba.ar"

for ttl in range(65):
	print ttl
	pk = IP(dst=h, ttl = ttl) / ICMP()
	ans= sr(pk, timeout = 5)
	#if(len(ans) > 0):
	print(ans)
	# else:
	# 	print("timeout")
