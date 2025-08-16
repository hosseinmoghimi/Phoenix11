from django.contrib import admin
from .models import School,Course,CourseClass,Teacher,Student,Major

admin.site.register(School)
admin.site.register(Course)
admin.site.register(CourseClass) 
admin.site.register(Student) 
admin.site.register(Teacher)
admin.site.register(Major)