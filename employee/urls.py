from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Django's built-in auth views for logout
from .views import CustomLogoutView

urlpatterns = [
    path('login/', views.employee_login, name='employee_login'),
    path('register/', views.employee_register, name='employee_register'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='employee_logout'), # Using Django's LogoutView
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('exam/<int:test_schedule_id>/', views.take_exam, name='take_exam'),
    path('exam/<int:test_schedule_id>/submit/', views.submit_exam, name='submit_exam'), # Dedicated URL for submission
    path('results/<int:attempt_id>/', views.view_employee_result, name='view_employee_result'),
]