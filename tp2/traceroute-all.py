#! /usr/bin/env python
import logging
import sys
import math
logging.getLogger("scapy").setLevel(1)

from scapy.all import *
from socket import gethostbyname

def main():
    if (len(sys.argv)!=3): 
        print "Uso: iteraciones destino"
        return
    
    ECHO_REPLY = 0
    TIME_EXCEEDED = 11
    TTL_EXPIRED_CODE = 0

    ip = gethostbyname(sys.argv[2])
    print >> sys.stderr, "[INFO] Starting Traceroute to host %s(%s)" % (sys.argv[2], ip)

    iterations = int(sys.argv[1])
    for z in xrange(iterations):
        print >> sys.stderr, "[INFO] Comenzando iteracion ", z
        pk = IP(dst = ip, ttl = range(1, 65)) / ICMP()
        ans, unans = sr(pk, timeout = 10, verbose=False)
        # Ignoramos los unanswered.
        print >> sys.stderr, "[INFO] Perdidos: %d" % (len(unans))
        if len(ans) == 0: continue
        sorted(ans, key=lambda pkt: pkt[0].ttl)

        for (snd, rcv) in ans:
            if rcv.type == ECHO_REPLY:
                break
            if rcv.type == TIME_EXCEEDED and rcv.code == TTL_EXPIRED_CODE:
                print "%d %s %.6f" % (snd.ttl, rcv.src, rcv.time - snd.time),
                # Este paquete nos sirve.
            else:
                print >> sys.stderr, "[WARNING] unexpected ICMP response. Tipo: %d, Code: %d" % (rcv.type, rcv.code)
        print ""

if __name__ == "__main__":
    main()
