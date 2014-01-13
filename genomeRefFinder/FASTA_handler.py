#!/usr/bin/env python

import sys

sym_per_row= 50;

class FASTAHandler:

	def __init__(self, chrom, filename):
		self.filename = filename
		self.fasta = open(self.filename, 'r')
		
		header = self.fasta.readline();
		self.chromosome = header.split('>')[1].strip() 	#get chrom
		self.offset = len(header);
		
		if (chrom != self.chromosome):
			print >> sys.stderr, "Error: Declared chromosome inside file does not agree:"
			print >> sys.stderr, "inside:", self.chromosome, "   outside:", chrom
			exit(-1);


	def close(self):
		self.fasta.close()


	def getReferenceBase(self, bp, length=1, printRC=False):
		if length <=0:
			print >> sys.stderr, "Cannot fetch length", length
			exit(-1);
		
		if length==1:
			return self.getSingleReferenceBase(bp, printRC)
		else:
			return self.getMultipleReferenceBase(bp, length, printRC)
			

    
	def getSingleReferenceBase(self, bp, printRC=False):
		bpos= bp-1
		rows = bpos/sym_per_row;
		base_row = rows*sym_per_row;
		cols = bpos - base_row;		

		if printRC:
			return "[row="+str(rows+2)+" col="+str(cols)+']'

		chars = self.offset + base_row + rows + cols
		self.fasta.seek(chars)

		return self.fasta.read(1)

	def getMultipleReferenceBase(self, bp, length, printRC=False, seekbackfirstchar=False):
		bpos=bp-1
		rows = bpos/sym_per_row;
		base_row = rows*sym_per_row;
		cols = bpos - base_row;		

		if printRC:
			return "[row="+str(rows+2)+" col="+str(cols)+']'

		chars = self.offset + base_row + rows + cols
		self.fasta.seek(chars)

		res=""
		first_char=True
# If the first character is lower case, move backwards until it finds an uppercase one and then resume search
# only if seekbackfirstchar is true.

		while (length > 0):
			base = self.fasta.read(1)[0];
			
			if (base=='\n'):
				continue;		#Skip new lines

			base_upper = base.upper();		#Skip non-coding
			if base!=base_upper:
				if seekbackfirstchar and first_char:
					chars -= 2; 			# move back one character (2 to counter each read which shift pos forward)
					self.fasta.seek(chars);
				continue;
			
			res += base
			length -=1;

			first_char = False;
		return res;
