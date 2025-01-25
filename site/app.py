import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from models import db
from db_connect_func import get_and_save_oceanarium_by_id
from login_register import check_if_email_correct, anti_sql_injection_login_check, checking_if_login_correct, check_email_exists, add_user_to_db, get_user_from_db

app = Flask(__name__)
app.secret_key = 'sekretny_klucz'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
db.init_app(app)

# Strona główna
@app.route('/')
def home():
    #Obejscie przez brak czasu
    session['oceanarium_id'] = 1
    get_and_save_oceanarium_by_id(int(session['oceanarium_id']))
    return render_template('main.html', active_page='home')

# Strona akwariów
@app.route('/aquariums')
def aquariums():
    return render_template('aquariums.html', active_page='aquariums')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        if checking_if_login_correct(login, password) and anti_sql_injection_login_check(login, password):
            session['logged_in'] = True
            user_info = get_user_from_db(login)
            session['username'] = user_info.Nazwa
            session['email'] = user_info.Email
            session['czyPracownil'] = user_info.czyPracownik
            return redirect(url_for('user_page'))
        else:
            wrong_login = "Wrong username or password"
            return render_template('login.html', wrong_login=wrong_login)
    return render_template('login.html')

# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register(confirm_password=None):
    if request.method == 'POST':
        login = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #wczytanie z pamieci loginu przed errorem
        if login == "" and session.get('input_username') != None:
            login = session.get('input_username')
        else:
            session['input_username'] = login

        input_username = login
        #wczytanie z pamieci emaila przed errorem
        if email == "" and session.get('input_email') != None:
            email = session.get('input_email')
        else:
            session['input_email'] = email

        if check_if_email_correct(email):
            input_mail = email
        else:
            return render_template('register.html', input_username=input_username, input_mail="Email",
                                   wrong_register="Email is incorrect")
        if checking_if_login_correct(login, None):
            return render_template('register.html', input_username="Username", input_mail="Email",
                                   wrong_register='Account already exists')
        elif check_email_exists(email):
            return render_template('register.html', input_username=input_username,
                                   wrong_register='Email already exists')
        else:
            if password == confirm_password:
                was_successful = add_user_to_db(login, email, password)
                if was_successful:
                    return redirect(url_for('login'))
                else:
                    return "An error occurred during login"
            else:
                return render_template('register.html', input_username=input_username, input_mail=input_mail,
                                       wrong_register='Passwords do not match. Please try again.')
    return render_template('register.html', input_username="Username", input_mail="Email")

# Panel pracownika
@app.route('/employee')
def employee():
    if not session.get('logged_in') or session.get('role') != 'employee':
        return redirect(url_for('login'))
    return render_template('employee.html', active_page='employee')

# Kupno biletów
@app.route('/tickets')
def tickets():
    if not session.get('logged_in') or session.get('role') != 'customer':
        return redirect(url_for('login'))
    return render_template('tickets.html', active_page='tickets')

if __name__ == '__main__':
    app.run(debug=True)
