#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
import random

from website.db import db

views = Blueprint('views', __name__)

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@views.route("/funktion-eins", methods=["GET","POST"])
def funktion_one():
    return render_template("funktion_one.html")

@views.route("/funktion-zwei", methods=["GET","POST"])
def funktion_two():
    return render_template("funktion_two.html")

@views.route("/funktion-drei", methods=["GET","POST"])
def funktion_three():
    return render_template("funktion_three.html")

@views.route("/hilfe", methods=["GET"])
def hilfe():
    return render_template("help.html")

@views.route("/impressum", methods=["GET"])
def impressum():
    return render_template("impressum.html")

@views.route("/blog")
def blog():
    return render_template("blog.html")

@views.route("/funktion-drei/help")
def fk3_help():
    return render_template("fk3help.html")

@views.route("/offene-bereiche", methods=["GET", "POST"])
def offene_bereiche():
    bereiche = db.records("SELECT bereichID, bereichName FROM sarguhl_bereich.bereich WHERE status = %s ORDER BY bereichID desc", 0)
    c_bereiche = db.records("SELECT bereichID, bereichName FROM sarguhl_bereich.bereich WHERE status = %s ORDER BY bereichID desc", 1)
    db.commit()

    print(bereiche)

    return render_template("offene_bereiche.html", bereiche=bereiche, c_bereiche=c_bereiche)

@views.route("/offene-bereiche/add", methods=["GET", "POST"])
def add_entry():
    if request.method == 'POST':
        print("Adding DB")

        requ = request.get_json(force=True)
        bereich_nummer = requ["bereich_nummer"]
        bereich_name = requ["bereich_name"]
        pw = requ["sendMessage"]
        if int(bereich_nummer) is None:
            print("lmao")
            return
        if str(bereich_name) is None:
            print("lmao")
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