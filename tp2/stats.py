drtt=[[]]*100
import csv
with open('out.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		drtt[int(row[0])].append(row[2])

#ahi mande los rtts, no se como hacer con los drtts

#usar st.normaltest(drtt) para ver si los drtts obtenidos son normales a traves del tiempo

#returns a 2-tuple of the chi-squared statistic, and the associated p-value.
#if the p-val is very small, it means it is unlikely that the data came from a normal distribution. For example:

#Grubbs' test detects one outlier at a time. This outlier is expunged from the dataset and the test is iterated until no outliers are detected. 
n=len(drtt)
alpha=0.95
G = (max(drtt) - sum(drtt)/n) / numpy.std(rtt[ttl])
#For the two-sided test, the hypothesis of no outliers is rejected at significance level alpha if (formula que puse en el while)
#the test should not be used for sample sizes of six or fewer since it frequently tags most of the points as outliers.
while (len(drtt) > 6 and G > (n-1)/math.sqrt(n)*math.sqrt((st.t.cdf(alpha/n,n-2)**2)/(n - 2 + st.t.cdf(alpha/n,n-2)**2))): #o era cdf?
	print "Outlier: ", max(drtt)
	drtt.remove(max(drtt))
	n -= 1
	G = (max(drtt) - sum(drtt)/n) / numpy.std(rtt[ttl])

#Y para el mapa, en las pags que pusieron, de las ips que nos dan solo dice que son de eeuu
