from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import messages
from models import *


# Login
def log(request):
    # Redirect to dashboard if the user is log.
    if request.user.is_authenticated():
        return redirect('Platform.views.home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Platform.views.home')
            else:
                return render_to_response('login.html')

    return render_to_response('login.html')


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
    # Call the .html with informations to insert.
    c_list = Course.objects.all()
    return render(request, 'courses.html', {'course_list': c_list})


# List of user's courses
@login_required
def mycourses(request):
    sub_list = Course.objects.filter(owner=request.user)
    # Call the .html with informations to insert.
    course_list = request.user.userprofile.courses_list.all()
    return render(request, 'mycourses.html', locals())


# Add a new course in db.
@login_required
def newcourse(request):
    # Use the model CourseForm.
    form = CourseForm()
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields.
        form = CourseForm(request.POST)
        if form.is_valid():
            # Save the course.
            obj = form.save(commit=False)
            obj.owner = request.user
            obj = form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert.
    return render(request, 'newcourse.html', locals())


@login_required
def deletecourse(request, Course_id):
    deletedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can delete a course.
    if request.user != deletedcourse.owner:
        return redirect('Platform.views.home')

    deletedcourse.delete()
    return redirect('Platform.views.mycourses')


# Edition of courses.
@login_required
def editcourse(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')

    # Use the model CourseForm.
    form = CourseForm(instance=editedcourse)
    subscribed = editedcourse.userprofile_set.all()
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields.
        form = CourseForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course.
            form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert.
    return render(request, 'editcourse.html', locals())


# To send the course to somebody else.
@login_required
def changeowner(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)
    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')

    # Use the model ChangeCourseOwnerForm.
    form = ChangeCourseOwnerForm(instance=editedcourse)
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields of the POST request.
        form = ChangeCourseOwnerForm(request.POST, instance=editedcourse)
        if form.is_valid():
            # Save the course.
            request = form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert.
    return render(request, 'changeowner.html', locals())


# The page to subscribe students to your course.
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
    # Call the .html with informations to insert.
    detailedcourse = Course.objects.get(id=Course_id)
    return render(request, 'details.html', locals())
