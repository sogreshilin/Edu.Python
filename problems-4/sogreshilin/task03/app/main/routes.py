from app.main import bp
from app import app, db
from flask import render_template, flash, redirect, url_for, jsonify, request, Response
from flask_login import login_required, current_user

from app.models import User


@app.before_first_request
def setup():
    db.create_all()


@bp.route('/')
@login_required
def index():
    users = list()
    users = list(map(lambda user: user.user_name,
                User.query.filter(User.registration_time > current_user.registration_time).all()))
    print(users)
    return render_template('index.html', users=users, the_last_registered_one=not users)
