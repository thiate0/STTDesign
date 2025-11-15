#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'exportation COMPLÈTE des données MySQL locales
Exporte TOUS les produits et TOUS les mouvements (même orphelins)
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
print("📤 EXPORTATION COMPLÈTE DES DONNÉES MYSQL LOCALES")
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
    
    # ==========================================
    # Export des produits
    # ==========================================
    print("\n📦 Exportation des produits...")
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    
    # Convertir les dates et Decimal en chaînes
    for produit in produits:
        if 'date_ajout' in produit and produit['date_ajout']:
            produit['date_ajout'] = produit['date_ajout'].strftime('%Y-%m-%d %H:%M:%S')
        # Convertir les prix
        if 'prix_achat' in produit and produit['prix_achat'] is not None:
            produit['prix_achat'] = float(produit['prix_achat'])
        if 'prix_unitaire' in produit and produit['prix_unitaire'] is not None:
            produit['prix_unitaire'] = float(produit['prix_unitaire'])
    
    produit_ids = {p['id'] for p in produits}
    print(f"✅ {len(produits)} produit(s) exporté(s)")
    print(f"   IDs des produits : {sorted(produit_ids)}")
    
    # ==========================================
    # Export de TOUS les mouvements
    # ==========================================
    print("\n📊 Exportation de TOUS les mouvements...")
    cursor.execute("SELECT * FROM mouvements")
    mouvements = cursor.fetchall()
    
    print(f"✅ {len(mouvements)} mouvement(s) trouvé(s) dans la base")
    
    # Analyser les mouvements
    mouvements_ok = []
    mouvements_orphelins = []
    
    for mouvement in mouvements:
        # Convertir les dates
        if 'date_mouvement' in mouvement and mouvement['date_mouvement']:
            mouvement['date_mouvement'] = mouvement['date_mouvement'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Convertir les Decimal en float
        for key in ['prix_achat', 'prix_vente', 'prix_unitaire', 'montant_total', 'benefice']:
            if key in mouvement and mouvement[key] is not None:
                mouvement[key] = float(mouvement[key])
        
        # Vérifier si le produit existe
        if mouvement['produit_id'] in produit_ids:
            mouvements_ok.append(mouvement)
        else:
            mouvements_orphelins.append(mouvement)
            print(f"   ⚠️  Mouvement ID {mouvement['id']} → produit_id {mouvement['produit_id']} (produit n'existe plus)")
    
    print(f"\n📊 Analyse des mouvements :")
    print(f"   ✅ {len(mouvements_ok)} mouvement(s) avec produits existants")
    print(f"   ⚠️  {len(mouvements_orphelins)} mouvement(s) orphelin(s) (produit supprimé)")
    
    # ==========================================
    # Demander quoi faire avec les orphelins
    # ==========================================
    if mouvements_orphelins:
        print("\n" + "=" * 60)
        print("⚠️  MOUVEMENTS ORPHELINS DÉTECTÉS")
        print("=" * 60)
        
        print("\nCes mouvements référencent des produits qui n'existent plus.")
        print("Vous avez 3 options :\n")
        print("1. Exporter SEULEMENT les mouvements avec produits existants")
        print("2. Exporter TOUS les mouvements (y compris orphelins)")
        print("3. Créer des produits fictifs pour les orphelins et tout exporter")
        
        choix = input("\nVotre choix (1/2/3) : ")
        
        if choix == "1":
            # Exporter seulement les mouvements OK
            mouvements_a_exporter = mouvements_ok
            print(f"\n✅ Export de {len(mouvements_a_exporter)} mouvements (orphelins exclus)")
            
        elif choix == "2":
            # Exporter tous les mouvements
            mouvements_a_exporter = mouvements
            print(f"\n✅ Export de {len(mouvements_a_exporter)} mouvements (tous, avec orphelins)")
            print("⚠️  Note : Les orphelins seront ignorés lors de l'import sur PythonAnywhere")
            
        elif choix == "3":
            # Créer des produits fictifs pour les orphelins
            produits_fictifs_ids = {m['produit_id'] for m in mouvements_orphelins}
            
            print(f"\n🔧 Création de {len(produits_fictifs_ids)} produit(s) fictif(s)...")
            
            for produit_id in produits_fictifs_ids:
                # Trouver un mouvement avec ce produit_id pour récupérer le prix
                mouv_exemple = next(m for m in mouvements_orphelins if m['produit_id'] == produit_id)
                prix_achat = mouv_exemple.get('prix_achat', 0)
                
                produit_fictif = {
                    'id': produit_id,
                    'nom': f'Produit supprimé (ID {produit_id})',
                    'description': 'Produit recréé pour conserver l\'historique',
                    'quantite': 0,
                    'prix_achat': float(prix_achat),
                    'categorie': 'Archive',
                    'date_ajout': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                produits.append(produit_fictif)
                print(f"   ✅ Produit fictif créé : ID {produit_id}")
            
            mouvements_a_exporter = mouvements
            print(f"\n✅ Export de {len(produits)} produits (avec {len(produits_fictifs_ids)} fictifs)")
            print(f"✅ Export de {len(mouvements_a_exporter)} mouvements (tous)")
        else:
            print("\n❌ Choix invalide, export annulé")
            cursor.close()
            conn.close()
            exit(1)
    else:
        mouvements_a_exporter = mouvements
        print(f"\n✅ Tous les mouvements ont des produits existants")
    
    # ==========================================
    # Sauvegarder dans un fichier JSON
    # ==========================================
    data = {
        'produits': produits,
        'mouvements': mouvements_a_exporter,
        'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'statistiques': {
            'total_produits': len(produits),
            'total_mouvements': len(mouvements_a_exporter),
            'mouvements_orphelins_exclus': len(mouvements_orphelins) if choix == "1" else 0
        }
    }
    
    filename = f'export_complet_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
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
    print(f"   • Mouvements exportés : {len(mouvements_a_exporter)}")
    if mouvements_orphelins and choix == "1":
        print(f"   • Mouvements orphelins exclus : {len(mouvements_orphelins)}")
    print(f"   • Fichier créé : {filename}")
    print("\n📝 Prochaine étape :")
    print(f"   1. Uploadez '{filename}' sur PythonAnywhere")
    print("   2. Lancez le script 'import_donnees_v2.py' sur PythonAnywhere")
    
except mysql.connector.Error as e:
    print(f"\n❌ Erreur MySQL : {e}")
    print("\n💡 Vérifiez :")
    print("   1. MySQL est démarré")
    print("   2. Les identifiants dans ce script sont corrects")
    print("   3. La base de données 'gestion_stock' existe")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
