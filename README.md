# WoW Community Sync — V1 Checklist

## ✅ Déjà fait

### WoW Addon

* [x] Collecte des personnages
* [x] Collecte des professions
* [x] Collecte des recettes
* [x] Collecte de l'équipement
* [x] Stockage via SavedVariables

### Client Python

* [x] Détection des SavedVariables
* [x] Parsing Lua
* [x] Modèles de données
* [x] Synchronisation avec l'API
* [x] Authentification
* [x] Gestion des sessions
* [x] Login
* [x] Logout
* [x] Remember me
* [x] Fermeture propre du processus
* [x] Gestion des mauvais identifiants
* [x] Synchronisation des personnages
* [x] Historique des événements
* [x] Gestion des erreurs API

### Backend

* [x] API Node.js / Express
* [x] PostgreSQL
* [x] Authentification
* [x] Sessions
* [x] Personnages
* [x] Professions
* [x] Recettes
* [x] Équipement
* [x] Historique des événements
* [x] Synchronisation des données
* [x] Suppression des anciennes professions
* [x] 44/44 tests backend
* [x] 20/20 tests Python
* [x] CI/CD fonctionnelle

---

# 🎯 V1 — À faire

## 🖥️ Client Python

* [ ] Améliorer les messages d'erreur du login
* [ ] Ajouter un état `Loading / Syncing` plus propre
* [ ] Empêcher les doubles clics sur `Sync`
* [ ] Afficher la date de la dernière synchronisation
* [ ] Afficher une confirmation après une synchronisation réussie
* [ ] Gérer proprement l'API inaccessible
* [ ] Finaliser les détails UI

  * [ ] Espacements
  * [ ] Icônes
  * [ ] Couleurs
  * [ ] Textes
  * [ ] États des boutons

---

## 🔐 Authentification

* [ ] Forgot Password → redirection temporaire vers `http://localhost:3000`
* [ ] Préparer la future page Forgot Password
* [ ] Améliorer la gestion de l'expiration de session côté client

> 🔒 Le stockage du token dans Windows Credential Manager est volontairement reporté après la V1.

---

## 🌐 API

* [ ] Vérifier que toutes les routes nécessaires à la V1 sont présentes
* [ ] Vérifier les réponses d'erreur destinées au client
* [ ] Vérifier les principaux cas limites
* [ ] Conserver les tests backend existants comme garde-fou

---

## 🎨 Frontend Web

### Auth

* [ ] Page Login
* [ ] Page Register
* [ ] Gestion des erreurs d'authentification
* [ ] Logout

### Dashboard

* [ ] Dashboard utilisateur
* [ ] Liste des personnages
* [ ] Détail d'un personnage
* [ ] Professions
* [ ] Recettes
* [ ] Équipement
* [ ] Historique des synchronisations

---

# 🚫 V2 — Hors scope

* [ ] Discord
* [ ] Système d'amis
* [ ] Groupes communautaires
* [ ] Chat
* [ ] Notifications avancées
* [ ] Statistiques avancées
* [ ] Recherche communautaire avancée
* [ ] Marketplace
* [ ] Système de permissions avancé
* [ ] Application mobile
* [ ] Architecture distribuée / microservices

---

# 🏁 Ordre de finalisation

1. [ ] Finaliser le client Python
2. [ ] Finaliser l'API V1
3. [ ] Développer le frontend Web V1
4. [ ] Tester le parcours complet
5. [ ] Corriger les derniers bugs
6. [ ] Vérifier CI/CD
7. [ ] Préparer la release V1

---

## 🎯 Objectif V1

> Une application fonctionnelle permettant à un utilisateur de se connecter, synchroniser ses personnages WoW et consulter ses données depuis une interface web simple.

**Principe :** ne pas ajouter de grosses fonctionnalités avant la release V1.
