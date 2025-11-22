# LITReview - Application de Critiques Littéraires

Application web Django permettant de demander et publier des critiques de livres et articles.

##  Fonctionnalités

- ✅ Inscription et authentification utilisateurs
- ✅ Création de tickets (demandes de critiques)
- ✅ Publication de critiques (en réponse ou autonome)
- ✅ Flux personnalisé des utilisateurs suivis
- ✅ Système de suivi d'utilisateurs
- ✅ CRUD complet sur ses propres posts

##  Technologies

- **Framework** : Django 
- **Base de données** : SQLite3
- **Frontend** : HTML, CSS , Bootstrap
- **Python** : 3.13.3

##  Installation

### Prérequis
- Python 3.13 ou supérieur
- Git

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/sofianeallouche/litreview.git
cd litreview
```

2. **Créer et activer l'environnement virtuel**
```bash
# Windows
python -m venv env
env\Scripts\activate

# Mac/Linux
python3 -m venv env
source env/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**
```bash
python manage.py makemigrations 
python manage.py migrate
```

5. **Créer un superutilisateur (optionnel)**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
Ouvrez votre navigateur : `http://127.0.0.1:8000/`

## Structure du Projet
```
litreview/
├── litreview_project/     # Configuration Django
│   ├── settings.py        # Paramètres
│   ├── urls.py            # URLs 
│   └── wsgi.py
├── reviews/               # Application principale
│   ├── models.py          # Modèles (User, Ticket, Review, UserFollows)
│   ├── views.py           # Vues
│   ├── forms.py           # Formulaires
│   └── templates/         # Templates HTML
├── media/                 # Fichiers uploadés par utilisateurs
├── db.sqlite3             # Base de données
├── manage.py              # Script de gestion Django
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

##  Modèles de Données

### Ticket
- `title` : Titre du ticket
- `description` : Description
- `user` : Créateur
- `image` : Image (optionnelle)
- `time_created` : Date de création

### Review
- `ticket` : Ticket associé
- `rating` : Note (0-5)
- `headline` : Titre de la critique
- `body` : Contenu
- `user` : Auteur
- `time_created` : Date de création

### UserFollows
- `user` : Utilisateur qui suit
- `followed_user` : Utilisateur suivi
- Contrainte : `unique_together` pour éviter les doublons

## 🧪 Tests
```bash
# Lancer tous les tests
python manage.py test

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
```

## 📋 Conformité

- ✅ **PEP8** : Code conforme aux standards Python
- ✅ **WCAG 2.1** : Accessibilité niveau AA
- ✅ **Django Best Practices** : Structure et sécurité

## 📄 Licence

Ce projet est développé dans le cadre de la formation OpenClassrooms.

## 👨‍💻 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- Email: votre.email@example.com

## 🙏 Remerciements

- OpenClassrooms pour le cahier des charges
- La communauté Django

