from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('browse', views.browse, name='browse'),
    path('search', views.Search, name="search"),
    path('<f>/<p>/<doc>', views.show_pdf, name='docs'),
]
