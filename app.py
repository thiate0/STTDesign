from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

# Fonction pour se connecter à la base de données MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion MySQL: {e}")
        return None

# Initialiser la base de données
def init_db():
    try:
        # Connexion sans spécifier la base de données pour la créer si nécessaire
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # Créer la base de données si elle n'existe pas
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {MYSQL_DATABASE}")
        
        # Créer la table produits
        cursor.execute('''
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
        
        # Créer la table mouvements
        cursor.execute('''
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
        
        
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Base de données MySQL initialisée avec succès!")
        
    except Error as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        print("\nVérifiez:")
        print("1. MySQL est installé et démarré")
        print("2. Les paramètres dans config.py sont corrects")
        print("3. L'utilisateur MySQL a les droits nécessaires")

# Route principale - Liste des produits
@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'error')
        return render_template('index.html', produits=[], total_produits=0, valeur_totale=0, produits_faible_stock=0)
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produits ORDER BY nom')
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Calculer les statistiques
    types_produits = len(produits)  # Nombre de types de produits différents
    total_unites = sum([p['quantite'] for p in produits])  # Total des unités en stock
    valeur_totale = sum([p['quantite'] * float(p['prix_achat']) for p in produits])
    produits_disponibles = sum([p['quantite'] for p in produits if p['quantite'] > 0])  # Somme des quantités disponibles
    
    return render_template('index.html', 
                         produits=produits,
                         types_produits=types_produits,
                         total_unites=total_unites,
                         valeur_totale=valeur_totale,
                         produits_disponibles=produits_disponibles)

# Route pour ajouter un produit
# @app.route('/ajouter', methods=('GET', 'POST'))
# def ajouter():
#     if request.method == 'POST':
#         nom = request.form['nom']
#         description = request.form['description']
#         quantite = request.form['quantite']
#         prix_achat = request.form['prix_achat']
#         categorie = request.form['categorie']
        
#         if not nom or not quantite or not prix_achat:
#             flash('Le nom, la quantité et le prix d\'achat sont obligatoires!', 'error')
#         else:
#             conn = get_db_connection()
#             if conn:
#                 cursor = conn.cursor()
#                 cursor.execute(
#                     'INSERT INTO produits (nom, description, quantite, prix_achat, categorie) VALUES (%s, %s, %s, %s, %s)',
#                     (nom, description, quantite, prix_achat, categorie)
#                 )
#                 conn.commit()
#                 cursor.close()
#                 conn.close()
#                 flash('Produit ajouté avec succès!', 'success')
#                 return redirect(url_for('index'))
#             else:
#                 flash('Erreur de connexion à la base de données', 'error')
    
#     return render_template('ajouter.html')
@app.route('/ajouter', methods=('GET', 'POST'))
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        quantite = int(request.form['quantite'])
        prix_achat = float(request.form['prix_achat'])
        categorie = request.form['categorie']
        
        if not nom or not quantite or not prix_achat:
            flash('Le nom, la quantité et le prix d\'achat sont obligatoires!', 'error')
        else:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                # --- 1️⃣ Insérer le produit ---
                cursor.execute(
                    'INSERT INTO produits (nom, description, quantite, prix_achat, categorie) VALUES (%s, %s, %s, %s, %s)',
                    (nom, description, quantite, prix_achat, categorie)
                )
                produit_id = cursor.lastrowid

                # --- 2️⃣ Enregistrer un mouvement de type "ajout" ---
                montant_total = quantite * prix_achat
                cursor.execute('''
                    INSERT INTO mouvements (produit_id, type_mouvement, quantite, prix_achat, prix_vente,
                                            montant_total, benefice, stock_avant, stock_apres)
                    VALUES (%s, 'ajout', %s, %s, 0, %s, 0, 0, %s)
                ''', (produit_id, quantite, prix_achat, montant_total, quantite))

                conn.commit()
                cursor.close()
                conn.close()
                flash('✅ Produit ajouté avec succès et mouvement enregistré!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Erreur de connexion à la base de données', 'error')
    
    return render_template('ajouter.html')

# Route pour modifier un produit
@app.route('/modifier/<int:id>', methods=('GET', 'POST'))
def modifier(id):
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'error')
        return redirect(url_for('index'))
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produits WHERE id = %s', (id,))
    produit = cursor.fetchone()
    
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        quantite = request.form['quantite']
        prix_achat = request.form['prix_achat']
        categorie = request.form['categorie']
        
        if not nom or not quantite or not prix_achat:
            flash('Le nom, la quantité et le prix d\'achat sont obligatoires!', 'error')
        else:
            cursor.execute(
                'UPDATE produits SET nom = %s, description = %s, quantite = %s, prix_achat = %s, categorie = %s WHERE id = %s',
                (nom, description, quantite, prix_achat, categorie, id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Produit modifié avec succès!', 'success')
            return redirect(url_for('index'))
    
    cursor.close()
    conn.close()
    return render_template('modifier.html', produit=produit)

# Route pour supprimer un produit
@app.route('/supprimer/<int:id>', methods=('POST',))
def supprimer(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produits WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Produit supprimé avec succès!', 'success')
    else:
        flash('Erreur de connexion à la base de données', 'error')
    return redirect(url_for('index'))

# Route pour rechercher des produits
@app.route('/rechercher')
def rechercher():
    query = request.args.get('q', '')
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'error')
        return render_template('rechercher.html', produits=[], query=query)
    
    cursor = conn.cursor(dictionary=True)
    search_pattern = f'%{query}%'
    cursor.execute(
        'SELECT * FROM produits WHERE nom LIKE %s OR description LIKE %s OR categorie LIKE %s',
        (search_pattern, search_pattern, search_pattern)
    )
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('rechercher.html', produits=produits, query=query)

# Route pour afficher les mouvements
# @app.route('/mouvements')
# def mouvements():
#     conn = get_db_connection()
#     if not conn:
#         flash('Erreur de connexion à la base de données', 'error')
#         return render_template('mouvements.html', mouvements=[], stats={'total_mouvements': 0, 'total_ventes': 0, 'total_quantite_vendue': 0, 'total_benefices': 0})
    
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute('''
#         SELECT m.*, p.nom as produit_nom, p.categorie
#         FROM mouvements m
#         JOIN produits p ON m.produit_id = p.id
#         ORDER BY m.date_mouvement DESC
#     ''')
#     mouvements = cursor.fetchall()
    
#     # Statistiques
#     cursor.execute('''
#         SELECT 
#             COUNT(*) as total_mouvements,
#             COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN montant_total ELSE 0 END), 0) as total_ventes,
#             COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN quantite ELSE 0 END), 0) as total_quantite_vendue,
#             COALESCE(SUM(CASE WHEN type_mouvement = 'vente' THEN benefice ELSE 0 END), 0) as total_benefices
#         FROM mouvements
#     ''')
#     stats = cursor.fetchone()
    
#     cursor.close()
#     conn.close()
#     return render_template('mouvements.html', mouvements=mouvements, stats=stats)
@app.route('/mouvements')
def mouvements():
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'error')
        return render_template('mouvements.html', mouvements=[], stats={'total_mouvements': 0, 'total_ventes': 0, 'total_quantite_vendue': 0, 'total_benefices': 0})
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT m.*, p.nom as produit_nom, p.categorie
        FROM mouvements m
        JOIN produits p ON m.produit_id = p.id
        ORDER BY m.date_mouvement DESC
    ''')
    mouvements = cursor.fetchall()

    # --- 1️⃣ Total des ventes ---
    cursor.execute('''
        SELECT 
            COALESCE(SUM(montant_total), 0) AS total_ventes,
            COALESCE(SUM(quantite), 0) AS total_quantite_vendue,
            COALESCE(SUM(benefice), 0) AS total_benefices
        FROM mouvements
        WHERE type_mouvement = 'vente'
    ''')
    ventes = cursor.fetchone()

    # --- 2️⃣ Total des achats ---
    cursor.execute('''
        SELECT COALESCE(SUM(montant_total), 0) AS total_achats
        FROM mouvements
        WHERE type_mouvement = 'ajout'
    ''')
    achats = cursor.fetchone()

    # --- 3️⃣ Calcul du total net ---
    total_ventes_net = (ventes['total_ventes'] or 0) - (achats['total_achats'] or 0)

    # --- 4️⃣ Statistiques globales ---
    stats = {
        'total_mouvements': len(mouvements),
        'total_ventes': total_ventes_net,
        'total_quantite_vendue': ventes['total_quantite_vendue'] or 0,
        'total_benefices': ventes['total_benefices'] or 0
    }

    cursor.close()
    conn.close()
    return render_template('mouvements.html', mouvements=mouvements, stats=stats)

# Route pour enregistrer une vente
@app.route('/vendre', methods=('GET', 'POST'))
def vendre():
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        produit_id = request.form['produit_id']
        quantite_vendue = int(request.form['quantite'])
        prix_vente = float(request.form['prix_vente'])
        
        # Récupérer le produit
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM produits WHERE id = %s', (produit_id,))
        produit = cursor.fetchone()
        
        if not produit:
            flash('Produit introuvable!', 'error')
        elif produit['quantite'] < quantite_vendue:
            flash(f'Stock insuffisant! Disponible: {produit["quantite"]} unités', 'error')
        else:
            # Calculer les montants
            montant_total = quantite_vendue * prix_vente
            cout_achat = quantite_vendue * float(produit['prix_achat'])
            benefice = montant_total - cout_achat
            stock_avant = produit['quantite']
            stock_apres = stock_avant - quantite_vendue
            
            # Enregistrer le mouvement
            cursor.execute('''
                INSERT INTO mouvements (produit_id, type_mouvement, quantite, prix_achat, prix_vente,
                                       montant_total, benefice, stock_avant, stock_apres)
                VALUES (%s, 'vente', %s, %s, %s, %s, %s, %s, %s)
            ''', (produit_id, quantite_vendue, produit['prix_achat'], prix_vente,
                  montant_total, benefice, stock_avant, stock_apres))
            
            # Mettre à jour le stock
            cursor.execute('UPDATE produits SET quantite = %s WHERE id = %s',
                        (stock_apres, produit_id))
            
            conn.commit()
            flash(f'Vente enregistrée! Montant: {montant_total:.2f} € - Bénéfice: {benefice:.2f} €', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('mouvements'))
    
    # Récupérer tous les produits pour le formulaire
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produits WHERE quantite > 0 ORDER BY nom')
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('vendre.html', produits=produits)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
