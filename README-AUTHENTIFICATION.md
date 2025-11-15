# 🔐 SYSTÈME D'AUTHENTIFICATION - Gestion de Stock STTDesign

## 📦 CONTENU DE L'ARCHIVE

```
authentification-complete.zip
│
├── app.py                          🔄 Application avec authentification
├── auth.py                         ⭐ Module d'authentification
├── init_auth.py                    ⭐ Script d'initialisation
├── login.html                      ⭐ Page de connexion
├── base.html                       🔄 Template avec menu utilisateur
├── INSTALLATION-RAPIDE-AUTH.md     📖 Guide rapide (5 min)
└── GUIDE-AUTHENTIFICATION.md       📖 Guide complet
```

---

## 🎯 OBJECTIF

Ajouter un système d'authentification complet à votre application de gestion de stock :
- 🔐 Connexion/Déconnexion
- 🛡️ Protection de toutes les pages
- 👤 Gestion des utilisateurs
- 🔒 Mots de passe sécurisés
- 📊 Système de rôles (admin/user)

---

## ⚡ INSTALLATION RAPIDE

### **1. Extraire l'archive**
### **2. Uploader les fichiers**
- `app.py` → Remplace l'ancien
- `auth.py` → Nouveau fichier
- `init_auth.py` → Nouveau fichier
- `templates/login.html` → Nouveau template
- `templates/base.html` → Remplace l'ancien

### **3. Initialiser**
```bash
python init_auth.py
```

### **4. Redémarrer l'application**
```bash
python app.py  # En local
```
ou
```
Web → Reload  # Sur PythonAnywhere
```

### **5. Se connecter**
- Username: `admin`
- Password: `admin123`

---

## 📖 GUIDES DISPONIBLES

### **INSTALLATION-RAPIDE-AUTH.md**
- ⏱️ 5 minutes
- ⭐ Facile
- 📋 Procédure pas à pas
- ✅ Checklist

### **GUIDE-AUTHENTIFICATION.md**
- 📚 Guide complet
- 🔧 Personnalisation
- 👥 Gestion des utilisateurs
- 🆘 Dépannage détaillé
- 💡 Conseils avancés

---

## 🔐 IDENTIFIANTS PAR DÉFAUT

**⚠️ IMPORTANT : À CHANGER IMMÉDIATEMENT**

```
Username: admin
Password: admin123
```

---

## ✨ FONCTIONNALITÉS

### **Sécurité**
- ✅ Mots de passe hashés (Werkzeug)
- ✅ Sessions Flask sécurisées
- ✅ Protection de toutes les routes
- ✅ Redirection automatique si non connecté

### **Interface**
- ✅ Page de login moderne
- ✅ Menu utilisateur dans navbar
- ✅ Affichage du rôle
- ✅ Bouton de déconnexion

### **Base de données**
- ✅ Table `utilisateurs` créée automatiquement
- ✅ Champs : username, password, nom, email, rôle, actif
- ✅ Suivi de la dernière connexion

---

## 📊 CE QUI CHANGE

### **Fichiers modifiés :**
1. **app.py** - Routes protégées + login/logout
2. **templates/base.html** - Menu utilisateur

### **Fichiers ajoutés :**
1. **auth.py** - Fonctions d'authentification
2. **init_auth.py** - Initialisation DB
3. **templates/login.html** - Page de connexion

### **Fichiers inchangés :**
- `config.py`
- Tous les autres templates
- Structure de la base de données existante

---

## 🚀 COMPATIBILITÉ

### **Testé avec :**
- ✅ Python 3.8+
- ✅ Flask 2.0+
- ✅ MySQL 5.7+
- ✅ PythonAnywhere
- ✅ Localhost

### **Dépendances :**
- Flask (déjà installé)
- Werkzeug (inclus avec Flask)
- mysql-connector-python (déjà installé)

---

## 👥 GESTION DES UTILISATEURS

### **Utilisateur par défaut :**
- Username: `admin`
- Rôle: `admin`
- Statut: Actif

### **Ajouter des utilisateurs :**
Via MySQL ou script Python (voir guide complet)

### **Rôles disponibles :**
- `admin` - Accès complet
- `user` - Accès standard

---

## 🔧 PERSONNALISATION

### **Changer les couleurs**
Éditez `templates/login.html` :
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### **Changer le logo**
Éditez `templates/login.html` :
```html
<i class="bi bi-shield-lock" style="font-size: 4rem; color: #039e9c;"></i>
```

### **Ajouter des champs**
Modifiez la table `utilisateurs` dans `init_auth.py`

---

## ✅ CHECKLIST D'INSTALLATION

- [ ] Archive extraite
- [ ] Fichiers uploadés (5 fichiers)
- [ ] `python init_auth.py` exécuté avec succès
- [ ] Message "Utilisateur admin créé" affiché
- [ ] Application redémarrée
- [ ] Page `/login` accessible
- [ ] Connexion avec admin/admin123 réussie
- [ ] Redirection vers page d'accueil
- [ ] Menu utilisateur visible en haut à droite
- [ ] Déconnexion fonctionne
- [ ] Accès refusé si non connecté

---

## 🆘 SUPPORT

### **Problèmes courants :**

**"Module auth not found"**
→ `auth.py` doit être au même niveau que `app.py`

**"Table utilisateurs doesn't exist"**
→ Lancez `python init_auth.py`

**"Mot de passe incorrect"**
→ Vérifiez les identifiants : `SELECT * FROM utilisateurs;`

**Redirection infinie**
→ Vérifiez que `app.secret_key` est défini

### **Vérifications :**
```sql
-- Voir tous les utilisateurs
SELECT * FROM utilisateurs;

-- Vérifier qu'un utilisateur est actif
SELECT username, actif FROM utilisateurs WHERE username = 'admin';
```

---

## 📞 CONTACT

Pour toute question :
1. Consultez **GUIDE-AUTHENTIFICATION.md**
2. Vérifiez les logs de l'application
3. Testez en local d'abord

---

## 🎉 RÉSULTAT FINAL

Après installation, votre application :
- ✅ Est entièrement sécurisée
- ✅ Nécessite une connexion
- ✅ Gère les utilisateurs
- ✅ A une interface professionnelle
- ✅ Est prête pour la production

**Bon développement ! 🚀**

---

## 📝 VERSION

**Version :** 1.0  
**Date :** Novembre 2025  
**Auteur :** STTDesign  
**Licence :** Propriétaire
