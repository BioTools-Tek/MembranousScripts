import sys

combined_positions = {}

def addtomap(filename):
	positions = {}
	
	for line in open(filename,'r'):
		num = int(line.strip())
		if num not in positions:
			positions[num] = 1
		else:
			print filename, num, "dupe"

	return positions;


pos1 = addtomap(sys.argv[1])
pos2 = addtomap(sys.argv[2])

for key in pos2:
	if key not in combined_positions:
		combined_positions[key] = 1
	else:
		print sys.argv[2], key, "duped again"


for key in pos1:
	if key not in combined_positions:
		combined_positions[key] = 1
	else:
		print "OVERLAP:", key

