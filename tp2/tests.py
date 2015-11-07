#!/usr/bin/env python

import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

ds = {}

with open(str(sys.argv[1]), 'r') as input_file:
	while input_file:
		ips = input_file.readline()
		if not ips:
			break
		ips = [i.replace("\n", "") for i in ips.split(" ")]
		ips = [i for i in ips if i != ""]

		ttls = [i.replace("\n", "") for i in input_file.readline().split(" ")]
		ttls = [float(i) for i in ttls if i != ""]
		
		if len(ttls) >= 5:
			ds[np.average(ttls)] = ips 
			# print(ips)
			# print len(ttls), np.average(ttls), np.std(ttls), "\n"
		
		d = input_file.readline()

# print ds
print "N\t\t\t= %d" % len(ds)
print "Mean\t\t\t= %f" % np.average(ds.keys())
print "Standard deviation\t= %f" % np.std(ds.keys())
print "Normal test\t\t=",  stats.normaltest(ds.keys())
plt.hist(ds.keys(), bins=200)
#plt.show()


#Queremos ver si el mayor elemento es un outlier:

while True:
	n = float(len(ds.keys()))
	
	G = max([(y_i - np.average(ds.keys()))/np.std(ds.keys()) for y_i in ds.keys()])
	alpha = .5
	t = stats.t.isf(alpha/n,n-2)
	print "T = %f" % t
	threshold = (n-1)/n**.5 * (t/(n-2+t))**.5
	if G > t:
		print "Outlier:", max(ds.keys()) , ds[max(ds.keys())]
		del ds[max(ds.keys())]
	else:
		break