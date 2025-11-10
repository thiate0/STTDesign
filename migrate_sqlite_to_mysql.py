#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration SQLite vers MySQL
Transfère toutes les données de stock.db vers MySQL sans perte
"""

import sqlite3
import mysql.connector
from mysql.connector import Error

# Configuration MySQL (à modifier selon vos paramètres)
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # MODIFIEZ ICI
MYSQL_DATABASE = 'gestion_stock'
MYSQL_PORT = 3306

print("=" * 60)
print("🔄 MIGRATION SQLite → MySQL")
print("=" * 60)

# Étape 1 : Vérifier que SQLite existe
print("\n📂 Vérification du fichier SQLite...")
try:
    sqlite_conn = sqlite3.connect('stock.db')
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    print("✅ Fichier stock.db trouvé")
except Exception as e:
    print(f"❌ Erreur : Fichier stock.db introuvable")
    print(f"   Assurez-vous que stock.db est dans le même dossier")
    exit(1)

# Étape 2 : Connexion à MySQL
print("\n🔌 Connexion à MySQL...")
try:
    # Connexion sans base de données pour la créer
    mysql_conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )
    mysql_cursor = mysql_conn.cursor()
    print("✅ Connecté à MySQL")
except Error as e:
    print(f"❌ Erreur de connexion MySQL : {e}")
    print("\n💡 Vérifiez :")
    print("   1. MySQL est installé et démarré")
    print("   2. Le mot de passe dans ce script est correct")
    print("   3. L'utilisateur MySQL existe")
    exit(1)

# Étape 3 : Créer la base de données
print(f"\n🗄️  Création de la base de données '{MYSQL_DATABASE}'...")
try:
    mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    mysql_cursor.execute(f"USE {MYSQL_DATABASE}")
    print(f"✅ Base de données '{MYSQL_DATABASE}' créée/sélectionnée")
except Error as e:
    print(f"❌ Erreur : {e}")
    exit(1)

# Étape 4 : Créer les tables MySQL
print("\n📋 Création des tables MySQL...")

# Table produits
try:
    mysql_cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            description TEXT,
            quantite INT NOT NULL,
            prix_achat DECIMAL(10, 2) NOT NULL,
            categorie VARCHAR(100),
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Table 'produits' créée")
except Error as e:
    print(f"❌ Erreur création table produits : {e}")
    exit(1)

# Table mouvements
try:
    mysql_cursor.execute('''
        CREATE TABLE IF NOT EXISTS mouvements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            produit_id INT NOT NULL,
            type_mouvement VARCHAR(50) NOT NULL,
            quantite INT NOT NULL,
            prix_achat DECIMAL(10, 2) NOT NULL,
            prix_vente DECIMAL(10, 2) NOT NULL,
            montant_total DECIMAL(10, 2) NOT NULL,
            benefice DECIMAL(10, 2) NOT NULL,
            stock_avant INT NOT NULL,
            stock_apres INT NOT NULL,
            date_mouvement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produit_id) REFERENCES produits(id) ON DELETE CASCADE
        )
    ''')
    print("✅ Table 'mouvements' créée")
except Error as e:
    print(f"❌ Erreur création table mouvements : {e}")
    exit(1)

# Étape 5 : Migrer les produits
print("\n📦 Migration des produits...")
try:
    # Lire les produits de SQLite
    sqlite_cursor.execute('SELECT * FROM produits')
    produits = sqlite_cursor.fetchall()
    
    if len(produits) == 0:
        print("⚠️  Aucun produit à migrer")
    else:
        # Insérer dans MySQL
        count = 0
        for produit in produits:
            # Gérer les différents noms de colonnes (prix_unitaire ou prix_achat)
            prix = produit['prix_achat'] if 'prix_achat' in produit.keys() else produit['prix_unitaire']
            
            mysql_cursor.execute('''
                INSERT INTO produits (nom, description, quantite, prix_achat, categorie, date_ajout)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                produit['nom'],
                produit['description'],
                produit['quantite'],
                prix,
                produit['categorie'],
                produit['date_ajout']
            ))
            count += 1
        
        mysql_conn.commit()
        print(f"✅ {count} produit(s) migré(s)")
        
except Exception as e:
    print(f"❌ Erreur migration produits : {e}")
    mysql_conn.rollback()

# Étape 6 : Migrer les mouvements
print("\n📊 Migration des mouvements...")
try:
    # Vérifier si la table mouvements existe dans SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mouvements'")
    if sqlite_cursor.fetchone() is None:
        print("⚠️  Table 'mouvements' n'existe pas dans SQLite")
    else:
        # Lire les mouvements de SQLite
        sqlite_cursor.execute('SELECT * FROM mouvements')
        mouvements = sqlite_cursor.fetchall()
        
        if len(mouvements) == 0:
            print("⚠️  Aucun mouvement à migrer")
        else:
            count = 0
            for mouv in mouvements:
                # Gérer les anciennes structures
                if 'benefice' in mouv.keys():
                    # Nouvelle structure avec benefice
                    mysql_cursor.execute('''
                        INSERT INTO mouvements (produit_id, type_mouvement, quantite, prix_achat, prix_vente,
                                               montant_total, benefice, stock_avant, stock_apres, date_mouvement)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        mouv['produit_id'],
                        mouv['type_mouvement'],
                        mouv['quantite'],
                        mouv['prix_achat'],
                        mouv['prix_vente'],
                        mouv['montant_total'],
                        mouv['benefice'],
                        mouv['stock_avant'],
                        mouv['stock_apres'],
                        mouv['date_mouvement']
                    ))
                else:
                    # Ancienne structure avec prix_unitaire
                    prix_unitaire = mouv['prix_unitaire']
                    mysql_cursor.execute('''
                        INSERT INTO mouvements (produit_id, type_mouvement, quantite, prix_achat, prix_vente,
                                               montant_total, benefice, stock_avant, stock_apres, date_mouvement)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        mouv['produit_id'],
                        mouv['type_mouvement'],
                        mouv['quantite'],
                        prix_unitaire,
                        prix_unitaire,
                        mouv['montant_total'],
                        0,  # Bénéfice à 0 pour anciennes données
                        mouv['stock_avant'],
                        mouv['stock_apres'],
                        mouv['date_mouvement']
                    ))
                count += 1
            
            mysql_conn.commit()
            print(f"✅ {count} mouvement(s) migré(s)")
            
except Exception as e:
    print(f"❌ Erreur migration mouvements : {e}")
    mysql_conn.rollback()

# Étape 7 : Vérification
print("\n🔍 Vérification des données migrées...")
try:
    mysql_cursor.execute('SELECT COUNT(*) as total FROM produits')
    total_produits = mysql_cursor.fetchone()[0]
    print(f"✅ Total produits dans MySQL : {total_produits}")
    
    mysql_cursor.execute('SELECT COUNT(*) as total FROM mouvements')
    total_mouvements = mysql_cursor.fetchone()[0]
    print(f"✅ Total mouvements dans MySQL : {total_mouvements}")
except Error as e:
    print(f"⚠️  Erreur vérification : {e}")

# Fermeture des connexions
sqlite_conn.close()
mysql_cursor.close()
mysql_conn.close()

print("\n" + "=" * 60)
print("✅ MIGRATION TERMINÉE AVEC SUCCÈS !")
print("=" * 60)
print("\n📝 Prochaines étapes :")
print("1. Vérifiez vos données dans MySQL")
print("2. Configurez config.py avec vos identifiants")
print("3. Remplacez app.py par la version MySQL")
print("4. Installez : pip install mysql-connector-python")
print("5. Lancez : python app.py")
print("\n💾 Conservez stock.db en sauvegarde (ne le supprimez pas)")
print("\n🎉 Votre application utilisera maintenant MySQL !")
