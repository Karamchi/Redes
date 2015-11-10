import sys
from numpy import average as avg
from collections import Counter

def parsefile(filename):
    result = []
    with open(filename, "r") as f:
        # Cada iteracion del traceroute es una linea
        for line in f.readlines():
            splitted = line.split(' ')
            # cada paquete del traceroute es esta formado por ttl ip rtt (separado por espacios)
            # por eso hacemos len(splitted)/3, cada grupo son 3 valores.
            info = []
            for i in xrange(len(splitted)/3):
                ttl, host, rtt = int(splitted[i*3]), splitted[i*3 + 1], float(splitted[i*3 + 2])
                info.append((ttl, host, rtt))
            result.append(info)

    return result

"""
    process1 procesa los resultados exactamente como pide el tp:
        * para cada TTL, promedia los valores que pasan por ahi, sin tener en cuenta si son los mismos hosts
        * calcula deltaTTL para cada TTL promediado.
"""
def process1(results):
    # ttl va a tener como claves los distintos ttls, y como valores todos los rtts de esos ttls.
    ttls = {}
    for r in results:
        for ttl, host, rtt in r:
            if ttl not in ttls:
                ttls[ttl] = []
            ttls[ttl].append(rtt)
    # prom va a tener como claves los distintos ttls, y como valor el promedio de los rtts.
    prom = {}
    for ttl in ttls:
        prom[ttl] = avg(ttls[ttl])

    ls = sorted(prom.keys())
    # res va a tener los delta rtts de proms. Si es < 0 el delta rtt, ponemos 0.
    res = [prom[ls[0]]]
    for i in xrange(len(ls) - 1):
        res.append(max(prom[ls[i+1]] - prom[ls[i]], 0.0))

    return res

"""
    process3 procesa los resultados como pide el tp,
    con la salvedad de que para cada ttl, solo toma los valores del host que mas aparezca.
"""
def process3(results):
    ttls = {}
    for r in results:
        for ttl, host, rtt in r:
            if ttl not in ttls:
                ttls[ttl] = []
            ttls[ttl].append((host, rtt))

    prom = {}
    for ttl in sorted(ttls.keys()):
        mch = Counter([host for host, rtt in ttls[ttl]]).most_common(1)[0]
        print >> sys.stderr, "[INFO] para ttl %d el host %s aparece %d veces" % (ttl, mch[0], mch[1])
        # nos quedamos solo con los ttls de los hosts que mas aparecen
        ttls[ttl] = [(host, rtt) for host, rtt in ttls[ttl] if host == mch[0]]
        prom[ttl] = avg([rtt for host, rtt in ttls[ttl]])
    ls = sorted(prom.keys())

    res = [prom[ls[0]]]
    for i in xrange(len(ls) - 1):
        res.append(max(prom[ls[i+1]] - prom[ls[i]], 0.0))
    return res 

"""
    process2 procesa los resultados como pide el tp,
    con la salvedad de que solo toma en cuenta los datos
    de la ruta mas frecuente.
    
    * Busca la ruta mas frecuente
    * calcula el promedio de los ttls
    * calcula el delta rtt
"""
def process2(results):
    return process1(mostcommonroute(results))

"""
    mostcommonroute filtra las rutas del resultado devolviendo
    las que son iguales a la ruta mas comun.
"""
def mostcommonroute(results):
    # para cada iteracion armamos un diccionario con (ttl, keys) como claves.
    ds = []
    for r in results:
        dic = {}
        for ttl, host, rtt in r:
            dic[(ttl, host)] = rtt
        ds.append(dic)

    # Nos armamos un string para cada ruta, que sea de la forma:
    # ttl1-host1|ttl2-host2|...|ttln-hostn
    # esa va a ser nuestra funcion de hasheo.
    hf = lambda d: '|'.join(["%d-%s" % k for k in sorted(d.keys())])

    cnt = {}
    for dic in ds:
        key = hf(dic)
        if key not in cnt:
            cnt[key] = []
        cnt[key].append(dic)

    mc = Counter([hf(d) for d in ds]).most_common(1)[0]
    print >> sys.stderr, "[INFO] most common route appears %d times." % mc[1]

    metrics = cnt[mc[0]]
    res = []

    for dic in metrics:
        res.append([(key[0], key[1], dic[key]) for key in sorted(metrics[0].keys())])
    return res

def col(mtx, index):
    return [rr[index] for rr in mtx]

def row(mtx, index):
    return mtx[index]

def printcol(mtx, index):
    for row in col(mtx, index):
        print row

def main():
   return

if __name__ == "__main__":
    main()
