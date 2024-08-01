from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from config import Config
from models import db, User
import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

logging.basicConfig(level=logging.DEBUG)

# Flag to check if the database has been created
database_initialized = False

@app.before_request
def create_tables():
    global database_initialized
    if not database_initialized:
        db.create_all()
        database_initialized = True

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            logging.debug(f"Encrypted password (login): {user.password}")  # Log encrypted password
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logging.debug(f"Encrypted password (register): {user.password}")  # Log encrypted password
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/users')
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'password': user.password} for user in users]
    return jsonify(user_list)

@app.route('/usage')
def usage():
    return render_template('usage.html')

@app.route('/algorithm')
def algorithm():
    return render_template('algorithm.html')

@app.route('/implementation')
def implementation():
    return render_template('implementation.html')

@app.route('/security')
def security():
    return render_template('security.html')

if __name__ == '__main__':
    app.run(debug=True)
