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
    wait = lambda x: 8 if x < 12 else 15 # Tiempo de espera variable.

    iterations = int(sys.argv[1])
    for z in xrange(iterations):
        print >> sys.stderr, "[INFO] Comenzando iteracion ", z
        for ttl in xrange(1, 65):
            pk = IP(dst = ip, ttl = ttl) / ICMP()
            ans, unans = sr(pk, timeout = wait(ttl), verbose=False)
            if len(ans) == 0: continue # next ttl
            snd, rcv = ans[0]
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
