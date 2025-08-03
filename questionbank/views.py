from django.shortcuts import render
from django.http import JsonResponse
from .models import Question
from django.core import serializers
# Create your views here.
def get_questions_api(request, technology_id):
    questions = Question.objects.filter(technology_id=technology_id).values(
        'id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d'
    )
    return JsonResponse(list(questions), safe=False)



