from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=15, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.user.username

class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=15, null=True)
    type = models.CharField(max_length=15, null=True)
    company = models.CharField(max_length=150, null=True)
    status = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.FileField(null=True)
    salary = models.FloatField()
    description = models.CharField(max_length=300)
    experience = models.CharField(max_length=15)
    skill = models.CharField(max_length=250)
    location = models.CharField(max_length=100, default='null')
    creationdate = models.DateField()

    def __str__(self):
        return self.title

class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    applydate = models.DateField()

    def __str__(self):
        return self.student.user.first_name
