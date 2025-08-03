from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='employee_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('technologies/', views.manage_technologies, name='admin_manage_technologies'),
    path('technologies/add/', views.add_technology, name='admin_add_technology'),
    path('technologies/update/<int:tech_id>/', views.update_technology, name='admin_update_technology'),
    path('technologies/delete/<int:tech_id>/', views.delete_technology, name='admin_delete_technology'),

    path('tests/', views.manage_tests, name='admin_manage_tests'),
    path('tests/add/', views.add_test_schedule, name='admin_add_test_schedule'),
    path('tests/update/<int:test_id>/', views.update_test_schedule, name='admin_update_test_schedule'),
    path('tests/delete/<int:test_id>/', views.delete_test_schedule, name='admin_delete_test_schedule'),

    path('questions/', views.manage_questions, name='admin_manage_questions'),
    path('questions/add/', views.add_question, name='admin_add_question'),
    path('questions/update/<int:question_id>/', views.update_question, name='admin_update_question'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='admin_delete_question'),

    # URL for result declaration/viewing by admin (might redirect to results app URLs or handle here)
    path('results/', views.view_all_exam_results, name='admin_view_all_exam_results'),
    path('results/<int:attempt_id>/detail/', views.view_detailed_exam_result, name='admin_view_detailed_exam_result'),
    path('results/<int:attempt_id>/declare/', views.declare_result, name='admin_declare_result'), # Optional: if admin explicitly "declares" individual results
]