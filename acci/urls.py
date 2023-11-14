
from django.contrib import admin
from django.urls import path
from .views import create_person, success_page, all_attendees, clear_database, download_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', create_person, name="create_person"),
    path('success', success_page, name='success_page'),  # Add the success page URL path
    path('list', all_attendees, name='all_attendees'),
    path('clear-confirmation/', clear_database, name='clear_database'),
    path('download-excel/', download_excel, name='download_excel'),

]
