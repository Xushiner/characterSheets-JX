from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.character import Character


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(data), characters=Character.get_all())


@app.route('/show/<int:character_id>')
def show_character(character_id):
    data = {
        'id': session['user_id']
    }
    character =Character.get_by_id(character_id)
    return render_template('sheet.html', character=character, user = User.get_by_id(data))


@app.route('/new/character')
def new_character():
    data = {
        'id': session['user_id']
    }
    return render_template('new_sheet.html', user=User.get_by_id(data))


@app.route('/character/create', methods=["POST"])
def create_character():
    data = {
        # "id" : session['id'],
        "name" : request.form['name'],
        "ancestry" : request.form['ancestry'],
        "novice_path" : request.form['novice_path'],
        "expert_path" : request.form['expert_path'],
        "master_path" : request.form['master_path'],
        "level" : request.form['level'],
        "insanity" : request.form['insanity'],
        "corruption" : request.form['corruption'],
        "power" : request.form['power'],
        "strength" : request.form['strength'],
        "agility" : request.form['agility'],
        "intellect" : request.form['intellect'],
        "will" : request.form['will'],
        "perception" : request.form['perception'],
        "speed" : request.form['speed'],
        "size" : request.form['size'],
        "health" : request.form['health'],
        "armor" : request.form['armor'],
        "defense" : request.form['defense'],
        "damage" : request.form['damage'],
        "healing_rate" : request.form['healing_rate'],
        "users_id" : request.form['users_id']
    }
            
    Character.create_character(data)

    return redirect('/dashboard')


@app.route('/edit/<int:character_id>')
def edit_character(character_id):
    character = Character.get_by_id(character_id)
    data = {
        'id': session['user_id']
    }
    return render_template('edit_sheet.html', character=character, user=User.get_by_id(data))


@app.route('/update', methods=["POST"])
def update_character():
    Character.update_character(request.form)

    return redirect("/dashboard")


@app.route('/delete/<int:character_id>')
def delete_by_id(character_id):
    Character.delete_character_by_id(character_id)
    return redirect('/dashboard')
