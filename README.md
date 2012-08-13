                               	   	  Penelope 
                               	  	 ==========

Penelope is a platform developed with Django for education. It is an inteface for courses and assignments administration with features like :

* Courses administration for teachers.
* Courses subscription for students.
* Assignments linked to courses.
* Students' Groups system to work on assignments.
* Upload of work on the server, with updates until deadline.
* Ask for some required files with a name, description and filetype.


Softwares :
-----------

* Django 1.4
* Python 2.7.1


Organisation :
--------------

-- Penelope (folder)
-- -- Penelope (project)


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


Installation :
--------------

* Be sure you have all softwares requirements (django & python). 
* Clone the repository to your computer.
* In the Penelope/Penelope folder open 'settings.py' and select app you want to be installed in INSTALLED_APPS list.
* Use in the Penelope folder :  `$ python manage.py syncdb` (it will verify your database's architecture) and `$ python manage.py runserver`

Notes :
-------

* The code have been verified to perform with future versions of django (no depreciated code).
* The Script AddUser.py can add students and teachers to the db, use  `python manage.py shell` and import the file.

Architecture :
--------------

Models :



