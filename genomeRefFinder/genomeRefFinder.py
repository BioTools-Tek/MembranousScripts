#!/usr/bin/env python

import sys
from FASTA_handler import FASTAHandler

ver="ver0.2"
name=sys.argv[0].split('/')[-1]

def usageExit():
	print >> sys.stderr, name, ver, '''

Print a table detailing which human genome version a particular reference base refers to for each position given in a column file with two extra MINOR and MAJOR base columns

usage: %s <column file> <[FASTAS]>''' % name
	exit(-1)


if len(sys.argv) < 3:
	usageExit()

colfile = sys.argv[1]
fasta_files= sys.argv[2:]


########################################################################

# Open and initialise FASTA

FASTA_dict = {}
hg_versions = []

for fast_file in fasta_files:
	hg_version = fast_file.split('/')[-2].strip()
	hg_versions.append(hg_version) if (hg_version not in hg_versions) else 0
	
	chrom = fast_file.split('/')[-1].split(".fa")[0]

	chromosome_map = {}
	chromosome_map[chrom] = FASTAHandler(chrom, fast_file)
	FASTA_dict[hg_version] = chromosome_map

hg_versions.sort()


class AutoVivification(dict):
	"""Implementation of perl's autovivification feature."""
	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			value = self[item] = type(self)()
			return value


reverse_complement = {}
reverse_complement['A'] = 'T'
reverse_complement['T'] = 'A'
reverse_complement['C'] = 'G'
reverse_complement['G'] = 'C'


#Stores results
prog=['|','/','-','\\']; 
pc=0; lc =0;
print >> sys.stderr, "Mapping Data... ",


alt_basemap = AutoVivification()   # [chrom][position][hgver] = [ref, alt, match=(n|p|-)]

RP="R +"
RN="R  -"
AP="A +"
AN="A  -"
BLANK=""

for line in open(colfile,'r'):
	lc += 1
	tokens = line.split('\t')
	
	chrom = tokens[0].strip()
	position = int(tokens[1].strip())
	
	# May need to switch these two around
	MIN = tokens[2].strip().upper()  # [0]
	MAJ = tokens[3].strip().upper()  # [0]
	
	hg_map = {}
	
	for hg_key in hg_versions:
		BEFORE_REF = FASTA_dict[hg_key][chrom].getReferenceBase(position-1).upper()
		REF  = FASTA_dict[hg_key][chrom].getReferenceBase(position).upper();
		AFTER_REF  = FASTA_dict[hg_key][chrom].getReferenceBase(position+1).upper();
		
		result_arr=[]
		for alter in [BEFORE_REF,REF, AFTER_REF]:
			res=BLANK
			
			#Check + for ref and alt
			if MAJ==alter:
				res=RP
			elif MIN==alter:
				res=AP
				
			
			#Check - for ref and alt
			elif MAJ==reverse_complement[alter]:
				res=RN
			
			elif MIN==reverse_complement[alter]:
				res=AN
			
			result_arr.append( res );
		
		hg_map[hg_key] = [ [BEFORE_REF,REF,AFTER_REF], result_arr]
		
	alt_basemap[chrom][position] = [ MAJ, MIN, hg_map]
#	print >> sys.stderr, ALT
	
	if lc%11==0:
		print >> sys.stderr, "\r\t\t",prog[pc%4],
		pc +=1



match_count = {}

for hg_key in hg_versions:
	match_count[hg_key] = [{},{},{}]  # Before map, At map, After map


print >> sys.stderr, "\nPrinting Table",

#Headers
print "chr\tposition\tMAJ\tMIN\t\t",
print '\t'.join(hg_key+"(-1)\t"+hg_key+"(0)\t"+hg_key+"(+1)" for hg_key in hg_versions),
print '\t\t',
print '\t'.join(hg_key+"(-1)?\t"+hg_key+"(0)?\t"+hg_key+"(+1)?" for hg_key in hg_versions)

num_positions = 0

for chrom in sorted(alt_basemap.keys()):	
	for position in sorted(alt_basemap[chrom].keys()):
		ref,alt,hg_map = alt_basemap[chrom][position]
		
		print chrom,'\t',position,'\t', ref,'\t', alt, "\t\t",
		
		for hg_key in hg_versions:
			bases = hg_map[hg_key][0];
			print '\t'.join(bases),
			
		print "\t\t",
		
		print >> sys.stderr, "\r\t\t", prog[pc%4],
		pc +=1
		
		for hg_key in hg_versions:
			results = hg_map[hg_key][1];
			index=0;
			for res in results:
				
				if res in match_count[hg_key][index]:
					match_count[hg_key][index][res] += 1
				else:
					match_count[hg_key][index][res] = 1

				if res in [AN,RN,BLANK]:
					print "!",

				print res,'\t',
				
				
				index += 1;
				
		print ""
		num_positions +=1;

print ""

for res in [RP,RN,AP,AN,BLANK]:
	print "Total",res,":",'\t'*(len(hg_versions)+8),
	
	for hg_key in hg_versions:
		for index in xrange(len(match_count[hg_key])):
			try:
				print "%d(%d%%)\t" % (match_count[hg_key][index][res],100*match_count[hg_key][index][res]/num_positions),
			except KeyError:
				print "0(0%)\t",
	print ""
print >> sys.stderr, ""
