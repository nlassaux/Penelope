##############################################################
##                                                          ##
##                                                          ##
##                    User creation script                  ##
##                                                          ##
##                                                          ##
##############################################################


from django.contrib.auth.models import User


def teacheradd(num):
    for i in range(1, num + 1):
        if not User.objects.filter(username='teacher%s' % i):
            query = User.objects.create_user('teacher%s' % i, 'student@mail.fr', 'password')


def studentadd(num):
    for i in range(1, num + 1):
        if not User.objects.filter(username='student%s' % i):
            query = User.objects.create_user('student%s' % i, 'student@mail.fr', 'password')


print ('##############################################################')
print ('##                                                          ##')
print ('##                                                          ##')
print ('##                    User creation script                  ##')
print ('##                                                          ##')
print ('##                                                          ##')
print ('##############################################################')


num = input("Teacher's number : ")
teacheradd(num)


num = input("Number of students : ")
studentadd(num)

exit()
