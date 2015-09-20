from scapy.all import rdpcap
from collections import Counter
from math import log

def protos(capture):
    tipos = [hex(x.type) for x in capture if "Ether" in x]
    cnt = Counter(tipos)
    tot = float(sum([cnt[x] for x in cnt]))
    probs = {}
    for x in cnt:
        probs[x] = cnt[x]/tot
    entr = -sum([probs[x] * log(probs[x]) for x in cnt])
    return (probs, entr)

def arp(capture):
    arps = [x["ARP"] for x in capture if "ARP" in x]
    isat = {}
    whohas = {}
    for x in arps:
        if x.op == 2:
            if x.hwsrc not in isat: isat[x.hwsrc] = set()
            isat[x.hwsrc].add(x.psrc)
        else:
            if x.hwsrc not in whohas: whohas[x.hwsrc] = set()
            whohas[x.hwsrc].add(x.psrc)

    return arps, isat, whohas


def main():
    c = rdpcap("temp.cap")
    print protos(c)

if __name__ == "__main__":
    main()
