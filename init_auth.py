#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation de la table utilisateurs
Crée la table et ajoute un utilisateur admin par défaut
"""

import mysql.connector
from werkzeug.security import generate_password_hash
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT

print("=" * 60)
print("👤 INITIALISATION DU SYSTÈME D'AUTHENTIFICATION")
print("=" * 60)

try:
    # Connexion à la base de données
    print("\n🔌 Connexion à MySQL...")
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT
    )
    cursor = conn.cursor()
    print("✅ Connecté à MySQL")
    
    # Créer la table utilisateurs
    print("\n📋 Création de la table 'utilisateurs'...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            nom_complet VARCHAR(100),
            email VARCHAR(100),
            role VARCHAR(20) DEFAULT 'user',
            actif BOOLEAN DEFAULT TRUE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            derniere_connexion TIMESTAMP NULL
        )
    ''')
    print("✅ Table 'utilisateurs' créée")
    
    # Vérifier si l'admin existe déjà
    cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE username = 'admin'")
    admin_existe = cursor.fetchone()[0] > 0
    
    if not admin_existe:
        print("\n👤 Création de l'utilisateur administrateur...")
        
        # Mot de passe par défaut : admin123
        # IMPORTANT : À changer lors du premier login !
        admin_password = 'Thioune321'
        password_hash = generate_password_hash(admin_password)
        
        cursor.execute('''
            INSERT INTO utilisateurs (username, password_hash, nom_complet, email, role)
            VALUES (%s, %s, %s, %s, %s)
        ''', ('Admin', password_hash, 'Administrateur', 'sttdesign@gmail.com', 'admin'))
        
        conn.commit()
        
        print("✅ Utilisateur admin créé")
        print("\n" + "=" * 60)
        print("🔐 IDENTIFIANTS PAR DÉFAUT")
        print("=" * 60)
        print(f"   Username : admin")
        print(f"   Password : {admin_password}")
        print("\n⚠️  IMPORTANT : Changez ce mot de passe lors de votre première connexion !")
        print("=" * 60)
    else:
        print("\n✅ L'utilisateur admin existe déjà")
    
    # Afficher les utilisateurs existants
    print("\n📋 Utilisateurs dans la base :")
    cursor.execute("SELECT id, username, nom_complet, role, actif FROM utilisateurs")
    utilisateurs = cursor.fetchall()
    
    for user in utilisateurs:
        statut = "🟢 Actif" if user[4] else "🔴 Inactif"
        print(f"   • ID {user[0]} : {user[1]} ({user[2]}) - {user[3]} {statut}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print("\n📝 Prochaines étapes :")
    print("   1. Lancez l'application : python app.py")
    print("   2. Allez sur : http://localhost:5000/login")
    print("   3. Connectez-vous avec admin/admin123")
    print("   4. Changez le mot de passe !")
    
except mysql.connector.Error as e:
    print(f"\n❌ Erreur MySQL : {e}")
    print("\n💡 Vérifiez :")
    print("   1. MySQL est démarré")
    print("   2. Les identifiants dans config.py sont corrects")
    print("   3. La base de données existe")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
