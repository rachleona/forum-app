import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from SafeSpace.db import get_db

from SafeSpace.auth import login_required, apology

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/<post_id>', methods=('POST'))
@login_required
def comment(post_id):  
    body = request.form["body"]
    anon = request.form["anon"]

    try:
        db.execute(
            'INSERT INTO comments (author, body, anon, likes, post) VALUES (?, ?, ?, ?, ?)', 
            (session.get('user_id'), body, anon, [], post_id)
        )
    except e as error:
        return apology("Something went wrong! Please try again.", 500)

    return db.execute( 
        'SELECT * FROM comments WHERE author = ? AND post_id = ? ORDER BY created DESC', (session.get('user_id'), post_id,)
    ).fetchone()

@bp.route('/edit/<comment_id>', methods=('POST'))
@login_required
def editComment(comment_id):
    comment = db.execute(
        'SELECT * FROM comments WHERE id = ?', (comment_id,)
    ).fetchone()

    if not comment['author'] == session.get('user_id'):
        return apology("Unauthorized access", 403)

    queries = json.load(request.form["queries"])
    try:
        for q in queries:
            db.execute(
                'UPDATE comments SET ' + q.col + ' = ? WHERE id = ?', (q.val, comment_id,)
            )
        db.execute('UPDATE comments SET edited = CURRENT_TIMESTAMP WHERE id = ?', (comment_id,))
    except e as error:
        return apology("Something went wrong! Please try again.", 500, error)
        
    return db.execute(
        'SELECT * FROM comments WHERE id = ?', (comment_id,)
    ).fetchone()

@bp.route('/like/<comment_id>', methods=('POST'))
@login_required
def likePost(comment_id):
    likes = json.load(request.form["likes"])
    user = session.get('user_id')
    if user in likes:
        list.remove(user)
    else:
        list.append(user)

    try:
        db.execute(
            'UPDATE comments SET likes = ? WHERE id = ?', (likes, comment_id,)
        )
    except e as error:
        return apology("Something went wrong! Please try again.", 500, error)

    return likes

@bp.route('/delete/<comment_id>', methods=('POST'))
@login_required
def deletePost(comment_id):
    comment =  db.execute(
        'SELECT author, post FROM comments WHERE id = ?', (comment_id,)
    ).fetchone()

    if not session.get('user_id') == comment['author']:
        return apology("Unauthorized access", 403)

    try:
        db.execute(
            'DELETE FROM comments WHERE id = ?', (comment_id,)
        )
    except e as error:
        return apology("Something went wrong! Please try again.", 500, error)

    return redirect(url_for(posts[comment['post']]))
