import functools

from datetime import datetime

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
        'SELECT a.id, b.username, a.created, a.title, a.body, a.edited, a.likes, a.anon FROM posts a, users b WHERE a.author = ? AND b.id = a.author ORDER BY created DESC LIMIT 200', (session.get('user_id'),)
    ).fetchall()

    if not posts:
       posts = None
    else:
        arr = []
        for row in posts:
            arr.append(dict(zip(['id', 'author', 'created', 'title', 'body', 'edited', 'likes', 'anon'], row)))
            arr[-1]['created'] = arr[-1]['created'].date()
        posts = arr

    return render_template("feed/view.html", posts=posts, title="Home")

@bp.route('/<username>')
def getPostsBy(username):
    db = get_db()
    posts = db.execute(
        'SELECT a.id, b.username, a.created, a.title, a.body, a.edited, a.likes, a.anon FROM posts a, users b WHERE b.username = ? AND a.anon = FALSE AND b.id = a.author ORDER BY created DESC LIMIT 200', (username,)
    ).fetchall()

    if not posts:
       posts = None
    else:
        arr = []
        for row in posts:
            arr.append(dict(zip(['id', 'author', 'created', 'title', 'body', 'edited', 'likes', 'anon'], row)))
            arr[-1]['created'] = arr[-1]['created'].date()
        posts = arr

    return render_template("feed/view.html", posts=posts, title=username + "'s posts")

@bp.route('/discover')
def getAllPosts():
    db = get_db()
    posts = db.execute(
        'SELECT a.id, b.username, a.created, a.title, a.body, a.edited, a.likes, a.anon FROM posts a, users b WHERE b.id = a.author ORDER BY created DESC LIMIT 200',
    ).fetchall()

    if not posts:
       posts = None
    else:
        arr = []
        for row in posts:
            arr.append(dict(zip(['id', 'author', 'created', 'title', 'body', 'edited', 'likes', 'anon'], row)))
            arr[-1]['created'] = arr[-1]['created'].date()
        posts = arr

    return render_template("feed/view.html", posts=posts, title="discover")
