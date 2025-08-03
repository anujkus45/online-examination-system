from django.urls import path
from . import views

# This app primarily contains models.
# Question management (CRUD) is handled through the 'administrator' app's views.
# You might add API endpoints here if you need to fetch questions dynamically
# (e.g., via AJAX for a complex exam interface).
urlpatterns = [
    path('api/questions/<int:technology_id>/', views.get_questions_api, name='get_questions_api'),
]

