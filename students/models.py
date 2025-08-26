from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    student_class = models.IntegerField()
    age = models.IntegerField()
    profile_pic = models.ImageField(upload_to='profile_pics/')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')],default='Male') # blank=True, null=True means that this field is optional

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
