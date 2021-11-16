### TASK 1: Fetching user specified  protein sequence data ### 
# The aim of this script is to fetch protein sequence data detailed in user input and to provide the user with a summary of actions taken. 

#!/usr/bin/python3

# Load necessary modules 
import os, subprocess 

### ASK USER FOR INFO ###

# Ask user to specify protein family
protein_family=input("Which protein family are you analysing?\n\t> ")
print(protein_family, "selected")

# Ask user to specify taxonomic group
taxonomic_group=input("Which taxonomic group are you analysing?\n\t> ")
print(taxonomic_group, "selected")

esearch_command="esearch -db protein_family -query taxonomic_group"


	#esearch -db protein -query "taxonomic_group AND protein_family" | efetch -db protein -format uid > uid_output

	#cat uid_output | wc -l > seq_number
	
	#if (seq_number > 1000):
	#	answer=input("More than 1000 sequences, do you wish to continue (Yes or No)?\n\t> ")
	#	if answer == "Yes":
	#		print("Continuing to the next step")
	#	else:
	# 		 exit("Exiting script due to 1000+ sequences"

# These will then be input to the command used to fetch the sequences,
# before downloading check the number of sequeces and the composition


# Perform command to fetch protein sequence data
subprocess.call("esearch_command, shell=True")

### CHECK IN WITH USER ###

# More than 1000 sequences - do you wish to continue?

# The sequences come from more than one species - do you wish to continue?


# Once sequences are fetched provide user with a summary
