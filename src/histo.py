import protos
from pylab import *
from scapy.all import *
#import numpy as np
import sys
import math

a=rdpcap(sys.argv[1])

arp,isat = protos.arp2(a)

isat2 = [i[0] for i in isat]

d = dict()
for x in isat2:
    if x not in d:
	d[x]=1
    else:
	d[x] += 1

k = sorted(d, key=d.__getitem__)
d = sorted(d.values())
s = sum([i for i in d])
p = [key/float(s) for key in d]
t = [-math.log(x) for x in p]
entr = -sum([x * math.log(x) for x in p])

plt.bar(range(len(d)),t)
plt.plot([0,len(d)],[entr,entr])

for i in range(len(k)):
	plt.text(i+0.4,0, k[i],fontsize=10,horizontalalignment='center')

plt.savefig(sys.argv[2])
