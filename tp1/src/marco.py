import protos
from pylab import *
from scapy.all import *
import numpy as np
import sys

a=rdpcap(sys.argv[1])

arp,isat = protos.arp2(a)
s=set(isat)
with open(sys.argv[2],"a") as f:
	for i in s:
		f.write("\"%s\" -> \"%s\"\n" % (i[0], i[1]))
