import protos
from pylab import *
import sys
import math

d = dict()
d["IPv4"]=49230
d["ARP"]=579
d["IPv6"]=2

k = sorted(d, key=d.__getitem__)
d = sorted(d.values())
s = sum(d)
p = [key/float(s) for key in d]
t = [-math.log(x)/math.log(2) for x in p]
entr = -sum([x * math.log(x,2) for x in p])

plt.bar(range(len(d)),t,width=0.9)
plt.plot([0,len(d)],[entr,entr],color="red",linewidth=5,label="Entropia de la fuente")
plt.title("Entropia")
plt.xlabel("Tipo de paquete")
plt.ylabel("-log(Probabilidad)")
#plt.axes().get_xaxis().set_visible(False)
plt.legend()

for i in range(len(k)):
	plt.text(i+0.45,0, k[i],fontsize=10,horizontalalignment='center',verticalalignment='bottom',fontweight='bold')
plt.savefig(sys.argv[1])
