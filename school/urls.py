from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),  
    path('export-to-excel/',login_required(views.ExportToExcelView.as_view()),name="export_to_excel"),
    path('import-from-excel/',login_required(apis.ImportFromExcelApi.as_view()),name="import_from_excel"),  

    path('schools/',login_required(views.SchoolsView.as_view()),name="schools"),  
    path('add-school/',login_required(apis.AddSchoolApi.as_view()),name="add_school"),
    path('school/<int:pk>/',login_required(views.SchoolView.as_view()),name="school"), 

    
    path('import-students-from-excel/',login_required(apis.ImportStudentsFromExcelApi.as_view()),name="import_students_from_excel"),  
    path('export-students-to-excel/',login_required(views.ExportStudentsToExcelView.as_view()),name="export_students_to_excel"),  
    path('students/',login_required(views.StudentsView.as_view()),name="students"),  
    path('add-student/',login_required(apis.AddStudentApi.as_view()),name="add_student"),
    path('student/<int:pk>/',login_required(views.StudentView.as_view()),name="student"), 


    path('sessions/',login_required(views.SessionsView.as_view()),name="sessions"),  
    path('add-session/',login_required(apis.AddSessionApi.as_view()),name="add_session"),
    path('session/<int:pk>/',login_required(views.SessionView.as_view()),name="session"), 



    path('student_in_sessions/',login_required(views.StudentInSessionsView.as_view()),name="student_in_sessions"),  
    path('add-student_in_session/',login_required(apis.AddStudentInSessionApi.as_view()),name="add_student_in_session"),
    path('student_in_session/<int:pk>/',login_required(views.StudentInSessionView.as_view()),name="studentinsession"), 




    path('majors/',login_required(views.MajorsView.as_view()),name="majors"),  
    path('add-major/',login_required(apis.AddMajorApi.as_view()),name="add_major"),
    path('major/<int:pk>/',login_required(views.MajorView.as_view()),name="major"), 




    path('teachers/',login_required(views.TeachersView.as_view()),name="teachers"),  
    path('add-teacher/',login_required(apis.AddTeacherApi.as_view()),name="add_teacher"),
    path('teacher/<int:pk>/',login_required(views.TeacherView.as_view()),name="teacher"), 




    path('import-teachers-from-excel/',login_required(apis.ImportTeachersFromExcelApi.as_view()),name="import_teachers_from_excel"),  
    path('export-teachers-to-excel/',login_required(views.ExportTeachersToExcelView.as_view()),name="export_teachers_to_excel"), 
    path('courses/',login_required(views.CoursesView.as_view()),name="courses"),  
    path('add-course/',login_required(apis.AddCourseApi.as_view()),name="add_course"),
    path('course/<int:pk>/',login_required(views.CourseView.as_view()),name="course"),  
    
    path('course-classes/',login_required(views.CourseClassesView.as_view()),name="course_classes"),  
    path('add-course-class/',login_required(apis.AddCourseClassApi.as_view()),name="add_course_class"),
    path('course-class/<int:pk>/',login_required(views.CourseClassView.as_view()),name="courseclass"),  
    
]
