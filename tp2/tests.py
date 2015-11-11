#!/usr/bin/env python

import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import analysis
import math

f = "results/"+sys.argv[1]
res = analysis.parsefile(f)
res = analysis.process3(res)

#print res

ds = [math.log(a[0],2) for a in res]
hosts = [a[1] for a in res]
#ds = [a[0] for a in res]

print ds
print hosts

#print "\n",
#print "N\t\t\t= %d" % len(ds)
#print "Mean\t\t\t= %f" % np.average(ds)
#print "Standard deviation\t= %f" % np.std(ds)
#print "Normal test\t\t=",  stats.normaltest(ds)
#plt.hist(ds, bins=200)
#plt.show()
print "\n",

#Grubbs:

while True:
	n = float(len(ds))
#	print ds

	G = max([(y_i - np.average(ds))/np.std(ds) for y_i in ds])
	alpha = .05
	t = (stats.t.isf(alpha/n,n-2))
	#print "T = %f" % t
	threshold = (n-1)/n**.5 * (t/(n-2+t))**.5
	if G > threshold:
		print ds.index(max(ds))	
		ant = hosts[ds.index(max(ds))-1]
		h = hosts.pop(ds.index(max(ds)))
		print "Outlier:", ant, "->", h , max(ds)
		ds.remove(max(ds))
	else:
		break

print "\n",
