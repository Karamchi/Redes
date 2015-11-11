#!/bin/bash

UNIVERSITIES="www.msu.ru www.u-tokyo.ac.jp www.tsinghua.edu.cn berkeley.edu www.cuni.cz uwaterloo.ca lnu.edu.ua www.unsw.com new.aucegypt.edu www.uom.gr" 

mkdir -p results

for u in $UNIVERSITIES
do
	echo "Traceroute para $u"
	python traceroute-all.py 100 $u > "results/$u"
done

for u in $UNIVERSITIES
do
	echo "Traceroute one para $u"
	#python traceroute-one.py 50 $u > "results/$u-one"
done
