from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import EmployeeResult
from employee.models import EmployeeTestAttempt # To access attempt details
from questionbank.models import Answer # To display answers
from administrator.models import Technology # To filter by technology if needed

# Helper function for admin check
def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- Admin Views for Results ---
@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def view_all_results_admin(request):
    all_results = EmployeeResult.objects.all().order_by('-declared_at')
    technologies = Technology.objects.all()

    selected_tech_id = request.GET.get('technology')
    if selected_tech_id:
        all_results = all_results.filter(test_schedule__technology__id=selected_tech_id)

    context = {
        'all_results': all_results,
        'technologies': technologies,
        'selected_tech_id': int(selected_tech_id) if selected_tech_id else None,
    }
    return render(request, 'results/view_results.html', context)

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def view_detailed_result_admin(request, result_id):
    result = get_object_or_404(EmployeeResult, id=result_id)
    attempt = result.test_attempt # Get the associated test attempt

    # If the attempt is not linked or not found, handle gracefully
    if not attempt:
        messages.warning(request, "Associated test attempt not found for this result.")
        answers = []
        correct_count = 0
        total_questions = 0
        total_marks_obtained = result.score # Use the stored score
        total_possible_marks = 0 # Cannot determine without attempt
    else:
        answers = Answer.objects.filter(test_attempt=attempt).select_related('question').order_by('question__id')
        correct_count = 0
        total_marks_obtained = 0
        total_possible_marks = 0

        for ans in answers:
            total_possible_marks += ans.question.marks
            if ans.selected_option == ans.question.correct_option:
                correct_count += 1
                total_marks_obtained += ans.question.marks
        total_questions = answers.count()

    context = {
        'result': result,
        'attempt': attempt, # Pass the attempt object for display
        'answers': answers,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'total_marks_obtained': total_marks_obtained,
        'total_possible_marks': total_possible_marks,
    }
    return render(request, 'results/employee_result.html', context) # Re-using the employee result display template


