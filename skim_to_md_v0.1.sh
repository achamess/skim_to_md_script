#!/Users/alex/anaconda/bin/python
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


'''

#%%
#import modules
import subprocess
import glob
import jinja2
import datetime
import os

#jinja2.Environment(trim_blocks=True, lstrip_blocks=True)


#%%
'''
get arguments from command line to set variables for final output file
https://stackoverflow.com/questions/7427101/simple-argparse-example-wanted-1-argument-3-results
'''


# set the input variables
title = input("What is the TITLE of the paper? ").strip('\n')
citekey = input("What is the CITEKEY? ").strip('\n')
ref = input("What is the full REFERENCE of the paper? ").strip('\n')
tags = input("Provide a list of tags (optional; comma separated) ").strip('\n')
#tags = args.tags


#https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
#get current date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
timestamp = now.strftime("%Y%m%d%H%M%S")



#the template for output. eventually will be external, but for now, inside the script. 
template = jinja2.Template("""+++\ntitle = '{{ title }}'\ntags = []\ndate = {{ date }}\n+++\n
## Summary:\n\n
## Quote:\n>{{ quote }}\n\n**Citekey**: {{citekey}}
**Reference**: {{ ref }}\n\n## Comments:\n""")


#\n[Link to Source]("{{"< ref '{{ pdf_path }}' >"}}")
#maybe add later



#%%

''' extract the annotations, highlights, etc. from the PDF using skimnotes. 
split the global notes stream into individual highlights. 
'''

#find the pdf
pdf = glob.glob("*.pdf")
pdf = pdf[0].replace('"','')
pdf_path = os.path.relpath(pdf)


# call skimnotes with the pdf file name
# creates a text file 
notes = subprocess.Popen("skimnotes get -format text {} -".format(pdf), 
              stdout=subprocess.PIPE, shell=True).stdout.read()


'''
turn byte object into string
https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
'''

notes=notes.decode("utf-8")

#split by double line break
#http://www.pythonforbeginners.com/dictionary/python-split
notes_split = notes.split("\n\n")




#%%
'''
use a counter to make files out of the notes_split list
http://itsaboutcs.blogspot.com/2015/02/renaming-files-in-directory-in.html
http://cmdlinetips.com/2012/09/three-ways-to-write-text-to-a-file-in-python/
'''

i = 1
for item in notes_split:
    f= open('./%s.md'%(str(timestamp) + "." + str(i)),'w')
    result = template.render(title=title, citekey=citekey, ref=ref, quote = item, date=date, pdf_path = pdf_path)
    f.write(result)
    f.close()
    i = i+1
    
#%%