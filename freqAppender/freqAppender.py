#!/usr/bin/env python

# This does not append to VCF files, I will need to rewrite this soon for just that reason

import sys

def usageExit():
	print >> sys.stderr, "Appends frequencies to a column file with <chr>DELIM<position> where DELIM is either tab or ':'"
	print >> sys.stderr, "\tusage: %s <colfile> <frequencies_folder>" % sys.argv[0].split('/')[-1]
	exit(0)

len(sys.argv)!=3 and usageExit()

colfile=sys.argv[1]
freq_fold=sys.argv[2]


class FrequencyHandler:
	freq_map = {} # [chrom][position] = {A:0.6, G:0.4}
	curr_chrom = ""
	freq_ref = None
	freq_fold = ""

	def __init__(self, freq_fold):
		self.freq_fold = freq_fold;
		self.chrom_frequency_map = {}


	def openNewFreq(self, chrom):
		freq_file = self.freq_fold+'/'+chrom+".frq"
		self.freq_ref = open(freq_file, 'r')
		
		print >> sys.stderr, "Populating: ",freq_file
		self.curr_chrom = chrom
		self.populateChromFreqMap()
		
		#insert new map into overall
		self.freq_map[chrom]=self.chrom_frequency_map

	def populateChromFreqMap(self):
		count = 0
		self.freq_ref.readline() #strip header
		
		for line in self.freq_ref:
			count += 1
			tokes = line.split('\t');
			
			if count%123==0:
				print >> sys.stderr, '\rMapping:',count, "positions",
			
			#4567812  (chrBlah)
			key = int(tokes[1].strip())
			
			value_map = {}
			vals = tokes[4:]
			for v in vals:
				letter, fract = v.split(':')
				value_map[letter.strip()[0]] = float(fract.strip())
			
			self.chrom_frequency_map[key] = value_map
		self.freq_ref.close();



fh = FrequencyHandler(freq_fold)


for line in open(colfile):
	line = line.splitlines()[0]
	
	tokens = []
	if line.find(':')!=-1:
		tokens = line.split(':')
	else:
		tokens = line.split('\t')
	
	chrom = tokens[0].strip()
	pos = tokens[1].strip()
	
	if fh.curr_chrom != chrom:
		fh.openNewFreq(chrom)
	try:
		freqs = fh.freq_map[chrom][int(pos.strip())]
	except KeyError:
		freqs="NOT FOUND"
		
	print '\t'.join(tokens),'\t',freqs
	
#print "FINAL"
#print fh.freq_map


