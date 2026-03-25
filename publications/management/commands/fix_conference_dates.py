import re
from datetime import date
from django.core.management.base import BaseCommand
from publications.models import Publication


class Command(BaseCommand):
    help = 'Backfills missing publication_date for conference (and other) entries by scanning the citation field'

    def handle(self, *args, **kwargs):
        # Target publications missing a date
        qs = Publication.objects.filter(publication_date__isnull=True)
        self.stdout.write(f"Found {qs.count()} publications without a date. Attempting to fix...")

        fixed = 0
        skipped = 0

        for pub in qs:
            # Try to find a 4-digit year (1900-2099) in citation, then title
            year = None
            for text in [pub.citation or '', pub.title or '', pub.authors or '']:
                match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
                if match:
                    year = int(match.group(1))
                    break

            if year:
                pub.publication_date = date(year, 1, 1)
                pub.save(update_fields=['publication_date'])
                fixed += 1
                self.stdout.write(f"  Fixed: [{pub.category}] {pub.title[:60]}... → {year}")
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Fixed: {fixed}, Could not determine year for: {skipped}"
        ))
