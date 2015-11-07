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
        lines = []
        last_src = "127.0.0.1"
        last_rtt = 0
        for ttl in range(1, 65):
            pk = IP(dst = host, ttl = ttl) / ICMP()
            ans, unans = sr(pk, timeout = 3, verbose=False)
            if(len(ans) == 0):
                # No obtuve respuesta. Que hacemos?
                print "Paquete salteado. TTL: ", ttl
                continue
            snd, rcv = ans[0]
            if last_src == rcv.src:
                break
            time = rcv.time - snd.time 
            if (last_src, rcv.src) not in rtts:
                rtts[(last_src, rcv.src)] = []
            rtts[(last_src, rcv.src)].append(max(time - last_rtt, 0))
            print "Agregando (%s -> %s) con RTT: %.4f" % (last_src, rcv.src, time - last_rtt)
            last_src = rcv.src
            last_rtt = time
            rtt[ttl].append(time)
            csvsalida.writerow((ttl, rcv.src, time))
            lines.append([ttl, rcv.src, sum(rtt[ttl])/len(rtt[ttl]), numpy.std(rtt[ttl])])
        
        print "%d %s\t%.2f %.2f" % (lines[0][0], lines[0][1] , lines[0][2], lines[0][3])
        for i in range(1,len(lines)): 
            a = lines[i][2] - lines[i-1][2]
            a = 0 if a < 0 else a
            print "%d %s\t%.2f %.2f" % (lines[i][0], lines[i][1], a, lines[i][3])
        print " " 
    for (p, q) in rtts:
        print "(%s -> %s): \n\t" % (p, q),
        for r in rtts[(p, q)]:
            print " %.4f " % r,
        print "\n\t %.5f" % (sum(rtts[(p,q)])/len(rtts[(p,q)]))

if __name__ == "__main__":
    main()
