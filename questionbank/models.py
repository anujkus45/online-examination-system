from django.db import models
from administrator.models import Technology # Import Technology from administrator app
from employee.models import EmployeeTestAttempt # Import EmployeeTestAttempt

# Model for individual questions
class Question(models.Model):
    # Choices for options (A, B, C, D)
    OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    technology = models.ForeignKey(Technology, on_delete=models.CASCADE,
                                   help_text="The technology this question belongs to.")
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES,
                                      help_text="Select the correct option (A, B, C, or D).")
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=1.0,
                                help_text="Marks awarded for correctly answering this question.")

    class Meta:
        ordering = ['technology', 'id'] # Order for consistent display/management

    def __str__(self):
        return f"[{self.technology.name}] {self.question_text[:75]}..." # Display first 75 chars

# Model to store an employee's selected answer for a specific question in a specific attempt
class Answer(models.Model):
    test_attempt = models.ForeignKey(EmployeeTestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=Question.OPTION_CHOICES, null=True, blank=True,
                                       help_text="The option selected by the employee (Null if not answered).")

    class Meta:
        unique_together = ('test_attempt', 'question') # An employee can only answer a specific question once per attempt.
        ordering = ['question__id']

    def __str__(self):
        return f"Attempt {self.test_attempt.id} - Q{self.question.id} - Ans: {self.selected_option}"

    def is_correct(self):
        return self.selected_option == self.question.correct_option