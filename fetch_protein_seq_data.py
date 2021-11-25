### TASK 1: Fetching user specified  protein sequence data ### 

# The aim of this script is to fetch protein sequence data detailed in user input and to provide the user with a summary of actions taken. 


#!/usr/local/bin/python3


### Load necessary modules ###
import os, subprocess, sys, re

	### Do you need to install esearch? ###

	# Can you check if it installed first?
	#sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"



### ASK USER FOR INFO ###

# Ask user to specify protein family
protein_fam=input("Which protein family are you analysing?\n\t> ")
print(protein_fam, "selected")

# Ask user to specify taxonomic group
taxon_gr=input("Which taxonomic group are you analysing?\n\t> ")
print(taxon_gr, "selected")



### Set variables ###
space = " AND "
quote = "\""
full_query = quote + taxon_gr + space + protein_fam + quote
entrez_sum=" > entrez_sum.txt"
fetch_fasta=" | efetch -format fasta > fasta_seq"

esearch_count="esearch -db protein -query "+full_query+entrez_sum
esearch_fasta="esearch -db protein -query "+full_query+fetch_fasta



### How many sequences? ###
subprocess.call(esearch_count, shell=True)

# Open file containing entrez summary 
with open("entrez_sum.txt") as my_file:
      entrez_sum = my_file.read()

# Format entrez_sum to a list so it can be iterated over
entrez_summary = entrez_sum.split("\n")

# Find countline 
count_line=[]
for sum in entrez_summary:
     if re.search(r'Count', sum) :
             count_line.append(sum)

# Extract count from countline
count = re.findall(r'\d+',str(count_line))
count_str = str(count).strip("['']")
x = int(count_str)

print("Number of sequences:",+x)



### >1000 sequences ###

# This block interacts with the user if there are more than 1000 sequences present

# Find out how user would like to proceed:
if (x > 1000):
  while True:
    try:
      a=input("More than 1000 sequences, do you wish to continue? (Yes or No)\n\t> ")
      if a == "Yes" or a == "No":
        break;
      else:
        print("Please type Yes or No\n")
    except:
      continue

# If user wishes to continue despite large size:
if (a == "Yes"):
  print("Continuing...")

# If user wishes to exit due to large size:
if (a == "No"):
  sys.exit("Exiting...")

#print to check you made it to the bottom
print("you made it")



### Download FASTA sequences ###

print("Fetching sequences in fasta format")
 
subprocess.call(esearch_fasta, shell=True)



### CHECK IN WITH USER ###

# The sequences come from more than one species - do you wish to continue?

# Once sequences are fetched provide user with a summary
