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
        'SELECT * FROM posts WHERE id = ?', (post_id,)
    ).fetchone()

    comments = db.execute(
        'SELECT * FROM comments WHERE post = ? ORDER BY created', (post_id,)
    )

    return render_template("posts/view.html", post=post, comments=comments)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def createPost():
    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]
        anon = request.form["anon"]

        try:
            db.execute(
                'INSERT INTO posts (author, title, body, likes, anon) VALUES( ?, ?, ?, ?, ? )',
                (session.get("user_id"), title, body, [], anon)
            )
        except e as error:
            return apology("Something went wrong! Please try again.", 500, error)

        return redirect(url_for(feed.me))

    return render_template("posts/create.html")

@bp.route('/edit/<post_id>', methods=('GET', 'POST'))
@login_required
def editpost(post_id):
    post = db.execute(
        'SELECT * FROM posts WHERE id = ?', (post_id,)
    ).fetchone()

    if not post['author'] == session.get('user_id'):
        return apology("Unauthorized access", 403)

    if request.method == 'POST':
        queries = json.load(request.form["queries"])
        try:
            for q in queries:
                db.execute(
                    'UPDATE posts SET ' + q.col + ' = ? WHERE id = ?', (q.val, post_id,)
                )
            db.execute('UPDATE posts SET edited = CURRENT_TIMESTAMP WHERE id = ?', (post_id,))
        except e as error:
            return apology("Something went wrong! Please try again.", 500, error)
            
        return redirect(url_for(posts[post_id]))

    return render_template("posts/create.html", post=post)

@bp.route('/like/<post_id>', methods=('POST'))
@login_required
def likePost(post_id):
    likes = json.load(request.form["likes"])
    user = session.get('user_id')

    if user in likes:
        list.remove(user)
    else:
        list.append(user)

    try:
        db.execute(
            'UPDATE posts SET likes = ? WHERE id = ?', (likes, post_id,)
        )
    except e as error:
        return apology("Something went wrong! Please try again.", 500, error)

    return likes

@bp.route('/delete/<post_id>', methods=('POST'))
@login_required
def deletePost(post_id):
    author =  db.execute(
        'SELECT author FROM posts WHERE id = ?', (post_id,)
    ).fetchone()['author']

    if not session.get('user_id') == author:
        return apology("Unauthorized access", 403)

    try:
        db.execute(
            'DELETE FROM posts WHERE id = ?', (post_id,)
        )
    except e as error:
        return apology("Something went wrong! Please try again.", 500, error)

    return redirect(url_for(feed.me))
