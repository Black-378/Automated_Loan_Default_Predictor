from django import forms
from .models import LoanApplication 

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        # We only want the user to fill these 5 things. 
        # The AI will fill 'prediction_result' automatically later.
        fields = ['principal', 'terms', 'age', 'gender', 'education']

        # Making the form look professional with CSS classes
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'principal': forms.NumberInput(attrs={'class': 'form-control'}),
            'terms': forms.NumberInput(attrs={'class': 'form-control'}),
        }