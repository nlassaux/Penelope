# Penelope

* * * 

## Présentation :
Penelope est une plateforme développée avec Django dont le rôle premier est de faciliter et accélérer les tâches récurrentes des enseignants. Attachée à un système de gestion d'élèves, Penelope devient un outil pour permettre à un enseignant d'informer ses élèves des tâches qu'ils ont à effectuer dans le cadre d'un cours, de suivre leur travail, le tester, le télécharger et mettre à la disposition des étudiants du contenu pour les cours.

**Pourquoi Django ?**

Django est un framework Python pour le web. Basé sur la méthode DRY (Don't Repeat Yourself) et une architecture MVC (Model View Controler), on obtient un site parfaitement organisé, avec un nombre de lignes de code réduit et la possibilité d'effectuer des modifications ou de maintenir son code, en un temps réduit.

**Avancement**

Un enseignant peut créer des cours, des devoirs, y assigner des fichiers requis, créer des groupes d'étudiants pour qu'ils travaillent ensemble, télécharger leur travail.

Un étudiant dispose de sa liste de cours et de devoirs, il peut envoyer son travail.

**Future évolution**

On pourra accentuer la communication entre étudiants et enseignants. Par exemple mettre en place un système de messagerie sur la plateforme. La mise à disposition de la part des enseignants de contenu (pdf, html, autre) dans un cours pourra rendre Penelope plus complet.

Tenir informé l'enseignant de l'état de son devoir : ("tous les étudiants ont envoyé les fichiers demandés" ou inversement "personne n'a complété les fichiers"…)

Les enseignants pourraient également tester la qualité du code uploadé par les élèves, tester la longueur d'un fichier pdf… 

Pour les groupes, un système de constitution de ceux-ci par les élèves serait intéressant.

Vous l'aurez compris, Penelope peut se voir ajouté de nombreuses fonctionnalités pour couvrir de nombreuses nécessités.

## L'architecture de Penelope :

Django organise un projet en blocks fonctionnels appelés applications (apps). Cela permet de rajouter des fonctionnalités rapidement, sans toucher au reste, en rajoutant une app. Celle-ci dispose de ses propres modèles, ses vues, ses fichiers pour l'administration. 

Le dossier qui porte le nom du projet (Penelope) est l'application principale, qui apporte les fonctionnalités fondamentales à la plateforme. Elle contient comme toute application les fichiers views.py, models.py, urls.py, admin.py, tests.py mais à cela s'ajoute le fichier settings.py qui sert pour toutes les apps.

Vous pouvez appeler les modules, des fonctions en les important quand vous en avez besoin. `from Penelope.models import *` importera les modèles de l'application principale `from an_app.models import *` trouvera les modèles de cette application et les importera.

**Les fichiers :**

![](https://github.com/nico401/Penelope/blob/master/Rapport/She%CC%81ma.png?raw=true)

* _settings.py_ (dans l'app principale) : contient les réglages de la BDD, les divers chemins vers les dossiers importants, les informations de timezone, la liste des apps..
* _views.py_ : Fonctions qui sélectionnent les données à afficher dans une page et appellent le template adéquat. Peut effectuer des vérifications, du traitement de requêtes POST, GET…
* _urls.py_ : Table de correspondance urls <-> vues.
* _models.py_ : Les modèles utilisés dans le projets. Des objets à stocker en BDD ou des formulaires traitées comme des objets. Django créé automatiquement les tables nécessaire en BDD pour correspondre aux modèles créés (après redémarrage du serveur). 
* _admin.py_ (facultatif) : Détermine les objets/modèles à afficher en partie admin, comment les afficher… 
* _tests.py_ (facultatif) : Fonctions exécutées lors d'un `$ python manage.py test 'appname'` ou un `$ python manage.py test` (pour ce dernier, nos tests sont effectués après les tests de base de Django).

**Les dossiers :**

* Templates : Les fichiers .html qui sont appelés par les vues.
* Templatestags (facultatif) : Les fonctions appelées dans les templates (sous forme de tags).
* fixtures (facultatif) : Les fichiers pour peupler la BDD avant les tests (en json ou xml).

## Urls.py

Ce fichier permet de mentionner la vue correspondant à une url. On peut faire passer à la vue des informations dans l'url en mettant le nom de variable entre parenthèses. 
    
     url(r'^(?P<Course_id>\d+)/details/$', 'Penelope.views.detailcourse'), 

Si on appelle `/1/details/` on aura dans la vue detailcourse la variable :`Course_id = 1`.

Le `$` à la fin précise que c'est la fin de l'url. Il n'est pas obligatoire mais enlève tous les cas qui pourraient arriver qui donneraient `/1/details/autrechose/` C'est une sécurité.

## Les Modules de Django :
Django propose des modules, sous formes d'app, dont les fichiers sont dans ceux de Django. Ils comprennent une gestion des utilisateurs, des sessions, des messages (e.g : "Vous avez un message", "Cours sauvegardé avec succès"…) que l'on peut déclarer et afficher sur les templates, un panneau d'administration permettant d'éditer toutes les entrées en BDD, un système de recherche des fichiers statics et enfin des fonctions supplémentaires pour les modèles (humanization des noms…).

**L'administration**

L'administration de Django est accessible depuis `www.site.fr/admin/`. Dans `app/admin.py` vous pouvez rajouter au fur et à mesure les modèles crées avec la ligne : `admin.site.register(models.NomDuModele)`. Ceux autorisés pourront alors modifier, créer, supprimer les entrées de ce modèle dans l'administration.

La majorité de ces actions sont faisable depuis les fonctionnalités pour les utilisateurs. Un enseignant ne doit pas accéder à un panneau spécial pour supprimer un devoir par exemple, le panneau d'administration est prévu pour être utilisé plus ponctuellement.

Vous pouvez également changer la façon dont les modèles sont affichés en définissant dans ce même fichier des champs à regrouper, des styles de présentation… 

[admin](https://docs.djangoproject.com/en/1.4/ref/contrib/admin/)

**Gestion des utilisateurs**

Le système intégré à Django pour les utilisateurs est très bien fait, on y retrouve une gestion de permissions (type read/write/delete sur les tables de la partie admin) et les champs les plus importants pour définir une personne (first-name, last-name, mail…).

S'appuie là dessus le système de sessions pour qu'un utilisateur puisse se connecter et se déconnecter, que ses informations soient accessibles pour les afficher dans le template...

Penelope nécessitait néanmoins des champs supplémentaires (pour définir qui était enseignant/étudiant, pour leur liste de cours et de devoirs).

La solution (décrite dans la documentation de Django) était de créer un modèle `UserProfile` qui se lie en One-To-One au modèle User et permet d'étendre les champs de base. `User.objects.get(id=1).userprofile.status` renverra le status de l'utilisateur avec l'id = 1 par exemple.

Cela rajoute un modèle (donc une table dans la base) mais reste propre et nous ne modifions pas le système de base de Django.

## Les Modèles :
Dans Django les modèles ont une importance primordiale car ils permettent de créer les tables en BDD automatiquement avec les champs correspondants puis de manipuler les entrées facilement.

    # The course model.
	class Course(models.Model):
    	name = models.CharField(max_length=40)
    	description = models.CharField(max_length=100, blank=True)
    	owner = models.ForeignKey(User, related_name='course', limit_choices_to={'userprofile__status': 'teacher'})
    	editdate = models.DateTimeField(auto_now=True)
    	years = models.CharField(max_length=11, choices=YEARS_CHOICES, default='%d - %d' % (date.year, date.year + 1))
    	subscribed = models.ManyToManyField(User, related_name='course_list', blank=True, null=True, limit_choices_to={'userprofile__status': 'student'})

Le modèle ci-dessus permet à Django de créer lors du démarrage du serveur ou lors d'un `python manage.py syncdb` une table course avec les champs name, description… 

On notera le bout de code qui permet de définir le nom de l'objet (celui affiché dans l'administration, dans la liste) comme étant le nom du cours.

    def __unicode__(self):
        return self.name

**Les utilisateurs**

Les utilisateurs sont définis comme étant étudiants ou enseignants, ils sont définis d'une part par un modèle de Django et d'autre part par une extension de ce modèle : UserProfile.

**Le Cours**

Le cours dans Penelope est la base des fonctionnalités. Un nom, une description et une année lui sont associés. Ensuite vous y souscrivez les élèves qui y assistent et ils seront automatiquement associés aux devoirs contenus dans le cours.

**Le Devoir**

Le devoir correspond au traditionnel travail à rendre. vous pouvez en créer autant que vous voulez dans un cours, y associer des chargés de correction, de suivi … qui auront la possibilité de relever le travail des élèves, de modifier les groupes ou de modifier les termes du devoir. Vous avez le choix entre laisser le champs libre aux élèves et leur laisser envoyer tous les fichiers qu'ils souhaitent pour finir leur devoir, ou préciser les fichiers à rendre avec leur nom, une description, un type (tar.gz ou pdf par exemple), une taille limite.

**Le Groupe**

L'élève qui doit rendre son devoir peut avoir à faire ce dernier seul, auquel cas il appartient à un groupe dont il est le seul membre. Penelope permet également aux étudiants de faire le travail à plusieurs. Alors le travail envoyé par un des membres représentera le travail du groupe. Il est consultable, modifiable par les autres membres.

**Un fichier requis**

Lorsqu'un enseignant défini un fichier requis dans son devoir, il peut préciser le type de fichier demandé, le nom, une description.

**Un fichier**

Les fichiers correspondent au travail envoyé par les élèves. Le fichier envoyé est stocké dans le dossier Media et le modèle du fichier pointe vers lui. Ils appartiennent à un groupe et sont définis pour un seul devoir. Si c'est activé, les fichiers sont attachés à un fichier requis.

![](https://github.com/nico401/Penelope/blob/master/Rapport/Models.png?raw=true)

## Les Vues :
Les vues ont un rôle se rapprochant de celui de contrôleur dans le modèles MVC. Les fonctions récupèrent en arguments le contenu de la requête, les informations passées en GET, POST..

**Information de l'utilisateur**

Grâce au module de sessions de Django, les vues peuvent accéder aux informations de l'utilisateur qui a envoyé la requête avec : `request.user`, par exemple : `request.user.username` pour avoir le nom d'utilisateur. Cela nous permet d'effectuer des tests en fonction du contenu de `request.user.userprofile.status`.

**Traitement des informations**

La vue a pour rôle principal d'effectuer dans ses vues les modifications de la base de données, de traiter des fichiers.


**Rendu d'un template**

    return render(request, 'editassignment.html', locals())

Après les traitements il est important que la vue appelle un template (fichier .html). Le fichier settings.py contient tous les chemins vers les dossiers de templates, django cherchera automatiquement dedans le fichier avec le nom demandé. La ligne de code ci-dessus demande le fichier editassignment.html. Il l'enverra ensuite en retour avec toutes les variables que la vue a déclaré grâce à locals(). Cela permet de ne pas avoir à mentionner à la main les variables une par une, mais en contre-partie on doit faire attention à ce qui est déclaré. Voici un exemple de boucle protégeant les informations :
 
    variable_commune = id_du_cours
    if request.user.userprofile == 'teacher':
        variable_sensible = note_d_un_élève
    
    return render(request, 'untemplate.html', locals())

Dans cet exemple la note ne sera déclarée que si l'utilisateur est un enseignant, donc l'élève ne pourra pas la voir, même en analysant la requête.

_Note_ : Il est également possible de passer un dictionnaire à la place pour cibler les informations à envoyer.

Django permet aussi de rediriger l'utilisateur vers une autre vue. Utile pour revenir sur une page précédente par exemple, pour renvoyer sur une autre page si les autorisations de l'utilisateur ne sont pas suffisantes.

    return redirect('Penelope.views.home')

## Les Formulaires :
La majorité des interactions entre les utilisateurs et le serveur se font à l'aide de formulaires. Comment sont-ils définis, comment les utilise-t-on et à quel point sont-ils sécurisés ?

Django dispose d'un excellent système de formulaire que nous essayerons d'utiliser dans la majorité des cas.

**Créer un formulaire**

Lorsqu'un formulaire est attaché à un modèle afin de faire une entrée en BDD, ou d'en modifier une, Django propose de créer un formulaire et de le définir comme étant lié à ce modèle. Dans le fichier models.py :

    class CourseForm(forms.ModelForm):
        class Meta:
            model = Course

Cela créera un formulaire automatiquement avec tous les champs nécessaires pour remplir une entrée du modèle (un pour le nom, la description…). Néanmoins le cours dispose d'un champs en timestamp qui permet de mettre à jour la dernière date d'édition (inutile de demander de le remplir). Django permet de spécifier les champs à afficher dans le formulaire. Cela donnera : 

    class CourseForm(forms.ModelForm):
        class Meta:
            model = Course
            fields = ('name', 'description', 'years')

On a name, description et years comme étant les seules informations à préciser lors de la création d'un cours.

_Note_ : L'autre technique reste de faire notre formulaire dans le template en html/css/javascript.

**Passer le formulaire au template**

On a vu que l'on pouvait passer des informations au template depuis la vue, on passera ainsi le formulaire.
    
    # Formulaire vide
    form = CourseForm()

    # Formulaire avec un cours en instance (pour les modifications)
    course_instance = Course.objects.get(id=1) #Récupère le premier cours
    form = CourseForm(instance = course_instance)

Le deuxième exemple est utilisé pour faire un update sur un champs en BDD. Le formulaire est pré-rempli avec des données qui seront ensuite ré-enregistrés lors de l'envoi.

Et dans le template on peut l'appeler :
    
    # Affiche juste le champs name  
    {{ form.name }} 
    
    # Affiche tous les champs en liste avec des <p>…</p>
    {{ form.as_p }} 

**Récupérer le contenu du formulaire**
    
    # Test si le formulaire a été envoyé
    if request.method == 'POST':
        # Récupère le contenu du formulaire
        form = CourseForm(request.POST)
        # Vérifie si le contenu des champs correspond au type d'informations demandée.
        if form.is_valid():
            # Sauvegarde le formulaire comme une nouvelle entrée
            form.save()
            # Tout est bon, on redirige.
            return redirect('Avant')
        
La ligne `form = CourseForm(request.POST)` peut être remplacée par `form = CourseForm(request.POST, instance=un_cours_comme_objet)` On a une instance de précisée, cela dira à Django de faire un update de l'objet.

Si aucune instance n'est donnée, le form.save() créera un objet.

Point intéressant, le `if form.is_valid()`. Vérifie si le contenu correspond à ce qui est attendu dans le modèle. La date envoyée est-t-elle conforme ? Le nom a-t-il 30 caractères maximum ? ou encore les champs nécessaires on-t-ils bien été remplis ?

A cela s'ajoute une sécurisation des données envoyées pour pas que du code soit exécuté côté serveur.

**Sécurité avec CRSF Tokens**

Dans le template après la balise `<form>` on doit ajouter `{% csrf_token %}` si le module dans Django est activé. Cela vérifie que la requête reçue par la vue provient bien du formulaire. C'est une sécurité supplémentaire fournie par Django.


