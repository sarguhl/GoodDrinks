from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Note, User
from . import user_db as database
import json
import random
from website.db import db

views = Blueprint('views', __name__)
placeholder_sentence = ["Today I though about...", "It's important that...", "I want to remember...", "I think about...", "Today happened...", "WOW! Note this..."]

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            database.session.delete(note)
            database.session.commit()
    
    return jsonify({})

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html", current_user=current_user)

@views.route("/funktion-eins", methods=["GET","POST"])
def funktion_one():
    return render_template("funktion_one.html", current_user=current_user)

@views.route("/funktion-zwei", methods=["GET","POST"])
def funktion_two():
    return render_template("funktion_two.html", current_user=current_user)

@views.route("/funktion-drei", methods=["GET","POST"])
def funktion_three():
    return render_template("funktion_three.html", current_user=current_user)

@views.route("/hilfe", methods=["GET"])
def hilfe():
    return render_template("help.html", current_user=current_user)

@views.route("/impressum", methods=["GET"])
def impressum():
    return render_template("impressum.html", current_user=current_user)

@views.route("/blog")
def blog():
    result = Note.query.all()
    print(result)
    app_version = db.records("SELECT version FROM appinfo WHERE versionId = 1")
    return render_template("blog.html", session = result, user = current_user, current_user=current_user, app_version = app_version[0][0])

@views.route("/funktion-drei/help")
def fk3_help():
    return render_template("fk3help.html", current_user=current_user)

@views.route("/offene-bereiche", methods=["GET", "POST"])
def offene_bereiche():
    bereiche = db.records("SELECT bereichID, bereichName FROM sarguhl_bereich.bereich WHERE status = %s ORDER BY bereichID desc", 0)
    c_bereiche = db.records("SELECT bereichID, bereichName FROM sarguhl_bereich.bereich WHERE status = %s ORDER BY bereichID desc", 1)
    db.commit()

    print(bereiche)

    return render_template("offene_bereiche.html", bereiche=bereiche, c_bereiche=c_bereiche, current_user=current_user)

@views.route("/offene-bereiche/add", methods=["GET", "POST"])
def add_entry():
    if request.method == 'POST':
        print("Adding DB")

        requ = request.get_json(force=True)
        bereich_nummer = requ["bereich_nummer"]
        bereich_name = requ["bereich_name"]
        pw = requ["sendMessage"]
        if int(bereich_nummer) is None:   
            return
        if str(bereich_name) is None:
            return

        if pw == "1234":
            db.execute("INSERT IGNORE INTO bereich (bereichID, bereichName) VALUES (%s, %s)", int(bereich_nummer), str(bereich_name))
            db.commit()
        else:
            return

    return "ok"

@views.route("/offene-bereiche/delete", methods=["GET", "POST"])
def declined_post():
    if request.method == 'POST':
        declined = request.get_json(force=True)
        delete_all = declined["declined"]
        psw = declined["sendMessage"]
        if psw == "1234":
            db.execute("TRUNCATE TABLE bereich")
            db.commit()
        else:
            return

    return "ok"

@views.route("/offene-bereiche/rev", methods=["GET", "POST"])
def resolve_bereich():
    if request.method == "POST":
        bereiche = db.records("SELECT bereichID, bereichName FROM sarguhl_bereich.bereich WHERE status = %s ORDER BY bereichID desc", 0)
        c_bereiche = db.records("SELECT bereichID, bereichName FROM sarguhl_bereich.bereich WHERE status = %s ORDER BY bereichID desc", 1)
        db.commit()
        status = 1
        rev = request.get_json(force=True)
        bereichId = rev["bereichId"]
        for current in bereiche:
            print(current[0])
            if current[0] == int(bereichId):
                status = 1
        for current in c_bereiche:
            if current[0] == int(bereichId):
                print(current[0])
                print(bereichId)
                status = 0

        db.execute("UPDATE bereich SET status = %s WHERE bereichID = %s", status, bereichId)
        db.commit()

    return "ok"

@views.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    result = User.query.all()
    if request.method == 'POST':
        print("postmethod active")
        status = request.get_json()
        note = status["note"]
        title = status["title"]
        status = status["status"]
        print(note, title, status)
        
        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, tag=status,title=title)
            database.session.add(new_note)
            database.session.commit()
            flash('Note added!', category='success')
    if current_user.user_state == "admin":      
        return render_template("admin.html", user=current_user, users = result, current_user=current_user)
    else: render_template("login.html")

@views.route("/admin/updateappinfo", methods=["POST"])
def admin_updateappinfo():
    if request.method == "POST":
        version_request = request.get_json()
        version = version_request["id"]
        if len(version) <= 3:
            flash("Version is too short!", category='error')
        else:
            db.execute("UPDATE appinfo SET version = %s WHERE versionId = 1", version)
            db.commit()

    return "ok"

@views.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user_name = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        print("lololol")
        user = request.get_json()
        type = user["type"]

        user = User.query.filter_by(id=user_id).first()
        if not user:
            flash("Email already exists.", category='error')
        # elif len(email) < 4:
        #     flash('Email must be greater than 3 characters.', category='error')
        # elif len(name) < 2:
        #     flash('First name must be greater than 1 character.', category='error')
        else:
            # new_user = User(email=email, first_name=name)
            database.engine.execute(f"UPDATE user SET user_state = ? WHERE user.id = ?", type, user_id)
            database.session.commit()
            return redirect(url_for("views.admin"))

    if current_user.user_state == "admin": 
        return render_template("edit_user.html", user_id=user_id, current_user=current_user, user=user_name)
    else: render_template("login.html")

@views.route("/edit/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    if current_user.user_state != "admin":
        return
    else:
        if request.method == "POST":
            user = request.get_json()
            userId = user["user_id"]

            user_exists = User.query.filter_by(id=userId).first()
            if not user:
                flash("User doesn't exist!")
            else:
                database.engine.execute("DELETE FROM user WHERE user.id = ?", user_id)
                database.session.commit()
                return redirect(url_for("views.admin"))
        
    return "ok"


@views.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
       