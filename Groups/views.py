from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Groups.models import *


@login_required
def detailgroup(request, Group_id):
    detailedgroup = Group.objects.get(id=Group_id)
    return render(request, 'detailgroup.html', locals())
