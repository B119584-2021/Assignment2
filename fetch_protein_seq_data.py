### TASK 1: Fetching user specified  protein sequence data ### 
# The aim of this script is to fetch protein sequence data detailed in user input and to provide the user with a summary of actions taken. 

#!/usr/bin/python3

# Load necessary modules 
import os, subprocess, sys 

	### Do you need to install esearch? ###

	# Can you check if it installed first?
	#sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"



### ASK USER FOR INFO ###

# Ask user to specify protein family
protein_family=input("Which protein family are you analysing?\n\t> ")
print(protein_family, "selected")

# Ask user to specify taxonomic group
taxonomic_group=input("Which taxonomic group are you analysing?\n\t> ")
print(taxonomic_group, "selected")

esearch1="esearch -db protein -query protein_family AND taxonomic_group"
esearch_command="esearch -db protein -query "protein_family AND taxonomic_group" | efetch -format uid > uid_output"
# esearch_fasta="esearch -db protein -query protein_family AND taxonomic_group | efetch -format fasta > fasta_uid"

	#esearch -db protein -query "taxonomic_group AND protein_family" | efetch -db protein -format uid > uid_output

	#cat uid_output | wc -l > seq_number

# These will then be input to the command used to fetch the sequences,
# before downloading check the number of sequeces and the composition


# Perform command to fetch protein sequence data
subprocess.call(esearch1, shell=True)
subprocess.call(esearch_command, shell=True)



with open(r"uid_output", 'r') as fp:
     x = len(fp.readlines())
     print('total lines:', x)



### >1000 sequences ###

# This block interacts with the user if there are more than 1000 sequences present
#x=1800 # x is the number of sequences

# Find out how user would like to proceed:
if (x > 100):
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



# Fetch the sequences in fasta format 
# subprocess.call(esearch_fasta, shell=True)



### CHECK IN WITH USER ###

# The sequences come from more than one species - do you wish to continue?

# Once sequences are fetched provide user with a summary
