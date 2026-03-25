import re
from datetime import datetime
from import_export import resources, fields
from import_export.widgets import DateWidget
from .models import Publication

class FlexibleDateWidget(DateWidget):
    """Widget to handle multiple date formats and extraction from text."""
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            # Try to extract year from citation if date is missing
            citation = row.get('DATA', '') or row.get('CITATION', '') or row.get('Citation', '')
            # Regex: look for a 4-digit year like 2012 or (2012)
            year_match = re.search(r'\(?(\b20\d{2}|19\d{2}\b)\)?', citation)
            if year_match:
                try:
                    return datetime(int(year_match.group(1)), 1, 1).date()
                except (ValueError, TypeError):
                    return None
            return None
        
        # Try common formats
        formats = ['%Y-%m-%d', '%b %d, %Y', '%d-%m-%Y', '%d/%m/%Y', '%m/%d/%Y', '%Y']
        for fmt in formats:
            try:
                return datetime.strptime(str(value).strip(), fmt).date()
            except (ValueError, TypeError):
                continue
        return super().clean(value, row, *args, **kwargs)

class PublicationResource(resources.ModelResource):
    # Map CSV columns (case-insensitive mapping handled in before_import_row)
    citation = fields.Field(attribute='citation', column_name='DATA')
    publication_date = fields.Field(attribute='publication_date', column_name='DATE', widget=FlexibleDateWidget())
    external_link = fields.Field(attribute='external_link', column_name='LINK')
    title = fields.Field(attribute='title', column_name='TITLE')
    authors = fields.Field(attribute='authors', column_name='AUTHORS')
    
    def before_import_row(self, row, **kwargs):
        # 1. Handle case-insensitive headers and common variations (including spaces)
        for key in list(row.keys()):
            k_upper = str(key).upper().replace(' ', '_')
            val = row.pop(key)
            
            if k_upper == 'AUTHORS': row['AUTHORS'] = val
            elif k_upper == 'TITLE': row['TITLE'] = val
            elif k_upper in ['DATE', 'PUBLICATION_DATE']: row['DATE'] = val
            elif k_upper in ['DATA', 'CITATION', 'SOURCE']: row['DATA'] = val
            elif k_upper in ['LINK', 'EXTERNAL_LINK', 'URL']: row['LINK'] = val
            elif k_upper == 'CATEGORY': row['category'] = val
            elif k_upper == 'SCOPE': row['scope'] = val
            elif k_upper == 'IS_ACTIVE': row['is_active'] = val
            elif k_upper == 'IS_FEATURED': row['is_featured'] = val
            else:
                row[key] = val # Restore original for other fields

        # 2. Map Category values if needed
        cat = str(row.get('category', '')).lower().strip()
        if 'conference' in cat: row['category'] = 'conference'
        elif 'journal' in cat: row['category'] = 'journal'
        elif 'book' in cat or 'guideline' in cat: row['category'] = 'book'
        
        # 3. Map Scope values
        scope = str(row.get('scope', '')).lower().strip()
        if 'national' in scope: row['scope'] = 'national'
        elif 'international' in scope: row['scope'] = 'international'

        # 4. Map Boolean values (Yes/No to True/False)
        for bool_field in ['is_active', 'is_featured']:
            val = str(row.get(bool_field, '')).lower().strip()
            if val in ['yes', 'true', '1', 'active']:
                row[bool_field] = True
            elif val in ['no', 'false', '0', 'hidden']:
                row[bool_field] = False

        # 5. Extract Title and Authors from Citation (DATA) if missing
        citation = row.get('DATA', '')
        if citation:
            parts = [p.strip() for p in citation.split('.') if p.strip()]
            if not row.get('TITLE') or row.get('TITLE') == row.get('DATA'):
                if parts: row['TITLE'] = parts[0][:499]
                
            if not row.get('AUTHORS') or row.get('AUTHORS') == "Unknown Authors":
                for part in parts:
                    if re.search(r'\(\d{4}\)', part):
                        author_part = part.split('(')[0].strip()
                        if author_part:
                            row['AUTHORS'] = author_part
                            break
    class Meta:
        model = Publication
        fields = ('id', 'citation', 'publication_date', 'external_link', 'title', 'authors', 'journal', 'category')
        import_id_fields = ('title',)
        skip_unchanged = True
