"""
Module d'authentification
Gère la connexion, déconnexion et vérification des utilisateurs
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

def login_required(f):
    """
    Décorateur pour protéger les routes
    Redirige vers login si l'utilisateur n'est pas connecté
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hasher un mot de passe"""
    return generate_password_hash(password)

def verify_password(password_hash, password):
    """Vérifier un mot de passe"""
    return check_password_hash(password_hash, password)
