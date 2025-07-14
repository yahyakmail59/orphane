from django.contrib import admin
from .models import Orphan, Sponsorship

@admin.register(Orphan)
class OrphanAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'id_number', 'date_of_birth', 'guardian_name')

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('orphan', 'sponsor_name', 'sponsorship_date', 'amount', 'receipt_image')
