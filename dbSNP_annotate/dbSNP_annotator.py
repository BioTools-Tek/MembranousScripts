#!/usr/bin/env python

import sys

def usage():
	print >> sys.stderr, "%s <chr:pos_input> <dbSNPCoding folder> [--ends-only]" % sys.argv[0].split('/')[-1]
	exit(0)


len(sys.argv)<3 and usage()

positions_file=sys.argv[1]
snpconfig_fold=sys.argv[2]
try:
	ends=sys.argv[3].startswith("--ends")
except IndexError:
	ends=False



class SNPHandler:
	# [chrom][start_position] = [dbsnp1,dbsnp2]
	snp_map = {}
	curr_chrom = ""
	snp_ref = None
	snp_fold = ""

	def __init__(self, snp_fold):
		self.snp_fold = snp_fold;
		self.chrom_snp_map = {}


	def openNewSNP(self, chrom):
		snp_file = self.snp_fold+"/snppos."+chrom
		self.snp_ref = open(snp_file, 'r')
		
		print >> sys.stderr, "Populating: ",snp_file
		self.curr_chrom = chrom
		self.populateChromSNPMap()
		
		#insert new map into overall
		self.snp_map[chrom]=self.chrom_snp_map

	def populateChromSNPMap(self):
		count = 0
		self.snp_ref.readline() #strip header
		
		for line in self.snp_ref:
			count += 1
			tokes = line.split('\t');
			
			if count%123==0:
				print >> sys.stderr, '\rMapping:',count, "positions",
			
			#4567812 
			stapos = int(tokes[1].strip())
			endpos = int(tokes[2].strip())
			marker = tokes[3].strip()
			
			#insert start
			start_marker = (marker,"start")
			end_marker = (marker,"end")
			
			if stapos not in self.chrom_snp_map:
				self.chrom_snp_map[stapos] = [start_marker];
			else:
				if start_marker not in self.chrom_snp_map[stapos]:
					self.chrom_snp_map[stapos].append( start_marker );
			
			#insert end
			if endpos not in self.chrom_snp_map:
				self.chrom_snp_map[endpos] = [end_marker];
			else:
				if end_marker not in self.chrom_snp_map[endpos]:
					self.chrom_snp_map[endpos].append( end_marker );
		
		self.snp_ref.close();



sh = SNPHandler(snpconfig_fold)

found=0

for line in open(positions_file,'r'):
	tokes = line.splitlines()[0].split(':')
	
	chrom=tokes[0].strip()
	try:
		pos = int(tokes[1].strip())
	except ValueError:
		continue
	
	if sh.curr_chrom != chrom:
		sh.openNewSNP(chrom)

	valid_snps="--"
	try:
		buff=[]
		snps = sh.snp_map[chrom][pos]

		if ends:
			for mark,typ in snps:
				if typ=="end":
					buff.append(mark)
			valid_snps=','.join(buff)
		else:
			valid_snps=str(snps)
		found +=1
	except KeyError:
		valid_snps="--"

	print '\t'.join(tokes),'\t',valid_snps

print >> sys.stderr, "\nFound:",found
