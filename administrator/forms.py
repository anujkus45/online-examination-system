from django import forms
from .models import Technology, TestSchedule
from questionbank.models import Question # Import Question from questionbank app

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TestScheduleForm(forms.ModelForm):
    class Meta:
        model = TestSchedule
        fields = ['technology', 'start_time', 'end_time', 'duration_minutes', 'total_questions', 'is_active']
        widgets = {
            'technology': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_questions': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Activate Test'
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['technology', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'marks']
        widgets = {
            'technology': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }