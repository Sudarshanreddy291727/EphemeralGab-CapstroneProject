import uuid
from flask import render_template, url_for, flash, redirect, session, request
from app import app, db, socketio
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_socketio import emit

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['connection_id'] = user.connection_id
            return redirect(url_for('chat'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            connection_id = str(uuid.uuid4())
            user = User(username=form.username.data, password=form.password.data, connection_id=connection_id)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully! Your connection ID is {connection_id}', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already taken. Please choose another one.', 'danger')
    return render_template('register.html', form=form)

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        connection_id = request.form.get('connection_id')
        user = User.query.filter_by(connection_id=connection_id).first()
        if user:
            session['connection_id'] = connection_id
            return redirect(url_for('chat'))
        else:
            flash('Invalid Connection ID', 'danger')
    return render_template('connect.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    connection_id = session.get('connection_id')
    if not connection_id:
        return redirect(url_for('connect'))

    return render_template('chat.html', connection_id=connection_id)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    emit('message', msg, broadcast=True)
