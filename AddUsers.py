##############################################################################
##                                                                          ##
##                                                                          ##
##                            User creation script                          ##
##                                                                          ##
##                                                                          ##
##############################################################################


from django.contrib.auth.models import User
from Penelope.models import *
import os


def clear():
    os.system(['clear', 'cls'][os.name == 'nt'])


clear()


def teacheradd(num):
    for i in range(1, num + 1):
        if not User.objects.filter(username='teacher%s' % i):
            query = User.objects.create_user('teacher%s' % i, '', 'password')
            query = UserProfile.objects.get(user__username='teacher%s' % i)
            query.status = 'Teacher'
            query.save()


def studentadd(num):
    for i in range(1, num + 1):
        if not User.objects.filter(username='student%s' % i):
            query = User.objects.create_user('student%s' % i, '', 'password')
            query = UserProfile.objects.get(user__username='student%s' % i)
            query.status = 'Student'
            query.save()


print ('##############################################################')
print ('##                                                          ##')
print ('##                                                          ##')
print ('##                    User creation script                  ##')
print ('##                                                          ##')
print ('##                                                          ##')
print ('##############################################################')

print('')
print('')

num1 = input("Teacher's number : ")
teacheradd(num1)


num2 = input("Number of students : ")
studentadd(num2)

print('')
print('')

print ('##############################################################')
print ('##                                                          ##')
print ('##      You have created %s teachers and %s students         ##' % (num1, num2))
print ('##     Usernames are student1, student2, teacher1...        ##')
print ('##              All passwords are "password"                ##')
print ('##                                                          ##')
print ('##############################################################')

print('')
print('')
print('')

exit()
