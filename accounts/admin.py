from django.contrib import admin
from .models import Profile 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__username',)
