from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('first_name')
        password = request.form.get('password')
        
        user = User.query.filter_by(first_name=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Willkommen {user.first_name}!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash("Email doesn't exist.", category="error")
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(first_name=first_name).first()
        if user:
            flash("User Existiert bereits.", category='error')
        elif len(first_name) < 3:
            flash('User-ID muss länger als 3 sein.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Passwort muss min. 4 zeichen haben.', category='error')
        else:
            new_user = User(first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account erstellt!', category='success')
            return redirect(url_for("views.home"))
            
    return render_template("sign-up.html", user=current_user)