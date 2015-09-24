import protos
from pylab import *
from scapy.all import *
from collections import Counter
#import numpy as np
import sys
import math

a=rdpcap(sys.argv[1])

arp,isat = protos.arp2(a)

isat2 = Counter([p for (p, q) in isat])



tot = float(sum([isat2[x] for x in isat2]))
probs = {}
for x in isat2:
	probs[x] = isat2[x]/tot
entr = -sum([probs[x] * math.log(probs[x],2) for x in isat2])

isat3 = {}
for key1 in isat2:
	amount = -math.log(probs[key1], 2)
	if amount in isat3:
		isat3[amount].add(key1)
	else:
		isat3[amount] = set([key1])


ys = sorted([x for x in isat3])
for y in ys:
	if len(isat3[y]) > 5:
		isat3[y] = "%d nodos" % len(isat3[y])
	else:
		print(isat3[y])
		isat3[y] = " ".join(isat3[y])

xs = [isat3[y] for y in ys]

plt.bar(range(len(ys)),ys,width=1)
plt.plot([0,len(ys)],[entr,entr],color="red",linewidth=5,label="Entropia de la fuente")
plt.title("Entropia")
plt.xlabel("IP del nodo")
plt.ylabel("-log(Probabilidad)")
plt.legend()

for i in range(len(xs)):
	plt.text(i+0.45,0, xs[i],fontsize=10,horizontalalignment='center',fontweight='bold',verticalalignment='bottom',rotation=90)
	plt.text(len(xs)-1+0.45,0, xs[len(xs)-1],fontsize=10,horizontalalignment='center',fontweight='bold',rotation=90,verticalalignment='bottom')
plt.savefig(sys.argv[2])
