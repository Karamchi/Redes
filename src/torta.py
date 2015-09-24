import protos
from pylab import *
from scapy.all import *

a=rdpcap(sys.argv[1])

probs,entr = protos.protos(a)

tipos=dict()
tipos['0x806']="ARP"
tipos['0x800']="IPv4"
tipos['0x86dd']="IPv6"

y=[probs.get(key)*len(a) for key in probs]

def valor(values):
    def my_autopct(pct):
	    total = sum(values)
	    val = int(round(pct*total/100.0))
	    return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

plt.pie(y, labels = [tipos.get(key) for key in probs],autopct=valor(y))

plt.title("Tipos de paquetes")

plt.savefig(sys.argv[2])
