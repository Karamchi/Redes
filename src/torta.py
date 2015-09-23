import protos
from pylab import *
from scapy.all import *

a=rdpcap(sys.argv[1])
#protos.arp(a)

probs,entr = protos.protos(a)

plt.pie([probs.get(key) for key in probs], labels = [key for key in probs])
#, colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'),    autopct=None, pctdistance=0.6,shadow=False,    labeldistance=1.1, startangle=None, radius=None)
plt.legend()

plt.savefig(sys.argv[2])
