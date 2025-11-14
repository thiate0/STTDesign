#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'importation des données vers PythonAnywhere
À exécuter DEPUIS PythonAnywhere (console Bash)
"""

import mysql.connector
import json
import sys
from datetime import datetime

# ============================================
# CONFIGURATION - MODIFIEZ VOS IDENTIFIANTS PYTHONANYWHERE
# ============================================
PYTHONANYWHERE_MYSQL_HOST = 'STTDesign.mysql.pythonanywhere-services.com'  # ⚠️ CHANGEZ
PYTHONANYWHERE_MYSQL_USER = 'STTDesign'  # ⚠️ CHANGEZ
PYTHONANYWHERE_MYSQL_PASSWORD = 'stt_dbtm@4'  # ⚠️ CHANGEZ
PYTHONANYWHERE_MYSQL_DATABASE = 'STTDesign$gestion_stock'  # ⚠️ CHANGEZ
PYTHONANYWHERE_MYSQL_PORT = 3306

print("=" * 60)
print("📥 IMPORTATION DES DONNÉES VERS PYTHONANYWHERE")
print("=" * 60)

# Demander le nom du fichier
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input("\n📁 Nom du fichier JSON (ex: export_donnees_20250115.json) : ")

try:
    # Charger le fichier JSON
    print(f"\n📂 Lecture du fichier '{filename}'...")
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    produits = data['produits']
    mouvements = data['mouvements']
    
    print(f"✅ Fichier chargé")
    print(f"   • {len(produits)} produit(s)")
    print(f"   • {len(mouvements)} mouvement(s)")
    
    # Connexion à MySQL PythonAnywhere
    print("\n🔌 Connexion à MySQL PythonAnywhere...")
    conn = mysql.connector.connect(
        host=PYTHONANYWHERE_MYSQL_HOST,
        user=PYTHONANYWHERE_MYSQL_USER,
        password=PYTHONANYWHERE_MYSQL_PASSWORD,
        database=PYTHONANYWHERE_MYSQL_DATABASE,
        port=PYTHONANYWHERE_MYSQL_PORT
    )
    cursor = conn.cursor()
    print("✅ Connecté à MySQL PythonAnywhere")
    
    # Vérifier si des données existent déjà
    cursor.execute("SELECT COUNT(*) FROM produits")
    count_produits = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM mouvements")
    count_mouvements = cursor.fetchone()[0]
    
    if count_produits > 0 or count_mouvements > 0:
        print(f"\n⚠️  ATTENTION : Des données existent déjà !")
        print(f"   • {count_produits} produit(s)")
        print(f"   • {count_mouvements} mouvement(s)")
        
        reponse = input("\nVoulez-vous supprimer les données existantes ? (oui/non) : ")
        if reponse.lower() in ['oui', 'o', 'yes', 'y']:
            print("\n🗑️  Suppression des données existantes...")
            cursor.execute("DELETE FROM mouvements")
            cursor.execute("DELETE FROM produits")
            conn.commit()
            print("✅ Données existantes supprimées")
        else:
            print("\n❌ Importation annulée")
            cursor.close()
            conn.close()
            sys.exit(0)
    
    # Importer les produits
    print("\n📦 Importation des produits...")
    for produit in produits:
        cursor.execute('''
            INSERT INTO produits (id, nom, description, quantite, prix_achat, categorie, date_ajout)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            produit['id'],
            produit['nom'],
            produit['description'],
            produit['quantite'],
            produit['prix_achat'],
            produit.get('categorie'),
            produit.get('date_ajout')
        ))
    
    conn.commit()
    print(f"✅ {len(produits)} produit(s) importé(s)")
    
    # Importer les mouvements
    if mouvements:
        print("\n📊 Importation des mouvements...")
        for mouvement in mouvements:
            cursor.execute('''
                INSERT INTO mouvements (id, produit_id, type_mouvement, quantite, prix_achat, prix_vente,
                                       montant_total, benefice, stock_avant, stock_apres, date_mouvement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                mouvement['id'],
                mouvement['produit_id'],
                mouvement['type_mouvement'],
                mouvement['quantite'],
                mouvement['prix_achat'],
                mouvement['prix_vente'],
                mouvement['montant_total'],
                mouvement['benefice'],
                mouvement['stock_avant'],
                mouvement['stock_apres'],
                mouvement.get('date_mouvement')
            ))
        
        conn.commit()
        print(f"✅ {len(mouvements)} mouvement(s) importé(s)")
    
    # Vérification
    print("\n🔍 Vérification finale...")
    cursor.execute("SELECT COUNT(*) FROM produits")
    total_produits = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM mouvements")
    total_mouvements = cursor.fetchone()[0]
    
    print(f"✅ Données vérifiées")
    print(f"   • {total_produits} produit(s) dans la base")
    print(f"   • {total_mouvements} mouvement(s) dans la base")
    
    # Fermeture
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ IMPORTATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print("\n🎉 Vos données sont maintenant en ligne !")
    print("\n📝 Prochaines étapes :")
    print("   1. Rechargez votre application web sur PythonAnywhere")
    print("   2. Vérifiez vos données sur votre site")
    
except FileNotFoundError:
    print(f"\n❌ Erreur : Le fichier '{filename}' n'a pas été trouvé")
    print("\n💡 Assurez-vous d'avoir uploadé le fichier dans le bon dossier")
except mysql.connector.Error as e:
    print(f"\n❌ Erreur MySQL : {e}")
    print("\n💡 Vérifiez :")
    print("   1. Les identifiants dans ce script sont corrects")
    print("   2. La base de données existe sur PythonAnywhere")
    print("   3. Les tables sont créées (lancez app.py une fois)")
except KeyError as e:
    print(f"\n❌ Erreur : Clé manquante dans le fichier JSON : {e}")
    print("\n💡 Le fichier JSON est peut-être corrompu ou incomplet")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
