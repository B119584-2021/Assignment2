#!/usr/local/bin/python3

#This script aims to complete alignment of sequences
#Potentially also provide the user with a list of the species included and the number of sequences?


### Import necessary modules ###
import re
from collections import Counter


#Open the fasta file
with open("fasta_seq") as my_file:
      fasta_seq = my_file.read()


#Split sequence into a list so that elements can be iterated over
fasta = fasta_seq.split("\n")

species = []

for line in fasta:
     if re.search(r'>',line) :
             species.append(line.split("[")[-1].strip("]"))

species_count=dict(Counter(species))

for names in species:
     count = species.count(names)
     print(names+":"+ str(count))

## Need to get the file to a point where I can take the set values and print them to the screen

with open(names_species, 'w') as species_names:
 species_names.write('')
 names=[]
for name in species :
	count = species.count(name)
	species_names.write(name+': '+count)

#perform alignment
#perform clustering and plotting
