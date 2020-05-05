from django.contrib import admin
from core.models import Entry

#adds Entry to admin page 
admin.site.register(Entry)