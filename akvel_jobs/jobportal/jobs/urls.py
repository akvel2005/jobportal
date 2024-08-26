from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('jobs/', views.job_list, name='job-list'),
    path('post-job/', views.post_job, name='post-job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply-job'),
    path('view-applications/<int:job_id>/', views.view_applications, name='view-applications'),
      path('', views.job_list, name='job-list'),
]

