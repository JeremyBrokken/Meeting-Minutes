#store standard roots, users can go to (other than auth i.e. login)
from flask import Blueprint, render_template, request, flash, jsonify #render_template allows to render a template created
#Goal, define this file is a blueprint, of app = has roots/URLs inside of it
from flask_login import login_required, current_user
from . models import Minute
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) #when navigating to main page(hitting this root), run whats inside home(function) [decorator]
@login_required #homepage cannot be accessed unless logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Minute is too short!', category='error')
        else:
            new_minute = Minute(data=note, user_id=current_user.id)
            db.session.add(new_minute)
            db.session.commit()
            flash('Note added', category='success')
    
    return render_template ("home.html", user=current_user)

@views.route('/delete-note', methods=['POST']) #delete note java function as post
def delete_note(): #function
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note: #if note found
        if note.user_id == current_user.id: #security check
            db.session.delete(note) #delete note
            db.session.commit() #commit db.session action
            return jsonify({})
            