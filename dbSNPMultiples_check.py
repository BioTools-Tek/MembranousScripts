#!/usr/bin/env python

import sys

if len(sys.argv)<2:
	print >> sys.stderr, '''Looks for multiply-mapped rs snps between assemblies given in two different columns

usage: %s <chrpos_rs130s_rs138s tabbed file>
''' % sys.argv[0].split('/')[-1]
	exit(-1)


f=open(sys.argv[1],'r')


for line in f:
	tokes = line.split('\t')

	snp_130s=[]
	snp_138s=[]

	if len(tokes)>3:
		if len(tokes[2].strip())==0:
			continue
		
		if len(tokes[3].strip())==0:
			continue
		
		#Find rs_130 snp		
		for t in tokes[2].split(')'):
			if len(t)<5:
				continue
			
			rs,state=t.split("',")
			if state.strip()=="'end'":
				rs = rs.split("('")[1]
				snp_130s.append(rs.strip())
	
		#Find rs_138 snps
		for t in tokes[3].split(')'):
			if len(t)<5:
				continue
			
			rs,state=t.split("',")
			if state.strip()=="'end'":
				rs = rs.split("('")[1]
				snp_138s.append(rs.strip())
	
	if len(snp_130s)==0:
		continue
	
	#Check for depreciated
	for rs_130 in snp_130s:
		if rs_130 not in snp_138s:
			
			ind = snp_130s.index(rs_130);
			snp_130s[ind] = '*'+rs_130

			#Ambigous deprec.
			if len(snp_130s)==1:
				snp_130s[ind] = '+'+snp_130s[ind]
	
	if len(snp_138s)>1:
		print tokes[0],tokes[1],'\t',','.join(snp_130s),'\t',','.join(snp_138s)


