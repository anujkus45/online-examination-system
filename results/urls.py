from django.urls import path
from . import views

urlpatterns = [
    # Admin-facing result views
    path('all/', views.view_all_results_admin, name='view_all_results'), # Admin view of all results
    path('detail/<int:result_id>/', views.view_detailed_result_admin, name='view_detailed_result_admin'), # Admin detailed view

    
]