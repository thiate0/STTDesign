# Système de Gestion de Stock

Application web de gestion de stock développée avec Python Flask.

## Fonctionnalités

✅ **Tableau de bord** avec statistiques en temps réel
✅ **Ajouter** des produits au stock
✅ **Modifier** les informations des produits
✅ **Supprimer** des produits
✅ **Rechercher** des produits par nom, description ou catégorie
✅ **Enregistrer des ventes** avec calcul automatique
✅ **Historique complet** des mouvements de stock
✅ **Statistiques des ventes** (montant total, unités vendues)
✅ **Mise à jour automatique** du stock après chaque vente
✅ **Traçabilité** (stock avant/après chaque mouvement)
✅ **Alertes** pour les produits en stock faible (< 10 unités)
✅ **Calcul automatique** de la valeur totale du stock
✅ **Interface responsive** et moderne avec Bootstrap

## Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Lancer l'application** :
```bash
python app.py
```

3. **Ouvrir votre navigateur** et aller à :
```
http://localhost:5000
```

## Utilisation

### Page d'accueil
- Vue d'ensemble avec statistiques (nombre de produits, valeur totale, produits en stock faible)
- Liste complète de tous les produits
- Recherche rapide

### Ajouter un produit
1. Cliquez sur "Ajouter un produit" dans la barre de navigation
2. Remplissez le formulaire :
   - Nom (obligatoire)
   - Description (optionnel)
   - Catégorie (optionnel)
   - Quantité (obligatoire)
   - Prix unitaire (obligatoire)
3. Cliquez sur "Ajouter le Produit"

### Modifier un produit
1. Cliquez sur l'icône crayon (✏️) à côté du produit
2. Modifiez les informations
3. Cliquez sur "Enregistrer les Modifications"

### Supprimer un produit
1. Cliquez sur l'icône poubelle (🗑️) à côté du produit
2. Confirmez la suppression

### Rechercher un produit
1. Utilisez la barre de recherche en haut de la page
2. Entrez le nom, la description ou la catégorie
3. Les résultats s'affichent automatiquement

### Enregistrer une vente
1. Cliquez sur "Vendre" dans la barre de navigation
2. Sélectionnez le produit à vendre dans la liste déroulante
3. Entrez la quantité à vendre
4. Le montant total est calculé automatiquement
5. Vérifiez le stock restant
6. Cliquez sur "Confirmer la Vente"
7. Le stock est mis à jour automatiquement

### Consulter l'historique des mouvements
1. Cliquez sur "Mouvements" dans la barre de navigation
2. Visualisez toutes les ventes effectuées
3. Consultez les statistiques (total ventes, unités vendues)
4. Vérifiez le stock avant/après chaque mouvement

## Structure du Projet

```
gestion-stock/
│
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── stock.db              # Base de données SQLite (créée automatiquement)
│
└── templates/            # Templates HTML
    ├── base.html         # Template de base
    ├── index.html        # Page d'accueil
    ├── ajouter.html      # Formulaire d'ajout
    ├── modifier.html     # Formulaire de modification
    ├── rechercher.html   # Page de recherche
    ├── vendre.html       # Formulaire de vente
    └── mouvements.html   # Historique des mouvements
```

## Base de Données

L'application utilise SQLite avec deux tables principales:

### Table `produits`
- id (PRIMARY KEY)
- nom
- description
- quantite
- prix_unitaire
- categorie
- date_ajout

### Table `mouvements`
- id (PRIMARY KEY)
- produit_id (FOREIGN KEY)
- type_mouvement (vente, etc.)
- quantite
- prix_unitaire
- montant_total
- stock_avant
- stock_apres
- date_mouvement

## Technologies Utilisées

- **Backend** : Python Flask
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3, Bootstrap 5
- **Icônes** : Bootstrap Icons

## Personnalisation

### Changer le port
Modifiez la dernière ligne de `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=VOTRE_PORT)
```

### Modifier le seuil d'alerte de stock
Cherchez `< 10` dans les fichiers templates et modifiez selon vos besoins.

### Ajouter des catégories
Modifiez les options dans `ajouter.html` et `modifier.html`.

## Améliorations Possibles

- Authentification utilisateur
- Export des données en Excel/CSV
- Graphiques et statistiques avancées
- Gestion multi-utilisateurs
- Historique des mouvements de stock
- Code-barres / QR codes
- Alertes par email pour stock faible
- Gestion des fournisseurs

## Licence

Ce projet est libre d'utilisation pour vos besoins personnels ou commerciaux.
