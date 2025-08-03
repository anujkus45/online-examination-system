from django.db import models
from django.contrib.auth.models import User # Django's built-in User model
from administrator.models import TestSchedule # Import TestSchedule from administrator app

# Employee Profile linked to Django's User model
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True,
                                   help_text="Unique identification number for the employee.")
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username # Or self.employee_id

# Model to track an employee's attempt at a specific test schedule
class EmployeeTestAttempt(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    test_schedule = models.ForeignKey(TestSchedule, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True, help_text="Time when the employee started the test.")
    end_time = models.DateTimeField(null=True, blank=True, help_text="Time when the employee submitted or timed out.")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                help_text="Employee's score (e.g., percentage).")
    is_completed = models.BooleanField(default=False, help_text="True if the test attempt has been submitted.")

    class Meta:
        unique_together = ('employee', 'test_schedule') # An employee can only attempt a specific test schedule once.
        ordering = ['-start_time'] # Order by latest attempt first

    def __str__(self):
        return f"{self.employee.employee_id} - {self.test_schedule.technology.name} Test Attempt"