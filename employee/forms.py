from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile # Import EmployeeProfile for registration
from django.core.exceptions import ValidationError
import re

class EmployeeRegistrationForm(forms.ModelForm):

    # ... (existing fields)
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check password length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Must contain one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Must contain one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Must contain one digit
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")

        # Must contain one special character
        if not re.search(r'[\W_]', password):
            raise ValidationError("Password must contain at least one special character.")

        return password
    
    # Fields from User model
    username = forms.CharField(max_length=150, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, 
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label="Confirm Password",
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Fields for EmployeeProfile
    employee_id = forms.CharField(max_length=20,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  help_text="Your unique employee identification number.")
    department = forms.CharField(max_length=100, 
                                 widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 help_text="e.g., HR, IT, Marketing")


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password'] # Base User fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

    

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id and EmployeeProfile.objects.filter(employee_id=employee_id).exists():
            raise ValidationError("An employee with this ID already exists.")
        return employee_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create EmployeeProfile after user is saved
            EmployeeProfile.objects.create(
                user=user,
                employee_id=self.cleaned_data.get('employee_id'),
                department=self.cleaned_data.get('department')
            )
        return user

class EmployeeLoginForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))