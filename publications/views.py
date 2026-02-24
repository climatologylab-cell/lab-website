from django.shortcuts import render
from .models import Publication
from django.db.models import Q

def publication_list(request, category=None, scope=None):
    """
    Unified view for listing publications with search and sort.
    Optional 'category' argument filters the query.
    Optional 'scope' argument for conferences (national/international).
    """
    # Base queryset
    queryset = Publication.objects.filter(is_active=True)
    
    if category:
        queryset = queryset.filter(category=category)
        
    # Scope filtering
    if scope:
        queryset = queryset.filter(scope=scope)
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(abstract__icontains=search_query) |
            Q(authors__icontains=search_query) |
            Q(journal__icontains=search_query)
        )
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'latest':
        queryset = queryset.order_by('-publication_date')
    elif sort_by == 'oldest':
        queryset = queryset.order_by('publication_date')
    elif sort_by == 'az':
        queryset = queryset.order_by('title')
    elif sort_by == 'za':
        queryset = queryset.order_by('-title')
    else:
        queryset = queryset.order_by('-publication_date')  # Default
        
    # Map category codes to display titles
    titles = {
        'journal': 'Journal Articles',
        'conference': 'Conference Papers',
        'book': 'Book Chapters',
        'thesis': 'Theses',
        'report': 'Technical Reports',
        'guideline': 'Guidelines',
        'other': 'Other Documents',
    }
    
    
    page_title = titles.get(category, 'All Publications')
    
    if category == 'conference' and scope:
        if scope == 'national':
            page_title = 'National Conference Papers'
        elif scope == 'international':
            page_title = 'International Conference Papers'
    
    context = {
        'publications': queryset,
        'page_title': page_title,
        'current_category': category,
        'current_scope': scope,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'publication_list.html', context)

