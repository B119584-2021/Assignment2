#!/usr/local/bin/python3

#This script aims to complete alignment of sequences
#Potentially also provide the user with a list of the species included and the number of sequences?


### Import necessary modules ###
import re, subprocess
import pandas as pd


#Open the fasta file
with open("fasta_seq.fa") as my_file:
      fasta_seq = my_file.read()


#Split sequence into a list so that elements can be iterated over
fasta = fasta_seq.split("\n")

species_name = []
species_id = []

for line in fasta:
     if re.search(r'>',line) :
             species_name.append(line.split("[")[-1].strip("]"))
	     species_id.append(line.split(" ")[0])


# Create a dataframe which contains the species ID and name
s1 = pd.Series(species_id)
s2 = pd.Series(species_name)
pd.DataFrame( { 'ID' : s1, 'Name' : s2 } )

species_file = []

for names in species:
     count = species.count(names)
     species_file.append(names+": "+ str(count))

species_count = set(species_file)

#Print species names and counts to the screen
print(species_count.replace(",","\n")

## Need to get the file to a point where I can take the set values and print them to the screen

subprocess.call("clustalo -i fasta_seq.fa", shell=True)

#perform alignment - read through the help informaiton (clustalo --help from commandline)
#perform clustering and plotting
