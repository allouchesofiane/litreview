# Comptes de Test - LITReview

Ce fichier contient les informations de connexion pour tester l'application.

## Comptes Utilisateurs

### Utilisateur 1 : Alice
- **Nom d'utilisateur :** `alice`
- **Mot de passe :** `testpass123`
- **Description :** Utilisateur actif avec plusieurs tickets et critiques

### Utilisateur 2 : Bob
- **Nom d'utilisateur :** `bob`
- **Mot de passe :** `testpass123`
- **Description :** Utilisateur suivant Alice, a publié des critiques

### Utilisateur 3 : Charlie
- **Nom d'utilisateur :** `charlie`
- **Mot de passe :** `testpass123`
- **Description :** Utilisateur avec aucune d'activité

## Compte Administrateur

### Admin
- **Nom d'utilisateur :** `admin`
- **Mot de passe :** `admin123`
- **URL d'accès :** http://127.0.0.1:8000/admin/
- **Permissions :** Accès complet à l'interface d'administration Django

## Données de Test Incluses

La base de données `db.sqlite3` contient déjà :
- ✅ 4 utilisateurs (alice, bob, charlie, admin)
- ✅ Plusieurs tickets de demande de critique
- ✅ Plusieurs critiques publiées
- ✅ Relations d'abonnement entre utilisateurs

