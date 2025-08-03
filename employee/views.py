from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone # Use Django's timezone aware datetime
from django.contrib.auth.views import LogoutView

from .forms import EmployeeLoginForm, EmployeeRegistrationForm
from .models import EmployeeProfile, EmployeeTestAttempt
from administrator.models import TestSchedule, Technology
from questionbank.models import Question, Answer # Important: Answer model is tied to Question and EmployeeTestAttempt

import datetime
import random # For randomizing questions

# --- Authentication Views ---
def employee_login(request):
    if request.user.is_authenticated:
        # If user is admin, redirect to admin dashboard
        if request.user.is_staff:
            return redirect('admin_dashboard')
        # If user is regular employee, redirect to employee dashboard
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name if user.first_name else user.username}!")
                # Check if the user is an admin or regular employee
                if user.is_staff:
                    return redirect('admin_dashboard')
                return redirect('employee_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = EmployeeLoginForm()
    return render(request, 'employee/login.html', {'form': form})

def employee_register(request):
    if request.user.is_authenticated:
        return redirect('employee_dashboard') # Already logged in

    if request.method == 'POST':
        user_form = EmployeeRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save() # This also creates the EmployeeProfile due to save method in form
            messages.success(request, "Registration successful! Please log in.")
            return redirect('employee_login')
    else:
        user_form = EmployeeRegistrationForm()
    return render(request, 'employee/register.html', {'user_form': user_form})

# Logout is handled by Django's built-in LogoutView in urls.py

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect('home') # Redirect to home page after logout


# --- Employee Dashboard ---
@login_required
def employee_dashboard(request):
    try:
        employee_profile = request.user.employee_profile
    except EmployeeProfile.DoesNotExist:
        messages.error(request, "Your employee profile is missing. Please contact administration.")
        logout(request) # Log out invalid users
        return redirect('employee_login')

    current_time = timezone.now()

    # Get available tests
    available_tests = TestSchedule.objects.filter(
        is_active=True,
        start_time__lte=current_time,
        end_time__gte=current_time
    ).exclude(employeetestattempt__employee=employee_profile, employeetestattempt__is_completed=True) # Exclude already completed tests

    # Get ongoing tests (started but not completed)
    ongoing_tests = EmployeeTestAttempt.objects.filter(
        employee=employee_profile,
        is_completed=False,
        test_schedule__end_time__gte=current_time # Still within the test schedule's end time
    ).select_related('test_schedule__technology')

    # Get past attempts/results
    past_attempts = EmployeeTestAttempt.objects.filter(
        employee=employee_profile,
        is_completed=True
    ).order_by('-end_time').select_related('test_schedule__technology')

    context = {
        'employee': employee_profile,
        'available_tests': available_tests,
        'ongoing_tests': ongoing_tests,
        'past_attempts': past_attempts,
    }
    return render(request, 'employee/dashboard.html', context)


# --- Exam Taking Views ---
@login_required
def take_exam(request, test_schedule_id):
    test_schedule = get_object_or_404(TestSchedule, id=test_schedule_id)
    employee_profile = request.user.employee_profile
    current_time = timezone.now()

    # 1. Basic Validity Checks
    if not test_schedule.is_active or current_time < test_schedule.start_time or current_time > test_schedule.end_time:
        messages.error(request, "This test is not currently available.")
        return redirect('employee_dashboard')

    # 2. Check for existing attempts
    test_attempt = EmployeeTestAttempt.objects.filter(
        employee=employee_profile,
        test_schedule=test_schedule
    ).first()

    if test_attempt and test_attempt.is_completed:
        messages.warning(request, "You have already completed this test.")
        return redirect('view_employee_result', attempt_id=test_attempt.id)
    elif test_attempt and not test_attempt.is_completed:
        # Resume an ongoing test
        if current_time > test_attempt.start_time + datetime.timedelta(minutes=test_schedule.duration_minutes):
            messages.error(request, "Time limit for this test has expired. Submitting your answers.")
            return redirect('submit_exam', test_schedule_id=test_schedule.id) # Force submission
        # Calculate time left
        time_elapsed_seconds = (current_time - test_attempt.start_time).total_seconds()
        remaining_time_seconds = (test_schedule.duration_minutes * 60) - time_elapsed_seconds
        if remaining_time_seconds < 0: remaining_time_seconds = 0

        # Retrieve previously answered questions to pre-fill if any
        existing_answers = {ans.question_id: ans.selected_option for ans in test_attempt.answers.all()}
        questions = list(Question.objects.filter(technology=test_schedule.technology).order_by('?')[:test_schedule.total_questions])

    else:
        # Create a new attempt
        test_attempt = EmployeeTestAttempt.objects.create(
            employee=employee_profile,
            test_schedule=test_schedule,
            start_time=current_time,
            is_completed=False
        )
        messages.info(request, "Exam started. Good luck!")
        # Get questions for the first time
        questions = list(Question.objects.filter(technology=test_schedule.technology).order_by('?')[:test_schedule.total_questions])
        random.shuffle(questions) # Shuffle to ensure different order each time
        remaining_time_seconds = test_schedule.duration_minutes * 60
        existing_answers = {}

    context = {
        'test_schedule': test_schedule,
        'questions': questions,
        'test_attempt_id': test_attempt.id,
        'time_left_seconds': int(remaining_time_seconds),
        'existing_answers': existing_answers,
    }
    return render(request, 'employee/exam.html', context)


@login_required
def submit_exam(request, test_schedule_id):
    if request.method != 'POST':
        messages.error(request, "Invalid request method for exam submission.")
        return redirect('employee_dashboard')

    test_schedule = get_object_or_404(TestSchedule, id=test_schedule_id)
    employee_profile = request.user.employee_profile
    current_time = timezone.now()

    test_attempt = get_object_or_404(EmployeeTestAttempt,
                                     employee=employee_profile,
                                     test_schedule=test_schedule,
                                     is_completed=False) # Only process incomplete attempts

    # Ensure exam is submitted within valid time limit (or force submit if time up)
    if current_time > test_attempt.start_time + datetime.timedelta(minutes=test_schedule.duration_minutes):
        messages.warning(request, "Your exam was automatically submitted as the time limit expired.")
    elif current_time > test_schedule.end_time:
        messages.warning(request, "The exam window has closed. Your exam was automatically submitted.")

    questions = Question.objects.filter(technology=test_schedule.technology)
  
    score = 0
    total_possible_marks = 0
    # Clear previous answers for this attempt before saving new ones (in case of re-submission/resume)
    test_attempt.answers.all().delete()

    for question in questions:
        selected_option = request.POST.get(f'question_{question.id}')
        # Record the answer regardless of whether it's correct or chosen
        Answer.objects.create(
            test_attempt=test_attempt,
            question=question,
            selected_option=selected_option # This will be None if not answered
        )
        total_possible_marks += question.marks
        if selected_option == question.correct_option:
            score += question.marks

    # Calculate percentage score
    # Ensure no division by zero if there are no questions
    percentage_score = (score / total_possible_marks) * 100 if total_possible_marks > 0 else 0

    test_attempt.score = percentage_score
    test_attempt.is_completed = True
    test_attempt.end_time = current_time
    test_attempt.save()

    messages.success(request, f"Exam submitted! Your score: {percentage_score:.2f}%")
    return redirect('view_employee_result', attempt_id=test_attempt.id)


# --- Employee Result View ---
@login_required
def view_employee_result(request, attempt_id):
    employee_profile = request.user.employee_profile
    attempt = get_object_or_404(EmployeeTestAttempt, id=attempt_id, employee=employee_profile, is_completed=True)
    answers = Answer.objects.filter(test_attempt=attempt).select_related('question').order_by('question__id')

    # Calculate summary details
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
    return render(request, 'results/employee_result.html', context) # Re-use results app template