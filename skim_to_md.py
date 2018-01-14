#! /Users/alex/anaconda/bin/python
# -*- coding: utf-8 -*-

'''
This is a Python script that takes a PDF annotated in Skim.app and produces individual markdown (.md)
files for each annotation individually. 

Input: A PDF File highlighted/annotated in Skim.app
Output: Individual .md files for each highlight

Requirements:
- skimnotes (https://sourceforge.net/projects/skim-app/files/SkimNotes%20framework%20and%20tool/)
- Python 3

Usage:
- Create a directory (or use an existing one) where the extracts will go
- The PDF of interest must be in the same directory as the script.
- Run the script from the command line and answer the prompts

Note on PDF annotation:
    This script expects that highlighted text comes with summary notes. The summary note
    is used to name the file. So in addition to highlighting a text block, you need to 
    also make an anchored note in Skim and position it to immediately precede a highlight. 


'''

#%%
#import modules
import sys
import subprocess
import glob
import jinja2
import datetime
import os
import re
import bibtexparser #https://bibtexparser.readthedocs.io/en/v0.6.2/index.html
import argparse 


#jinja2.Environment(trim_blocks=True, lstrip_blocks=True)


#%%
'''
get arguments from command line to set variables for final output file
https://stackoverflow.com/questions/7427101/simple-argparse-example-wanted-1-argument-3-results
'''
parser = argparse.ArgumentParser()
parser.add_argument("tags", help="Add your tags here")
args = args = parser.parse_args()
tags = args.tags
print (tags)

#tags = input("Provide a list of tags (optional; comma separated) ").strip('\n')
#modify tags -> separate each tag, put in double quotes, and separate by commas
#https://stackoverflow.com/questions/32765735/python-enclose-each-word-of-a-space-separated-string-in-quotes
# set tags. if empty, do nothing, else, fill with tags given by user
if tags == "":
    pass
else:
    tags= ' '.join('"#{}",'.format(word) for word in tags.split(',')).rstrip(',')


# User needs to set path to bibliography (.bib) file
path_to_bibliography = "/Users/alex/Dropbox/Papers3_Citations/Bibliography-Master.bib"
path_to_zk = "/Users/alex/Dropbox/Sublime_Zettel/Paper_Notes/"

#get bibliography 
with open(path_to_bibliography) as bibtex_file:
    bibtex_str = bibtex_file.read()
bib_database = bibtexparser.loads(bibtex_str)
dicts = bib_database.entries
     
#%% 
#get path to current PDF opened in Skim
pdf_path = subprocess.Popen("osascript skim_current_page.scpt",stdout=subprocess.PIPE, shell=True).stdout.read().decode("utf-8").strip('\n')

#get the bibtex record of the current pdf
for item in dicts:
    if (item.get("file") is not None) and pdf_path in item.get("file"):
        record = item
        print(item.get('title'))
        print("[@"+item.get('ID')+"]")
    else:
        pass


#%% Get information about paper from Bibtex record

# set the input variables
#title = ref.get('title')
citekey = "[@"+record.get('ID')+"]"    
# formatted reference for note 
author_short= record.get('author').split(',',1)[0]
ref =author_short + " " "*et al.*" + " " + "(" + record.get('year') + ")"+"."\
+ " " + record.get('title') + "." + " " + record.get('journal') + " " + \
"*"+ record.get('volume') + "*" + "," + " " + str(record.get('pages'))

#https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
#get current date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
timestamp = now.strftime("%Y%m%d%H%M%S")

#make a folder for the notes if it doesn't exist
#https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
directory = path_to_zk + os.path.basename(pdf_path).replace(".pdf","")
if not os.path.exists(directory):
    os.makedirs(directory)


#%%


#the template for output. eventually will be external, but for now, inside the script. 
template = jinja2.Template("""+++\ntitle = '{{ note_id }}'\ntags = [{{ tags }}]\ndate = {{ date }}\n+++\n
## Summary:\n {{ summary }}\n\n
## Quote:\n>{{ quote }}\n\n**Citekey**: {{citekey}}\n**Reference**: {{ ref }}\n\n
[Link to PDF]({{ pdf_path }})\n\n
## Comments:\n""")


#\n[Link to Source]("{{"< ref '{{ pdf_path }}' >"}}")
#maybe add later



#%%

''' extract the annotations, highlights, etc. from the PDF using skimnotes. 
split the global notes stream into individual highlights. 
'''

# call skimnotes with the pdf file name
# creates a text file 
#turn byte object into string
#https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
notes = subprocess.Popen("skimnotes get -format text {} -".format(pdf_path),stdout=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

#split by double line break
#http://www.pythonforbeginners.com/dictionary/python-split
notes_split = notes.split("\n\n")

#%%
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
   #note_hyphens = re.sub("(\w)\-\s(\w)","\1\2",note)
    #print(note_hyphens)
    #note_hyphens = re.sub("+-\s+")

#turn summaries and quotes into pairs in a dictionary
#https://stackoverflow.com/questions/4576115/convert-a-list-to-a-dictionary-in-python
note_dict = dict(zip(notes_split[::2], notes_split[1::2]))



#%%
'''
use a counter to make files out of the notes_split list
http://itsaboutcs.blogspot.com/2015/02/renaming-files-in-directory-in.html
http://cmdlinetips.com/2012/09/three-ways-to-write-text-to-a-file-in-python/
'''

#i = 1
#for item in notes_split:
#   f= open('./%s.md'%(str(timestamp) + "." + str(i)),'w')
#    result = template.render(title=title, citekey=citekey, ref=ref, quote = item, date=date, pdf_path = pdf_path,
#    tags=tags)
#    f.write(result)
#    f.close()
#    i = i+1
#    

#check files in directory
#turn summary one-liner into file title and fill with paired quoted text
# checks to see if file already exists based on file name (summary one liner needed for ID)  
#  how to check the file names <- https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string


files = [f for f in os.listdir(directory) if os.path.isfile(f)]  
print (files)
i = 1
for key, value in note_dict.items():
    note_id = str(str(timestamp) + "." + str(i) + " " + str(key))
    fn = (os.path.join(directory,'%s.md'%(note_id)))
    print(fn)
    summary = str(key)
    result = template.render(note_id=note_id, citekey=citekey, ref=ref,\
    quote = value, date=date, summary = summary,pdf_path = pdf_path,tags=tags)
    if any(str(key) in file_name for file_name in files): 
        pass
    else:
        f = open(fn,'w')
        f.write(result)
        f.close()
    i = i+1    
#%%