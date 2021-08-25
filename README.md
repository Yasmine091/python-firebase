# Firebase

Avoir un compte Firebase : 
- https://console.firebase.google.com/u/0/

Créer un utilisateur pour se connecter par email/mot de passe :
- Développer > Authentication > Sign-in method : activer adresse email/mot de passe
- Développer > Authentication > Users : créer un utilisateur

Créer une application Firebase :
- Vue d'ensemble > Ajouter une application > Web
- Récupérer le contenu de la variable "firebaseConfig" pour la suite

Créer une base de données Firebase :
- Développer > Database


# Installation de l'ensemble des paquets

```
sudo pip3 install -r requirements.txt

django-admin startproject djangofirebase
cd djangofirebase
python3 manage.py migrate
python3 manage.py runserver
```

# Ressources

- https://www.hackanons.com/2018/03/python-django-with-google-firebase.html
- https://github.com/thisbejim/Pyrebase


# Site de démo

- https://pyrebase.herokuapp.com

# Compte d'essai

```
d.john@gmail.com:JohnDoe123456
```