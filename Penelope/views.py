from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from models import *


# Login
def connection(request):
    # Redirect to dashboard if the user is log
    if request.user.is_authenticated():
        return redirect('Penelope.views.home')

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
def disconnection(request):
    logout(request)
    return redirect('Penelope.views.home')


# Dashboard
@login_required
def home(request):
    mycourse_list = Course.objects.filter(owner=request.user)
    # Call the .html
    return render(request, 'dashboard.html', locals())


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


# Course's details - Modified for app
@login_required
def detailcourse(request, Course_id):
    # Call the .html with informations to insert
    detailedcourse = Course.objects.get(id=Course_id)
    subscribed = detailedcourse.subscribed.filter()

    # Only subscribed students and owner(teacher) can view the course
    if detailedcourse not in request.user.course_list.all() and request.user != detailedcourse.owner:
        return redirect('Penelope.views.home')

    # delete if assignments not used
    assignments = detailedcourse.assignment.filter(visible=True)
    return render(request, 'detailcourse.html', locals())


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


@login_required
def clearallstudents(request, Course_id):
    editedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can edit a course.
    if request.user != editedcourse.owner:
        return redirect('Penelope.views.home')

    groups_list = Group.objects.filter(assignment__in=editedcourse.assignment.all())
    for group in groups_list:
        group.delete()

    subscribed = editedcourse.subscribed.clear()

    return redirect('Penelope.views.detailcourse', Course_id=Course_id)


@login_required
def deletecourse(request, Course_id):
    deletedcourse = Course.objects.get(id=Course_id)  # (The ID is in URL)

    # Only the owner can delete a course
    if request.user != deletedcourse.owner:
        return redirect('Penelope.views.home')

    deletedcourse.delete()
    return redirect('Penelope.views.home')


# Page to edit an assignment
@login_required
def editassignment(request, Assignment_id):

    # Use the id in the url (GET) to select our assignment
    editedassignment = Assignment.objects.get(id=Assignment_id)

    # Only the owner can edit an assignment
    if request.user != editedassignment.course.owner:
        return redirect('Penelope.views.home')

    # Use the model EditAssignmentForm
    form = EditAssignmentForm(instance=editedassignment)

    # Test if it's a POST request.
    if request.method == 'POST':
        # Assign to form all fields
        form = EditAssignmentForm(request.POST, instance=editedassignment)
        if form.is_valid():
            # Save the assignment
            form.save()
            return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)
    # Call the .html with informations to insert (with locals())
    return render(request, 'editassignment.html', locals())


# Page to detail an assignment
@login_required
def detailassignment(request, Assignment_id):

    detailedassignment = Assignment.objects.get(id=Assignment_id)

    if detailedassignment.course not in request.user.course_list.all() and request.user != detailedassignment.course.owner:
        return redirect('Penelope.views.home')

    form = UploadWorkForm()

    if request.user.userprofile.status == 'student':
        try:
            mygroup = request.user.group_list.get(assignment=detailedassignment)
            groupwork = Work.objects.filter(group=mygroup)
        # UGLY ---- To change
        except Group.DoesNotExist:
            nogroup='nogroup'
        if request.method == 'POST':
            form = UploadWorkForm(request.POST, request.FILES)
            if form.is_valid():
                path = '/test'
                addwork = Work(file=request.FILES['file'], group=mygroup, uploader=request.user)
                addwork.save()
                return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)
    else:
        groupless = User.objects.filter(course_list__assignment=detailedassignment).exclude(group_list__assignment=detailedassignment)

    return render(request, 'detailassignment.html', locals())


# Page to add an assignment
@login_required
def addassignment(request, Course_id):

    editedcourse = Course.objects.get(id=Course_id)

    # Only the owner can edit an assignment
    if request.user.userprofile.status != 'teacher':
        return redirect('Penelope.views.home')

    # Use the model EditAssignmentForm
    form = AddAssignmentForm()

    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields
        form = AddAssignmentForm(request.POST)
        if form.is_valid():
            # Save the assignment
            save = form.save(commit=False)
            save.course = Course.objects.get(id=Course_id)
            save = form.save()
            return redirect('Penelope.views.detailassignment', Assignment_id=save.id)
    # Call the .html with informations to insert
    return render(request, 'addassignment.html', locals())


# Page to delete an assignment
@login_required
def deleteassignment(request, Assignment_id):

    deletedassignment = Assignment.objects.get(id=Assignment_id)  # (The ID is in URL)

    # Only the owner can delete an assignment
    if request.user != deletedassignment.course.owner:
        return redirect('Penelope.views.home')

    deletedassignment.delete()
    return redirect('Penelope.views.detailcourse', Course_id=deletedassignment.course.id)


# Page to detail a group
@login_required
def detailgroup(request, Group_id):

    detailedgroup = Group.objects.get(id=Group_id)

    if detailedgroup.assignment.course not in request.user.course_list.all() and request.user != detailedgroup.assignment.course.owner:
        return redirect('Penelope.views.home')

    return render(request, 'detailgroup.html', locals())


# Page to add a group
@login_required
def addgroup(request, Assignment_id):

    editedassignment = Assignment.objects.get(id=Assignment_id)

    # Only the owner of the assignment can add a group
    if request.user != editedassignment.course.owner:
        return redirect('Penelope.views.home')

    subscribed = editedassignment.course.subscribed.all()

    # Create groups and add users in
    if request.method == 'POST':
        for student in subscribed:

            groupnum = request.POST[student.username]
            query = Group.objects.filter(assignment=editedassignment, name=groupnum)
            if query:
                query = Group.objects.get(assignment=editedassignment, name=groupnum)
            else:
                query = Group.objects.create(assignment=editedassignment, name=groupnum)

            query.members.add(student)

        return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)

    return render(request, 'editgroups.html', locals())


# Page to add a group
@login_required
def userasgroup(request, Assignment_id):

    editedassignment = Assignment.objects.get(id=Assignment_id)

    # Only the owner of the assignment can add a group
    if request.user != editedassignment.course.owner:
        return redirect('Penelope.views.home')

    subscribed = editedassignment.course.subscribed.all()

    # We delete all groups before creating new ones
    groups_list = Group.objects.filter(assignment=editedassignment)
    for group in groups_list:
        group.delete()

    # Assign to a student a group
    groupnum = 1
    for student in subscribed:
        query = Group.objects.create(assignment=editedassignment, name=groupnum)
        student.group_list.add(query)
        groupnum += 1

    return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)


# Page to download a work
@login_required
def downloadwork(request, Work_id):
    downloadededwork = Work.objects.get(id=Work_id)
    filename = downloadededwork.file.name.split('/')[-1]
    response = HttpResponse(downloadededwork.file ,mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


# Page to delete a work
@login_required
def deletework(request, Work_id):
    deletedwork = Work.objects.get(id=Work_id)

    deletedwork.delete()

    return redirect('Penelope.views.detailassignment', Assignment_id=deletedwork.group.assignment.id)
