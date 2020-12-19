import functools

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

        try:
            db.execute(
                'INSERT INTO profiles (user, firstname, lastname, gender, bio, pronouns, age, birthday) VALUES(?, ?, ?, ?, ?, ?, ?)',
                (user, firstname, lastname, gender, bio, pronouns, age, birthday)
            )
        except:
            return apology("Something went wrong! Please try again.", 500)

        profile = db.execute(
            'SELECT firstname, lastname, gender, bio, pronouns, age, birthday FROM profiles WHERE user = ?', (user,)
        )

        session['user_profile'] = profile
        print(profile)
        return redirect(url_for(profile.me))

    return render_template("profile/edit.html", profile=session.get('user_profile'), create=True)

@bp.route('/<username>')
def user_profile(username):
    profile = db.execute(
        'SELECT user, firstname, lastname, gender, pronouns, age, birthday FROM profiles WHERE user = (SELECT id FROM users WHERE username = ?)', (username,)
    ).fetchone()

    if not profile:
        return apology("Could not get requested content", 404)
    
    return render_template("profile/view.html", profile=profile)

@bp.route('/me')
@login_required
def my_profile(): 
    profile = session.get('user_profile')
    return render_template("profile/view.html", profile=profile)

@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit_profile():
    if request.method == 'POST':
        user = session.get('user_id')
        queries = request.form.get("queries")
        try:
            for(let q in queries)
            {
                db.execute(
                    'UPDATE profiles SET ' + q.col + ' = ? WHERE user = ?', (q.val, user,)
                )
            }
        except e as error:
            return apology("Something went wrong! Please try again.", 500)

        session['user_profile'] = db.execute(
            'SELECT firstname, lastname, bio, gender, age, pronouns, birthday FROM profiles WHERE user = ?', (user,)
        )

        return redirect(url_for('profile.me'))

    return render_template("profile/edit.html", profile=session.get('user_profile'))
