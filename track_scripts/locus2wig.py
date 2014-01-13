#!/usr/bin/env python

#browser position chr19:49304200-49310700
#browser hide all
#	150 base wide bar graph at arbitrarily spaced positions,
#	threshold line drawn at y=11.76
#	autoScale off viewing range set to [0:25]
#	priority = 10 positions this as the first graph
#	Note, one-relative coordinate system in use for this format
#track type=wiggle_0 name="variableStep" description="variableStep format" visibility=full autoScale=off viewLimits=0.0:25.0 color=50,150,255 yLineMark=11.76 yLineOnOff=on priority=10
#variableStep chrom=chr19 span=150
#49304701 10.0
#49304901 12.5
#49305401 15.0
#49305601 17.5
#49305901 20.0
#49306081 17.5
#49306301 15.0
#49306691 12.5
#49307871 10.0

import sys

lfile=""
trackname=""
max_y_val=-1

def usageExit():
	print >> sys.stderr, '''Converts locusZoom input file formats to bigwig: 
e.g. chr:position<tab>E_LOG  file

usage: %s <locusZoom.input> "<track name>" [max_y_value]

max_y_value is automatically calculated if not given

''' % sys.argv[0].split('/')[-1].strip()
	exit(-1)


if len(sys.argv)>=3:
	lfile=sys.argv[1]
	trackname=sys.argv[2]
	if len(sys.argv)==4:
		max_y_val=int(sys.argv[3])
	elif len(sys.argv)>4:
		usageExit()
else:
	usageExit()


chrom=""
min=sys.maxint;
max=-1

score_max=25;
arr=[]

#Parse
for line in open(lfile):
	if line[0]=='c':
		chrpos, score = line.split('\t')
		chr, pos = chrpos.split(':')
		pos = int(pos)
		chr = chr.strip()
		
		if chrom=="":
			chrom=chr;
		elif chr!=chrom:
			print >> sys.stderr, "Error in chroms:", chr, chrom, pos
			exit(-1)
		
		if pos < min:
			min = pos
		
		elif pos > max:
			max = pos;
		
		try:
			neg_log = int(score.split("e-")[1])
		except IndexError:
#			print >> sys.stderr, "\rsetting:", score, "to 0      ",
			neg_log = 0
		
		score_max = neg_log if neg_log > score_max else score_max
		
		arr.append( (str(pos),str(neg_log)) )


if (max_y_val==-1):
	yscale = (10*((score_max/10)+2)) 
	print >> sys.stderr, "max-y-scale set at:", yscale;


#Print
print "browser position", "%s:%d-%d" % (chrom, min-10,max+10)
print "browser hide all\n"

print 'track type=wiggle_0 name="%s" description="%s" visibility=full autoScale=off\
 viewLimits=0.0:%d.0 color=50,150,255' % (trackname, trackname, yscale) #round up
print "variableStep chrom=%s span=150" % chrom

for x in arr:
	print x[0]+'\t'+x[1]





