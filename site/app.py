import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, session, url_for
from flask import Flask, render_template, request, redirect, url_for, session
from db_connect_func import get_and_save_oceanarium_by_id

app = Flask(__name__)
app.secret_key = 'sekretny_klucz'

# Strona główna
@app.route('/')
def home():
    #Obejscie przez brak czasu
    session['oceanarium_id'] = 1
    get_and_save_oceanarium_by_id(session, session['oceanarium_id'])
    return render_template('main.html', active_page='home')

# Strona akwariów
@app.route('/aquariums')
def aquariums():
    return render_template('aquariums.html', active_page='aquariums')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Weryfikacja logowania (tu trzeba podpiąć bazę danych)
        if username == 'employee' and password == 'password123':
            session['logged_in'] = True
            session['role'] = 'employee'
            return redirect(url_for('employee'))
        elif username == 'customer' and password == 'password123':
            session['logged_in'] = True
            session['role'] = 'customer'
            return redirect(url_for('tickets'))
        else:
            error = "Nieprawidłowy login lub hasło"
            return render_template('login.html', error=error, active_page='login')
    return render_template('login.html', active_page='login')

# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

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
