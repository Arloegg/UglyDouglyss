from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_comment(id, check_author=True):
    comment = get_db().execute(
        'SELECT c.id, p.id, c.body, c.created, c.author_id, username'
        ' FROM comment c'
        ' JOIN post p ON c.post_id = p.id'
        ' JOIN user u ON c.author_id = u.id'
        ' WHERE c.post_id = ?'
        ' ORDER BY c.created ASC',
        (id,)
    ).fetchall()

    return comment

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, p.body, p.created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY p.created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/<int:id>/comment', methods=('GET', 'POST'))
@login_required
def comments(id):
    post = get_post(id, check_author=False)
    
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        error = None
        
        if not comment_text:
            error = 'Text is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (post_id, author_id, body)'
                ' VALUES (?, ?, ?)',
                (id, g.user['id'], comment_text)
            )
            db.commit()
            return redirect(url_for('blog.comments', id=id))
    
    db = get_db()
    comments = db.execute(
        'SELECT c.id, p.id, c.body, c.created, c.author_id, username'
        ' FROM comment c'
        ' JOIN post p ON c.post_id = p.id'
        ' JOIN user u ON c.author_id = u.id'
        ' WHERE c.post_id = ?'
        ' ORDER BY c.created ASC',
        (id,)
    ).fetchall()
    return render_template('blog/comments.html', post=post, comments=comments)

@bp.route('/<int:postid>/comment/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_comment(postid, id):
    post = get_post(postid, check_author=False)
    db = get_db()
    comment = db.execute(
        'SELECT c.id, c.body, c.author_id FROM comment c WHERE c.id = ?',
        (id,)
    ).fetchone()
    
    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")
    
    if comment['author_id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':
        body = request.form['body']
        error = None

        if not body:
            error = 'Text is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE comment SET body = ?'
                ' WHERE id = ?',
                (body, id)
            )
            db.commit()
            return redirect(url_for('blog.comments', id=postid))

    return render_template('blog/updateComment.html', post=post, comment=comment)

@bp.route('/<int:postid>/comment/<int:id>/delete', methods=('POST',))
@login_required
def delete_comment(postid, id):
    get_post(postid, check_author=False)
    db = get_db()
    comment = db.execute(
        'SELECT c.author_id FROM comment c WHERE c.id = ?',
        (id,)
    ).fetchone()
    
    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")
    
    if comment['author_id'] != g.user['id']:
        abort(403)
    
    db.execute('DELETE FROM comment WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.comments', id=postid))

