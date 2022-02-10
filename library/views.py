from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from datetime import datetime,timedelta,date
from library.forms import EmployeeForm
from . models import *


# Create your views here.
def index(request):
   return  render(request,"library/index.html")

def signup(request):
   if request.method == "POST":
      username = request.POST['username']
      email = request.POST['email']
      role_select = request.POST['select']
      password = request.POST['password']
      confirm_password = request.POST['confirm_password']
      if User.objects.filter(email=email).exists():
         messages.warning(request, 'This email is already taken: Try another Email')
         return redirect('index')
      if User.objects.filter(username=username).exists():
         messages.warning(request, 'This username Exists')
         return redirect('index')
      if len(username) < 4:
         messages.error(request, " Your username must be under 10 characters")
         return redirect('index')
      if len(password) < 6:
         messages.error(request, " Your password must be under 6 characters")
         return redirect('index')
      if password!= confirm_password:
         messages.error(request, "Passwords do not matched")
         return redirect('index')
      else:
          if role_select == "Student":
              myuser1 = User.objects.create_user(username, email, password)
              myuser1.is_active = False
              myuser1.save()
              current_site = get_current_site(request)
              mail_subject = 'Activate your blog account.'
              message = render_to_string('library/acc_active_email.html',
              {
                  'user': myuser1,
                  'domain': current_site.domain,
                  'uid': urlsafe_base64_encode(force_bytes(myuser1.pk)),
                  'token': account_activation_token.make_token(myuser1),
              })
              to_email = email
              emails = EmailMessage(mail_subject, message, to=[to_email])
              emails.send()
              my_admin_group = Group.objects.get_or_create(name='Student')
              my_admin_group[0].user_set.add(myuser1)
              messages.success(request, "We have sent an email with a confirmation link to your email address. In order to complete the sign-up process, please click the confirmation link.")
              return redirect('index')
          else:
              myuser1 = User.objects.create_user(username, email, password)
              myuser1.is_active = False
              myuser1.save()
              current_site = get_current_site(request)
              mail_subject = 'Activate your blog account.'
              message = render_to_string('library/acc_active_email.html',
              {
                  'user': myuser1,
                  'domain': current_site.domain,
                  'uid': urlsafe_base64_encode(force_bytes(myuser1.pk)),
                  'token': account_activation_token.make_token(myuser1),
              })
              to_email = email
              print(to_email)
              emails = EmailMessage(mail_subject, message, to = [to_email])
              emails.send()
              my_admin_group = Group.objects.get_or_create(name='Admin')
              my_admin_group[0].user_set.add(myuser1)
              messages.success(request, "We have sent an email with a confirmation link to your email address. In order to complete the sign-up process, please click the confirmation link.")
              return redirect('index')
   return render(request, 'library/signup.html')

def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()

def afterlogin(request):
    if is_admin(request.user):
        messages.success(request, "Successfully Login! Welcome to Admin Page")
        return redirect('AdminPage')
    elif is_student(request.user):
        messages.success(request, "Successfully Login! Welcome to Student Page")
        return redirect('StudentPage')
    else:
        return render(request,'library/index.html')
    return HttpResponse("404 Error")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request,"Thank you for your email confirmation. Now you can login your account.")
        return HttpResponseRedirect('/logins')
    else:
        messages.error(request, "Activation link is invalid!")
        return HttpResponseRedirect('/logins')

def logouts(request):
    logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('index')

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def AdminPage(request):
    Allbooks = Book.objects.all()
    content = {'Allbooks':Allbooks}
    return render(request,"library/AdminPage.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def adminbookview(request,sno):
    viewbook = Book.objects.filter(sno=sno)
    content = {'viewbook':viewbook[0]}
    return render(request,"library/viewbook.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def deletebook(request,sno):
    dellbook = Book.objects.get(sno=sno)
    addhistory = Userhistory(username=request.user, useractivity=f"You deleted {dellbook.bookname}")
    addhistory.save()
    dellbook.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('AdminPage')

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def editbook(request,sno):
    editbook = Book.objects.get(sno=sno)
    return render(request,"library/editbook.html", {'editbook':editbook})

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def updatebook(request, sno):
    books = Book.objects.get(sno=sno)
    bookedit = EmployeeForm(request.POST, files=request.FILES,instance= books)
    if request.method == 'POST':
        if bookedit.is_valid():
            bookedit.save()
            messages.success(request, "Successfully Edit")
            addbookinhistory = Userhistory(username=request.user, useractivity=f"You updated '{books.bookname}' Book")
            addbookinhistory.save()
            return redirect('AdminPage')
        else:
            messages.error(request, "Invalid Data")
            return redirect('AdminPage')
    return render(request,"library/adminpae.html")

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def addbook(request):
    if request.method == "POST":
        bookname = request.POST['bookname']
        authorname = request.POST['authorname']
        isbn = request.POST['isbn']
        nofpages = request.POST['nofpages']
        category = request.POST['category']
        description = request.POST['description']
        image = request.FILES.get('image')
        bookdata = Book(bookname=bookname, authorname=authorname, isbn=isbn, nofpages=nofpages, category=category,
                              description=description,image=image)
        bookdata.save()
        addbookinhistory = Userhistory(username=request.user,useractivity=f"You created {bookname} by {authorname}")
        addbookinhistory.save()
        messages.success(request, 'Successfully Added')
        return redirect('AdminPage')
    return render(request,"library/addbook.html")

@login_required(login_url='/logins')
@user_passes_test(is_student)
def StudentPage(request):
    allbooks = []
    bookcategory = Book.objects.values('category')
    getcategory = {category['category'] for category in bookcategory}
    for cat in getcategory:
        fetchcategory = Book.objects.filter(category=cat)
        allbooks.append(fetchcategory)
    content = {'Allbooks':allbooks}
    return render(request,"library/StudentPage.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_student)
def StudentViewBook(request,sno):
    viewbook = Book.objects.filter(sno=sno)
    content = {'viewbook':viewbook[0]}
    return render(request,"library/StudentViewBook.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_student)
def studentsearch(request):
    search = request.GET['search']
    if len(search) > 30:
        searchresult=Book.objects.none()
    else:
        bookname = Book.objects.filter(bookname__icontains=search)
        authorname = Book.objects.filter(authorname__icontains=search)
        category = Book.objects.filter(category__icontains=search)
        description = Book.objects.filter(description__icontains=search)
        searchresult = bookname.union(authorname,category,description)
        addhistory = Userhistory(username=request.user, useractivity=f"You searched {search}")
        addhistory.save()
        if searchresult.count() == 0:
            messages.warning(request, "No Search Results, Please Refine your search.")
        content={'searchresult':searchresult, 'search':search}
    return render(request,"library/studentsearch.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def adminsearch(request):
    search = request.GET['search']
    if len(search) > 30:
        searchresult = Book.objects.none()
    else:
        bookname = Book.objects.filter(bookname__icontains=search)
        authorname = Book.objects.filter(authorname__icontains=search)
        category = Book.objects.filter(category__icontains=search)
        description = Book.objects.filter(description__icontains=search)
        searchresult = bookname.union(authorname,category,description)
        addhistory = Userhistory(username=request.user, useractivity=f"You searched {search}")
        addhistory.save()
        if searchresult.count() == 0:
            messages.warning(request,"No Search Results, Please Refine your search.")
        content = {'searchresult':searchresult,'search':search}
    return render(request,"library/adminsearch.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def Viewstudentrecord(request):
    student = User.objects.filter(groups__name='Student')
    content = {'student': student}
    return render(request,"library/StudentRecord.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def issuebook(request,id):
    if request.method == "POST":
        bookname = request.POST['bookname']
        studentname = request.POST['studentname']
        issuedbook = Issuebook(bookname=bookname,studentname=studentname)
        issuedbook.save()
        messages.success(request,f"{bookname} has been Successfully Issued to {studentname}")
        deleterequest = Requestbook.objects.get(id=id)
        deleterequest.delete()
        addhistory = Userhistory(username=request.user, useractivity=f"You issued {bookname} book to {studentname}")
        addhistory.save()
        return redirect('AdminPage')
    allbook = Book.objects.all()
    allstudent = User.objects.filter(groups__name='Student')
    content = {'allstudent': allstudent,'allbook':allbook}
    return render(request,"library/issuebook.html",content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def viewissuedbookadmin(request):
    issuedbooks = Issuebook.objects.all()
    listdata = []
    for list in issuedbooks:
        issuedates = str(list.issuedate.day)+'-'+str(list.issuedate.month)+'-'+str(list.issuedate.year)
        expiredate = str(list.expirydate.day)+'-'+str(list.expirydate.month)+'-'+str(list.expirydate.year)
        days1 = (date.today()-list.issuedate)
        d = days1.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*50
        t = (list.bookname,list.studentname,issuedates,expiredate,fine,list.id)
        listdata.append(t)
    return render(request,'library/viewissuedbookadmin.html',{'listdata':listdata})

@login_required(login_url='/logins')
@user_passes_test(is_student)
def viewissuedbookstudent(request):
    issuedbooks = Issuebook.objects.filter(studentname=request.user)
    listdata = []
    for list in issuedbooks:
        issuedates = str(list.issuedate.day)+'-'+str(list.issuedate.month)+'-'+str(list.issuedate.year)
        expiredate = str(list.expirydate.day)+'-'+str(list.expirydate.month)+'-'+str(list.expirydate.year)
        days1 = (date.today()-list.issuedate)
        d = days1.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*50
        books = Book.objects.filter(bookname=list.bookname)
        for book in books:
            t = (book.bookname,book.authorname,book.category,book.isbn,issuedates,expiredate,fine,list.id)
            listdata.append(t)
    return render(request,'library/viewissuedbookstudent.html', {'listdata':listdata})

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def deleteissuebook(request,id):
    dellbook = Issuebook.objects.get(id=id)
    dellbook.delete()
    addhistory = Userhistory(username=request.user, useractivity=f"You deleted Issued book {dellbook}")
    addhistory.save()
    messages.success(request, "Successfully Deleted")
    return redirect('viewissuedbookadmin')

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def deleteuser(request,id):
    deluser = User.objects.get(id=id)
    deluser.delete()
    addhistory = Userhistory(username=request.user, useractivity=f"You deleted {deluser}")
    addhistory.save()
    messages.success(request, "Successfully Deleted")
    return redirect('Viewstudentrecord')

@login_required(login_url='/logins')
@user_passes_test(is_student)
def requestbook(request):
    alllimits = []
    getlimit = Requestbook.objects.filter(user_name=request.user)
    for limit in getlimit:
        limits = limit.setlimit
        alllimits.append(limits)
    if request.method == "POST":
        if alllimits:
            newlimit = alllimits[-1]
            setlimit = newlimit + 1
            bookname = request.POST['bookname']
            user_name = request.POST['user_name']
            getissuebook=Issuebook.objects.filter(studentname=request.user)
            if len(alllimits) == 1 and len(getissuebook) < 2:
                issuedbook = Requestbook(bookname=bookname, user_name=user_name, setlimit=setlimit)
                issuedbook.save()
                addhistory = Userhistory(username=request.user, useractivity=f"You requested for {bookname}")
                addhistory.save()
                messages.success(request, f"Your {bookname} book Request have received successfully to Admin")
                return redirect('requestbook')
            else:
                if setlimit >= 3 or len(getissuebook) == 2:
                    messages.error(request, "Limit Reached! You can only two book request")
                    return redirect('requestbook')
                issuedbook = Requestbook(bookname=bookname, user_name=user_name, setlimit=setlimit)
                issuedbook.save()
                addhistory = Userhistory(username=request.user, useractivity=f"You requested for {bookname}")
                addhistory.save()
                messages.success(request, f"Your {bookname} book Request have received successfully to Admin")
                return redirect('requestbook')
        else:
            getissuebook = Issuebook.objects.filter(studentname=request.user)
            if len(getissuebook) >= 2:
                messages.error(request, "Limit Reached! You can only two book request")
                return redirect('requestbook')
            setlimit = 1
            bookname = request.POST['bookname']
            user_name = request.POST['user_name']
            issuedbook = Requestbook(bookname=bookname, user_name=user_name, setlimit=setlimit)
            issuedbook.save()
            addhistory = Userhistory(username=request.user, useractivity=f"You requested for {bookname}")
            addhistory.save()
            messages.success(request, f"Your {bookname} book Request have received successfully to Admins")
            return redirect('requestbook')
    allbook = Book.objects.all()
    content = {'allbook': allbook}
    return render(request,"library/requestbook.html",content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def viewrequestbyadmin(request):
    allrequest = Requestbook.objects.all()
    content = {'allrequest': allrequest}
    return render(request, "library/viewrequestbyadmin.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_student)
def returnbook(request,id):
    retbook = Issuebook.objects.get(id=id)
    addhistory = Userhistory(username=request.user, useractivity=f"You returned {retbook.bookname} book to admin")
    addhistory.save()
    retbook.delete()
    messages.success(request,"your Book has been Successfully Returned to Admin")
    return redirect('viewissuedbookstudent')

@login_required(login_url='/logins')
@user_passes_test(is_student)
def viewrequestedbook(request):
    requestedbook = Requestbook.objects.filter(user_name=request.user)
    content = {'requestedbook':requestedbook}
    return render(request,"library/viewrequestedbookstudent.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_student)
def deleterequest(request,id):
    delrequest = Requestbook.objects.get(id=id)
    addhistory = Userhistory(username=request.user, useractivity=f"You deleted request for {delrequest.bookname} book")
    addhistory.save()
    deluser.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('viewrequestedbook')

@login_required(login_url='/logins')
@user_passes_test(is_student)
def viewstudenthistory(request):
    allhistory = Userhistory.objects.filter(username=request.user)
    content = {"allhistory":allhistory}
    return render(request,"library/allhistorystudent.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def viewadminhistory(request):
    allhistory = Userhistory.objects.filter(username=request.user)
    content = {"allhistory":allhistory}
    return render(request,"library/allhistoryadmin.html", content)

@login_required(login_url='/logins')
@user_passes_test(is_student)
def clearstudenthistory(request):
    clearhistory = Userhistory.objects.filter(username=request.user)
    clearhistory.delete()
    messages.success(request, "Successsfully cleared all History")
    return redirect("viewstudenthistory")

@login_required(login_url='/logins')
@user_passes_test(is_admin)
def clearadminhistory(request):
    clearhistory = Userhistory.objects.filter(username=request.user)
    clearhistory.delete()
    messages.success(request, "Successsfully cleared all History")
    return redirect("viewadminhistory")