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
    posts = db.execute(
        'SELECT * FROM posts WHERE author = ? ORDER BY created DESC LIMIT 200', (session.get('user_id'),)
    )
    return render_template("feed/view.html", posts=posts)

@bp.route('/<user_id>')
def getPostsBy(user_id):
    posts = db.execute(
        'SELECT * FROM posts WHERE author = ? AND anon = FALSE ORDER BY created DESC LIMIT 200', (user_id,)
    )

    return render_template("feed/view.html", posts=posts)

@bp.route('/discover')
def getAllPosts():
    posts = db.execute(
        'SELECT * FROM posts ORDER BY created DESC LIMIT 200', (user_id,)
    )

    return render_template("feed/view.html", posts=posts)
