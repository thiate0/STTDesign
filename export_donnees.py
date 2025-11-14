#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'exportation des données MySQL locales
Exporte toutes les données des tables produits et mouvements
"""

import mysql.connector
import json
from datetime import datetime

# ============================================
# CONFIGURATION - MODIFIEZ VOS IDENTIFIANTS LOCAUX
# ============================================
LOCAL_MYSQL_HOST = 'localhost'
LOCAL_MYSQL_USER = 'root'
LOCAL_MYSQL_PASSWORD = ''  # ⚠️ CHANGEZ ICI
LOCAL_MYSQL_DATABASE = 'gestion_stock'
LOCAL_MYSQL_PORT = 3306

print("=" * 60)
print("📤 EXPORTATION DES DONNÉES MYSQL LOCALES")
print("=" * 60)

try:
    # Connexion à MySQL local
    print("\n🔌 Connexion à MySQL local...")
    conn = mysql.connector.connect(
        host=LOCAL_MYSQL_HOST,
        user=LOCAL_MYSQL_USER,
        password=LOCAL_MYSQL_PASSWORD,
        database=LOCAL_MYSQL_DATABASE,
        port=LOCAL_MYSQL_PORT
    )
    cursor = conn.cursor(dictionary=True)
    print("✅ Connecté à MySQL local")
    
    # Export des produits
    print("\n📦 Exportation des produits...")
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    
    # Convertir les dates en chaînes
    for produit in produits:
        if 'date_ajout' in produit and produit['date_ajout']:
            produit['date_ajout'] = produit['date_ajout'].strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"✅ {len(produits)} produit(s) exporté(s)")
    
    # Export des mouvements
    print("\n📊 Exportation des mouvements...")
    cursor.execute("SELECT * FROM mouvements")
    mouvements = cursor.fetchall()
    
    # Convertir les dates en chaînes
    for mouvement in mouvements:
        if 'date_mouvement' in mouvement and mouvement['date_mouvement']:
            mouvement['date_mouvement'] = mouvement['date_mouvement'].strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"✅ {len(mouvements)} mouvement(s) exporté(s)")
    
    # Sauvegarder dans un fichier JSON
    data = {
        'produits': produits,
        'mouvements': mouvements,
        'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    filename = f'export_donnees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n💾 Données sauvegardées dans : {filename}")
    
    # Fermeture
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ EXPORTATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print(f"\n📋 Résumé :")
    print(f"   • Produits exportés : {len(produits)}")
    print(f"   • Mouvements exportés : {len(mouvements)}")
    print(f"   • Fichier créé : {filename}")
    print("\n📝 Prochaine étape :")
    print(f"   1. Uploadez '{filename}' sur PythonAnywhere")
    print("   2. Lancez le script 'import_donnees.py' sur PythonAnywhere")
    
except mysql.connector.Error as e:
    print(f"\n❌ Erreur MySQL : {e}")
    print("\n💡 Vérifiez :")
    print("   1. MySQL est démarré")
    print("   2. Les identifiants dans ce script sont corrects")
    print("   3. La base de données 'gestion_stock' existe")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
