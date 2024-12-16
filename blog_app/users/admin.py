from django.contrib import admin
from .models import Profile
from .models import Complaint


admin.site.register(Profile)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_submitted')  # Fields to display in the admin list view
    search_fields = ('name', 'email', 'subject')  # Searchable fields
