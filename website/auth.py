from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import user_db as database
from website.db import db
from .models import User
from datetime import datetime

now = datetime.now()

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Welcome {user.first_name}!', category='success')
                login_user(user, remember=True)
                current_time = now.strftime("%d/%m/%Y %H:%M:%S")
                db.execute("INSERT INTO sarguhl_bereich.login (employee, action, time) VALUES (%s, %s, %s)", f"{user.first_name} ID: {user.id}", f"Logged In", current_time)
                db.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash("Email doesn't exist.", category="error")
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    db.execute("INSERT INTO sarguhl_bereich.login (employee, action, time) VALUES (%s, %s, %s)", f"{current_user.first_name} ID: {current_user.id}", f"Logged Out", current_time)
    db.commit()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
@login_required
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        employee_type = request.form.get('type')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Mitarbeiter existiert bereits.", category='error')
        elif len(email) < 3:
            flash('Die Mitarbeiter-Nummer muss mindestens 4 Zeichen lang sein.', category='error')
        elif len(first_name) < 2:
            flash('Der Name muss mindestens 2 Zeichen lang sein.', category='error')
        elif password1 != password2:
            flash('Die Passw??rter stimmen nicht ??berein.', category='error')
        elif len(password1) < 3:
            flash('Das Passwort muss mindestens 4 Zeichen lang sein', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), user_state="employee")
            database.session.add(new_user)
            flash('Account created!', category='success')
            database.session.commit()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            db.execute("INSERT INTO sarguhl_bereich.log (employee, action, time) VALUES (%s, %s, %s)", f"{current_user.first_name} ID: {current_user.id}", f"Created User {first_name}", current_time)
            db.commit()
    if current_user.user_state == "admin":
        database.session.commit()
        return render_template("sign-up.html", user=current_user)
    else: render_template("login.html")

