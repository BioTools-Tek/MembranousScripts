#!/usr/bin/env python

import sys, shlex

f = open(sys.argv[1],'r')

## EUR
#map= { 
#	"(0.8,1]"   : '255,0,0',	#red
#	"(0.6,0.8]" : '250,150,122'	#orange
#}

## AFR
map= { 
	"(0.8,1]"   : '0,76,153',	#Blue
	"(0.6,0.8]" : '0,153,153'	#Cyan
}

f.readline()

name = sys.argv[1]
var = name.split('/')[-1].split('.metal')[0]

print '''track name="LD centred on %s" itemRgb="On"''' % var

for line in f:
	tokes=shlex.split(line)
	tokes= [x.replace('"',"") for x in tokes]
#	print tokes

	pos=tokes[1].split(':')

	if tokes[9] == "NA":
		continue

	eval=float(tokes[9])
	group=tokes[10]

	color=""
	if group in map:
		color=map[group]
	else:
		if (eval > 0.6):
			print >> sys.stderr, "Eval > 0.6", eval
			exit(-1)

		continue

	print "%s\t%d\t%d\t...\t0\t+\t0\t0\t%s" % (
		pos[0],
		int(pos[1]) -1,
		int(pos[1]),
		color
	)

f.close()

print ""
print ""
