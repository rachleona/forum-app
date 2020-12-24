import functools
import json
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from SafeSpace.db import get_db

from SafeSpace.auth import login_required, apology

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/<post_id>', methods=['POST'])
@login_required
def comment(post_id): 
    db = get_db() 
    body = request.form["body"]
    anon = request.form["anon"]

    if anon == 'true':
        anon = True
    else:
        anon = False

    if not db.execute(
        'INSERT INTO comments (author, body, anon, likes, post) VALUES (?, ?, ?, ?, ?)', 
        (session.get('user_id'), body, anon, json.dumps([]), post_id)
    ):
        return json.dumps([])

    db.commit()

    comment = dict(zip(['id', 'author', 'post', 'anon', 'created', 'body', 'likes'],
        db.execute( 
            'SELECT a.id, b.username, a.post, a.anon, a.created, a.body, a.likes FROM comments a, users b WHERE a.author = ? AND b.id = a.author AND a.post = ? ORDER BY created DESC', (session.get('user_id'), post_id,)
        ).fetchone()))
    
    comment['created'] = comment['created'].date().strftime('%Y-%m-%d')
    
    return json.dumps(comment)

# @bp.route('/edit/<comment_id>', methods=('POST'))
# @login_required
# def editComment(comment_id):
#     db = get_db()
#     comment = db.execute(
#         'SELECT * FROM comments WHERE id = ?', (comment_id,)
#     ).fetchone()

#     if not comment['author'] == session.get('user_id'):
#         return apology("Unauthorized access", 403)

#     queries = json.load(request.form["queries"])
#     try:
#         for q in queries:
#             db.execute(
#                 'UPDATE comments SET ' + q.col + ' = ? WHERE id = ?', (q.val, comment_id,)
#             )
#         db.execute('UPDATE comments SET edited = CURRENT_TIMESTAMP WHERE id = ?', (comment_id,))
#     except:
#         return apology("Something went wrong! Please try again.", 500)
        
#     return db.execute(
#         'SELECT * FROM comments WHERE id = ?', (comment_id,)
#     ).fetchone()

@bp.route('/like/<comment_id>', methods=['POST'])
@login_required
def likePost(comment_id):
    db = get_db()
    likes = json.loads(request.form["likes"])
    user = session.get('user_id')

    if user in likes:
        likes.remove(user)
    else:
        likes.append(user)

    likes = json.dumps(likes)

    if not db.execute(
        'UPDATE comments SET likes = ? WHERE id = ?', (likes, comment_id,)
    ):
        return request.form["likes"]

    db.commit()

    return likes

@bp.route('/delete/<comment_id>', methods=['POST'])
@login_required
def deletePost(comment_id):
    db = get_db()
    comment =  db.execute(
        'SELECT author, post FROM comments WHERE id = ?', (comment_id,)
    ).fetchone()

    if not session.get('user_id') == comment['author']:
        flash("Unauthorized access")
        return "403"

    if not db.execute(
        'DELETE FROM comments WHERE id = ?', (comment_id,)
    ):
        flash("Something went wrong! Please try again.")
        return "500"

    db.commit()

    return "200"
