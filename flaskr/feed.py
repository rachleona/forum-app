import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from SafeSpace.db import get_db

from SafeSpace.auth import login_required, apology

bp = Blueprint('feed', __name__, url_prefix='/feed')


@bp.route('/me')
@login_required
def myFeed():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM posts WHERE author = ? ORDER BY created DESC LIMIT 200', (session.get('user_id'),)
    ).fetchall()

    if not posts:
       posts = None
    else:
        arr = []
        for row in posts:
            arr.append(dict(zip(['id', 'author', 'created', 'title', 'body', 'edited', 'likes', 'anon'], row)))
        posts = arr

    return render_template("feed/view.html", posts=posts, title="Home")

@bp.route('/<user_id>')
def getPostsBy(user_id):
    db = get_db()
    posts = db.execute(
        'SELECT * FROM posts WHERE author = ? AND anon = FALSE ORDER BY created DESC LIMIT 200', (user_id,)
    ).fetchall()

    if not posts:
       posts = None
    else:
        arr = []
        for row in posts:
            arr.append(dict(zip(['id', 'author', 'created', 'title', 'body', 'edited', 'likes', 'anon'], row)))
        posts = arr

    return render_template("feed/view.html", posts=posts, title=user_id + "'s posts")

@bp.route('/discover')
def getAllPosts():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM posts ORDER BY created DESC LIMIT 200',
    ).fetchall()

    if not posts:
       posts = None
    else:
        arr = []
        for row in posts:
            arr.append(dict(zip(['id', 'author', 'created', 'title', 'body', 'edited', 'likes', 'anon'], row)))
        posts = arr

    return render_template("feed/view.html", posts=posts, title="discover")
