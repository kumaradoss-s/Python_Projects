from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required

main_routes = Blueprint('main_routes', __name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


# @app.routes("/")
# @app.routes("login", methods=['GET', 'POST'])
@main_routes.route("/")
@main_routes.route("/home")
def home():
    return render_template('home.html', posts=posts)


@main_routes.route("/about")
def about():
    return render_template('about.html', title='About')


@main_routes.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_routes.home"))
    form = RegistrationForm()
    # db.create_all()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", 'success')
        return redirect(url_for('main_routes.login'))
    return render_template('register.html', title='Register', form=form)


@main_routes.route("/login", methods=['GET', 'POST'])
# @app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_routes.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main_routes.home"))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@main_routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main_routes.home"))


@main_routes.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
