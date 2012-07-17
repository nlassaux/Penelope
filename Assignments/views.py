from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Platform.models import *
from Assignments.models import *


@login_required
def editassignment(request, Assignment_id):
    # Use the id in the url (GET) to select our assignment.
    editedassignment = Assignment.objects.get(id=Assignment_id)

    # Only the owner can edit an assignment.
    if request.user != editedassignment.course.owner:
        return redirect('Platform.views.home')

    # Use the model EditAssignmentForm
    form = EditAssignmentForm(instance=editedassignment)
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields.
        form = EditAssignmentForm(request.POST, instance=editedassignment)
        if form.is_valid():
            # Save the assignment.
            form.save()
            return redirect('/%s/details' % editedassignment.course.id)
    # Call the .html with informations to insert.
    return render(request, 'editassignment.html', locals())


@login_required
def assignment_details(request, Assignment_id):
    detailedassignment = Assignment.objects.get(id=Assignment_id)
    return render(request, 'detailassignment.html', locals())


@login_required
def addassignment(request, Course_id):
    # Only the owner can edit an assignment.
    if request.user.userprofile.status != 'Teacher':
        return redirect('Platform.views.home')

    # Use the model EditAssignmentForm
    form = AddAssignmentForm()
    # Test if its a POST request.
    if request.method == 'POST':
        # Assign to form all fields.
        form = AddAssignmentForm(request.POST)
        if form.is_valid():
            # Save the assignment.
            save = form.save(commit=False)
            save.course = Course.objects.get(id=Course_id)
            save = form.save()
            return redirect('/%s/details' % Course_id)
    # Call the .html with informations to insert.
    return render(request, 'addassignment.html', locals())
