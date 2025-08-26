from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),
    path('remove/<int:id>/', views.remove_student, name='remove_student'),
    path('display/', views.display_student, name='display_student'),
    path('search/', views.search_student, name='search_student'),


    path('profile/<int:id>/', views.student_profile, name='student_profile'),
    path('class/<int:class_id>/', views.class_view, name='class_view'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('download-report/<int:id>/', views.download_report, name='download_report'),


    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),



    
]
