#!/usr/bin/env osascript 
tell application "Papers"
	set p to selected publications of front library window
	set pathToFile to full path of primary file item of item 1 of p
	set BibString to bibtex string of item 1 of p
	set FullRef to formatted reference of item 1 of p
	set ck to citekey of item 1 of p
	set output to pathToFile & " + " & BibString & "+" & FullRef & "+" & ck
	
end tell


