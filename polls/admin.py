from django.contrib import admin
from .models import Urlentry, Leads

# Register your models here.
@admin.register(Urlentry)
class UrlentryAdmin(admin.ModelAdmin):
    fields = ['url_text', 'url_short', 'author', 'url_id', 'create_date','datetime_available_from', 'datetime_available_to', 'partner_ads','qr_code','snapshot']
    list_display = ('url_text', 'url_short', 'author', 'url_id', 'create_date','datetime_available_from', 'datetime_available_to', 'partner_ads','qr_code','snapshot')
    list_filter = ['create_date','author', 'url_short']
    list_per_page = 10
    date_hierarchy = 'create_date'
    ordering = ['url_short']

@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    fields = ['urlentry', 'follow_date', 'follower_info', 'follower_os_info', 'follower_fromwhere']
    list_display = ('urlentry','follow_date','follower_info','follower_os_info','follower_fromwhere')
    list_filter = ['urlentry','follow_date']
    list_per_page = 10
    date_hierarchy = 'follow_date'