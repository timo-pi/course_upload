from django.contrib import admin
from .models import Course

@admin.register(Course)
class PetAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'path', 'deletion_date', 'description']
# admin.site.register(Course)

