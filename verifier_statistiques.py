#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification et correction des statistiques
Vérifie que les calculs dans la table mouvements sont corrects
"""

import mysql.connector
from decimal import Decimal

# ============================================
# CONFIGURATION - MODIFIEZ VOS IDENTIFIANTS
# ============================================
MYSQL_HOST = 'STTDesign.mysql.pythonanywhere-services.com'
MYSQL_USER = 'STTDesign'
MYSQL_PASSWORD = 'votre_mot_de_passe'  # ⚠️ CHANGEZ ICI
MYSQL_DATABASE = 'STTDesign$gestion_stock'

print("=" * 70)
print("🔍 VÉRIFICATION DES STATISTIQUES")
print("=" * 70)

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor(dictionary=True)
    
    # ====================
    # VÉRIFIER LES CALCULS ACTUELS
    # ====================
    print("\n📊 STATISTIQUES ACTUELLES DANS LA BASE :")
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_mouvements,
            COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN montant_total ELSE 0 END), 0) as total_ventes,
            COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN quantite ELSE 0 END), 0) as total_quantite_vendue,
            COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN benefice ELSE 0 END), 0) as total_benefices
        FROM mouvements
    ''')
    stats = cursor.fetchone()
    
    print(f"\n   📋 Total Mouvements : {stats['total_mouvements']}")
    print(f"   💰 Total Ventes (Caisse) : {stats['total_ventes']:.2f} FCFA")
    print(f"   📦 Unités Vendues : {stats['total_quantite_vendue']}")
    print(f"   📈 Bénéfices : {stats['total_benefices']:.2f} FCFA")
    
    # ====================
    # DÉTAIL DES MOUVEMENTS PAR TYPE
    # ====================
    print("\n" + "=" * 70)
    print("📊 DÉTAIL PAR TYPE DE MOUVEMENT :")
    print("=" * 70)
    
    cursor.execute('''
        SELECT 
            type_mouvement,
            COUNT(*) as nombre,
            SUM(quantite) as total_quantite,
            SUM(montant_total) as total_montant,
            SUM(benefice) as total_benefice
        FROM mouvements
        GROUP BY type_mouvement
    ''')
    types = cursor.fetchall()
    
    for t in types:
        print(f"\n   {t['type_mouvement'].upper()} :")
        print(f"      • Nombre : {t['nombre']}")
        print(f"      • Quantité totale : {t['total_quantite']}")
        print(f"      • Montant total : {t['total_montant']:.2f} FCFA")
        print(f"      • Bénéfice total : {t['total_benefice']:.2f} FCFA")
    
    # ====================
    # VÉRIFIER CHAQUE MOUVEMENT DE VENTE
    # ====================
    print("\n" + "=" * 70)
    print("🔍 VÉRIFICATION DES VENTES (calculs détaillés) :")
    print("=" * 70)
    
    cursor.execute('''
        SELECT 
            m.*,
            p.nom as produit_nom,
            p.prix_achat as prix_achat_actuel
        FROM mouvements m
        JOIN produits p ON m.produit_id = p.id
        WHERE m.type_mouvement = 'vente'
        ORDER BY m.id
    ''')
    ventes = cursor.fetchall()
    
    problemes = []
    
    for v in ventes:
        montant_calcule = float(v['quantite']) * float(v['prix_vente'])
        benefice_calcule = float(v['quantite']) * (float(v['prix_vente']) - float(v['prix_achat']))
        
        montant_ok = abs(float(v['montant_total']) - montant_calcule) < 0.01
        benefice_ok = abs(float(v['benefice']) - benefice_calcule) < 0.01
        
        if not montant_ok or not benefice_ok:
            problemes.append(v)
            print(f"\n   ⚠️  PROBLÈME - Vente ID {v['id']} : {v['produit_nom']}")
            print(f"      • Quantité : {v['quantite']}")
            print(f"      • Prix achat : {v['prix_achat']:.2f} FCFA")
            print(f"      • Prix vente : {v['prix_vente']:.2f} FCFA")
            print(f"      • Montant enregistré : {v['montant_total']:.2f} FCFA")
            print(f"      • Montant correct : {montant_calcule:.2f} FCFA → {'✅ OK' if montant_ok else '❌ ERREUR'}")
            print(f"      • Bénéfice enregistré : {v['benefice']:.2f} FCFA")
            print(f"      • Bénéfice correct : {benefice_calcule:.2f} FCFA → {'✅ OK' if benefice_ok else '❌ ERREUR'}")
    
    if not problemes:
        print("\n   ✅ Tous les calculs de ventes sont corrects !")
    else:
        print(f"\n   ❌ {len(problemes)} vente(s) avec des calculs incorrects")
    
    # ====================
    # RECALCULER MANUELLEMENT POUR VÉRIFICATION
    # ====================
    print("\n" + "=" * 70)
    print("🧮 CALCUL MANUEL DES STATISTIQUES :")
    print("=" * 70)
    
    cursor.execute("SELECT * FROM mouvements WHERE type_mouvement = 'vente'")
    toutes_ventes = cursor.fetchall()
    
    total_ventes_manuel = sum([float(v['montant_total']) for v in toutes_ventes])
    total_qte_manuel = sum([int(v['quantite']) for v in toutes_ventes])
    total_benefice_manuel = sum([float(v['benefice']) for v in toutes_ventes])
    
    print(f"\n   💰 Total Ventes (Caisse) : {total_ventes_manuel:.2f} FCFA")
    print(f"   📦 Unités Vendues : {total_qte_manuel}")
    print(f"   📈 Bénéfices : {total_benefice_manuel:.2f} FCFA")
    
    # Comparer avec la base
    diff_ventes = abs(float(stats['total_ventes']) - total_ventes_manuel)
    diff_benefices = abs(float(stats['total_benefices']) - total_benefice_manuel)
    
    if diff_ventes < 0.01 and diff_benefices < 0.01:
        print("\n   ✅ Les statistiques de la base sont correctes !")
    else:
        print("\n   ⚠️  Différences détectées :")
        if diff_ventes > 0.01:
            print(f"      • Ventes : {diff_ventes:.2f} FCFA de différence")
        if diff_benefices > 0.01:
            print(f"      • Bénéfices : {diff_benefices:.2f} FCFA de différence")
    
    # ====================
    # LISTE COMPLÈTE DES VENTES
    # ====================
    print("\n" + "=" * 70)
    print("📋 LISTE COMPLÈTE DE TOUTES LES VENTES :")
    print("=" * 70)
    
    for i, v in enumerate(toutes_ventes, 1):
        date = v['date_mouvement'].strftime('%Y-%m-%d %H:%M') if v['date_mouvement'] else 'N/A'
        cursor.execute("SELECT nom FROM produits WHERE id = %s", (v['produit_id'],))
        produit = cursor.fetchone()
        nom_produit = produit['nom'] if produit else f"ID {v['produit_id']}"
        
        print(f"\n   {i}. Vente ID {v['id']} - {date}")
        print(f"      • Produit : {nom_produit}")
        print(f"      • Quantité : {v['quantite']}")
        print(f"      • Prix achat : {v['prix_achat']:.2f} FCFA")
        print(f"      • Prix vente : {v['prix_vente']:.2f} FCFA")
        print(f"      • Montant total : {v['montant_total']:.2f} FCFA")
        print(f"      • Bénéfice : {v['benefice']:.2f} FCFA")
    
    # ====================
    # PROPOSITION DE CORRECTION
    # ====================
    if problemes:
        print("\n" + "=" * 70)
        print("🔧 CORRECTION DES ERREURS :")
        print("=" * 70)
        
        reponse = input(f"\nVoulez-vous corriger les {len(problemes)} vente(s) avec erreurs ? (oui/non) : ")
        
        if reponse.lower() in ['oui', 'o', 'yes', 'y']:
            print("\n🔧 Correction en cours...")
            
            for v in problemes:
                montant_correct = float(v['quantite']) * float(v['prix_vente'])
                benefice_correct = float(v['quantite']) * (float(v['prix_vente']) - float(v['prix_achat']))
                
                cursor.execute('''
                    UPDATE mouvements 
                    SET montant_total = %s, benefice = %s 
                    WHERE id = %s
                ''', (montant_correct, benefice_correct, v['id']))
                
                print(f"   ✅ Vente ID {v['id']} corrigée")
            
            conn.commit()
            print("\n✅ Corrections appliquées avec succès !")
            
            # Recalculer les stats
            cursor.execute('''
                SELECT 
                    COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN montant_total ELSE 0 END), 0) as total_ventes,
                    COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN quantite ELSE 0 END), 0) as total_quantite_vendue,
                    COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN benefice ELSE 0 END), 0) as total_benefices
                FROM mouvements
            ''')
            nouvelles_stats = cursor.fetchone()
            
            print("\n📊 NOUVELLES STATISTIQUES :")
            print(f"   💰 Total Ventes (Caisse) : {nouvelles_stats['total_ventes']:.2f} FCFA")
            print(f"   📦 Unités Vendues : {nouvelles_stats['total_quantite_vendue']}")
            print(f"   📈 Bénéfices : {nouvelles_stats['total_benefices']:.2f} FCFA")
        else:
            print("\n❌ Corrections annulées")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ VÉRIFICATION TERMINÉE")
    print("=" * 70)
    
    print("\n📝 RECOMMANDATIONS :")
    print("   1. Rechargez votre application web (Web → Reload)")
    print("   2. Visitez la page Mouvements")
    print("   3. Vérifiez que les statistiques sont correctes")
    
except mysql.connector.Error as e:
    print(f"\n❌ Erreur MySQL : {e}")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
