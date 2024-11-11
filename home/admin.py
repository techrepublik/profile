from django.contrib import admin
from django.db.models.lookups import PostgresOperatorLookup

from .models import Position, Faculty, Department

admin.site.register(Position)
admin.site.register(Faculty)
admin.site.register(Department)
