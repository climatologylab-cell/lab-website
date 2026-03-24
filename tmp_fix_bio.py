import re
import os

filepath = r'c:\Users\Gourav\OneDrive\Desktop\Internship IITR\Lab\templates\team.html'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any multi-line expanded-bio paragraph with a simple single-line one
# This helps with Django template tag rendering issues.
new_text = re.sub(r'<p class="expanded-bio">\{\{.*?\}\}</p>', 
                  '<p class="expanded-bio">{{ member.bio|default:"Information coming soon..." }}</p>', 
                  text, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content if 'content' in locals() else new_text) # Wait, my previous content was not correct.
