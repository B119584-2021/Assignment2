#!/usr/local/bin/python3

### Load necessary modules ###
import os, subprocess, sys, re



### ASK USER FOR INFO ###

# Ask user to specify protein family
protein_fam = input( "Which protein family are you analysing?\n\t> " )

# If variable is empty, repeat request
while not protein_fam :
  print( "Please provide a protein family" )
  try :
   protein_fam = input( "\t> " )
  except :
    continue

# Print selection of protein_fam to screen
print( protein_fam, "selected\n" )


# Ask user to specify taxonomic group
taxon_gr = input( "Which taxonomic group are you analysing?\n\t> " )

# If variable is empty, repeat request
while not taxon_gr :
  print( "Please provide a taxon group" )
  try :
   taxon_gr = input( "\t> " )
  except :
    continue
print( taxon_gr, "selected\n" )



### SET VARIABLES ###
space = " AND "
quote = "\""
full_query = quote + taxon_gr + space + protein_fam + quote
entrez_sum = " > entrez_sum.txt"
fetch_fasta = " | efetch -format fasta > fasta_seq.fa"

# Combine variables to generate esearch command variables 
esearch_count = "esearch -db protein -query " + full_query + entrez_sum
esearch_fasta = "esearch -db protein -query " + full_query + fetch_fasta



### HOW MANY SEQUENCES? ###
subprocess.call( esearch_count, shell = True )

# Open file containing entrez summary 
with open( "entrez_sum.txt" ) as my_file:
      entrez_sum = my_file.read()

# Format entrez_sum to a list so it can be iterated over
entrez_summary = entrez_sum.split( "\n" )


## Find countline 
# Create empty list
count_line = []

# Iterate over summary and store line with sequence count
for sum in entrez_summary :
     if re.search( r'Count', sum ) :
             count_line.append( sum )

# Extract count from countline
count = re.findall( r'\d+', str( count_line ) )
count_str = str( count ).strip( "['']" )

# Set sequence count as variable x
x = int( count_str )

if x < 1 :
  print( "There were no sequences found for your search" )
  sys.exit( "Exiting...\n" )

# Print sequence count to screen for user to see
print( "Number of sequences:", +x, "\n" )



### >1000 sequences ###

# This block interacts with the user if > 1000 or < 10

# Find out how user would like to proceed:
a = 0
while x > 1000 :
  a = input( "More than 1000 sequences, do you wish to continue? (Yes or No)\n\t> " )
  try :
    if a == "Yes" or a == "No" :
      break ;
    a = input( "Please type Yes or No\n\t> " )
  except :
    continue

if ( not a == True ) :
  if ( a == "Yes" ) :
    print( "Continuing...\n" )
  if ( a == "No" ):
    sys.exit( "Exiting due to more than 1000 sequences\n" )


# If there are fewer than 10 sequences
b = 0
while x <= 10 :
  b = input( "There are less than 10 sequences, would you like to continue? (Yes or No)\n\t> " )
  try :
    if b == "Yes" or b == "No" :
      break ;
  except :
    continue

if ( not b == True ) :
  if ( b == "Yes" ) :
    print( "Continuing" )
  if ( b == "No" ) :
    sys.exit( "Exiting due to less than 10 sequences\n" )



### Download FASTA sequences ###

print( "Fetching sequences in FASTA format\n" )
 
subprocess.call( esearch_fasta, shell = True )



### Import necessary modules ###
import re, subprocess, sys
import pandas as pd



### Open FASTA file and assess sequences ###

# Open the FASTA file
with open( "fasta_seq.fa" ) as my_file :
      fasta_seq = my_file.read()


# Split sequence into a list so that elements can be iterated over
fasta = fasta_seq.split( "\n" )


# Create empty lists for series used to make dataframe
species_name = []
species_id = []
species_info = []


# The loop iterates over FASTA file, adding each sequences name, id and info to lists 
for line in fasta :
	if re.search( r'>', line ) : 
		species_name.append( line.split( "[" )[ -1 ].strip( "]" ) )
		species_id.append( line.split( " " )[ 0 ] )
		name = line.split( "[" )[ -1 ].strip( "]" )
		id = line.split( " " )[ 0 ]
		species_info.append( line.replace( id , "" ).replace( name, "" ).strip( "[]" ) )


# Create a dataframe which contains the species ID and name
s1 = pd.Series( species_id )
s2 = pd.Series( species_name )
s3 = pd.Series( species_info )

All_IDs_names = pd.DataFrame( { 'ID' : s1, 'Name' : s2, 'Info' : s3 } )


# Save a file that contains the IDs, names and info of the species proteins in the original fasta file 
All_IDs_names.to_csv( "Sum_IDs_names_info.csv ", sep = "\t" )

# Create and save a file that lists unique species and their counts
unique_species_count = pd.DataFrame( All_IDs_names['Name'].value_counts() )
unique_species_count.to_csv( "Unique_species_count.csv", sep = "\t" )
unique_species_count = pd.read_csv( "Unique_species_count.csv", sep = "\t" )
unique_species_count.columns = ['Name', 'Count']
unique_species_count.to_csv( "Unique_species_count.csv", sep = "\t" )

# Print the top and bottom 15 unique species to the screen
print( "\nMost frequently occurring species:\n")
print( unique_species_count.head(15) )
print( "\nLeast frequently occurring species:\n" )
print( unique_species_count.tail(15) )

# Set variable with highest species count
max = unique_species_count['Count'][0]



### User input to assess the dataset ###

# Explain what printed lines above are
print( "\nThe most and least frequent species have been listed for the downloaded sequences.\n" )

while True:
  try:
    a = input( "Would you like to keep all sequences and proceed with alignment? Type 'keep all'\nWhat is the minimum number of sequences you would like to keep? Type 'x'\n\t> " )

    # To keep all sequences 
    if a == "keep all" :
      print( "Keeping all sequences" )
      # Create input_fasta.fa and write fasta_seq contents to file
      inputf = open( "input_fasta.fa", "w" )
      inputf.write( fasta_seq )
      inputf.close()
      break

    # To only keep a subset of sequences 
    if int(a) <= max :
      print( "Subsetting desired sequences" )
      # Create list of unique names to subset sequences for
      subset = unique_species_count[ (unique_species_count['Count'] > int(a)) ]
      names = list( subset['Name'] )

      fasta = fasta_seq.split( ">" )
      symbol = ">"

      # Create a new fasta file split into whole sequences
      fasta_list = []
      for line in fasta :
        fasta_list.append( symbol + line )

      # Iterate over the objects in the new fasta file
      # Will only keep sequences in list "names" 
      inputf = open( "input_fasta.fa", "w" )
      for line in fasta_list :
        for name in names :
          if re.search( name, line ) :
            inputf.write( line )
      inputf.close()
      break

  except:
    print( "Wrong input, please input keep all or a number" )
    continue



### Alignment and plotting ###

# Alignment is carried out using clustalo 
subprocess.call( "clustalo -i input_fasta.fa --outfmt msf --wrap=80 > aligned_seq.msf", shell = True )

# A prettier alignment is carried out with showalign
subprocess.call( "showalign -sequence aligned_seq.msf", shell = True )

# subprocess.call("patmatmotifs -sequence fasta_seq.fa", shell = True )

# Conservation is plotted using plotcon
subprocess.call( "plotcon -sformat msf aligned_seq.msf -graph svg", shell = True )

