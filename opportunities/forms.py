from django import forms
from .models import Opportunity


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = (
            'name', 'customer', 'amount', 'stage',
            'probability', 'expected_closing_date',
            'assigned_to', 'notes'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500 Software Licenses Deal'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stage': forms.Select(attrs={'class': 'form-select'}),
            'probability': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'expected_closing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deal notes or proposal terms...'}),
        }
