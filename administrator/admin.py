from django.contrib import admin
from .models import Technology, TestSchedule
from employee.models import EmployeeProfile
from questionbank.models import Question, Answer
from results.models import EmployeeResult  # Assuming you create this model later

# Register your models here so they appear in the Django admin interface.

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(TestSchedule)
class TestScheduleAdmin(admin.ModelAdmin):
    list_display = ('technology', 'start_time', 'end_time', 'duration_minutes', 'total_questions', 'is_active')
    list_filter = ('technology', 'is_active')
    search_fields = ('technology__name',)
    date_hierarchy = 'start_time'

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')
    search_fields = ('user__username', 'employee_id', 'department')
    raw_id_fields = ('user',) # Allows searching for user by ID/username

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'technology', 'correct_option', 'marks')
    list_filter = ('technology',)
    search_fields = ('question_text',)
    raw_id_fields = ('technology',)

