#! /Users/alex/anaconda/bin/python
# -*- coding: utf-8 -*-

'''
This is a Python script that takes a PDF annotated in Skim.app and produces individual markdown (.md)
files for each annotation individually. 

Input: A PDF File highlighted/annotated in Skim.app and contained in Papers3
Output: Individual .md files for each highlight

Requirements:
- skimnotes (https://sourceforge.net/projects/skim-app/files/SkimNotes%20framework%20and%20tool/)
- Python 3
- Papers3
- Skim.app

Usage:
- Select the paper in Papers3.app and make the current open window
- Run the script. 

Note on PDF annotation:
    This script expects that highlighted text comes with summary notes. The summary note
    is used to name the file. So in addition to highlighting a text block, you need to 
    also make an anchored note in Skim and position it to immediately precede a highlight. 


'''

#%% Module Import 

import subprocess
import jinja2
import datetime
import os
import re
import bibtexparser #https://bibtexparser.readthedocs.io/en/v0.6.2/index.html
import argparse 


#%% Set paths and set time stamps
# User needs to set path to bibliography (.bib) file
path_to_bibliography = "/Users/alex/Dropbox/Papers3_Citations/Bibliography-Master.bib"
path_to_zk = "/Users/alex/Dropbox/Sublime_Zettel/Paper_Notes/"


#get current date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
timestamp = now.strftime("%Y%m%d%H%M")

#%% Jinja Template for output 

#the template for output. eventually will be external, but for now, inside the script. 
template = jinja2.Template("""---\ntitle: {{ note_id }}\ntags: {{ tags }}\ndate: {{ date }}\n---\n# {{ note_id }}\n\n
## Summary:\n {{ summary }}\n\n
## Quote:\n>{{ quote }}\n\n**Citekey**: {{citekey}}\n**Reference**: {{ ref }}\n\n
[Link to PDF]({{ pdf_path }})\n\n
## Comments:\n""")

#%% Applescripts
get_path_skim = '''
tell application "Skim"
	set props to properties of document 1
	set pathToFile to path of props
	get pathToFile
end tell
'''
tags = "#neuro"
#%% Get command line arguments
#
#'''
#get arguments from command line to set variables for final output file
#https://stackoverflow.com/questions/7427101/simple-argparse-example-wanted-1-argument-3-results
#'''
#parser = argparse.ArgumentParser()
#parser.add_argument('-t', help= "Tags (comma separated)")
#parser.add_argument('-s', help= "Summary notes (paired)?", action='store_true')
#parser.add_argument('-p', help= "Does this paper have a listing in Papers3?", action='store_true', required = True)
#
#args = args = parser.parse_args()
#tags = args.t
#print (tags)
#
##modify tags -> separate each tag, put in double quotes, and separate by commas
##https://stackoverflow.com/questions/32765735/python-enclose-each-word-of-a-space-separated-string-in-quotes
##set tags. if empty, do nothing, else, fill with tags given by user
#
#if tags == "":
#    pass
#else:
#    tags= ' '.join('#{}'.format(word) for word in tags.split(',')).rstrip(',')

#%% Run internal scripts 

p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
stdout, stderr = p.communicate(get_path_skim)

pdf_path = stdout.strip('\n')


#%% 
#ref = input("What is the REFERENCE for this document? ")
#citekey = input ("What is the CITEKEY for this document? ")

#%% Notes Processing and Cleanup

''' extract the annotations, highlights, etc. from the PDF using skimnotes. 
split the global notes stream into individual highlights. 
'''
# call skimnotes with the pdf file name
# creates a text file 
#turn byte object into string
#https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
notes = subprocess.Popen("skimnotes get -format text '{}' -".format(pdf_path),stdout=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

#split by double line break
#http://www.pythonforbeginners.com/dictionary/python-split
notes_split = notes.split("\n\n")

#cleanup notes
#remove split page hyphens
#remove "Highlight"
# remove "Anchored Note"

for i in range(len(notes_split)):
    note = notes_split[i]
    note = re.sub("\-\s","",note) #remove split page hyphens
    note = re.sub("\* Highlight, page \d+\n","", note)
    note = re.sub("\* Anchored Note, page \d+\n","", note)
    notes_split[i] = note
 

#%% Check files in directory and look at quoted text to see if already exists (For w/o Summary)
'''
use a counter to make files out of the notes_split list
http://itsaboutcs.blogspot.com/2015/02/renaming-files-in-directory-in.html
http://cmdlinetips.com/2012/09/three-ways-to-write-text-to-a-file-in-python/
'''

#check files in directory
#turn summary one-liner into file title and fill with paired quoted text
# checks to see if file already exists based on file name (summary one liner needed for ID)  
#  how to check the file names <- https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string

#find all .md files in directory
#http://www.pythonforbeginners.com/code-snippets-source-code/python-os-listdir-and-endswith


#set directory to notes in ZK
directory = path_to_zk + os.path.basename(pdf_path).replace(".pdf","").rstrip('\n')
if not os.path.exists(directory):
    os.makedirs(directory)

all_files = [f for f in os.listdir(directory)]
files = []
for f in all_files:
    if f.endswith(".md"):
        files.append(f)  
        
#get the quoted text into a list
quotes = []
for i in range(len(files)):
    print (i)
    with open(os.path.join(directory,files[i]), "r") as f:
        text = f.read()
        pattern = re.search(">(.*)\n", text)
        quotes.append(pattern.group(1))   
    f.close()
    

#%% Create extracts   

# set ref and citekey internally from document anchored notes    
ref = notes_split[0]
citekey = notes_split[1]  

#create extracts    
i = 1
#set starting index to 2 because [0,1] used for ref and citekey 
for item in notes_split[2:]:
    uid = str(str(timestamp) + "." + str(i))
    note_id = str(uid) 
    #note_id = str(str(timestamp) + "." + str(i) + " " + str(key))
    fn = (os.path.join(directory,'%s.md'%(note_id)))
    print(fn)
    #summary = str(key)
    result = template.render(note_id=note_id, citekey=citekey, ref=ref,\
    quote = item, date=date,pdf_path = pdf_path,tags=tags)
    if item in quotes:
        print (item) 
        print (item in quotes)
        pass
    else:
        f = open(fn,'w')
        f.write(result)
        f.close()
    i = i+1   

subprocess.Popen(['open', directory]) #open folder with extracts in Finder

#%%

