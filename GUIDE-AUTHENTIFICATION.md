# 🔐 GUIDE D'INSTALLATION - Système d'Authentification

## 📋 APERÇU

Ce système d'authentification ajoute à votre application :
- ✅ Page de connexion sécurisée
- ✅ Gestion des sessions utilisateurs
- ✅ Protection de toutes les routes
- ✅ Mots de passe hashés (sécurisés)
- ✅ Système de rôles (admin/user)
- ✅ Interface utilisateur moderne

---

## 📦 FICHIERS MODIFIÉS/AJOUTÉS

### **NOUVEAUX fichiers :**
1. `auth.py` - Module d'authentification
2. `init_auth.py` - Script d'initialisation
3. `templates/login.html` - Page de connexion

### **FICHIERS MODIFIÉS :**
1. `app.py` - Ajout des routes auth + protection
2. `templates/base.html` - Ajout menu utilisateur

---

## 🚀 INSTALLATION

### **ÉTAPE 1 : Uploader les fichiers**

#### **Sur votre PC (en local) :**
1. Remplacez `app.py` par la nouvelle version
2. Ajoutez `auth.py` dans le dossier racine
3. Ajoutez `init_auth.py` dans le dossier racine
4. Remplacez `templates/base.html`
5. Ajoutez `templates/login.html`

#### **Sur PythonAnywhere :**
1. Files → `/home/STTDesign/STTDesign/`
2. Uploadez tous les fichiers ci-dessus

---

### **ÉTAPE 2 : Initialiser la table utilisateurs**

#### **En local :**
```bash
cd votre-dossier-projet
python init_auth.py
```

#### **Sur PythonAnywhere :**
```bash
cd STTDesign
python3 init_auth.py
```

**Résultat attendu :**
```
======================================================================
👤 INITIALISATION DU SYSTÈME D'AUTHENTIFICATION
======================================================================

🔌 Connexion à MySQL...
✅ Connecté à MySQL

📋 Création de la table 'utilisateurs'...
✅ Table 'utilisateurs' créée

👤 Création de l'utilisateur administrateur...
✅ Utilisateur admin créé

======================================================================
🔐 IDENTIFIANTS PAR DÉFAUT
======================================================================
   Username : admin
   Password : admin123

⚠️  IMPORTANT : Changez ce mot de passe lors de votre première connexion !
======================================================================

✅ INITIALISATION TERMINÉE AVEC SUCCÈS !
```

---

### **ÉTAPE 3 : Redémarrer l'application**

#### **En local :**
```bash
# Arrêtez l'app (Ctrl+C)
python app.py
```

#### **Sur PythonAnywhere :**
- Allez dans **Web**
- Cliquez sur **Reload**

---

### **ÉTAPE 4 : Première connexion**

1. Ouvrez : `http://localhost:5000` (local) ou `http://STTDesign.pythonanywhere.com` (en ligne)
2. Vous serez redirigé vers `/login`
3. Connectez-vous :
   - **Username :** `admin`
   - **Password :** `admin123`
4. Vous êtes connecté ! 🎉

---

## 🔐 FONCTIONNALITÉS

### **1. Page de connexion**
- Design moderne et sécurisé
- Validation des identifiants
- Messages d'erreur clairs
- Option "Se souvenir de moi"

### **2. Protection des routes**
Toutes les pages nécessitent maintenant une connexion :
- ✅ `/` - Accueil
- ✅ `/ajouter` - Ajouter produit
- ✅ `/vendre` - Vendre
- ✅ `/mouvements` - Historique
- ✅ `/modifier/<id>` - Modifier
- ✅ `/supprimer/<id>` - Supprimer
- ✅ `/rechercher` - Rechercher

### **3. Navbar avec utilisateur**
La barre de navigation affiche maintenant :
- Nom de l'utilisateur connecté
- Son rôle (admin/user)
- Bouton de déconnexion

### **4. Sécurité**
- Mots de passe hashés avec Werkzeug
- Sessions Flask sécurisées
- Protection CSRF intégrée
- Redirection automatique si non connecté

---

## 👥 GESTION DES UTILISATEURS

### **Table utilisateurs**

Structure de la table :
```sql
CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nom_complet VARCHAR(100),
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    derniere_connexion TIMESTAMP NULL
);
```

### **Ajouter un utilisateur manuellement**

#### **Via MySQL :**
```sql
-- Connexion à MySQL
mysql -h STTDesign.mysql.pythonanywhere-services.com -u STTDesign -p

USE STTDesign$gestion_stock;

-- Ajouter un utilisateur (le mot de passe sera "password123")
INSERT INTO utilisateurs (username, password_hash, nom_complet, email, role)
VALUES (
    'john',
    'scrypt:32768:8:1$...',  -- Hash de "password123"
    'John Doe',
    'john@example.com',
    'user'
);
```

#### **Via Python :**
```python
from auth import hash_password
import mysql.connector

# Connexion
conn = mysql.connector.connect(...)
cursor = conn.cursor()

# Hasher le mot de passe
password_hash = hash_password('password123')

# Insérer l'utilisateur
cursor.execute('''
    INSERT INTO utilisateurs (username, password_hash, nom_complet, email, role)
    VALUES (%s, %s, %s, %s, %s)
''', ('john', password_hash, 'John Doe', 'john@example.com', 'user'))

conn.commit()
print("✅ Utilisateur créé")
```

---

## 🔧 PERSONNALISATION

### **Changer le mot de passe admin**

#### **Méthode 1 : Via MySQL**
```sql
UPDATE utilisateurs 
SET password_hash = 'nouveau_hash' 
WHERE username = 'admin';
```

#### **Méthode 2 : Via Python**
```python
from auth import hash_password
import mysql.connector

conn = mysql.connector.connect(...)
cursor = conn.cursor()

nouveau_mdp = hash_password('nouveau_mot_de_passe')
cursor.execute('UPDATE utilisateurs SET password_hash = %s WHERE username = %s', 
               (nouveau_mdp, 'admin'))
conn.commit()
print("✅ Mot de passe changé")
```

### **Désactiver un utilisateur**

```sql
UPDATE utilisateurs SET actif = FALSE WHERE username = 'john';
```

### **Voir tous les utilisateurs**

```sql
SELECT id, username, nom_complet, role, actif, derniere_connexion 
FROM utilisateurs;
```

---

## 🎨 PERSONNALISER LA PAGE DE LOGIN

Le fichier `templates/login.html` peut être personnalisé :

```html
<!-- Changer les couleurs -->
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>

<!-- Changer le logo -->
<i class="bi bi-shield-lock" style="font-size: 4rem; color: #039e9c;"></i>

<!-- Changer le texte -->
<p class="text-muted">STT_Design - Gestion de Stock</p>
```

---

## 🔄 MIGRATION VERS PYTHONANYWHERE

### **Si vous avez déjà des données :**

1. **En local :**
   ```bash
   python init_auth.py
   ```

2. **Uploader les fichiers sur PythonAnywhere**

3. **Sur PythonAnywhere :**
   ```bash
   cd STTDesign
   python3 init_auth.py
   ```

4. **Recharger :**
   Web → Reload

5. **Tester :**
   - Visitez votre site
   - Vous serez redirigé vers `/login`
   - Connectez-vous avec `admin` / `admin123`

---

## 🆘 DÉPANNAGE

### **"Module auth not found"**
→ Le fichier `auth.py` n'est pas dans le bon dossier
→ Il doit être au même niveau que `app.py`

### **"Table utilisateurs doesn't exist"**
→ Lancez `python init_auth.py`

### **"Nom d'utilisateur ou mot de passe incorrect"**
→ Vérifiez que l'utilisateur existe : `SELECT * FROM utilisateurs;`
→ Vérifiez que `actif = TRUE`

### **Redirection infinie vers /login**
→ Vérifiez que la session fonctionne
→ Vérifiez que `app.secret_key` est défini dans `app.py`

### **"werkzeug.security not found"**
→ Werkzeug est inclus avec Flask, mais réinstallez si besoin :
```bash
pip install werkzeug
```

---

## ✅ CHECKLIST D'INSTALLATION

- [ ] Fichiers uploadés (app.py, auth.py, init_auth.py, templates)
- [ ] `python init_auth.py` lancé avec succès
- [ ] Utilisateur admin créé
- [ ] Application redémarrée
- [ ] Page de login accessible
- [ ] Connexion avec admin/admin123 réussie
- [ ] Toutes les pages protégées fonctionnent
- [ ] Menu utilisateur visible dans la navbar
- [ ] Déconnexion fonctionne

---

## 🎉 RÉSULTAT FINAL

Votre application est maintenant sécurisée ! 🔐

**Fonctionnalités :**
- ✅ Connexion obligatoire
- ✅ Gestion des utilisateurs
- ✅ Mots de passe sécurisés
- ✅ Interface professionnelle
- ✅ Système de rôles
- ✅ Sessions persistantes

**Prochaines étapes possibles :**
- Ajouter une page de gestion des utilisateurs (pour admin)
- Ajouter un système de changement de mot de passe
- Ajouter un système "Mot de passe oublié"
- Ajouter des permissions par rôle (admin vs user)
- Ajouter un journal des connexions

---

## 📞 SUPPORT

Pour toute question :
1. Vérifiez les logs : `tail -f /var/log/yourusername.pythonanywhere.com.error.log`
2. Testez en local d'abord
3. Vérifiez que MySQL fonctionne
4. Vérifiez que tous les fichiers sont uploadés

**Bon développement ! 🚀**
