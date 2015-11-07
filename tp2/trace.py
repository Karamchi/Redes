#! /usr/bin/env python
import logging
import sys
import numpy
import math
logging.getLogger("scapy").setLevel(1)

from scapy.all import *
#from scipy import stats as st
import csv


def main():
    if (len(sys.argv)!=4): 
        print "Uso: iteraciones destino salida"
        return

    host = sys.argv[2]
    rtt = [[]] * 65
    salida = open(sys.argv[3] + ".csv", "w")
    csvsalida = csv.writer(salida)
    rtts = {}

    for z in xrange(int(sys.argv[1])):
        pk = IP(dst = host, ttl = range(1, 65)) / ICMP()
        ans, unans = sr(pk, timeout = 10, verbose=False)
        # Ignoramos los unanswered.
        print "Perdidos: %d" % (len(unans))
        sorted(ans, key=lambda pkt: pkt[0].ttl)
        
        # Ahora tenemos los ans ordenados por TTL
        # Tenemos que armar la hash table que queriamos.
        # Para eso, queremos juntar el paquete i con el paquete i+1
        for i in xrange(0, len(ans) - 1):
            psnd, prcv = ans[i]
            snd, rcv = ans[i + 1]
            if rcv.src == prcv.src:
                print "Breaking for"
                break
            time = max((rcv.time - snd.time) - (prcv.time - psnd.time), 0.0)
            if (prcv.src, rcv.src) not in rtts:
                rtts[(prcv.src, rcv.src)] = []
            rtts[(prcv.src, rcv.src)].append(time)
            print "Agregando (%s -> %s) con RTT: %.4f\t TTLs: (%d, %d)" % (prcv.src, rcv.src, time, psnd.ttl, snd.ttl)
        
    for (p, q) in rtts:
        print "(%s -> %s): \n\t" % (p, q),
        for r in rtts[(p, q)]:
            print " %.4f " % r,
        print "\n\t %.5f" % (sum(rtts[(p,q)])/len(rtts[(p,q)]))

if __name__ == "__main__":
    main()
