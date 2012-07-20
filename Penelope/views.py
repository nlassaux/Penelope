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
        return redirect('Penelope.views.home')

    # Call the LoginForm modek (empty)
    form = LoginForm()

    # Control if a POST request has been sent.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Penelope.views.home')
            else:
                return render(request, 'login.html', locals())

    return render(request, 'login.html', locals())


# Logout
def deconnexion(request):
    logout(request)
    return redirect('Penelope.views.home')


# Dashboard
@login_required
def home(request):
    mycourse_list = Course.objects.filter(owner=request.user)
    # Call the .html
    return render(request, 'dashboard.html', locals())


# List of courses
@login_required
def courseslist(request):
    # Call the .html with informations to insert
    course_list = Course.objects.all()
    return render(request, 'listcourses.html', locals())


# Add a new course in db
@login_required
def newcourse(request):
    # Only a teacher can add a course
    if request.user.userprofile.status != 'teacher':
        return redirect('Penelope.views.home')

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
            return redirect('Penelope.views.detailcourse', Course_id=save.id)
    # Call the .html with informations to insert
    return render(request, 'newcourse.html', locals())


@login_required
def deletecourse(request, Course_id):
    deletedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can delete a course
    if request.user != deletedcourse.owner:
        return redirect('Penelope.views.home')

    deletedcourse.delete()
    return redirect('Penelope.views.home')


# Edition of courses
@login_required
def editcourse(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course
    if request.user != editedcourse.owner:
        return redirect('Penelope.views.home')

    # Use the model CourseForm
    form = CourseForm(instance=editedcourse)
    # Test if its a POST request
    if request.method == 'POST':
        # Assign to form all fields
        form = CourseForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course.
            form.save()
            return redirect('Penelope.views.detailcourse', Course_id=Course_id)
    # Call the .html with informations to insert.
    return render(request, 'editcourse.html', locals())


# To send the course to another teacher
@login_required
def changeowner(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course
    if request.user != editedcourse.owner:
        return redirect('Penelope.views.home')

    # Use the model ChangeCourseOwnerForm
    form = ChangeCourseOwnerForm(instance=editedcourse)
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields of the POST request
        form = ChangeCourseOwnerForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course
            request = form.save()
            return redirect('Penelope.views.home')
    # Call the .html with informations to insert
    return render(request, 'changeowner.html', locals())


# The page to subscribe students to a course
@login_required
def addstudents(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Penelope.views.home')

    # Use the model AssSubscribedForm
    form = AddSubscribedForm(instance=editedcourse)
    # Test if its a POST request
    if request.method == 'POST':
        # Assign to form all fields of the POST request
        form = AddSubscribedForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course
            request = form.save()
            return redirect('Penelope.views.detailcourse', Course_id=Course_id)
    # Call the .html with informations to insert
    return render(request, 'addstudents.html', locals())


# Course's details
@login_required
def detailcourse(request, Course_id):
    detailedcourse = Course.objects.get(id=Course_id)
    # Save the list of users subscribed to the course
    subscribed = detailedcourse.userprofile_set.all()
    # Call the .html with informations to insert
    return render(request, 'detailcourse.html', locals())
