from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import CourseRepo,SchoolRepo,CourseClassRepo,TeacherRepo,StudentRepo,MajorRepo,SessionRepo,StudentInSessionRepo
from .serializers import CourseClassSerializer,SchoolSerializer,CourseSerializer,TeacherSerializer,StudentInSessionSerializer,SessionSerializer,StudentSerializer,MajorSerializer
from django.views import View
from django.http import HttpResponse
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.excel import ReportWorkBook,get_style
import json
from library.serializers import BookSerializer

from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext,AccountContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='school/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
from .constants import EXCEL_STUDENTS_DATA_START_ROW,EXCEL_TEACHERS_DATA_START_ROW

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddCourseClassContext(request,*args, **kwargs):
    context={}
    context['add_course_class_form']=AddCourseClassForm()
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)

def AddTeacherContext(request):
    context={}
    context['add_teacher_form']=AddTeacherForm()
    return context

def AddMajorContext(request):
    context={}
    context['add_major_form']=AddMajorForm()
    return context

class TeachersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        teachers=TeacherRepo(request=request).list(*args, **kwargs)
        context["teachers"]=teachers
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context["teachers_s"]=teachers_s
        if request.user.has_perm(APP_NAME+'.add_teacher'):
            context.update(AddTeacherContext(request=request))
        return render(request,TEMPLATE_ROOT+"teachers.html",context)
# Create your views here. 
   
class StudentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        students=StudentRepo(request=request).list(*args, **kwargs)
        context["students"]=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context["students_s"]=students_s
        if request.user.has_perm(APP_NAME+'.add_student'):
            context['add_student_form']=AddStudentForm()
        return render(request,TEMPLATE_ROOT+"students.html",context)
# Create your views here. 
   
 
         

class ExportStudentsToExcelView(View):
    def get(self,request,*args, **kwargs):
        
        EXPORT_STUDENTS=True
        EXPORT_TEACHERS=False
        EXPORT_MAJORS=False
        return ExportToExcelView().get(request=request,
                                       EXPORT_STUDENTS=EXPORT_STUDENTS,
                                       EXPORT_TEACHERS=EXPORT_TEACHERS,
                                       EXPORT_MAJORS=EXPORT_MAJORS)
         
  

class ExportTeachersToExcelView(View):
    def get(self,request,*args, **kwargs):
        
        EXPORT_STUDENTS=False
        EXPORT_TEACHERS=True
        EXPORT_MAJORS=False
        return ExportToExcelView().get(request=request,
                                       EXPORT_STUDENTS=EXPORT_STUDENTS,
                                       EXPORT_TEACHERS=EXPORT_TEACHERS,
                                       EXPORT_MAJORS=EXPORT_MAJORS)
         

class ExportToExcelView(View):
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        date=PersianCalendar().from_gregorian(now)

        
        report_work_book=ReportWorkBook(origin_file_name=f'school.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        
        EXPORT_STUDENTS=True
        EXPORT_TEACHERS=True
        EXPORT_MAJORS=True

        if 'EXPORT_STUDENTS' in kwargs:
            EXPORT_STUDENTS=kwargs['EXPORT_STUDENTS']

        if 'EXPORT_TEACHERS' in kwargs:
            EXPORT_TEACHERS=kwargs['EXPORT_TEACHERS']

        if 'EXPORT_MAJORS' in kwargs:
            EXPORT_MAJORS=kwargs['EXPORT_MAJORS']

        if EXPORT_STUDENTS:
            students=StudentRepo(request=request).list()
                
            lines=[]
            for i,student in enumerate(students,start=1):
                line={
                    'row':i,
                    'id':student.id,
                    'last_name':student.person_account.person.last_name,
                    'first_name':student.person_account.person.first_name,
                    'father_name':student.father_name,
                    'melli_code':student.person_account.person.melli_code,      
                    'birth_date':student.person_account.person.birth_date,      
                    'birth_location':student.person_account.person.birth_location,      
                }
                lines.append(line)
            headers=['ردیف',
                    'شناسه',
                    'نام خانوادگی',
                    'نام', 
                    'نام پدر', 
                    'کد ملی',
                    'تاریخ تولد',
                    'محل تولد',
            ]
          
            
            start_row=EXCEL_STUDENTS_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='students',
                title='students',
            )

            
        if EXPORT_TEACHERS:
            
            
            teachers=TeacherRepo(request=request).list()
            
                
            lines=[]
            for i,teacher in enumerate(teachers,start=1):
                line={
                    'row':i,
                    'id':teacher.id,
                    'last_name':teacher.person_account.person.last_name,
                    'first_name':teacher.person_account.person.first_name,
                    'father_name':teacher.father_name,
                    'melli_code':teacher.person_account.person.melli_code,      
                    'personneli_code':teacher.personneli_code,      
                    'birth_date':teacher.person_account.person.birth_date,      
                    'birth_location':teacher.person_account.person.birth_location,      
                }
                lines.append(line)
            headers=['ردیف',
                    'شناسه',
                    'نام خانوادگی',
                    'نام', 
                    'نام پدر', 
                    'کد ملی',
                    'کد پرسنلی',
                    'تاریخ تولد',
                    'محل تولد',
            ]
         
            start_row=EXCEL_TEACHERS_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='services',
                title='services',
            )

        
     
        if EXPORT_MAJORS:
            
            
            accounts=AccountRepo(request=request).list()
            
                
            lines=[]
            for i,account in enumerate(accounts,start=1):
                line={
                    'row':i,
                    'parent_code':account.parent_account.code if account.parent_account is not None else '',      
                    'id':account.id,
                    'code':account.code,      
                    'title':account.title,
                    'color':account.color,
                    'thumbnail_origin':str(account.thumbnail_origin),       
                }
                lines.append(line)
            headers=['ردیف',
                    'کد والد',
                    'شناسه',
                    'کد',
                    'عنوان',
                    'رنگ',
                    'تصویر',
            ]
         
            start_row=EXCEL_TEACHERS_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='accounts',
                title='accounts',
            )
        
        file_name=f"""Phoenix accounting {date.replace('/','').replace(':','')}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response


class ExportTeachersToExcelView(View):
  
    def get(self,request,*args, **kwargs):
        
        EXPORT_STUDENTS=False
        EXPORT_TEACHERS=True
        EXPORT_MAJORS=False
        return ExportToExcelView().get(request=request,
                                       EXPORT_STUDENTS=EXPORT_STUDENTS,
                                       EXPORT_TEACHERS=EXPORT_TEACHERS,
                                       EXPORT_MAJORS=EXPORT_MAJORS)
          


 
class StudentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        student=StudentRepo(request=request).student(*args, **kwargs)
        context["student"]=student
        student_s=json.dumps(StudentSerializer(student,many=False).data)
        context["student_s"]=student_s





        students_in_session=StudentInSessionRepo(request=request).list(student_id=student.id).order_by('session__session_no')
        context["students_in_session"]=students_in_session
        students_in_session_s=json.dumps(StudentInSessionSerializer(students_in_session,many=True).data)
        context["students_in_session_s"]=students_in_session_s



        context.update(AccountContext(request=request,account=student.person_account))
         
        return render(request,TEMPLATE_ROOT+"student.html",context)
 
 
class TeacherView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        teacher=TeacherRepo(request=request).teacher(*args, **kwargs)
        context["teacher"]=teacher
        teacher_s=json.dumps(TeacherSerializer(teacher,many=False).data)
        context["teacher_s"]=teacher_s

        context.update(AccountContext(request=request,account=teacher.person_account))

        return render(request,TEMPLATE_ROOT+"teacher.html",context)


class SchoolsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        schools=SchoolRepo(request=request).list(*args, **kwargs)
        context["schools"]=schools
        schools_s=json.dumps(SchoolSerializer(schools,many=True).data)
        context["schools_s"]=schools_s
        if request.user.has_perm(APP_NAME+'.add_school'):
            context['add_school_form']=AddSchoolForm()
        return render(request,TEMPLATE_ROOT+"schools.html",context)
    
 
class SchoolView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        school=SchoolRepo(request=request).school(*args, **kwargs)
        context["school"]=school
        school_s=json.dumps(SchoolSerializer(school,many=False).data)
        context["school_s"]=school_s



        course_classes=CourseClassRepo(request=request).list(school_id=school.id,*args, **kwargs)
        context["course_classes"]=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context["course_classes_s"]=course_classes_s


        return render(request,TEMPLATE_ROOT+"school.html",context)
 
 
class CoursesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        courses=CourseRepo(request=request).list(*args, **kwargs)
        context["courses"]=courses
        courses_s=json.dumps(CourseSerializer(courses,many=True).data)
        context["courses_s"]=courses_s
        if request.user.has_perm(APP_NAME+'.add_course'):
            context['add_course_form']=AddCourseForm()
        return render(request,TEMPLATE_ROOT+"courses.html",context)
   
 
class CourseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        course=CourseRepo(request=request).course(*args, **kwargs)
        context["course"]=course
        course_s=json.dumps(CourseSerializer(course,many=False).data)
        context["course_s"]=course_s


        books=course.books.all()
        context["books"]=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context["books_s"]=books_s


        course_classes=CourseClassRepo(request=request).list(course_id=course.id,*args, **kwargs)
        context["course_classes"]=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context["course_classes_s"]=course_classes_s



        return render(request,TEMPLATE_ROOT+"course.html",context)


class MajorView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        major=MajorRepo(request=request).major(*args, **kwargs)
        context["major"]=major
        major_s=json.dumps(MajorSerializer(major,many=False).data)
        context["major_s"]=major_s


        course_classes=CourseClassRepo(request=request).list(major_id=major.id,*args, **kwargs)
        context["course_classes"]=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context["course_classes_s"]=course_classes_s

        
        courses=major.courses.all()
        context["courses"]=courses
        courses_s=json.dumps(CourseSerializer(courses,many=True).data)
        context["courses_s"]=courses_s

        return render(request,TEMPLATE_ROOT+"major.html",context)


class CourseClassesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        course_classes=CourseClassRepo(request=request).list(*args, **kwargs)
        context["course_classes"]=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context["course_classes_s"]=course_classes_s
        if request.user.has_perm(APP_NAME+'.add_courseclass'):
            context.update(AddCourseClassContext(request=request))
        return render(request,TEMPLATE_ROOT+"course-classes.html",context)

   
class MajorsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        majors=MajorRepo(request=request).list(*args, **kwargs)
        context["majors"]=majors
        majors_s=json.dumps(MajorSerializer(majors,many=True).data)
        context["majors_s"]=majors_s
        if request.user.has_perm(APP_NAME+'.add_major'):
            context.update(AddMajorContext(request=request))
        return render(request,TEMPLATE_ROOT+"majors.html",context)
   
 
class CourseClassView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        course_class=CourseClassRepo(request=request).course_class(*args, **kwargs)
        context["course_class"]=course_class
        course_class_s=json.dumps(CourseClassSerializer(course_class,many=False).data)
        context["course_class_s"]=course_class_s


        books=course_class.course.books.all()
        context["books"]=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context["books_s"]=books_s
        
        teachers=course_class.teachers.all()
        context["teachers"]=teachers
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context["teachers_s"]=teachers_s
 

        sessions=SessionRepo(request=request).list(course_class_id=course_class.id).order_by('session_no')
        context["sessions"]=sessions
        sessions_s=json.dumps(SessionSerializer(sessions,many=True).data)
        context["sessions_s"]=sessions_s

        next_session_no=1
        if len(sessions)>0:
            next_session_no=sessions.last().session_no+1
        context["next_session_no"]=next_session_no
        
        students=course_class.students.all()
        context["students"]=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context["students_s"]=students_s
 

        return render(request,TEMPLATE_ROOT+"course-class.html",context)


class SessionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        
        sessions=SessionRepo(request=request).list(*args, **kwargs) 
        context["sessions"]=sessions
        sessions_s=json.dumps(SessionSerializer(sessions,many=True).data)
        context["sessions_s"]=sessions_s

        return render(request,TEMPLATE_ROOT+"sessions.html",context)



class SessionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        
        session=SessionRepo(request=request).session(*args, **kwargs) 
        context["session"]=session
        session_s=json.dumps(SessionSerializer(session,many=False).data)
        context["session_s"]=session_s


        students=session.course_class.students.all()
        context["students"]=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context["students_s"]=students_s



      


        students_in_session=StudentInSessionRepo(request=request).list(session_id=session.id).order_by('student__person_account__person__last_name')
        context["students_in_session"]=students_in_session
        students_in_session_s=json.dumps(StudentInSessionSerializer(students_in_session,many=True).data)
        context["students_in_session_s"]=students_in_session_s



        return render(request,TEMPLATE_ROOT+"session.html",context)


class StudentInSessionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        
        sessions=SessionRepo(request=request).list(*args, **kwargs) 
        context["sessions"]=sessions
        sessions_s=json.dumps(SessionSerializer(sessions,many=True).data)
        context["sessions_s"]=sessions_s

        return render(request,TEMPLATE_ROOT+"sessions.html",context)


class StudentInSessionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        
        session=SessionRepo(request=request).session(*args, **kwargs) 
        context["session"]=session
        session_s=json.dumps(SessionSerializer(session,many=False).data)
        context["session_s"]=session_s


        students=session.course_class.students.all()
        context["students"]=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context["students_s"]=students_s

        return render(request,TEMPLATE_ROOT+"session.html",context)
