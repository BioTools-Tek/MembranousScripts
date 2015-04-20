#!/usr/bin/env python

import sys
import Levenshtein as L
import json

if len(sys.argv) != 5:
	print >> sys.stderr, '''%s <multitrack bed> <cutoff freq> <min group size> <track prefix>
	
where:
  <multitrack bed>\tinput bed file with multiple tracks
  <cutoff freq>\tFraction of homology, groups based on those that have similarity greater than
  <min group size>\tExclude all groups smaller than this
  <track prefix>\tPrefix to prepend to every track name and description
	
Good defaults are 0.88 and 3, and 'EUR' respectively
	''' % sys.argv[0]
	exit(-1)


track_map = {}	# centred_pos --> multline_data
compr_map = {}		# centred_pos --> [ (key, homology_score) ]

tracks = open(sys.argv[1],'r')
cutoff_freq = float( sys.argv[2] )
min_group_size = int( sys.argv[3] )
filename_prefix = sys.argv[4].strip()


# Skip headers
line = ""
while not line.startswith("track"):
	print line,
	line = tracks.readline()


# Assign first track
temp_current_track = line.split('"')[1].split('on ')[1].strip()	# first track
temp_oneline = ""

# Loop over rest
for line in tracks:

	if line.startswith('track'):
		# Flush data + reset
		track_map[temp_current_track] = temp_oneline
		temp_oneline = ""		

		
		temp_current_track = line.split('"')[1].split('on ')[1].strip()
		continue

	# tracks, append into oneliner and perform ratios based on that
	temp_oneline += line

# Change to False if you will decode this from a JSON file later
use_json_debug = False
if not use_json_debug:

	# Track Map Populated, now perform ratio tests
	roving_index = 0	# Compare once only

	num_tracks = len(track_map)
	num_count = 0

	for center_key in track_map:

		center_data = track_map[center_key]
		
		roving_index += 1
		num_count += 1
		
		compr_map[center_key] = []
		
		print >> sys.stderr, "\r[%03d/%03d] comparing --> %s to %d tracks  " % (num_count, num_tracks, center_key, num_tracks - roving_index),
		
		for foreignkey in track_map.keys()[roving_index:]:
			
			foreign_data = track_map[foreignkey]
			

			ratio = L.ratio( center_data, foreign_data )
			
			# Insert into both? (Yes for now)
			if not foreignkey in compr_map:
				compr_map[foreignkey] = []
			
			compr_map[center_key].append( [foreignkey, ratio] )
			compr_map[foreignkey].append( [center_key, ratio] )
			
	json.dump( compr_map, open('debug', 'w'));
	print >> sys.stderr, ""


if use_json_debug:
	with open('debug','r') as df:
		compr_map = json.load(df)

#keys = compr_map.keys()
#pop_map = dict(map(lambda x: [x,0], keys))
groups = []

while len(compr_map) > 0:
	key = compr_map.keys()[0].encode('ascii','replace')
	new_group = [key]
		
	for fkey,score in compr_map[key]:
		fkey = fkey.encode('ascii','replace')
		
		if score >= cutoff_freq:
			new_group.append(fkey)
	
	#remove used keys
	for knv in new_group:
#		print >> sys.stderr, "removing -->",
		compr_map.pop(knv, None)
		
	if len(new_group)> min_group_size:
		groups.append(new_group)


# Print new bed, sorted by groups
for g in groups:
	for b in g:
		print '''track name="%s centred on %s" itemRgb="On"''' % (filename_prefix, b)
		print track_map[b]
		
print >> sys.stderr, "Num groups:", len(groups)


		
