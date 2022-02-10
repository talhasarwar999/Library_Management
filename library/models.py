from django.db import models
from simple_history import register
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Models
class Signup(models.Model):
    sno = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=131)
    email = models.CharField(max_length=25)
    role_select=models.CharField(max_length=25)
    password = models.CharField(max_length=30)
    confirm_password = models.CharField(max_length=31)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    history= HistoricalRecords()

class Book(models.Model):
    catchoice = [
        ('Education','Education'),
        ('Entertainment','Entertainment'),
        ('Comics','Comics' ),
        ('Biography','Biography'),
        ('History','History'),
    ]
    sno = models.BigAutoField(primary_key=True)
    bookname = models.CharField(max_length=131)
    authorname = models.CharField(max_length=25)
    category = models.CharField(max_length=25,choices=catchoice,default='education')
    isbn = models.IntegerField(blank=True,null=True)
    nofpages = models.IntegerField(blank=True,null=True)
    description = models.CharField(max_length=384,blank=True)
    image=models.ImageField(upload_to='librarymanage/images', blank=True,null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    history = HistoricalRecords()

def get_expiry():
    return datetime.today() + timedelta(days=15)

class Issuebook(models.Model):
    id = models.BigAutoField(primary_key=True)
    bookname=models.CharField(max_length=100)
    studentname=models.CharField(max_length=101)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    history = HistoricalRecords()

class Requestbook(models.Model):
    id = models.BigAutoField(primary_key=True)
    bookname=models.CharField(max_length=1000)
    user_name=models.CharField(max_length=100)
    setlimit=models.IntegerField(default=0,null=True)
    requestdate = models.DateField(auto_now=True)
    history = HistoricalRecords()

class Userhistory(models.Model):
    useractivity=models.CharField(max_length=2000, blank=True)
    username=models.CharField(max_length=2000, blank=True)
    todaydate = models.DateField(auto_now=True)