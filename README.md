# skim_to_md

This is a script in python that takes highlighted text from a PDF in [Skim.app]() and produces individual markdown files for each highlight. 

## What it does

- Export highlights from a PDF annotated in Skim.app
- Converts each highlight into a single Markdown-formatted file 
- Names each file uniquely 

This is a work in progress and eventually, I hope to add additional features.

In addition to the highlighted text, the output files have other fields, including:
- Title
- Tags
- Reference citation
- Citekey: For reference managers such as Papers3.app, Zotero, Bibdesk...
- Summary
- Comments

These bits of info are usually what one needs to have at hand for producing some kind of writing or scholarly output. Kind of like old school index-cards were used for research once upon a time.

## Who's it for?

Anyone who does work wtih texts - academics, journalists, writers, researchers, etc.

## Requirements
- [skimnotes - command line tool for Skim.app](https://sourceforge.net/projects/skim-app/files/SkimNotes%20framework%20and%20tool/)
- [Skim.app](https://sourceforge.net/projects/skim-app)

## Roadmap

- Format notes using a templating engine such as Django or Jinja2
- Add additional information to the final note, including a bibtex citekey and full reference 
- Add additional fields in the markdown note for comments, thoughts, and related information.