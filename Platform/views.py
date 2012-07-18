from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from models import *


# Login
def log(request):
    # Redirect to dashboard if the user is log
    if request.user.is_authenticated():
        return redirect('Platform.views.home')

    form = LoginForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Platform.views.home')
            else:
                return render(request, 'login.html', locals())

    return render(request, 'login.html', locals())


# Logout
def deconnexion(request):
    logout(request)
    return redirect('Platform.views.home')


# Dashboard
@login_required
def home(request):
    # Call the .html
    return render(request, 'dashboard.html')


# List of courses
@login_required
def courses(request):
    # Call the .html with informations to insert
    c_list = Course.objects.all()
    return render(request, 'listcourses.html', {'course_list': c_list})


# List of user's courses
@login_required
def mycourses(request):
    # Only a teacher can access to mycourse page
    if request.user.userprofile.status != 'Teacher':
        return redirect('Platform.views.home')

    mycourse_list = Course.objects.filter(owner=request.user)
    # Call the .html with informations to insert.
    return render(request, 'mycourses.html', locals())


# Add a new course in db
@login_required
def newcourse(request):
    # Only a teacher can add a course
    if request.user.userprofile.status != 'Teacher':
        return redirect('Platform.views.home')

    # Use the model CourseForm
    form = CourseForm()
    # Test if its a POST request
    if request.method == 'POST':
        # Assign to form all fields
        form = CourseForm(request.POST)
        if form.is_valid():
            # Save the course
            save = form.save(commit=False)
            save.owner = request.user
            save = form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert
    return render(request, 'newcourse.html', locals())


@login_required
def deletecourse(request, Course_id):
    deletedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can delete a course
    if request.user != deletedcourse.owner:
        return redirect('Platform.views.home')

    deletedcourse.delete()
    return redirect('Platform.views.mycourses')


# Edition of courses
@login_required
def editcourse(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')

    # Use the model CourseForm
    form = CourseForm(instance=editedcourse)
    # Test if its a POST request
    if request.method == 'POST':
        # Assign to form all fields
        form = CourseForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course.
            form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert.
    return render(request, 'editcourse.html', locals())


# To send the course to somebody else
@login_required
def changeowner(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)
    # Only the owner can edit a course
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')

    # Use the model ChangeCourseOwnerForm
    form = ChangeCourseOwnerForm(instance=editedcourse)
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields of the POST request
        form = ChangeCourseOwnerForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course
            request = form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert
    return render(request, 'changeowner.html', locals())


# The page to subscribe students to your course
@login_required
def addstudents(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)
    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')

    # Use the model ChangeCourseOwnerForm.
    form = AddSubscribedForm(instance=editedcourse)
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields of the POST request.
        form = AddSubscribedForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course.
            request = form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert.
    return render(request, 'addstudents.html', locals())


# Course's details
@login_required
def course_details(request, Course_id):
    # Call the .html with informations to insert
    detailedcourse = Course.objects.get(id=Course_id)
    subscribed = detailedcourse.userprofile_set.all()
    return render(request, 'detailcourse.html', locals())
