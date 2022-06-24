from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Accounts.models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
import json
from django.http import JsonResponse
from django.utils import timezone


#Imports for Video Call Feature
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# Views For All
def home(request):
    return render(request, 'Accounts/homepage.html')


def loginPage(request):
    """if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('searchCollege')

        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'Accounts/login.html')
    """

    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        try:
            if user is not None:
                login(request, user)
                error = "no"
                g = request.user.groups.all()[0].name
                if g == 'Students':

                    return render(request, 'Accounts/homepage.html')
                elif g == 'Organization':

                    return render(request, 'Accounts/collegeHome.html')

            else:
                error = "yes"

        except Exception as e:
            error = "yes"

    f = {'error': error}

    return render(request, 'Accounts/login.html', f)


# View To Logout
def logoutUser(request):
    logout(request)
    return redirect('loginPage')


# View for signUp page
def signUp(request):
    context = {}
    return render(request, 'Accounts/signUp.html')


# Registration
# View for Student Registration
def student_registration(request):
    error = ""
    user = "none"
    if request.method == 'POST':
        std_fullName = request.POST.get('std_fullName')
        std_userName = request.POST.get('std_username')
        std_email = request.POST.get('std_email')
        std_phone = request.POST.get('std_phone')
        std_password = request.POST.get('std_password')
        confirmStdPassword = request.POST.get('confirmStdPassword')
        std_gender = request.POST.get('std_gender')
        try:
            if std_password == confirmStdPassword:
                reg = StdDetails(std_fullname=std_fullName, std_username=std_userName, std_email=std_email, std_phone=std_phone, std_password=std_password, std_gender=std_gender)
                reg.save()
                user = User.objects.create_user(username=std_userName, password=std_password, first_name=std_fullName, email=std_email)
                std_group = Group.objects.get(name='Students')
                std_group.user_set.add(user)
                user.save()

                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
        # print("Error:",e)
    d = {'error': error}

    #if request.POST.get('std_fullname') and request.POST.get('std_username') and request.POST.get('std_email') and request.POST.get('std_phone') and request.POST.get('std_password') and request.POST.get('std_gender'):
            #saverecord = StdDetails()
            #saverecord.std_fullname = request.POST.get('std_fullname')
            #saverecord.std_userName = request.POST.get('std_username')
            #saverecord.std_email = request.POST.get('std_email')
            #saverecord.std_phone = request.POST.get('std_phone')
            #saverecord.std_password = request.POST.get('std_password')
            #saverecord.std_gender = request.POST.get('std_gender')
            #saverecord.save()
            #messages.success(request, "New Student Successfully Added.")
            #return render(request, 'Accounts/studentRegistration.html')
    return render(request, 'Accounts/studentRegistration.html', d)
       #return render(request, 'Accounts/studentRegistration.html', context)
    #else:
        #return render(request, 'Accounts/studentRegistration.html')


# View for College Registration
def registerCollege(request):
    error = ""
    user = "none"
    if request.method == 'POST':
        cs_name = request.POST.get('cs_name')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_email = request.POST.get('contact_person_email')
        contact_phone = request.POST.get('contact_phone')
        cs_website = request.POST.get('cs_website')
        cs_username = request.POST.get('cs_username')
        cs_password = request.POST.get('cs_password')
        cs_confirmPassword = request.POST.get('cs_confirmPassword')
        cs_district = request.POST.get('cs_district')
        cs_address = request.POST.get('cs_address')
        cs_type = request.POST.get('cs_type')

        try:
            if cs_password == cs_confirmPassword:
                s = OrgDetails(org_name=cs_name, contact_person=contact_person_name, contact_email=contact_person_email,
                         phone_number=contact_phone, org_website=cs_website, cs_username=cs_username, cs_password=cs_password, org_district=cs_district,
                         org_address=cs_address, org_type=cs_type, is_registered=False)
                s.save()
                user = User.objects.create_user(username=cs_username, password=cs_password, first_name= cs_name)
                user.is_active = False
                std_group = Group.objects.get(name='Organization')
                std_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
        # print("Error:",e)
    context = {'error': error}
    return render(request, 'Accounts/collegeRegistration.html', context)


# Views for Search Home Page
# Filter college name column and make list of all college name
def collegeList(request):
    org = OrgDetails.objects.filter().values_list('org_name', flat=True)
    orgList = list(org)

    return JsonResponse(orgList, safe=False)


# View for search function
def searchCollegeByName(request):
    if request.method == 'POST':
        collegesearch = request.POST.get('collegesearch')
        if collegesearch == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            org = OrgDetails.objects.filter(org_name__contains=collegesearch).first()
            id = str(org.org_id)

            if org:
                return studentViewCollegeProfile(request, id)
            else:
                messages.info(request, "No College Matched Your Search")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# View for search college and filter page
def searchCollege(request):
    allCollege = OrgDetails.objects.all()
    location = OrgDetails.objects.all().values_list('org_district', flat=True).distinct()
    affiliation = OrgDetails.objects.all().values_list('org_affiliation', flat=True).distinct()
    if request.method == 'POST':
        collegesearch = request.POST.get('collegesearch')
        col_location = request.POST.get('location')
        col_affiliation = request.POST.get('affiliation')
        print(col_location)
        print(col_affiliation)

        if collegesearch!=None:
            allCollege = OrgDetails.objects.filter(org_name__icontains=collegesearch)

        if col_location!=None:
            allCollege = OrgDetails.objects.filter(org_district__icontains=col_location)

        if col_affiliation!=None:
            allCollege = OrgDetails.objects.filter(org_affiliation__icontains=col_affiliation)

        if col_location!=None and col_affiliation!=None:
            allCollege = OrgDetails.objects.filter(org_location__icontains=col_location, org_affiliation__icontains=col_affiliation)

    context = {"allCollege": allCollege, "location": location, "affiliation": affiliation}
    return render(request, 'Accounts/searchCollege.html', context)















# View for Student
# View for Blog Page
@login_required(login_url='loginPage')
def blogNews(request):
    allBlog = Blog.objects.all()
    allNews = News.objects.all()
    context = {'allBlog': allBlog, 'allNews': allNews}
    return render(request, 'Accounts/blogNews.html', context)


# View for Student to Compare College Page
@login_required(login_url='loginPage')
def compareCollege(request):
    displayName = OrgDetails.objects.all()
    collegeDetails = OrgDetails.objects.all()
    context = {"displayName": displayName, "collegeDetails": collegeDetails}
    return render(request, 'Accounts/compareCollege.html', context)


# View for Student to Book Appointment Page
@login_required(login_url='loginPage')
def bookAppointment(request):
    if not request.user.is_active:
        return redirect('loginpage')
    user = "none"
    allCollege = OrgDetails.objects.all()
    current_user = request.user
    username = current_user.username
    std = StdDetails.objects.filter(std_username=username)
    if request.method == 'POST':
        std_id = request.POST.get('std_id')
        org_id = request.POST.get('org_id')
        std_email = request.POST.get('std_email')
        std_name = request.POST.get('std_name')
        reason = request.POST.get('reason')
        appointmentdate = request.POST.get('appointmentdate')

        appointment = Appointment(std_id=std_id, org_id=org_id, name=std_name, email=std_email, reason=reason, appointment_date=appointmentdate)
        appointment.save()
        # print("Error:",e)
    d = {'allCollege': allCollege, 'std': std}
    return render(request, 'Accounts/bookAppointment.html', d)


# View for Student to View College Profile Page
def studentViewCollegeProfile(request, org_id):
    org = OrgDetails.objects.filter(org_id=org_id)
    d = {'org': org}
    return render(request, 'Accounts/studentViewCollegeProfile.html', d)














# View For College
# View for College Home Page/ View Appointment Page
@login_required(login_url='loginPage')
def collegeHome(request):
    context = {}
    return render(request, 'Accounts/collegeHome.html')


# View for College to View and Update Appointment
@login_required(login_url='loginPage')
def viewAppointment(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g = request.user.groups.all()[0].name
    if g == 'Organization':
        current_user = request.user.username
        org_id = OrgDetails.objects.filter(cs_username=current_user).values_list('org_id', flat=True)
        print(org_id)
        for i in org_id:
            appointment = Appointment.objects.filter(org_id=i)
        #upcomming_appointments = Appointment.objects.filter(org_id=org_id, appointment_date__gte=timezone.now(), status=True).order_by('appointment_date')
        #previous_appointments = Appointment.objects.filter(org_id=org_id,appointmentdate__lt=timezone.now()).order_by('-appointment_date') | Appointment.objects.filter(org_id=org_id, status=False).order_by('-appointment_date')
        d = {'appointment': appointment}
        #d = {'upcomming_appointments': upcomming_appointments, 'previous_appointments': previous_appointments}
        if request.method =='POST':
            roomName = request.POST.get('roomName')
            Appointment.objects.filter(org_id=i).update(roomname = roomName)

        return render(request, 'Accounts/collegeHome.html', d)


# View for College to update Appointment with Update Button
@login_required(login_url='loginPage')
def updateAppointment(request):
    if not request.user.is_active:
        return redirect('loginpage')


# View for College Profile Page for College
@login_required(login_url='loginPage')
def collegeProfile(request):
    if not request.user.is_active:
        return redirect('loginpage')

    current_user = request.user.username
    org_id = OrgDetails.objects.filter(cs_username=current_user).values_list('org_id', flat=True)
    for i in org_id:
        org = OrgDetails.objects.filter(org_id=i)
    context = {'org': org}
    return render(request, 'Accounts/collegeProfile.html', context)


# View for College to Edit College Profile Page
@login_required(login_url='loginPage')
def editCollegeProfile(request):
    if not request.user.is_active:
        return redirect('loginPage')

    org_id = OrgDetails.objects.filter(cs_username=request.user.username).values_list('org_id', flat=True)
    for i in org_id:
        org = OrgDetails.objects.filter(org_id=i)
    context = {'org': org}

    if request.method == 'POST':
        college_image = request.FILES.get('college_image')
        org_name = request.POST.get('org_name')
        org_phone = request.POST.get('org_phone')
        org_website = request.POST.get('org_website')
        org_email = request.POST.get('org_email')
        org_address = request.POST.get('org_address')
        org_type = request.POST.get('org_type')
        org_district = request.POST.get('org_district')
        org_username = request.POST.get('org_username')
        org_password = request.POST.get('org_password')
        admission_fee = request.POST.get('admission_fee')
        tution_fee = request.POST.get('tution_fee')
        acceptance_rate = request.POST.get('acceptance_rate')
        std_number = request.POST.get('std_number')
        org_overview = request.POST.get('org_overview')
        org_affiliation = request.POST.get('org_affiliation')
        org_location = request.POST.get('org_location')
        avg_gpa = request.POST.get('avg_gpa')
        if std_number == "":
            std_number=None

        if admission_fee == "":
            admission_fee = None

        if tution_fee == "":
            tution_fee = None

        if avg_gpa == "":
            avg_gpa=None

        OrgDetails.objects.filter(org_id=i).update(org_name=org_name, org_email=org_email, org_phone=org_phone, org_website=org_website, org_district=org_district, org_address=org_address, org_type=org_type,
                                                   cs_username=org_username, cs_password=org_password, students_no=std_number,
                                                   admission_fee=admission_fee, tution_fee=tution_fee, acceptance_rate=acceptance_rate,
                                                   avg_gpa=avg_gpa, org_affiliation=org_affiliation,org_location=org_location,
                                                   org_overview=org_overview, org_image=college_image)

    return render(request, 'Accounts/editCollegeProfile.html', context)


# View for College to Post Blogs and View Blog Posted
@login_required(login_url='loginPage')
def postBlog(request):
    error = ""
    if not request.user.is_active:
        return redirect('loginpage')
    current_user = request.user
    username = current_user.username
    org = OrgDetails.objects.filter(cs_username=username)
    org_id = OrgDetails.objects.filter(cs_username=request.user.username).values_list('org_id', flat=True)
    for i in org_id:
        selfBlog = Blog.objects.filter(college_id=i)
    context = {"org": org, "selfBlog": selfBlog}
    if request.method == 'POST':
        blog_title = request.POST.get('blog_title')
        blog_content = request.POST.get('blog_content')
        blog_image = request.FILES.get('blog_image')
        org_id = request.POST.get('org_id')
        blog = Blog(blog_title= blog_title, blog_content= blog_content, blog_image=blog_image, college_id=org_id)
        blog.save()

    return render(request, 'Accounts/postBlog.html', context)


# View for College to delete blog with Delete Button
@login_required(login_url='loginPage')
def deleteBlog(request, blog_id):
    if not request.user.is_active:
        return redirect('loginPage')
    b = Blog.objects.get(blog_id=blog_id)
    b.delete()
    return redirect('postBlog')













# View For Admin
# Admin Login Page
def adminLogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    context = {'error': error}
    return render(request, 'Accounts/adminLogin.html', context)


# Admin Logout
def adminLogout(request):
    if not request.user.is_staff:
        return redirect('adminLogin')
    logout(request)
    return redirect('adminLogin')


# View for Admin Dashboard and Blog View
@login_required(login_url='adminLogin')
def adminDashboard(request):
    if not request.user.is_staff:
        return redirect('adminLogin')
    allColleges = OrgDetails.objects.filter(is_registered=True)
    allStudents = StdDetails.objects.all()
    totalColleges = allColleges.count()
    totalStudents = allStudents.count()
    allBlogs = Blog.objects.all()
    context = {'totalColleges': totalColleges, 'totalStudents': totalStudents, 'allBlogs': allBlogs}
    return render(request, 'Accounts/adminDashboard.html', context)


# View for Admin to Delete Blog with Delete Button
@login_required(login_url='adminLogin')
def deleteBlogDashboard(request, blog_id):
    if not request.user.is_staff:
        return redirect('adminLogin')
    b = Blog.objects.get(blog_id=blog_id)
    b.delete()
    return redirect('adminDashboard')


# View for Admin to view all Students
@login_required(login_url='adminLogin')
def adminViewStudent(request):
    if not request.user.is_staff:
        return redirect('adminLogin')
    std = StdDetails.objects.all()
    s = {'std': std}
    return render(request, 'Accounts/adminViewStudents.html', s)


# Admin Delete Student
@login_required(login_url='adminLogin')
def admin_delete_student(request, std_id, std_userName):
    if not request.user.is_staff:
        return redirect('adminLogin')
    student = StdDetails.objects.get(std_id=std_id)
    student.delete()
    users = User.objects.filter(username=std_userName)
    users.delete()
    return redirect('adminViewStudent')


# View for Admin to view all registered college
@login_required(login_url='adminLogin')
def adminViewCollege(request):
    if not request.user.is_staff:
        return redirect('adminLogin')
    col = OrgDetails.objects.filter(is_registered=True)
    c = {'col': col}

    return render(request, 'Accounts/adminViewCollege.html', c)


# View for Admin to delete Registered College with Delete Button
@login_required(login_url='adminLogin')
def admin_delete_college(request, org_id, cs_username):
    if not request.user.is_active:
        return redirect('adminLogin')
    org = OrgDetails.objects.get(org_id=org_id)
    org.delete()
    users = User.objects.filter(username=cs_username)
    users.delete()
    return redirect('adminViewCollege')


# View for Admin to view and Register Unregistered College
@login_required(login_url='adminLogin')
def adminRegisterCollege(request):
    if not request.user.is_staff:
        return redirect('adminLogin')
    col = OrgDetails.objects.filter(is_registered=False)
    c = {'col': col}

    return render(request, 'Accounts/adminRegisterCollege.html', c)


# View for Admin to Register College with Register Button
@login_required(login_url='adminLogin')
def registerUnregisteredCollege(request, org_id, cs_username):
    if not request.user.is_active:
        return redirect('adminLogin')
    OrgDetails.objects.filter(org_id=org_id).update(is_registered = 1)
    AuthUser.objects.filter(username=cs_username).update(is_active = 1)

    return redirect('adminRegisterCollege')


# View for Admin to delete Unregistered College with Delete Button
@login_required(login_url='adminLogin')
def admin_delete_unregisteredCollege(request, org_id):
    if not request.user.is_active:
        return redirect('adminLogin')
    org = OrgDetails.objects.get(org_id=org_id)
    org.delete()
    return redirect('adminRegisterCollege')


# View for Admin to Post and View News
@login_required(login_url='adminLogin')
def adminNews(request):
    error = ""
    if not request.user.is_staff:
        return redirect('adminLogin')
    allNews = News.objects.all()
    context = {"allNews": allNews}
    if request.method == 'POST':
        news_headline = request.POST.get('news_headline')
        news_content = request.POST.get('news_content')
        news_image = request.FILES.get('news_image')
        news = News(news_headline= news_headline, news_content= news_content, news_image=news_image)
        news.save()

    return render(request, 'Accounts/adminNews.html', context)


# View for Admin to delete news with Delete Button
@login_required(login_url='adminLogin')
def deleteNews(request, news_id):
    if not request.user.is_active:
        return redirect('adminLogin')
    b = News.objects.get(news_id=news_id)
    b.delete()
    return redirect('adminNews')




















#Views for Video Counsellig Feature
@login_required(login_url='loginPage')
def lobby(request):
    return render(request, 'Accounts/lobby.html')


def room(request):
    return render(request, 'Accounts/room.html')


def getToken(request):
    appId = "0fb919ad5ab5445b8dd0a43fc4c3eac5"
    appCertificate = "378c0b3d00c44c05902b1c34f6651d7d"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)

