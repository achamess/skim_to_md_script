#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 23:53:39 2018

@author: alex
"""

import os
import re 

#find all .md files in directory
#http://www.pythonforbeginners.com/code-snippets-source-code/python-os-listdir-and-endswith
all_files = [f for f in os.listdir(directory)]
files = []
for f in all_files:
    if f.endswith(".md"):
        files.append(f)  
        
#get the quoted text into a list
quotes = []
for i in range(len(files)):
    print (i)
    with open(files[i], "r") as f:
        text = f.read()
        pattern = re.search("## Quote:\n>.*\n", text)
        quotes.append(pattern.group(0))   
    f.close()
     
#create extracts    
i = 1
for key, value in note_dict.items():
    uid = str(str(timestamp) + "." + str(i))
    note_id = str(uid + " " + str(key))
    #note_id = str(str(timestamp) + "." + str(i) + " " + str(key))
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




    



for file in:
    
    
    searchfile = open("file.txt", "r")
for line in searchfile:
    if "searchphrase" in line: print line
searchfile.close()