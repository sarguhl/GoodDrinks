import re
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
import random

views = Blueprint('views', __name__)

def step_calculator(zahl, ware_preis, letzte_preis):
    output_text = 0
    try:
        ergebnis = zahl * float(ware_preis)
        if ergebnis == 0:
            output_text = letzte_preis
            return output_text
        else:
            output_text = round(ergebnis, 2)
            return output_text
    except ValueError:
        output_text = letzte_preis
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
        höhe = request.form.get("zahl2")
        tiefe = request.form.get("zahl3")

        if breite == None:
            breite = 0
        elif breite == "":
            breite = 0

        if höhe == None:
            höhe = 0
        elif höhe == "":
            höhe = 0

        if tiefe == None:
            tiefe = 0
        elif tiefe == "":
            tiefe = 0

        try:
            ergebnis = int(breite) * kasten + int(höhe) * flaschen + int(tiefe) * bier_flaschen
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
    letzte_preis = 0
    output_text = 0
    ware_preis = 0

    if request.method == "POST":
        ware_preis = request.form.get("ware_preis")

        if request.form.get('submit_button', False) == 'x1':
            output_text = step_calculator(1,ware_preis, letzte_preis)

        elif request.form.get('submit_button', False) == 'x2':
            output_text = step_calculator(2,ware_preis, letzte_preis)

        elif request.form.get('submit_button', False) == 'x3':
            output_text = step_calculator(3,ware_preis, letzte_preis)

        elif request.form.get('submit_button', False) == 'x5':
            output_text = step_calculator(5,ware_preis, letzte_preis)

        elif request.form.get('submit_button', False) == 'x10':
            output_text = step_calculator(10,ware_preis, letzte_preis)
        
        elif request.form.get('submit_button', False) == "clear":
            ware_preis = 0
            output_text = 0


    return render_template("funktion_two.html", ergebnis=output_text, ware_preis=ware_preis)

@views.route("/funktion-drei", methods=["GET","POST"])
def funktion_three():
    output_text = ""
    
    if request.method == "POST":
        breite = request.form.get("zahl1")
        höhe = request.form.get("zahl2")
        tiefe = request.form.get("zahl3")
        ware_preis = request.form.get("ware_preis")

        if breite == None:
            breite = 0
        elif breite == "":
            breite = 0

        if höhe == None:
            höhe = 0
        elif höhe == "":
            höhe = 0

        if tiefe == None:
            tiefe = 0
        elif tiefe == "":
            tiefe = 0

        try:
            ergebnis = int(breite) * int(höhe) * int(tiefe) * float(ware_preis)
            if ergebnis == 0:
                output_text = "Es wurden keine Zahlen eingegeben."
            # Print to the Screen
            else:
                output_text = f"{round(ergebnis, 2)}€ | {int(breite)*int(höhe)*int(tiefe)} Gegenstände"
        except ValueError:
            output_text = ""

    return render_template("funktion_three.html", ergebnis=output_text)