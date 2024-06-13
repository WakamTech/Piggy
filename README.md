## Description détaillée du backend de l'application PIGGY

L'application PIGGY est une plateforme de commerce électronique destinée à faciliter la vente et l'achat de porcs et autres produits agricoles au Cameroun. Elle permet aux fermiers de vendre leurs produits directement aux consommateurs et aux bouchers, tout en offrant aux acheteurs un accès facile à des produits frais et de qualité. 

Ce document détaille la conception et l'implémentation du backend de l'application PIGGY en utilisant Python et Django. 

### I. Architecture du backend

L'architecture du backend est basée sur le framework Django, qui fournit une structure robuste et modulaire pour le développement d'applications web. Le backend est divisé en plusieurs couches:

* **Modèle (Model):** Cette couche définit la structure des données de l'application. Elle utilise un système de classes de modèles pour représenter les différents objets de l'application, tels que les utilisateurs, les annonces, les commandes, etc. Chaque modèle possède des attributs et des méthodes pour gérer ses données et ses relations avec d'autres modèles.

* **Vue (View):** Cette couche gère les requêtes HTTP reçues par le serveur web et génère les réponses correspondantes. Les vues sont des fonctions Python qui reçoivent une requête HTTP, traitent les données et renvoient une réponse au client. 

* **Modèle-Vue-Contrôleur (MVC):**  Le framework Django utilise un modèle MVC pour organiser le code et améliorer sa maintenabilité. Les vues sont responsables de l'interaction avec l'utilisateur, les modèles définissent les données et les contrôleurs agissent comme un intermédiaire pour gérer les actions de l'utilisateur et les données. 

### II. Implémentation des endpoints

Le backend de PIGGY expose une API RESTful pour permettre aux clients (applications mobiles, sites web) d'interagir avec ses fonctionnalités. Chaque endpoint correspond à une action spécifique sur les données de l'application. Voici une description détaillée des endpoints:

#### 1. Authentification

* **Inscription:** Permet aux nouveaux utilisateurs de s'inscrire à la plateforme en créant un compte. 
   * **Endpoint:** `/auth/register`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `phone`: Le numéro de téléphone de l'utilisateur (obligatoire).
      * `password`: Le mot de passe de l'utilisateur (obligatoire).
      * `role`: Le rôle de l'utilisateur (facultatif, valeurs possibles: `fermier`, `acheteur`, `boucherie`).
   * **Fonctionnement:** 
      * Le backend vérifie si le numéro de téléphone est déjà utilisé. Si oui, il renvoie une erreur.
      * Sinon, il crypte le mot de passe et enregistre un nouvel utilisateur dans la base de données avec le rôle spécifié. 

* **Connexion:** Permet aux utilisateurs de se connecter à leur compte en utilisant leur numéro de téléphone et leur mot de passe.
   * **Endpoint:** `/auth/login`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `phone`: Le numéro de téléphone de l'utilisateur (obligatoire).
      * `password`: Le mot de passe de l'utilisateur (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie si l'utilisateur existe. Si oui, il compare le mot de passe fourni avec le mot de passe haché stocké dans la base de données.
      * Si les informations d'identification sont correctes, il génère un jeton d'authentification JWT (JSON Web Token) et le renvoie au client. Le jeton contient des informations sur l'utilisateur et expire après un certain temps. 

* **Déconnexion:** Permet aux utilisateurs de se déconnecter de leur compte.
   * **Endpoint:** `/auth/logout`
   * **Méthode:** `POST`
   * **Paramètres:** 
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend invalide le jeton d'authentification en le supprimant de la liste des jetons valides. Cela empêche l'utilisateur de se reconnecter avec le même jeton.

#### 2. Gestion des utilisateurs

* **Obtenir le profil d'un utilisateur:** Permet à un utilisateur d'obtenir les informations de son profil.
   * **Endpoint:** `/users/{id}`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les informations de l'utilisateur correspondant à l'ID fourni et les renvoie au client.

* **Modifier le profil d'un utilisateur:** Permet à un utilisateur de modifier les informations de son profil.
   * **Endpoint:** `/users/{id}`
   * **Méthode:** `PUT`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `name`: Le nouveau nom de l'utilisateur (facultatif).
      * `email`: Le nouvel email de l'utilisateur (facultatif).
      * `address`: La nouvelle adresse de l'utilisateur (facultatif).
      * `notifications`: Activer/désactiver les notifications (facultatif, valeurs possibles: `true`, `false`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il met à jour les informations de l'utilisateur en utilisant les données fournies dans le corps de la requête.

* **Supprimer le profil d'un utilisateur:** Permet à un utilisateur de supprimer son compte.
   * **Endpoint:** `/users/{id}`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il supprime le compte de l'utilisateur correspondant à l'ID fourni.

#### 3. Gestion des annonces

* **Créer une annonce:** Permet aux utilisateurs de publier une nouvelle annonce pour vendre leurs produits. 
   * **Endpoint:** `/ads`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `title`: Le titre de l'annonce (obligatoire).
      * `city`: La ville où se trouve le produit (obligatoire).
      * `quantity`: La quantité du produit (obligatoire).
      * `price_per_kg`: Le prix par kilo (obligatoire).
      * `weight_avg`: Le poids moyen du produit (obligatoire).
      * `race`: La race du produit (facultatif).
      * `description`: Une description du produit (facultatif).
      * `images`: Un tableau d'URL d'images (facultatif, maximum 5 images).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il enregistre la nouvelle annonce dans la base de données avec les informations fournies.

* **Obtenir une annonce:** Permet à un utilisateur de récupérer les détails d'une annonce en fonction de son ID.
   * **Endpoint:** `/ads/{id}`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les détails de l'annonce correspondant à l'ID fourni et les renvoie au client.

* **Modifier une annonce:** Permet à un utilisateur de modifier les informations de ses annonces.
   * **Endpoint:** `/ads/{id}`
   * **Méthode:** `PUT`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `title`: Le nouveau titre de l'annonce (facultatif).
      * `city`: La nouvelle ville de l'annonce (facultatif).
      * `quantity`: La nouvelle quantité (facultatif).
      * `price_per_kg`: Le nouveau prix par kilo (facultatif).
      * `weight_avg`: Le nouveau poids moyen (facultatif).
      * `race`: La nouvelle race (facultatif).
      * `description`: La nouvelle description (facultatif).
      * `images`: Un tableau d'URL d'images (facultatif, maximum 5 images).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il met à jour les informations de l'annonce en utilisant les données fournies dans le corps de la requête.

* **Supprimer une annonce:** Permet à un utilisateur de supprimer ses annonces.
   * **Endpoint:** `/ads/{id}`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il supprime l'annonce correspondant à l'ID fourni.

* **Obtenir les annonces en fonction de la localisation:** Permet aux utilisateurs de filtrer les annonces en fonction de leur position géographique.
   * **Endpoint:** `/ads/location`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `city`: La ville (facultatif).
      * `latitude`: La latitude (facultatif).
      * `longitude`: La longitude (facultatif).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les annonces en utilisant les paramètres de recherche et les renvoie au client.

* **Obtenir les annonces en fonction des critères de recherche:** Permet aux utilisateurs de filtrer les annonces en fonction de différents critères tels que le prix, le poids, la race, etc.
   * **Endpoint:** `/ads/search`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `q`: Le mot-clé de la recherche (facultatif).
      * `city`: La ville (facultatif).
      * `price_min`: Le prix minimum (facultatif).
      * `price_max`: Le prix maximum (facultatif).
      * `weight_min`: Le poids minimum (facultatif).
      * `weight_max`: Le poids maximum (facultatif).
      * `race`: La race du produit (facultatif).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les annonces qui correspondent aux critères de recherche et les renvoie au client.

#### 4. Gestion des commandes

* **Créer une commande:** Permet aux utilisateurs de passer une commande pour acheter un produit.
   * **Endpoint:** `/orders`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `ad_id`: L'identifiant de l'annonce (obligatoire).
      * `quantity`: La quantité du produit à commander (obligatoire).
      * `address`: L'adresse de livraison (obligatoire).
      * `payment_method`: La méthode de paiement (obligatoire, valeurs possibles: `cash`, `mobile_money`, `wave`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il enregistre la nouvelle commande dans la base de données avec les informations fournies.

* **Obtenir une commande:** Permet à un utilisateur de récupérer les détails d'une commande en fonction de son ID.
   * **Endpoint:** `/orders/{id}`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les détails de la commande correspondant à l'ID fourni et les renvoie au client.

* **Modifier une commande:** Permet aux utilisateurs de modifier le statut de leurs commandes.
   * **Endpoint:** `/orders/{id}`
   * **Méthode:** `PUT`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `status`: Le nouveau statut de la commande (facultatif, valeurs possibles: `pending`, `accepted`, `rejected`, `delivered`, `cancelled`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il met à jour le statut de la commande en utilisant les données fournies dans le corps de la requête.

* **Supprimer une commande:** Permet aux utilisateurs de supprimer leurs commandes.
   * **Endpoint:** `/orders/{id}`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il supprime la commande correspondant à l'ID fourni.

* **Obtenir les commandes d'un utilisateur:** Permet aux utilisateurs de consulter la liste de leurs commandes.
   * **Endpoint:** `/orders/user`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère la liste des commandes associées à l'utilisateur et les renvoie au client.

* **Obtenir les commandes d'une annonce:** Permet aux utilisateurs de consulter la liste des commandes associées à une annonce.
   * **Endpoint:** `/orders/ad/{id}`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère la liste des commandes associées à l'annonce et les renvoie au client.

#### 5. Gestion des notifications

* **Envoyer une notification à un utilisateur:** Permet au backend de l'application d'envoyer des notifications push aux utilisateurs.
   * **Endpoint:** `/notifications`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `user_id`: L'identifiant de l'utilisateur (obligatoire).
      * `title`: Le titre de la notification (obligatoire).
      * `message`: Le message de la notification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il envoie la notification à l'utilisateur en utilisant un service de notification push (ex: Firebase Cloud Messaging, OneSignal, etc.).

#### 6. Gestion de l'administration

* **Obtenir la liste des utilisateurs (administrateur):** Permet à l'administrateur de consulter la liste des utilisateurs enregistrés.
   * **Endpoint:** `/admin/users`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `role`: Le rôle de l'utilisateur (facultatif, valeurs possibles: `fermier`, `acheteur`, `boucherie`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il récupère la liste des utilisateurs et les renvoie au client.

* **Modifier le profil d'un utilisateur (administrateur):** Permet à l'administrateur de modifier le profil d'un utilisateur, y compris son rôle.
   * **Endpoint:** `/admin/users/{id}`
   * **Méthode:** `PUT`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `role`: Le nouveau rôle de l'utilisateur (facultatif, valeurs possibles: `fermier`, `acheteur`, `boucherie`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il met à jour les informations de l'utilisateur en utilisant les données fournies dans le corps de la requête.

* **Supprimer le profil d'un utilisateur (administrateur):** Permet à l'administrateur de supprimer un compte utilisateur.
   * **Endpoint:** `/admin/users/{id}`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il supprime le compte de l'utilisateur correspondant à l'ID fourni.

* **Obtenir la liste des annonces (administrateur):** Permet à l'administrateur de consulter la liste des annonces publiées.
   * **Endpoint:** `/admin/ads`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `status`: Le statut de l'annonce (facultatif, valeurs possibles: `active`, `inactive`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il récupère la liste des annonces et les renvoie au client.

* **Valider une annonce (administrateur):** Permet à l'administrateur de valider une annonce et de la rendre visible aux acheteurs.
   * **Endpoint:** `/admin/ads/{id}/validate`
   * **Méthode:** `PUT`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il met à jour le statut de l'annonce à `active`.

* **Supprimer une annonce (administrateur):** Permet à l'administrateur de supprimer une annonce.
   * **Endpoint:** `/admin/ads/{id}`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il supprime l'annonce correspondant à l'ID fourni.

* **Obtenir la liste des commandes (administrateur):** Permet à l'administrateur de consulter la liste des commandes passées.
   * **Endpoint:** `/admin/orders`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `status`: Le statut de la commande (facultatif, valeurs possibles: `pending`, `accepted`, `rejected`, `delivered`, `cancelled`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il récupère la liste des commandes et les renvoie au client.

* **Modifier le statut d'une commande (administrateur):** Permet à l'administrateur de modifier le statut d'une commande (ex: accepter, refuser, marquer comme livrée, annuler).
   * **Endpoint:** `/admin/orders/{id}`
   * **Méthode:** `PUT`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `status`: Le nouveau statut de la commande (obligatoire, valeurs possibles: `pending`, `accepted`, `rejected`, `delivered`, `cancelled`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il met à jour le statut de la commande en utilisant les données fournies dans le corps de la requête.

* **Supprimer une commande (administrateur):** Permet à l'administrateur de supprimer une commande.
   * **Endpoint:** `/admin/orders/{id}`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il supprime la commande correspondant à l'ID fourni.

* **Obtenir les statistiques (administrateur):** Permet à l'administrateur de consulter les statistiques de l'application (ex: nombre d'utilisateurs, nombre d'annonces, nombre de commandes, revenus).
   * **Endpoint:** `/admin/stats`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification et si l'utilisateur est administrateur.
      * Il récupère les statistiques de l'application et les renvoie au client.

#### 7. Autres endpoints

* **Obtenir la liste des boucheries:** Permet aux utilisateurs de consulter la liste des boucheries enregistrées sur la plateforme.
   * **Endpoint:** `/butchers`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `city`: La ville (facultatif).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère la liste des boucheries et les renvoie au client.

* **Obtenir les conditions générales d'utilisation:** Permet aux utilisateurs de consulter les conditions générales d'utilisation de la plateforme.
   * **Endpoint:** `/terms`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère le contenu des conditions générales d'utilisation et les renvoie au client.

* **Obtenir les contacts du service client:** Permet aux utilisateurs de trouver les coordonnées du service client pour obtenir de l'aide.
   * **Endpoint:** `/support`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les coordonnées du service client et les renvoie au client.

* **Envoyer un message au service client:** Permet aux utilisateurs de contacter le service client pour signaler un problème ou poser une question.
   * **Endpoint:** `/support/message`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `subject`: Le sujet du message (obligatoire).
      * `message`: Le contenu du message (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il enregistre le message dans la base de données et envoie une notification au service client.

* **Obtenir les avis des clients pour une annonce:** Permet aux utilisateurs de consulter les avis des clients pour une annonce spécifique.
   * **Endpoint:** `/ads/{id}/reviews`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les avis des clients pour l'annonce et les renvoie au client.

* **Poster un avis pour une annonce:** Permet aux utilisateurs de laisser un avis et une note pour une annonce.
   * **Endpoint:** `/ads/{id}/reviews`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `rating`: La note de l'avis (obligatoire, valeur entre 1 et 5).
      * `comment`: Le commentaire de l'avis (facultatif).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il enregistre l'avis dans la base de données.

* **Obtenir le panier de l'utilisateur:** Permet aux utilisateurs de consulter les articles qu'ils ont ajoutés à leur panier.
   * **Endpoint:** `/cart`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère les articles du panier de l'utilisateur et les renvoie au client.

* **Ajouter un article au panier:** Permet aux utilisateurs d'ajouter un article à leur panier.
   * **Endpoint:** `/cart/add`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `ad_id`: L'identifiant de l'annonce (obligatoire).
      * `quantity`: La quantité (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il ajoute l'article au panier de l'utilisateur.

* **Supprimer un article du panier:** Permet aux utilisateurs de supprimer un article de leur panier.
   * **Endpoint:** `/cart/remove`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Corps de la requête:**
      * `ad_id`: L'identifiant de l'annonce (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il supprime l'article du panier de l'utilisateur.

* **Vider le panier:** Permet aux utilisateurs de vider complètement leur panier.
   * **Endpoint:** `/cart/clear`
   * **Méthode:** `DELETE`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il supprime tous les articles du panier de l'utilisateur.

* **Obtenir le total du panier:** Permet aux utilisateurs de consulter le total de leur panier, y compris les frais de livraison.
   * **Endpoint:** `/cart/total`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il calcule le total du panier, y compris les frais de livraison, et le renvoie au client.

* **Commander les articles du panier:** Permet aux utilisateurs de passer une commande en utilisant les articles de leur panier.
   * **Endpoint:** `/orders/cart`
   * **Méthode:** `POST`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
      * `address`: L'adresse de livraison (obligatoire).
      * `payment_method`: La méthode de paiement (obligatoire, valeurs possibles: `cash`, `mobile_money`, `wave`).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il crée une nouvelle commande en utilisant les articles du panier de l'utilisateur et les informations de livraison et de paiement fournies.

* **Obtenir les annonces publiées par un utilisateur:** Permet aux utilisateurs de consulter la liste des annonces qu'ils ont publiées.
   * **Endpoint:** `/users/{id}/ads`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère la liste des annonces publiées par l'utilisateur et les renvoie au client.

* **Obtenir les commandes liées à une annonce:** Permet aux utilisateurs de consulter la liste des commandes associées à une annonce spécifique.
   * **Endpoint:** `/ads/{id}/orders`
   * **Méthode:** `GET`
   * **Paramètres:**
      * `token`: Le jeton d'authentification (obligatoire).
   * **Fonctionnement:**
      * Le backend vérifie la validité du jeton d'authentification.
      * Il récupère la liste des commandes associées à l'annonce et les renvoie au client.

### III. Sécurité

L'application PIGGY utilise des mécanismes de sécurité pour protéger les données des utilisateurs et garantir un environnement sécurisé. Voici les mesures de sécurité mises en place:

* **Authentification JWT:** L'application utilise des jetons JWT pour authentifier les utilisateurs et les autoriser à accéder aux ressources protégées. 
* **Cryptage des mots de passe:** Les mots de passe des utilisateurs sont cryptés en utilisant un algorithme de hachage sûr, comme bcrypt.
* **Sécurisation des données:** Les données sensibles, telles que les informations personnelles et les informations de paiement, sont stockées dans la base de données de manière sécurisée.
* **Contrôle d'accès:** Le backend met en place des contrôles d'accès pour limiter l'accès aux ressources en fonction du rôle de l'utilisateur (administrateur, fermier, acheteur, boucher).
* **Gestion des erreurs:** Le backend gère les erreurs et les exceptions pour éviter les failles de sécurité et les attaques.
* **Tests de sécurité:** L'application est soumise à des tests de sécurité réguliers pour identifier et corriger les vulnérabilités potentielles.

### IV. Tests

La qualité du code est assurée par une suite de tests automatisés qui couvrent les différentes fonctionnalités du backend. Ces tests sont divisés en différents types:

* **Tests unitaires:** Ces tests vérifient le bon fonctionnement des fonctions et des méthodes individuelles.
* **Tests d'intégration:** Ces tests vérifient l'interaction entre les différentes composantes du backend.
* **Tests fonctionnels:** Ces tests vérifient le bon fonctionnement du backend dans son ensemble.

La couverture des tests est un indicateur important de la qualité du code. Un taux de couverture des tests élevé permet de s'assurer que le code fonctionne correctement et est conforme aux exigences.

### V. Défis et solutions

L'implémentation du backend de PIGGY a été confrontée à plusieurs défis, notamment:

* **Gestion de la localisation:** La plateforme doit prendre en compte la localisation des utilisateurs et des produits pour faciliter la recherche et la livraison.
* **Sécurité des paiements:** Le backend doit gérer les paiements en ligne de manière sécurisée et fiable.
* **Gestion des stocks:** Le backend doit gérer les stocks des produits disponibles et les mettre à jour en temps réel.
* **Performance:** Le backend doit être capable de gérer un grand nombre d'utilisateurs et de requêtes simultanées.

Pour relever ces défis, les solutions suivantes ont été mises en place:

* **Utilisation de la géolocalisation:** L'application utilise des API de géolocalisation pour déterminer la position des utilisateurs et des produits, et pour filtrer les annonces en fonction de la localisation.
* **Intégration d'une passerelle de paiement:** Le backend utilise une passerelle de paiement sécurisée pour traiter les paiements en ligne.
* **Système de gestion des stocks:** Le backend utilise un système de gestion des stocks pour suivre les produits disponibles et les mettre à jour en temps réel.
* **Optimisation des performances:** Le backend est optimisé pour gérer un grand nombre d'utilisateurs et de requêtes simultanées, en utilisant des techniques de mise en cache, de compression des données et d'optimisation des requêtes SQL.

### VI. Conclusion

Le backend de l'application PIGGY est un système complexe et performant qui permet de gérer les différentes fonctionnalités de la plateforme. Il utilise le framework Django pour fournir une structure robuste et modulaire, et expose une API RESTful pour permettre aux clients d'interagir avec les données. L'application est également sécurisée et protégée contre les failles de sécurité grâce à des mesures de sécurité strictes et à des tests automatisés.

La plateforme PIGGY a le potentiel de révolutionner le marché des produits agricoles en Côte d'ivoire en facilitant les échanges entre les fermiers, les bouchers et les consommateurs. 
