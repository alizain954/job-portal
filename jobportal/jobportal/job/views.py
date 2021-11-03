from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from datetime import  date
# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_login(request):
    error = ''
    if request.method == 'POST':
        u = request.POST[ 'uname' ]
        p = request.POST[ 'pwd' ]
        user = authenticate(username=u, password=p)
        if user is not None:
            return redirect('admin_home')

    return render(request, 'admin_login.html',)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    recruiter = Recruiter.objects.all()
    Studentuser = StudentUser.objects.all()
    pen = Recruiter.objects.filter(status='pending')
    rej = Recruiter.objects.filter(status='reject')


    r = 0;
    s = 0;
    p = 0;
    rj = 0;

    for i in recruiter:
        r+=1
    for i in Studentuser:
        s+=1
    for i in pen:
        p+=1
    for i in pen:
        rj+=1
    context = { 'r':r, 's':s, 'p':p, 'rj':rj}

    return render(request, 'admin_home.html', context)

def Logout(request):
    logout(request)
    return redirect('index')

def recruiter_login(request):
    error = ''
    if request.method == 'POST':
        u = request.POST[ 'uname' ]
        p = request.POST[ 'pwd' ]
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == 'recruiter' and user1.status =='accept':
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiter_login.html', d)

def recruiter_signup(request):
    error = ''
    if request.method == 'POST':
        f = request.POST[ 'fname' ]
        l = request.POST[ 'lname' ]
        e = request.POST[ 'email' ]
        con = request.POST[ 'contact' ]
        gen = request.POST[ 'gender' ]
        i = request.FILES[ 'image' ]
        p = request.POST[ 'pwd' ]
        company = request.POST[ 'company' ]
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=con, gender=gen, image=i, company=company, type='recruiter', status='pending')
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiter_signup.html', d)

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_home')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ''
    if request.method == 'POST':
        f = request.POST[ 'fname' ]
        l = request.POST[ 'lname' ]
        con = request.POST[ 'contact' ]
        gen = request.POST[ 'gender' ]


        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.mobile = con
        recruiter.gender = gen
        try:
            recruiter.save()
            recruiter.user.save()
            error = "no"
        except:
            error = "yes"
        try:
            i = request.FILES['image']
            recruiter.image = i
            recruiter.save()
            error = "no"
        except:
            pass
    d = {'recruiter':recruiter, 'error':error}
    return render(request, 'recruiter_home.html', d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ''
    if request.method == 'POST':
        f = request.POST[ 'fname' ]
        l = request.POST[ 'lname' ]
        con = request.POST[ 'contact' ]
        gen = request.POST[ 'gender' ]

        student.user.first_name = f
        student.user.last_name = l
        student.mobile = con
        student.gender = gen
        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"
        try:
            i = request.FILES[ 'image' ]
            student.image = i
            student.save()
            error = "no"
        except:
            pass
    d = {'student':student,'error':error}
    return render(request, 'user_home.html', d)

def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST[ 'uname' ]
        p = request.POST[ 'pwd' ]
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == 'student':
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error':error}
    return render(request, 'user_login.html', d)

def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST[ 'lname' ]
        e = request.POST[ 'email' ]
        con = request.POST[ 'contact' ]
        gen = request.POST[ 'gender' ]
        i = request.FILES[ 'image' ]
        p = request.POST[ 'pwd' ]
        try:
           user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
           StudentUser.objects.create(user=user, mobile=con, gender=gen, image=i, type='student')
           error ="no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'user_signup.html', d)

def view_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data':data}
    return render(request, 'view_user.html', d)

def delete_user(request, id):
    stu = User.objects.get(id=id)
    stu.delete()
    return redirect('view_user')

def delete_recruiter(request, id):
    recruiter = User.objects.get(id=id)
    recruiter.delete()
    return redirect('recruiter_all')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    d = {'data':data}
    return render(request, 'recruiter_pending.html', d)

def change_status(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter = Recruiter.objects.get(id=id)
    if request.method == 'POST':
        s = request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error = "no"
        except:
            error = "yes"
    d = {'recruiter':recruiter, 'error':error}
    return render(request, 'change_status.html', d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='accept')
    d = {'data':data}
    return render(request, 'recruiter_accepted.html', d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='reject')
    d = {'data':data}
    return render(request, 'recruiter_rejected.html', d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data':data}
    return render(request, 'recruiter_all.html', d)

def changepasswordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""

    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = { 'error':error}
    return render(request, 'changepasswordadmin.html', d)

def changepassworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""

    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = { 'error':error}
    return render(request, 'changepassworduser.html', d)


def changepasswordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""

    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = { 'error':error}
    return render(request, 'changepasswordrecruiter.html', d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST[ 'startdate' ]
        ed = request.POST[ 'enddate' ]
        sal = request.POST[ 'salary' ]
        l = request.FILES[ 'logo' ]
        exp = request.POST[ 'experience' ]
        skills = request.POST[ 'skills' ]
        des = request.POST[ 'description' ]
        loc = request.POST['location']
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter, title=jt ,start_date=sd, end_date=ed, salary=sal, image=l, description=des, experience=exp, skill=skills, location=loc, creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_job.html', d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    d = {'job':job}
    return render(request, 'job_list.html', d)

def edit_jobdetail(request, id):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=id)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST[ 'startdate' ]
        ed = request.POST[ 'enddate' ]
        sal = request.POST[ 'salary' ]
        exp = request.POST[ 'experience' ]
        skills = request.POST[ 'skills' ]
        des = request.POST[ 'description' ]
        loc = request.POST['location']

        job.title = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skill = skills
        job.description = des
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                job.start_date = sd
                job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
        else:
            pass
    d = {'error':error, 'job':job}
    return render(request, 'edit_jobdetail.html', d)

def change_companylogo(request, id):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=id)
    if request.method == 'POST':
        cl = request.FILES['logo']
        job.image = cl
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
    d = {'error':error, 'job':job}
    return render(request, 'change_companylogo.html', d)

def latest_job(request):
    data = Job.objects.all().order_by('-start_date')
    d = {'data':data}
    return render(request, 'latest_job.html', d)

def user_latestjob(request):
    job = Job.objects.all().order_by('-start_date')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li = []
    for i in data:
        li.append(i.job.id)
    d = {'job':job, 'li':li}
    return render(request, 'user_latestjob.html', d)

def job_detail(request, pid):
    job = Job.objects.get(id=pid)
    d = {'job':job}
    return render(request, 'job_detail.html', d)

def applyforjob(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error = "notopen"
    else:
        if request.method == 'POST':
            r = request.FILES[ 'resume' ]
            Apply.objects.create(student=student, resume=r, applydate=date.today(), job=job)
            error = "done"
    d = {'error':error}
    return render(request, 'applyforjob.html', d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data = Apply.objects.all()
    d = {'data':data}
    return render(request, 'applied_candidatelist.html', d)

def contactus(request):
    return render(request, 'contactus.html')

