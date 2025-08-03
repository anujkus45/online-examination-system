from django import forms
from .models import EmployeeResult

class EmployeeResultForm(forms.ModelForm):
    # This form is primarily for admin to declare/update a result.
    # Employee cannot use this to submit their exam.
    class Meta:
        model = EmployeeResult
        fields = ['score', 'passed', 'remarks'] # Exclude fields auto-populated or set by system
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'passed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'passed': 'Candidate Passed'
        }