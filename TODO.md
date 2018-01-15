## To Do 
- Add ability to choose whether to name based on summary note or not. Some PDFs won't have summary notes. I'd still like to be able to extract highlights without requiring a summary note
- Connect to bibtex library to extract metadata
- Make multiple templates and externalize 


## Log 

**2018-01-07**
- Changed the naming of each file to include a one-line summary that comes from the PDF.
- Anchor note: Highlight pairing
    + In the PDF, each highlight also gets a matching anchor note that I create. The anchor note is a summary one-liner. That summary one-liner because part of the name of the file and also the summary in the note. 
- Check to see if file already exists
    + Because the name now has a summary line in the title, I can use that string to see if a file already exists. 
    + Now, when the script is run, it checks to see what files already exist based on the summary line in the file name. So if the file already exists, it doesn't get ovewritten. In this way, I can return to a PDF at some time in the future, add a new highlight, and not overwrite existing files. 