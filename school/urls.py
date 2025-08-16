from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('schools/',login_required(views.SchoolsView.as_view()),name="schools"),  
    path('add-school/',login_required(apis.AddSchoolApi.as_view()),name="add_school"),
    path('school/<int:pk>/',login_required(views.SchoolView.as_view()),name="school"), 


    

    path('students/',login_required(views.StudentsView.as_view()),name="students"),  
    path('add-student/',login_required(apis.AddStudentApi.as_view()),name="add_student"),
    path('student/<int:pk>/',login_required(views.StudentView.as_view()),name="student"), 




    path('majors/',login_required(views.MajorsView.as_view()),name="majors"),  
    path('add-major/',login_required(apis.AddMajorApi.as_view()),name="add_major"),
    path('major/<int:pk>/',login_required(views.MajorView.as_view()),name="major"), 




    path('teachers/',login_required(views.TeachersView.as_view()),name="teachers"),  
    path('add-teacher/',login_required(apis.AddTeacherApi.as_view()),name="add_teacher"),
    path('teacher/<int:pk>/',login_required(views.TeacherView.as_view()),name="teacher"), 



    path('courses/',login_required(views.CoursesView.as_view()),name="courses"),  
    path('add-course/',login_required(apis.AddCourseApi.as_view()),name="add_course"),
    path('course/<int:pk>/',login_required(views.CourseView.as_view()),name="course"),  
    
    path('course-classes/',login_required(views.CourseClassesView.as_view()),name="course_classes"),  
    path('add-course-class/',login_required(apis.AddCourseClassApi.as_view()),name="add_course_class"),
    path('course-class/<int:pk>/',login_required(views.CourseClassView.as_view()),name="courseclass"),  
    
]
