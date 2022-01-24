#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
import random

views = Blueprint('views', __name__)

def step_calculator(zahl, ware_preis):
    try:
        ergebnis = zahl + int(ware_preis)
        if ergebnis == 0:
            return ergebnis
        else:
            return ergebnis
    except ValueError:
        return ergebnis

def leergut_berechnung():
    pass

def volumen_berechnung(breite, hoehe, tiefe, lose, ware_preis):
    try:
        print("foo 2")
        if ware_preis is  0:
            ergebnis = int(breite)*int(hoehe)*int(tiefe) + int(lose)
            output_text = str(ergebnis)
            return output_text

        else:
            ergebnis = int(breite) * int(hoehe) * int(tiefe) * float(ware_preis) + int(lose)
            output_text = f'{round(ergebnis, 2)}€ | {int(breite)*int(hoehe)*int(tiefe)}'
            return output_text
    except ValueError:
        output_text = ""
        return output_text

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@views.route("/funktion-eins", methods=["GET","POST"])
def funktion_one():
    output_text = ""

    kasten = 1.50
    flaschen = 0.15
    bier_flaschen = 0.08
    
    if request.method == "POST":
        breite = request.form.get("zahl1")
        hoehe = request.form.get("zahl2")
        tiefe = request.form.get("zahl3")

        if breite == None:
            breite = 0
        elif breite == "":
            breite = 0

        if hoehe == None:
            hoehe = 0
        elif hoehe == "":
            hoehe = 0

        if tiefe == None:
            tiefe = 0
        elif tiefe == "":
            tiefe = 0

        try:
            ergebnis = int(breite) * kasten + int(hoehe) * flaschen + int(tiefe) * bier_flaschen
            if ergebnis == 0:
                output_text = "Es wurden keine Zahlen eingegeben."
            # Print to the Screen
            else:
                output_text = f"{round(ergebnis, 2)}€"
        except ValueError:
            output_text = ""

    return render_template("funktion_one.html", ergebnis=output_text)

@views.route("/funktion-zwei", methods=["GET","POST"])
def funktion_two():
    ware_preis = 0

    if request.method == "POST":
        ware_preis = request.form.get("ware_preis")

        if request.form.get('submit_button', False) == 'x1':
            ware_preis = step_calculator(1,ware_preis)

        elif request.form.get('submit_button', False) == 'x2':
            ware_preis = step_calculator(2,ware_preis)

        elif request.form.get('submit_button', False) == 'x5':
            ware_preis = step_calculator(5,ware_preis)

        elif request.form.get('submit_button', False) == 'x10':
            ware_preis = step_calculator(10,ware_preis)
        
        elif request.form.get('submit_button', False) == "clear":
            ware_preis = 0


    return render_template("funktion_two.html", ergebnis=ware_preis, ware_preis=ware_preis)

@views.route("/funktion-drei", methods=["GET","POST"])
def funktion_three():
    output_text = ""
    
    if request.method == "POST":
        breite = request.form.get("zahl1")
        hoehe = request.form.get("zahl2")
        tiefe = request.form.get("zahl3")
        lose = request.form.get("zahl4")
        ware_preis = request.form.get("ware_preis")

        if ware_preis == None:
            ware_preis = 0
        elif ware_preis == "":
            ware_preis = 0

        if breite == None:
            breite = 0
        elif breite == "":
            breite = 0

        if hoehe == None:
            hoehe = 0
        elif hoehe == "":
            hoehe = 0

        if tiefe == None:
            tiefe = 0
        elif tiefe == "":
            tiefe = 0
        
        if lose == None:
            lose = 0
        elif lose == "":
            lose = 0
        
        output_text = volumen_berechnung(breite, hoehe, tiefe, lose, ware_preis)

    return render_template("funktion_three.html", ergebnis=output_text)

@views.route("/hilfe", methods=["GET"])
def hilfe():
    return render_template("help.html")

@views.route("/impressum", methods=["GET"])
def impressum():
    return render_template("impressum.html")