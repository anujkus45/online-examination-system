from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count

from .models import Technology, TestSchedule
from questionbank.models import Question # Import Question model from questionbank
from employee.models import EmployeeProfile, EmployeeTestAttempt # Import from employee app
from results.models import EmployeeResult # Import from results app

from .forms import TechnologyForm, TestScheduleForm, QuestionForm
from results.forms import EmployeeResultForm # Assuming you have a form for declaring results

# Helper function to check if the user is an administrator (staff status)
def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- Admin Dashboard ---
@login_required
@user_passes_test(is_admin, login_url='/employee/login/') # Redirect to employee login if not admin
def admin_dashboard(request):
    total_technologies = Technology.objects.count()
    total_test_schedules = TestSchedule.objects.count()
    active_test_schedules = TestSchedule.objects.filter(is_active=True).count()
    total_questions = Question.objects.count()
    total_employees = EmployeeProfile.objects.count()
    total_exam_attempts = EmployeeTestAttempt.objects.count()
    completed_exam_attempts = EmployeeTestAttempt.objects.filter(is_completed=True).count()

    context = {
        'total_technologies': total_technologies,
        'total_test_schedules': total_test_schedules,
        'active_test_schedules': active_test_schedules,
        'total_questions': total_questions,
        'total_employees': total_employees,
        'total_exam_attempts': total_exam_attempts,
        'completed_exam_attempts': completed_exam_attempts,
    }
    return render(request, 'admin/dashboard.html', context)


# --- Technology Management ---
@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def manage_technologies(request):
    technologies = Technology.objects.all().order_by('name')
    context = {'technologies': technologies}
    return render(request, 'admin/technology_management.html', context)

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def add_technology(request):
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Technology added successfully!")
            return redirect('admin_manage_technologies')
    else:
        form = TechnologyForm()
    return render(request, 'admin/technology_form.html', {'form': form, 'title': 'Add New Technology'})

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def update_technology(request, tech_id):
    technology = get_object_or_404(Technology, id=tech_id)
    if request.method == 'POST':
        form = TechnologyForm(request.POST, instance=technology)
        if form.is_valid():
            form.save()
            messages.success(request, "Technology updated successfully!")
            return redirect('admin_manage_technologies')
    else:
        form = TechnologyForm(instance=technology)
    return render(request, 'admin/technology_form.html', {'form': form, 'title': 'Update Technology'})

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def delete_technology(request, tech_id):
    technology = get_object_or_404(Technology, id=tech_id)
    if request.method == 'POST':
        try:
            technology.delete()
            messages.success(request, f"Technology '{technology.name}' deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting technology: {e}")
    return redirect('admin_manage_technologies')

# --- Test Schedule Management ---
@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def manage_tests(request):
    test_schedules = TestSchedule.objects.all().order_by('-start_time')
    context = {'test_schedules': test_schedules}
    return render(request, 'admin/test_scheduling.html', context)

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def add_test_schedule(request):
    if request.method == 'POST':
        form = TestScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Test schedule added successfully!")
            return redirect('admin_manage_tests')
    else:
        form = TestScheduleForm()
    return render(request, 'admin/test_schedule_form.html', {'form': form, 'title': 'Add New Test Schedule'})

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def update_test_schedule(request, test_id):
    test_schedule = get_object_or_404(TestSchedule, id=test_id)
    if request.method == 'POST':
        form = TestScheduleForm(request.POST, instance=test_schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Test schedule updated successfully!")
            return redirect('admin_manage_tests')
    else:
        form = TestScheduleForm(instance=test_schedule)
    return render(request, 'admin/test_schedule_form.html', {'form': form, 'title': 'Update Test Schedule'})

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def delete_test_schedule(request, test_id):
    test_schedule = get_object_or_404(TestSchedule, id=test_id)
    if request.method == 'POST':
        try:
            test_schedule.delete()
            messages.success(request, "Test schedule deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting test schedule: {e}")
    return redirect('admin_manage_tests')


# --- Question Management (Integrated with questionbank app's models) ---
@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def manage_questions(request):
    questions = Question.objects.all().order_by('technology__name', 'id')
    context = {'questions': questions}
    return render(request, 'admin/question_management.html', context)

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Question added successfully!")
            return redirect('admin_manage_questions')
    else:
        form = QuestionForm()
    return render(request, 'admin/question_form.html', {'form': form, 'title': 'Add New Question'})

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect('admin_manage_questions')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin/question_form.html', {'form': form, 'title': 'Update Question'})

@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        try:
            question.delete()
            messages.success(request, "Question deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting question: {e}")
    return redirect('admin_manage_questions')


# --- Results Management (Admin's view of all results) ---
@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def view_all_exam_results(request):
    # Fetch all completed attempts and their associated results
    attempts_with_results = EmployeeTestAttempt.objects.filter(is_completed=True).order_by('-end_time')
    # You might want to filter or paginate these for larger datasets

    context = {
        'attempts_with_results': attempts_with_results,
    }
    return render(request, 'results/view_results.html', context) # Re-using results app template


@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def view_detailed_exam_result(request, attempt_id):
    attempt = get_object_or_404(EmployeeTestAttempt, id=attempt_id, is_completed=True)
    answers = attempt.answers.all().select_related('question') # Get all answers for this attempt

    # Calculate details for the result page
    correct_count = 0
    total_marks_obtained = 0
    total_possible_marks = 0

    for ans in answers:
        total_possible_marks += ans.question.marks
        if ans.selected_option == ans.question.correct_option:
            correct_count += 1
            total_marks_obtained += ans.question.marks

    context = {
        'attempt': attempt,
        'answers': answers,
        'correct_count': correct_count,
        'total_questions': answers.count(),
        'total_marks_obtained': total_marks_obtained,
        'total_possible_marks': total_possible_marks,
    }
    return render(request, 'results/employee_result.html', context) # Re-using employee result template


@login_required
@user_passes_test(is_admin, login_url='/employee/login/')
def declare_result(request, attempt_id):
    attempt = get_object_or_404(EmployeeTestAttempt, id=attempt_id, is_completed=True)
    # Check if a result has already been declared for this attempt
    result, created = EmployeeResult.objects.get_or_create(
        employee=attempt.employee,
        test_schedule=attempt.test_schedule,
        defaults={
            'score': attempt.score,
            'declared_by': request.user,
            'passed': attempt.score >= 50 # Example: Pass if score is 50% or more
        }
    )

    if not created:
        messages.info(request, "Result for this attempt has already been declared.")
        if request.method == 'POST': # Allow updating declared result
            form = EmployeeResultForm(request.POST, instance=result)
            if form.is_valid():
                form.save()
                messages.success(request, "Result updated successfully.")
                return redirect('admin_view_detailed_exam_result', attempt_id=attempt.id)
        else:
            form = EmployeeResultForm(instance=result)
    else:
        messages.success(request, "Result declared successfully!")
        form = EmployeeResultForm(instance=result)

    context = {
        'attempt': attempt,
        'result_form': form,
        'result_declared': not created,
        'result_obj': result # Pass the result object to template
    }
    return render(request, 'admin/declare_result.html', context)