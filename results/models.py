from django.db import models
from django.contrib.auth.models import User
from employee.models import EmployeeProfile, EmployeeTestAttempt # Import from employee app
from administrator.models import TestSchedule # Import TestSchedule

class EmployeeResult(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE,
                                 help_text="The employee whose result this is.")
    test_schedule = models.ForeignKey(TestSchedule, on_delete=models.CASCADE,
                                      help_text="The test schedule this result is for.")
    # Link to the specific attempt
    test_attempt = models.OneToOneField(EmployeeTestAttempt, on_delete=models.SET_NULL, null=True, blank=True,
                                        help_text="The specific test attempt this result corresponds to. (Can be null if attempt deleted)")
    score = models.DecimalField(max_digits=5, decimal_places=2,
                                help_text="Final score obtained by the employee (e.g., percentage).")
    passed = models.BooleanField(default=False,
                                 help_text="Indicates if the employee passed the test based on set criteria.")
    declared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    help_text="The administrator who declared this result.")
    declared_at = models.DateTimeField(auto_now_add=True,
                                      help_text="Timestamp when the result was declared.")
    remarks = models.TextField(blank=True, null=True,
                               help_text="Any additional remarks or feedback for the result.")

    class Meta:
        # One result per employee per test schedule (ensure this is how results are finalized)
        # If multiple attempts are allowed, this needs rethinking, perhaps link to TestAttempt directly.
        unique_together = ('employee', 'test_schedule')
        ordering = ['-declared_at']
        verbose_name_plural = "Employee Results"

    def __str__(self):
        return f"Result for {self.employee.employee_id} on {self.test_schedule.technology.name} Test"