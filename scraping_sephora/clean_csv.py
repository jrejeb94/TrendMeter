#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print("Nombre d'arguments invalide. Nombre attendu : 1")

else:
    with open(sys.argv[-1],'r') as in_file, open('cleaned_'+sys.argv[-1],'w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate

            seen.add(line)
            out_file.write(line)