from flask import Blueprint, render_template, request, flash, jsonify,redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from flask import Flask
from . import db
from hashids import Hashids
import json
import sqlite3
views = Blueprint('views', __name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
app = Flask(__name__)
app.config['SECRET_KEY'] = "66e33578ba4455ed65c032fc9f0e2fff"

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
#-------------------------------------------------------------------------------------------------------
@views.route('/add-url', methods=('GET', 'POST'))
def add_url():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('please enter a URL!')
            return redirect(url_for('views.add_url'))
        
        ip_addr = request.remote_addr
        referrer = request.headers.get('Referer')
        url_data = conn.execute('INSERT INTO urls (original_url,ip,country) VALUES (?,?,?)', (url,ip_addr,referrer))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('search.html', short_url=short_url,user=current_user)
    
    return render_template('search.html',user=current_user)
#-------------------------------------------------------------------------------------------------
@views.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()
    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks FROM urls'' WHERE id = (?)', (original_id,)).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']
        referrer = request.headers.get('Referer')
        conn.execute('UPDATE urls SET clicks = ?,country=? WHERE id = ?',(clicks+1,referrer,original_id))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL',category='error')
        return redirect(url_for('views.home'))


@views.route('/stats')
def stats():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id, created, original_url, clicks,ip,country FROM urls').fetchall()
    conn.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)

    return render_template('analytics.html', urls=urls,user=current_user)