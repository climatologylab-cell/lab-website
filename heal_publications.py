from publications.models import Publication
from datetime import datetime, date
import re

count = 0
for p in Publication.objects.all():
    # If date is already set and not a default "future" date, skip
    if p.publication_date and p.publication_date.year < 2026:
        continue
        
    found_year = None
    
    # 1. Search in title
    title = p.title or ""
    year_in_title = re.search(r'\b(20\d{2}|19\d{2})\b', title)
    if year_in_title:
        found_year = int(year_in_title.group(1))
        
    # 2. Search in citation if not found or if title match is a part of authors
    if not found_year:
        citation = p.citation or ""
        year_in_citation = re.search(r'\b(20\d{2}|19\d{2})\b', citation)
        if year_in_citation:
            found_year = int(year_in_citation.group(1))
            
    if found_year:
        p.publication_date = date(found_year, 1, 1)
        p.save()
        count += 1

    # 3. Fix category if it was imported as 'conference_paper'
    if p.category == 'conference_paper':
        p.category = 'conference'
        p.save()
        
    # 4. Handle records where the date might be the 2026 default
    if p.publication_date and p.publication_date.year >= 2026:
        # Try to re-extract from citation
        citation = p.citation or ""
        year_match = re.search(r'\b(20\d{2}|19\d{2})\b', citation)
        if year_match:
            p.publication_date = date(int(year_match.group(1)), 1, 1)
            p.save()

print(f"Healed {count} publications from messy data.")
