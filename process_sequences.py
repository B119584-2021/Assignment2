#!/usr/local/bin/python3

# This script aims to complete alignment of sequences
# Potentially also provide the user with a list of the species included and the number of sequences?


### Import necessary modules ###
import re, subprocess, sys
import pandas as pd


# Open the fasta file
with open("fasta_seq.fa") as my_file:
      fasta_seq = my_file.read()


# Split sequence into a list so that elements can be iterated over
fasta = fasta_seq.split("\n")



### Create dataframe of unique species and their counts ###

# Create empty lists for series used to make dataframe
species_name = []
species_id = []
species_info = []


# The loop iterates over lines in fasta, adding each sequences name, id and info to lists 
for line in fasta :
	if re.search(r'>',line) : 
		species_name.append(line.split("[")[-1].strip("]"))
		species_id.append(line.split(" ")[0])
		name = line.split("[")[-1].strip("]")
		id = line.split(" ")[0]
		species_info.append(line.replace(id,"").replace(name,"").strip("[]"))


# Create a dataframe which contains the species ID and name
s1 = pd.Series(species_id)
s2 = pd.Series(species_name)
s3 = pd.Series(species_info)
All_IDs_names = pd.DataFrame( { 'ID' : s1, 'Name' : s2, 'Info' : s3 } )


# Save a file that contains the IDs, names and info of the species proteins in the original fasta file 
All_IDs_names.to_csv("All_IDs_names.csv", sep="\t")


# Create and save a file that lists unique species and their counts
unique_species_count = pd.DataFrame(All_IDs_names['Name'].value_counts())
unique_species_count.to_csv("Unique_species_count.csv", sep="\t")
unique_species_count = pd.read_csv("Unique_species_count.csv", sep="\t")
unique_species_count.columns = ['Name', 'Count']
unique_species_count.to_csv("Unique_species_count.csv", sep="\t")


# Print the top and bottom 15 unique species to the screen
print(unique_species_count.head(15))
print(unique_species_count.tail(15))



### User input to assess the dataset###

# Inform user of significance of the lines printed to the screen
print("The most and least frequenct species have been listed for the downloaded sequences.\n")

while True:
  try:
    a=input("Would you like to keep all sequences and proceed with alignment? Type 'keep all'\nWhat is the minimum number of sequences you would like to keep? Type 'x'\n\t> ")
    if a == "keep all" :
      print("Keeping all sequences")
      inputf = open("input_fasta.fa","w")
      inputf.write(fasta_seq)
      inputf.close()
      break
    if int(a) :
      print("Subsetting desired sequences")
      subset = unique_species_count[(unique_species_count['Count'] > int(a))]
      names = list(subset['Name']) # list of desired names to iterate over

      fasta = fasta_seq.split(">")
      symbol = ">"

      fasta_list = []
      for line in fasta :
        fasta_list.append(symbol+line)

      inputf = open("input_fasta.fa","w")
      for line in fasta_list :
        for name in names :
          if re.search(name, line) :
            inputf.write(line)
      inputf.close()
      break
  except:
    print("wrong input")
    continue



#if (int(a)):
#	subset = unique_species_count[(unique_species_count['Count'] > int(a))] 
#	names = list(subset['Name']) # list of desired names to iterate over
#
#	fasta = fasta_seq.split(">")
#	symbol = ">"
#
#	fasta_list = []
#	for line in fasta :
#		fasta_list.append(symbol+line)
#
#
#	inputf = open("input_fasta.fa","w")
#	for line in fasta_list :
#		for name in names :
#			if re.search(name, line) :
#				inputf.write(line)
#	inputf.close()


subprocess.call("clustalo -i input_fasta.fa > clustalo_alignment.txt", shell=True)


