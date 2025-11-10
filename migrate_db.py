import sqlite3

print("🔄 Migration de la base de données en cours...")

try:
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    
    # Vérifier et migrer la table produits
    print("📦 Vérification de la table produits...")
    
    # Vérifier si prix_achat existe
    cursor.execute("PRAGMA table_info(produits)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'prix_unitaire' in columns and 'prix_achat' not in columns:
        print("  ➜ Renommage de prix_unitaire en prix_achat...")
        # SQLite ne supporte pas ALTER COLUMN, donc on recrée la table
        cursor.execute('''
            CREATE TABLE produits_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                quantite INTEGER NOT NULL,
                prix_achat REAL NOT NULL,
                categorie TEXT,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            INSERT INTO produits_new (id, nom, description, quantite, prix_achat, categorie, date_ajout)
            SELECT id, nom, description, quantite, prix_unitaire, categorie, date_ajout
            FROM produits
        ''')
        cursor.execute('DROP TABLE produits')
        cursor.execute('ALTER TABLE produits_new RENAME TO produits')
        print("  ✅ Table produits mise à jour")
    
    # Supprimer la colonne prix_vente si elle existe
    if 'prix_vente' in columns:
        print("  ➜ Suppression de la colonne prix_vente...")
        cursor.execute('''
            CREATE TABLE produits_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                quantite INTEGER NOT NULL,
                prix_achat REAL NOT NULL,
                categorie TEXT,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            INSERT INTO produits_new (id, nom, description, quantite, prix_achat, categorie, date_ajout)
            SELECT id, nom, description, quantite, prix_achat, categorie, date_ajout
            FROM produits
        ''')
        cursor.execute('DROP TABLE produits')
        cursor.execute('ALTER TABLE produits_new RENAME TO produits')
        print("  ✅ Colonne prix_vente supprimée")
    
    # Vérifier et migrer la table mouvements
    print("📊 Vérification de la table mouvements...")
    
    cursor.execute("PRAGMA table_info(mouvements)")
    mouv_columns = [col[1] for col in cursor.fetchall()]
    
    if 'benefice' not in mouv_columns:
        print("  ➜ Ajout de la colonne benefice...")
        
        # Recréer la table avec la nouvelle structure
        cursor.execute('''
            CREATE TABLE mouvements_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produit_id INTEGER NOT NULL,
                type_mouvement TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                prix_achat REAL NOT NULL,
                prix_vente REAL NOT NULL,
                montant_total REAL NOT NULL,
                benefice REAL NOT NULL,
                stock_avant INTEGER NOT NULL,
                stock_apres INTEGER NOT NULL,
                date_mouvement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produit_id) REFERENCES produits (id)
            )
        ''')
        
        # Copier les anciennes données si elles existent
        if 'prix_unitaire' in mouv_columns:
            print("  ➜ Migration des anciennes données...")
            cursor.execute('''
                INSERT INTO mouvements_new (id, produit_id, type_mouvement, quantite, 
                                           prix_achat, prix_vente, montant_total, benefice,
                                           stock_avant, stock_apres, date_mouvement)
                SELECT id, produit_id, type_mouvement, quantite,
                       prix_unitaire as prix_achat,
                       prix_unitaire as prix_vente,
                       montant_total,
                       0 as benefice,
                       stock_avant, stock_apres, date_mouvement
                FROM mouvements
            ''')
        
        cursor.execute('DROP TABLE IF EXISTS mouvements')
        cursor.execute('ALTER TABLE mouvements_new RENAME TO mouvements')
        print("  ✅ Table mouvements mise à jour")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Migration terminée avec succès!")
    print("Vous pouvez maintenant lancer l'application avec: python app.py")
    
except Exception as e:
    print(f"\n❌ Erreur lors de la migration: {e}")
    print("\nSi l'erreur persiste, supprimez le fichier stock.db et relancez l'application.")
