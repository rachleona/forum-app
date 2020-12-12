import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from SafeSpace.db import get_db

from SafeSpace.auth import login_required, apology

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('/<post_id>')
@login_required
def viewPost(post_id):
    post = db.execute(
        'SELECT * FROM posts WHERE id = ? ORDER BY created', (post_id,)
    ).fetchone()

    comments = db.execute(
        'SELECT * FROM comments WHERE post = ?', (post_id,)
    )

    render_template("posts/view.html", post=post)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def createPost():
    if request.method == 'POST':
        title = request.form.get("title")
        body = request.form.get("body")
        anon = request.form.get("anon")

        db.execute(
            'INSERT INTO posts (author, title, body, likes, anon) VALUES( ?, ?, ?, ?, ? )',
            (session.get("user_id"), title, body, [], anon)
        )

        return redirect(url_for(feed.me))

    render_template("posts/create.html")

@bp.route('/edit/<post_id>', methods=('GET', 'POST'))
@login_required
def editpost(post_id):
    post = db.execute(
        'SELECT * FROM posts WHERE id = ? ORDER BY created', (post_id,)
    ).fetchone()

    if request.method == 'POST':
        #todo
        return redirect(url_for(posts[post_id]))
    
    if not post['author'] == session.get('user_id'):
        return apology("Unauthorized access", 403)

    render_template("posts/create.html", post=post)

@bp.route('/by/<user_id>')
@login_required
def getPostBy(user_id):
    posts = db.execute(
        'SELECT * FROM posts WHERE author = ? ORDER BY created', (user_id,)
    )

    render_template("feed/view.html", posts=posts)
