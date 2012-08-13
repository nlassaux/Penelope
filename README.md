# PENELOPE

Penelope is a platform developed with Django for education. It is an inteface for courses and assignments administration with features like :

* Courses administration for teachers.
* Courses subscription for students.
* Assignments linked to courses.
* A groups management to work on assignments.
* Upload of work on the server, with updates until deadline.
* Ask for some required files with a name, description and filetype.
* Download of all assignment's files by the teacher after the deadline or to correct.


Softwares :
-----------

* Django 1.4
* Python 2.7.1


Installation :
--------------

* Be sure you have all softwares requirements (django & python). 
* Clone the repository to your computer.
* In the Penelope/Penelope folder open 'settings.py' and select app you want to be installed in INSTALLED_APPS list.
* Use in the Penelope folder :  `$ python manage.py syncdb` (it will verify your database's architecture) and `$ python manage.py runserver`.

Notes :
-------

* The code have been verified to perform with future versions of django (no depreciated code).
* The Script AddUser.py can add students and teachers to the db, use  `python manage.py shell` and import the file.


Architecture :
--------------

### models.py :

* Users (defaut in Django)
* UserProfile (a model associate in OneToOne to a User to extend the defaut django's model)
* Course
* Assignment
* RequiredFile
* File
* All forms

### urls.py :

The url pattern use the request url to call a view with arguments if needed.

### views.py :

We have one function by url. Each one have the same construction (useless steps are not present) :

1.   Control of authentification with the decorator @login_required.
2.   A query in db for the concerned element.
3.   Verification of permissions (is the owner of the concerned course, is a member of the concerned group..).
4.   Compute (database connects...)
5.   Return with a .html call or a redirection (to another view).

The returned request has linked to it all declared variables because of `locals()`. They can be used in a template to be displayed. You can also send a list of variables.


Security :
----------

### Authentification :

Penelope uses the Django auth app. It uses cookies, login/logout signals, server verification.

Each called view control authentification with the decorator @login_required. A bad return sends the user to the path defined in settings.py : LOGIN_URL. 


### Role :

More verifications with user roles are performed in the beginning of views.

### Forms :

Django use a CRFS Token system to verify POST requests. Each called form that uses a model controls that fields 's content fits with model fields. Django provides a XSS prevent.



Todo (french) :
---------------

* Fusion rôles avec ceux de Django
* Bouton ajout étudiant sur la page editgroup
* Download tous les fichiers d'un groupe
* Finir le DnD avec AJAX et Jquery
* Modifier l'intégration des modals-box dans les pages de consultation de fichiers
* Factoriser le broadcrumb
* Ajouter la taille limite d'upload (50Mb ou au choix)
* Les owners des cours peuvent ajouter des admins
* Choisir les admins des assignments : ne pas mettre l'owner.
* Supprimer les archives crées pour l'upload