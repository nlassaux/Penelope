from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Groups.models import *


# Page to detail a group
@login_required
def detailgroup(request, Group_id):
    detailedgroup = Group.objects.get(id=Group_id)
    return render(request, 'detailgroup.html', locals())


# Page to add a group
@login_required
def addgroup(request, Assignment_id):
    # Only the owner of the assignment can add a group
    if request.user != editedassignment.course.owner:
        return redirect('Penelope.views.home')

    editedassignment = Assignment.objects.get(id=Assignment_id)
    subscribed = editedassignment.course.userprofile_set.all()

    # Create groups and add users in
    if request.method == 'POST':
        for member in subscribed:
            groupnum = request.POST[member.user.username]
            ask = Group.objects.filter(assignment=editedassignment, name=groupnum)
            if ask:
                ask = Group.objects.get(assignment=editedassignment, name=groupnum)
                ask.user.add(member.user)
            else:
                add = Group.objects.create(assignment=editedassignment, name=groupnum)
                ask = Group.objects.get(assignment=editedassignment, name=groupnum)
                ask.user.add(member.user)

    return render(request, 'addgroup.html', locals())
