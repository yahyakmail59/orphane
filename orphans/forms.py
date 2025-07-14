from django import forms
from .models import Orphan, Sponsorship

class OrphanForm(forms.ModelForm):
    class Meta:
        model = Orphan
        fields = ['full_name', 'id_number', 'date_of_birth', 'guardian_name', 'guardian_id_number', 'guardian_phone', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['orphan', 'sponsor_name', 'sponsorship_date', 'amount', 'receipt_image']
        widgets = {
            'orphan': forms.Select(attrs={'class': 'form-control'}),
            'sponsor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sponsorship_date': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'receipt_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
