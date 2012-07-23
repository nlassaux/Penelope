from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Penelope.models import *
from Assignments.models import *
from Groups.models import *


# Course's details - Modified for app
@login_required
def detailcourse(request, Course_id):

    # Call the .html with informations to insert
    detailedcourse = Course.objects.get(id=Course_id)

    subscribed = detailedcourse.userprofile_set.all()

    # delete if assignments not used
    assignments = detailedcourse.assignment_set.filter(visible=True)
    return render(request, 'detailcourse.html', locals())


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
            return redirect('Assignments.views.detailassignment', Assignment_id=Assignment_id)
    # Call the .html with informations to insert (with locals())
    return render(request, 'editassignment.html', locals())


# Page to detail an assignment --- TO OVERWRITE !! ---
@login_required
def detailassignment(request, Assignment_id):

    detailedassignment = Assignment.objects.get(id=Assignment_id)

    form = UploadWorkForm()

    if request.user.userprofile.status == 'student':
        try:
            mygroup = request.user.group_set.get(assignment=detailedassignment)
            groupwork = Work.objects.filter(group=mygroup)
        except Group.DoesNotExist:
            print "test"

    if request.method == 'POST':
        form = UploadWorkForm(request.POST, request.FILES)
        if form.is_valid():
            addwork = Work(file=request.FILES['file'], group=mygroup, uploader=request.user)
            addwork.save()
            return redirect('Assignments.views.detailassignment', Assignment_id=Assignment_id)
    return render(request, 'detailassignment.html', locals())


# Page to add an assignment
@login_required
def addassignment(request, Course_id):

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
            return redirect('Assignments.views.detailassignment', Assignment_id=save.id)
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
