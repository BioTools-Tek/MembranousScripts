#!/usr/bin/env python

import sys

def usage():
	print >> sys.stderr, '''Extracts names of individuals that fall into one of the population groups given in an input file
	
	%s <population_id.list> <column_pedfile> --idcol=N --popcol=N
	
where:
	idcol and popcol are mandatory arguments which refer to the columns in the column_pedfile indicating which columns contain name ids, and population ids respectively.
All files should be TAB delimited'''\
% sys.argv[0].split('/')[-1]
	exit(0)

if len(sys.argv)!=5:
	usage()

poplist = sys.argv[1]
pedcols = sys.argv[2]
id_c = int(sys.argv[3].split("--idcol=")[1])-1
pop_c= int(sys.argv[4].split("--popcol=")[1])-1


#Make acceptable tag list
tag_list = []
for line in open(poplist,'r'):
	if line[0]=='#':
		continue
	tag_list.append(line.split('\t')[0].strip())


#Make pedfile list
ped_ids=[]
for line in open(pedcols,'r'):
	tokes = line.splitlines()[0].split('\t')
	
	pop_name = tokes[pop_c].strip()
	if pop_name in tag_list:
		id_name = tokes[id_c].strip()
		
		if id_name not in ped_ids:
			ped_ids.append( id_name )

ped_ids.sort()
print '\n'.join(ped_ids)




