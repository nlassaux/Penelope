from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core import serializers
from models import *
from settings import *
import os


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

    # Use the model CourseForm with as initial values them of editedcourse
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

    # Use the model ChangeCourseOwnerForm with as initial values them of editedcourse
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

    # Use the model AssSubscribedForm with as initial values them of editedcourse
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

    for user in User.objects.filter(editedcourse__in=course_list):
        user.course_list.remove(editedcourse)

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

    # Control if the user is subscribed or is the owner of the assignment's course
    if detailedassignment.course not in request.user.course_list.all() and request.user != detailedassignment.course.owner:
        return redirect('Penelope.views.home')

    form = UploadFileForm()

    # If the user is a student, we load his group and his file.
    if request.user.userprofile.status == 'student':
        mygroup = request.user.group_list.filter(assignment=detailedassignment)
        memberlist = User.objects.filter(group_list__id=mygroup)
        groupfile = File.objects.filter(group=mygroup)
        if detailedassignment.method == 'required files':
            for required in detailedassignment.requiredfile_set.all():
                name = 'fileassociate' + unicode(required.id)

    # If the user is a teacher, we load the list of users without groups.
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


# Function to upload a file file with two methods : simple upload(1) and overwriting(2)
@login_required
def uploadfile(request, Assignment_id, RequiredFile_id):
    detailedassignment = Assignment.objects.get(id=Assignment_id)

    # Verify if the firm deadline is past
    if detailedassignment.firm_deadline_past():
        return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)

    # Verify if the user is subscribed to the course and if he his in a group attached to the assignment.
    if (detailedassignment.course not in request.user.course_list.all()) or not request.user.group_list.get(assignment=detailedassignment):
        return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)

    # Test if a post request has been sent and save informations
    if request.method == 'POST':
        mygroup = request.user.group_list.get(assignment=detailedassignment)
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            groupfile = mygroup.file_list.all()
            for file in groupfile:
                if file.filename() == request.FILES['file'].name:
                    file.delete()

        # 0 sent by get if no requirement and the id of requirement in other cases
        if RequiredFile_id == '0':
            requirement = None
        else:
            requirement = RequiredFile.objects.get(id=RequiredFile_id)

        # Upload and overwrite if the same file's name exists
        addfile = File(file=request.FILES['file'], group=mygroup, uploader=request.user, requiredfile=requirement)
        addfile.save()

    return redirect('Penelope.views.detailassignment', Assignment_id=Assignment_id)


# Page to download a file
@login_required
def downloadfile(request, File_id):
    downloadedfile = File.objects.get(id=File_id)
    filename = downloadedfile.file.name.split('/')[-1]
    response = HttpResponse(downloadedfile.file, mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


# Page to delete a file
@login_required
def deletefile(request, File_id):
    deletedfile = File.objects.get(id=File_id)
    deletedfile.delete()

    return redirect('Penelope.views.detailassignment', Assignment_id=deletedfile.group.assignment.id)


# Use Post informations to add rew requirements and update existing ones.
@login_required
def addrequirement(request, Assignment_id):
    if request.method == 'POST':
        editedassignment = Assignment.objects.get(id=Assignment_id)
        for i in range(1, int(request.POST.get('requiredfilesnb')) + 1):
            try:
                required = RequiredFile.objects.get(id=request.POST.get('requiredfileid' + unicode(i)))
                required.name = request.POST.get('requiredfilename' + unicode(i))
                required.description = request.POST.get('requiredfiledescription' + unicode(i))
                required.type = request.POST.get('requiredfiletype' + unicode(i))
                required.save()
            except:
                required = RequiredFile(assignment=editedassignment,
                    name=request.POST['requiredfilename' + unicode(i)],
                    description=request.POST['requiredfiledescription' + unicode(i)],
                    type=request.POST['requiredfiletype' + unicode(i)])
                required.save()

        return redirect('Penelope.views.editassignment', Assignment_id=Assignment_id)

    # This is used by ajax request in get to load all fields of forms with required objects
    if request.method == 'GET':
        editedassignment = Assignment.objects.get(id=request.GET['assignment_id'])
        # Send a xml formated file with required objects
        data = list(RequiredFile.objects.filter(assignment=editedassignment))
        response = serializers.serialize("xml", data)

        return HttpResponse(response)
