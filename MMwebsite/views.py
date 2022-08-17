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
        topic = request.form.get('topic')
        date = request.form.get('date')
        dateCompletion = request.form.get('dateCompletion')
        raisedBy = request.form.get('raisedBy')
        absentees = request.form.get('absentees')
        actionBy = request.form.get('actionBy')
        required = request.form.get('required')
        information = request.form.get('information')
        minute = [topic, date, dateCompletion, raisedBy, absentees, actionBy, required, information]
        
        if len(required) < 1:
            flash('Minute is too short!', category='error')
        else:
            new_minute = Minute(user_id=current_user.id, topic=topic, date=date, dateCompletion=dateCompletion, raisedBy=raisedBy, absentees=absentees, actionBy=actionBy, required=required, information=information)
            db.session.add(new_minute)
            db.session.commit()
            flash('Minute added', category='success')
    
    return render_template ("home.html", user=current_user)

@views.route('/delete-minute', methods=['POST']) #delete note java function as post
def delete_minute(): #function
    minute = json.loads(request.data)
    minuteId = minute['minuteId']
    minute = Minute.query.get(minuteId)
    if minute: #if minute found
        if minute.user_id == current_user.id: #security check
            db.session.delete(minute) #delete note
            db.session.commit() #commit db.session action
            return jsonify({})

    '''
    minute = json.loads(request.minute)
    minuteId = minute['noteId']
    minute = Minute.query.get(minute.Id)
    
    minutesId = Minute.id
    record = Minute.query.filter_by(minuteId=minuteId).first()
    db.session.delete(record)
    '''