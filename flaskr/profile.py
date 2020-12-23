import functools
import json
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from SafeSpace.db import get_db

from SafeSpace.auth import login_required, apology

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def createProfile():
    if request.method == 'POST':
        db = get_db()
        user = session.get('user_id')
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        bio = request.form['bio']
        gender = request.form['gender']
        pronouns = request.form['pronouns']
        age = request.form['age']
        birthday = request.form['birthday']

        if not db.execute(
            'INSERT INTO profiles (user, firstname, lastname, gender, bio, pronouns, age, birthday) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
            (user, firstname, lastname, gender, bio, pronouns, age, birthday)
        ):
            return apology("Something went wrong! Please try again.", 500)
        db.commit()

        columns = ['firstname', 'lastname', 'gender', 'bio', 'pronouns', 'age', 'birthday']
        profile = dict(zip(columns, db.execute(
            'SELECT firstname, lastname, gender, bio, pronouns, age, birthday FROM profiles WHERE user = ?', (user,)
        ).fetchone()))

        return redirect(url_for('profile.myProfile'))

    profile = dict(zip(['firstname', 'lastname', 'gender', 'bio', 'pronouns', 'age', 'birthday'], 
    db.execute(
        'SELECT firstname, lastname, gender, bio, pronouns, age, birthday FROM profiles WHERE user = (SELECT id FROM users WHERE username = ?)', (session.get('user_id'),)
    ).fetchone()))
    return render_template("profile/edit.html", profile=None if not profile else profile, create=(True if not profile else False))  

@bp.route('/<username>')
def userProfile(username):
    db = get_db()
    user = db.execute(
        'SELECT id FROM users WHERE username = ?', (username,)
    ).fetchone()

    if not user:
        return apology("Page not found", 404)

    profile = db.execute(
        'SELECT firstname, lastname, gender, bio, pronouns, age FROM profiles WHERE user = ?', (user[0],)
    ).fetchone()

    if not profile:
        return apology("Page not found", 404)
    
    profile = dict(zip(['firstname', 'lastname', 'gender', 'bio', 'pronouns', 'age'], profile), birthday=db.execute('SELECT birthday FROM profiles WHERE user = ?', (user[0],)).fetchone()[0])

    return render_template("profile/view.html", profile=profile, user=username)

@bp.route('/me')
@login_required
def myProfile(): 
    db = get_db()
    profile = db.execute(
        'SELECT firstname, lastname, gender, bio, pronouns, age FROM profiles WHERE user = ?', (session.get('user_id'),)
    ).fetchone()
    if not profile:
        return redirect(url_for('profile.createProfile'))
    
    profile = dict(zip(['firstname', 'lastname', 'gender', 'bio', 'pronouns', 'age'], profile), birthday=db.execute('SELECT birthday FROM profiles WHERE user = ?', (session.get('user_id'),)).fetchone()[0])
    return render_template("profile/view.html", profile=profile, user=session.get('user_name'))

@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def editProfile():
    db = get_db()
    if request.method == 'POST':
        user = session.get('user_id')
        queries = json.loads(request.form["queries"])

        try:
            for q in queries:
                value = requst.form[q]
                if q == 'birthday':
                    value = request.form[q].date
                db.execute(
                    'UPDATE profiles SET ' + q + ' = ? WHERE user = ?', (value, user,)
                )
        except:
            return apology("Something went wrong! Please try again.", 500)
        
        columns = ['firstname', 'lastname', 'bio', 'gender', 'age', 'pronouns', 'birthday']
        db.commit()

        return redirect(url_for('profile.myProfile'))

    profile = dict(zip(['firstname', 'lastname', 'gender', 'bio', 'pronouns', 'age', 'birthday'], 
    db.execute(
        'SELECT firstname, lastname, gender, bio, pronouns, age, birthday FROM profiles WHERE user = ?', (session.get('user_id'),)
    ).fetchone()))

    return render_template("profile/edit.html", profile=profile, create=False)
