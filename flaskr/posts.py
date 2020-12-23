import functools
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from SafeSpace.db import get_db

from SafeSpace.auth import login_required, apology

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('/<post_id>')
@login_required
def viewPost(post_id):
    db = get_db()
    post = db.execute(
        'SELECT a.id, a.created, a.title, a.body, a.anon, a.edited, a.likes, b.username FROM posts a, users b WHERE a.id = ? AND b.id = a.author', (post_id,)
    ).fetchone()

    if not post:
        return apology("Page not found", 404)

    post = dict(zip(['id', 'created', 'title', 'body', 'anon', 'edited', 'likes', 'author'], post))

    comments = db.execute(
        'SELECT a.created, a.body, a.post, a.anon, a.likes, b.username FROM comments a, users b WHERE a.post = ? AND b.id = a.author ORDER BY created', (post_id,)
    ).fetchall()

    if comments:
        comments = dict(zip(['created', 'body', 'post', 'anon', 'likes', 'author'], comments))

    return render_template("posts/view.html", post=post)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def createPost():
    if request.method == 'POST':
        db = get_db()
        title = request.form["title"]
        body = request.form["body"]
        anon = False if not request.form.get("anon") else True

        print(title, body, anon)

        if not db.execute(
            'INSERT INTO posts (author, title, body, likes, anon) VALUES( ?, ?, ?, ?, ? )',
            (session.get("user_id"), title, body, json.dumps([]), anon)
        ):
            return apology("Something went wrong! Please try again.", 500)

        db.commit()

        return redirect(url_for('feed.myFeed'))

    return render_template("posts/create.html", create=True, post=None)

@bp.route('/edit/<post_id>', methods=('GET', 'POST'))
@login_required
def editpost(post_id):
    db = get_db()
    if request.method == 'POST':
        queries = json.loads(request.form["queries"])
        try:
            for q in queries:
                if q in request.form:
                    value = request.form[q]
                else:
                    value = False

                db.execute(
                    'UPDATE posts SET ' + q + ' = ? WHERE id = ?', (value, post_id,)
                )
            db.execute('UPDATE posts SET edited = CURRENT_TIMESTAMP WHERE id = ?', (post_id,))
        except:
            return apology("Something went wrong! Please try again.", 500)
            
        db.commit()
        return redirect('/posts/' + post_id)

    post = db.execute(
        'SELECT author, title, body, anon FROM posts WHERE id = ? ', (post_id,)
    ).fetchone()

    if post['author'] != session.get('user_id'):
        return apology("Unauthorized access", 403)

    post = dict(zip(['author', 'title', 'body', 'anon'], post))
    post['id'] = post_id

    return render_template("posts/create.html", create=False, post=post)

@bp.route('/like/<post_id>', methods=['POST'])
@login_required
def likePost(post_id):
    db = get_db()
    print(request.form["likes"])
    likes = json.loads(request.form["likes"])
    user = session.get('user_id')

    if user in likes:
        likes.remove(user)
    else:
        likes.append(user)

    likes = json.dumps(likes)

    if not db.execute(
        'UPDATE posts SET likes = ? WHERE id = ?', (likes, post_id,)
    ):
        flash("Somethings wrong! Please try again later!")
        return request.form["likes"]

    db.commit()
    return likes

@bp.route('/delete/<post_id>', methods=['POST'])
@login_required
def deletePost(post_id):
    db = get_db()
    author =  db.execute(
        'SELECT author FROM posts WHERE id = ?', (post_id,)
    ).fetchone()['author']

    if not session.get('user_id') == author:
        return apology("Unauthorized access", 403)

    try:
        db.execute(
            'DELETE FROM posts WHERE id = ?', (post_id,)
        )
    except:
        return apology("Something went wrong! Please try again.", 500)

    db.commit()

    return redirect(url_for('feed.myFeed'))
