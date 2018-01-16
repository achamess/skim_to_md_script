template = jinja2.Template("""---\ntitle = '{{ note_id }}\ntags = {{ tags }}\ndate = {{ date }}\n---\n
## Summary:\n {{ summary }}\n\n
## Quote:\n>{{ quote }}\n\n**Citekey**: {{citekey}}\n**Reference**: {{ ref }}\n\n
[Link to PDF]({{ pdf_path }})\n\n
## Comments:\n""")