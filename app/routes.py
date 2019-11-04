from flask import url_for, request, render_template, redirect
from flask_login import login_required, login_user, logout_user, current_user
from app import db, app
from app.models import User, Article


def get_user(id=None, login=None):
    return User.query.filter_by(id=id).first() if id != None else User.query.filter_by(login=login).first()


def auth(login, password):
    user = get_user(login=login)
    if user != None:
        if user.check_password(password):
            return True
        else:
            return False


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('index.html', articles=current_user.articles.all(), title='Home', user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        print(auth(request.form.get('alias'), request.form.get('password')))
        if auth(request.form.get('alias'), request.form.get('password')):
            login_user(get_user(login=request.form.get('alias')))
            return redirect('/home')
    return render_template('login.html', title='Log in')


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')


@app.route('/post', methods=['POST'])
def post():
    if current_user.is_authenticated:
        if request.method == 'POST':
            a = Article(title=request.form.get('title'), body=request.form.get('body'), author=current_user)
            db.session.add(a)
            db.session.commit()
    return redirect('/home')


@app.route('/delete/<int:id>')
def delete(id):
    if current_user.is_authenticated:
        db.session.delete(Article.query.filter_by(id=id).first())
        db.session.commit()
    return redirect('/home')
