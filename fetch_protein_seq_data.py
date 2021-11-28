### TASK 1: Fetching user specified  protein sequence data ### 

# The aim of this script is to fetch protein sequence data detailed in user input and to provide the user with a summary of actions taken. 


#!/usr/local/bin/python3


### Load necessary modules ###
import os, subprocess, sys, re



### ASK USER FOR INFO ###

# Ask user to specify protein family
protein_fam=input("Which protein family are you analysing?\n\t> ")

# If variable is empty, repeat request
while not protein_fam :
  print("Please provide a protein family")
  try :
   protein_fam=input("\t> ")
  except :
    continue

# Print selection of protein_fam to screen
print(protein_fam, "selected\n")


# Ask user to specify taxonomic group
taxon_gr = input("Which taxonomic group are you analysing?\n\t> ")
# If variable is empty, repeat request
while not taxon_gr :
  print("Please provide a taxon group")
  try :
   taxon_gr = input("\t> ")
  except:
    continue
print(taxon_gr, "selected\n")



### Set variables ###
space = " AND "
quote = "\""
full_query = quote + taxon_gr + space + protein_fam + quote
entrez_sum=" > entrez_sum.txt"
fetch_fasta=" | efetch -format fasta > fasta_seq.fa"

# Combine variables to generate esearch command variables 
esearch_count="esearch -db protein -query "+full_query+entrez_sum
esearch_fasta="esearch -db protein -query "+full_query+fetch_fasta



### How many sequences? ###
subprocess.call(esearch_count, shell=True)

# Open file containing entrez summary 
with open("entrez_sum.txt") as my_file:
      entrez_sum = my_file.read()

# Format entrez_sum to a list so it can be iterated over
entrez_summary = entrez_sum.split("\n")


## Find countline 
# Create empty list
count_line = []

# Iterate over summary and store line with sequence count
for sum in entrez_summary:
     if re.search(r'Count', sum) :
             count_line.append(sum)

# Extract count from countline
count = re.findall(r'\d+',str(count_line))
count_str = str(count).strip("['']")

# Set sequence count as variable x
x = int(count_str)

if x < 1 :
  print("There were no sequences found for your search")
  sys.exit("Exiting...\n")

# Print sequence count to screen for user to see
print("Number of sequences:",+x,"\n")



### >1000 sequences ###

# This block interacts with the user if > 1000 or < 10

# Find out how user would like to proceed:
while x > 1000 :
  a = input("More than 1000 sequences, do you wish to continue? (Yes or No)\n\t> ")
  try :
    if a == "Yes" or a == "No" :
      break ;
    a = input("Please type Yes or No\n\t> ")
  except :
    continue

if (not a == True) :
  if (a == "Yes") :
    print("Continuing...\n")
  if (a == "No"):
    sys.exit("Exiting due to more than 1000 sequences\n")


# If there are fewer than 10 sequences
while x <= 10 :
  b = input("There are less than 10 sequences, would you like to continue? (Yes or No)\n\t> ")
  try :
    if b == "Yes" or b == "No" :
      break ;
  except :
    continue

if (not b == True) :
  if b == "Yes" :
    print("Continuing")
  if b == "No" :
    sys.exit("Exiting due to less than 10 sequences\n")



### Download FASTA sequences ###

print("Fetching sequences in FASTA format\n")
 
subprocess.call(esearch_fasta, shell=True)


