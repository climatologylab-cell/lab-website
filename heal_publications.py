from publications.models import Publication
from datetime import datetime
import re

count = 0
for p in Publication.objects.all():
    title = p.title or ""
    # Regex: Look for a year like 2012 in the middle of a messy title
    # Pattern: Captures Authors, Year, and Title separately
    match = re.search(r'^(.*?)\b(20\d{2}|19\d{2})\b[.\s]+(.*)$', title)
    
    if match:
        authors_found = match.group(1).strip(',. ')
        year_found = int(match.group(2))
        clean_title = match.group(3).strip('.- ')
        
        # 1. Populate missing year
        p.publication_date = datetime(year_found, 1, 1).date()
        
        # 2. Extract clean title
        if len(clean_title) > 5:
            p.title = clean_title
            
        # 3. Clean up authors if they are the default "Unknown" or just a snippet
        if not p.authors or 'Unknown' in p.authors or len(p.authors) < 10:
            if len(authors_found) > 5:
                p.authors = authors_found
        
        p.save()
        count += 1

print(f"Healed {count} publications from messy title data.")
