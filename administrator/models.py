from django.db import models
from django.contrib.auth.models import User # Django's built-in User model

# Model for Technologies (e.g., Python, Java, Django)
class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Python, Django, SQL")
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Technologies" # Correct plural in admin

    def __str__(self):
        return self.name

# Model for scheduling a specific test for a technology
class TestSchedule(models.Model):
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE,
                                   help_text="The technology this test is for.")
    start_time = models.DateTimeField(help_text="The date and time when the test becomes available.")
    end_time = models.DateTimeField(help_text="The date and time when the test is no longer available.")
    duration_minutes = models.IntegerField(default=60, help_text="Duration of the test in minutes.")
    total_questions = models.IntegerField(default=50, help_text="Number of questions to randomly select for this test.")
    is_active = models.BooleanField(default=False, help_text="Check to make this test schedule active and visible to employees.")

    class Meta:
        ordering = ['-start_time'] # Order by latest test first

    def __str__(self):
        return f"{self.technology.name} Test ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

