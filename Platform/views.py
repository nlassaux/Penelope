from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.template import RequestContext
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
def home(request):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    # Call the .html
    return render(request, 'dashboard.html')


# List of courses
def courses(request):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    # Call the .html with informations to insert.
    c_list = Course.objects.all()
    return render(request, 'courses.html', {'course_list': c_list})


# List of user's courses
def mycourses(request):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    sub_list = Course.objects.filter(owner=request.user)
    # Call the .html with informations to insert.
    course_list = request.user.userprofile.courses_list.all()
    return render(request, 'mycourses.html', locals())


# Add a new course in db.
def newcourse(request):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

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


def deletecourse(request, Course_id):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    deletedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can delete a course.
    if request.user != deletedcourse.owner:
        return redirect('Platform.views.home')

    deletedcourse.delete()
    return redirect('Platform.views.mycourses')


# Edition of courses.
def editcourse(request, Course_id):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')

    # Use the model CourseForm.
    form = CourseForm(instance=editedcourse)
    test = editedcourse.userprofile_set.all()
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
def changeowner(request, Course_id):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

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
            obj = form.save()
            return redirect('Platform.views.mycourses')
    # Call the .html with informations to insert.
    return render(request, 'changeowner.html', locals())


# The page to subscribe students to your course.
def addstudents(request, Course_id):
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Platform.views.home')


# Course's details
def course_details(request, Course_id):
    # Redirect to login if the user is not log.
    if not request.user.is_authenticated():
        return redirect('Platform.views.log')

    # Call the .html with informations to insert.
    detailedcourse = Course.objects.get(id=Course_id)
    return render(request, 'details.html', locals())
