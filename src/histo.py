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
#k = [i[7:] for i in k]
d = sorted(d.values())
s = sum([i for i in d])
p = [key/float(s) for key in d]
t = [-math.log(x)/math.log(2) for x in p]
entr = -sum([x * math.log(x,2) for x in p])

plt.bar(range(len(d)),t,width=0.9)
plt.plot([0,len(d)],[entr,entr],color="red",linewidth=5,label="Entropia de la fuente")
plt.title("Entropia")
plt.xlabel("IP del nodo")
plt.ylabel("-log(Probabilidad)")
#plt.axes().get_xaxis().set_visible(False)
plt.legend()

for i in range(len(k)):
	plt.text(i+0.45,0, k[i],fontsize=10,horizontalalignment='center',verticalalignment='bottom',fontweight='bold',color='white',rotation=90)
	plt.text(len(k)-1+0.45,0, k[len(k)-1],fontsize=10,verticalalignment='bottom',horizontalalignment='center',fontweight='bold',rotation=90)
"i%(len(k)/10)*0.2"
plt.savefig(sys.argv[2])
