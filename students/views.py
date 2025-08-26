from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os, csv
from django.db.models import Count
from .models import Student, Attendance
from .forms import StudentForm, AttendanceForm, CSVUploadForm, SignUpForm


# PUBLIC VIEWS

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'students/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'students/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# PRIVATE (LOGIN REQUIRED) VIEWS

@login_required
def home(request):
    # Total students
    total_students = Student.objects.count()

    # Class-wise strength
    class_counts = Student.objects.values('student_class').annotate(count=Count('id'))
    class_labels = [entry['student_class'] for entry in class_counts]
    class_data = [entry['count'] for entry in class_counts]

    # Gender distribution
    gender_counts = Student.objects.values('gender').annotate(count=Count('id'))
    gender_labels = [entry['gender'] for entry in gender_counts]
    gender_data = [entry['count'] for entry in gender_counts]

    context = {
        "total_students": total_students,
        "class_strength_data": {
            "labels": class_labels,
            "data": class_data
        },
        "gender_distribution_data": {
            "labels": gender_labels,
            "data": gender_data
        }
    }

    return render(request, 'students/home.html', context)

@login_required
def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'students/add_update.html', {'form': form})

@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('display_student')
    return render(request, 'students/add_update.html', {'form': form})

@login_required
def remove_student(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        messages.success(request, "Student removed successfully.")
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
    return redirect('display_student')

@login_required
def display_student(request):
    students = Student.objects.all()
    return render(request, 'students/display.html', {'students': students})

@login_required
def search_student(request):
    query = request.GET.get('query', '')
    students = Student.objects.filter(name__icontains=query)
    return render(request, 'students/search.html', {'students': students})

@login_required
def student_profile(request, id):
    student = get_object_or_404(Student, id=id)
    attendance = Attendance.objects.filter(student=student)
    return render(request, 'students/profile.html', {
        'student': student,
        'attendance': attendance
    })

@login_required
def class_view(request, class_id):
    students = Student.objects.filter(student_class=class_id)
    return render(request, 'students/class_view.html', {
        'students': students,
        'class_id': class_id
    })

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            for row in reader:
                try:
                    Student.objects.create(
                        name=row[0],
                        email=row[1],
                        student_class=int(row[2]),
                        age=int(row[3])
                    )
                except Exception as e:
                    messages.error(request, f"Error importing row: {row} - {str(e)}")
            messages.success(request, 'CSV imported successfully!')
            return redirect('display')
    else:
        form = CSVUploadForm()
    return render(request, 'students/upload_csv.html', {'form': form})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display')
    else:
        form = AttendanceForm()
    return render(request, 'students/attendance.html', {'form': form})

@login_required
def download_report(request, id):
    student = get_object_or_404(Student, id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_report.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Student Report for {student.name}")
    p.drawString(100, 780, f"Email: {student.email}")
    p.drawString(100, 760, f"Class: {student.student_class}")
    p.drawString(100, 740, f"Age: {student.age}")
    
    if student.profile_pic:
        image_path = os.path.join(settings.MEDIA_ROOT, str(student.profile_pic))
        if os.path.exists(image_path):
            p.drawImage(image_path, 400, 720, width=100, height=100)

    # Attendance Records
    p.drawString(100, 700, "Attendance Summary:")
    attendance = Attendance.objects.filter(student=student)
    y = 680
    for a in attendance:
        p.drawString(120, y, f"{a.date}: {a.status}")
        y -= 20
    
    p.showPage()
    p.save()
    return response
