from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
from app import db
from app.models import User, Review

user = Blueprint("user", __name__, template_folder="templates")


@user.route('/register', methods=['GET', 'POST'])
def register():
    """Register user to database and logs in the user"""
    form = RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=False)
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in the user"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash("Login unsuccessful. Please check email and password.")
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    """Redirects user to homepage after log out"""
    logout_user()
    return redirect(url_for('main.index'))


@user.route('/delete_comment', methods=['POST'])
@login_required
def delete_comment():
    """Deletes comment from database"""
    next_url = request.form.get('next_url')
    comment_id = request.args.get('comment_id')
    print(comment_id)
    comment_to_delete = Review.query.get_or_404(comment_id)
    if current_user.is_anonymous or comment_to_delete.user_id != current_user.id:
        abort(403)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(next_url)


@user.route('/edit_comment', methods=['POST'])
@login_required
def edit_comment():
    """Edits comment in database"""
    next_url = request.form.get('next_url')
    comment_id = request.args.get('comment_id')
    comment_to_edit = Review.query.get_or_404(comment_id)
    if current_user.is_anonymous or comment_to_edit.user_id != current_user.id:
        abort(403)
    comment_to_edit.body = request.form.get('edited_comment')
    db.session.commit()
    return redirect(next_url)

