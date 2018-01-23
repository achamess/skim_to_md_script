#!/usr/bin/env osascript 

tell application "Skim"
	set props to properties of document 1
	set pathToFile to path of props
	get pathToFile
end tell

tell application "Papers"
	set pfi to every primary file item whose full path contains pathToFile
	
	if pfi is not equal to {} then
		set p to properties of publication item of item 1 of pfi
		set BibString to bibtex string of p
		set FullRef to formatted reference of p
		set ck to citekey of p
		set output to pathToFile & "$#*" & BibString & "$#*" & FullRef & "$#*" & ck 
	else
		display dialog "This paper is not in your library"
	end if
end tell


(*

#I used this funky symbol set to separate because its unlikely to be found in any metadata from papers three
*)