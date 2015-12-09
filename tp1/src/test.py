from scapy.all import rdpcap
import numpy as np

from collections import Counter
from math import log

import matplotlib.pyplot as plt
import operator

def main():
  nombres = ["cap%df.cap" % i for i in xrange(1, 5)]
  pcaps = {}
  datos = {}
  counter = {}
  total = {}
  probs = {}
  simbs = {}
  entr = {}
  inf = {}
  for cap in nombres:
    print cap
    pcaps[cap] = rdpcap(cap)
    datos[cap] = {}
    datos[cap]["whsrc"] = [x["ARP"].psrc for x in pcaps[cap] if x["ARP"].op == 1]
    datos[cap]["iasrc"] = [x["ARP"].psrc for x in pcaps[cap] if x["ARP"].op == 2]
    datos[cap]["whdst"] = [x["ARP"].pdst for x in pcaps[cap] if x["ARP"].op == 1]
    datos[cap]["iadst"] = [x["ARP"].pdst for x in pcaps[cap] if x["ARP"].op == 2]
    
    simbs[cap] = {}
    counter[cap] = {}
    total[cap] = {}
    probs[cap] = {}
    entr[cap] = {}
    inf[cap] = {}
    for d in ["whsrc", "iasrc", "whdst", "iadst"]:
      simbs[cap][d] = set(datos[cap][d])
      counter[cap][d] = Counter(datos[cap][d])
      total[cap][d] = sum(counter[cap][d].values())
      probs[cap][d] = {}
      inf[cap][d] = {}
      for (elem, n) in counter[cap][d].items():
        p = float(n)/total[cap][d]
        probs[cap][d][elem] = p
        inf[cap][d][elem] = -log(p, 2)
      entr[cap][d] = -sum([x * log(x, 2) for x in probs[cap][d].values()])
      print "%s\tSimbolos: %d\tElementos: %d\tEntropia: %.4f" % (d, len(simbs[cap][d]), total[cap][d], entr[cap][d])
      # Graficamos los nodos y la entropia.

      
      for i in [30, 40]:
        sprobs = list(reversed(sorted(inf[cap][d].items(), key = operator.itemgetter(1))[:i]))
        labels, data = zip(*sprobs)
        fig = plt.figure()
        ind = np.arange(len(data))
        plt.bar(ind, data)
        plt.xticks(ind + .35, labels, rotation='vertical')
        #TODO: Agregarle la barra de la entropia!
        # La entropia de este caso esta en entr[cap][d]
        #TODO: Hacer que se vaya "mas para abajo"
        #HAY QUE HACER UN MKDIR de esta carpeta!
        plt.savefig("entr/%s-%s-entr-%d.png" % (cap, d, i))
      
      
      
      
if __name__ == "__main__":
  main()
