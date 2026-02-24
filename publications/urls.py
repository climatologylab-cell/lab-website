from django.urls import path
from . import views

app_name = 'publications'

urlpatterns = [
    path('', views.publication_list, name='index'),
    path('journals/', views.publication_list, {'category': 'journal'}, name='journals'),
    path('conferences/', views.publication_list, {'category': 'conference'}, name='conferences'),
    path('conference/national/', views.publication_list, {'category': 'conference', 'scope': 'national'}, name='conference_national'),
    path('conference/international/', views.publication_list, {'category': 'conference', 'scope': 'international'}, name='conference_international'),
    path('books/', views.publication_list, {'category': 'book'}, name='books'),
    path('guidelines/', views.publication_list, {'category': 'guideline'}, name='guidelines'),
    path('other/', views.publication_list, {'category': 'other'}, name='others'),
]
