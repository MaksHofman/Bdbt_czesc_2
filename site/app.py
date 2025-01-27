import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from models import *
from db_connect_func import get_and_save_oceanarium_by_id, get_aquarium_data, update_aquarium, get_all_aquariums, get_typ_ulgi
from login_register import check_if_email_correct, anti_sql_injection_login_check, checking_if_login_correct, check_email_exists, add_user_to_db, get_user_from_db
import base64

app = Flask(__name__)
app.secret_key = 'sekretny_klucz'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
db.init_app(app)

@app.template_filter('b64encode')
def b64encode_filter(data):
    """Encodes binary data to Base64 for use in templates."""
    if data is None:
        return ""
    return base64.b64encode(data).decode('utf-8')

@app.route('/')
def home():
    session['oceanarium_id'] = 1
    oceanarium = Oceanarium.query.get(int(session['oceanarium_id']))
    return render_template('main.html', active_page='home', oceanarium=oceanarium)


@app.route('/aquariums')
def aquariums():
    aquariums = Akwarium.query.all()
    return render_template('aquariums.html', aquariums=aquariums)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        if checking_if_login_correct(login, password) and anti_sql_injection_login_check(login, password):
            session['logged_in'] = True
            user_info = get_user_from_db(login)
            session['user_id'] = user_info["id"]
            session['username'] = user_info["Nazwa"]
            session['email'] = user_info["Email"]
            session['czyPracownik'] = user_info["czyPracownik"]
            if user_info["czyPracownik"]:
                return redirect(url_for('employee'))
            else:
                session['Typ_ulgi'] = get_typ_ulgi(int(user_info["id"]))
                return redirect(url_for('tickets'))
        else:
            wrong_login = "Wrong username or password"
            return render_template('login.html', wrong_login=wrong_login)
    return render_template('login.html')


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

        if login == "" and session.get('input_username') != None:
            login = session.get('input_username')
        else:
            session['input_username'] = login

        input_username = login

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



@app.route('/employee', methods=['GET'])
def employee():
    if not session.get("czyPracownik"):
        return redirect(url_for('login'))


    aquariums = Akwarium.query.all()

    return render_template('employee.html', aquariums=aquariums, active_page='employee')


@app.route('/edit_aquarium/<int:aquarium_id>', methods=['GET', 'POST'])
def edit_aquarium(aquarium_id):
    if not session.get("czyPracownik"):
        return redirect(url_for('login'))
    aquarium = Akwarium.query.get_or_404(aquarium_id)
    if request.method == 'POST':
        aquarium.pojemnosc = request.form['pojemnosc']
        aquarium.typ_wody = request.form['typ_wody']

        if 'zdjecie' in request.files and request.files['zdjecie'].filename:
            file = request.files['zdjecie']
            aquarium.zdjecie = file.read()  

        db.session.commit()
        return redirect(url_for('employee'))  

    return render_template('edit_aquarium.html', aquarium=aquarium)

@app.route('/employee/delete_aquarium/<int:aquarium_id>', methods=['POST'])
def delete_aquarium(aquarium_id):
    # Ensure that the user is a logged-in employee
    if not session.get('czyPracownik'):
        return redirect(url_for('login'))

    # Query for the aquarium by its ID
    aquarium_to_delete = Akwarium.query.get(aquarium_id)
    
    if aquarium_to_delete:
        # Delete the aquarium from the database
        db.session.delete(aquarium_to_delete)
        db.session.commit()
    
    # Redirect back to the employee page after deletion
    return redirect(url_for('employee'))

# Kupno biletów
@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    
    client_id = session.get('user_id')

    purchased_tickets = Bilet.query.filter_by(id_klienta=client_id).all()
    
    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        if ticket_type == 'Normalny' and session.get('czyPracownik') == False and session.get("Typ_ulgi") == ticket_type:
            new_ticket = Bilet(id_klienta=client_id, cena=50.00)
            db.session.add(new_ticket)
            db.session.commit()
        elif ticket_type == 'Studencki' and session.get('czyPracownik') == False and session.get("Typ_ulgi") == ticket_type:  
            new_ticket = Bilet(id_klienta=client_id, cena=30.00) 
            db.session.add(new_ticket)
            db.session.commit()
        else:
            pass

        return redirect(url_for('tickets')) 
    
    return render_template('tickets.html', tickets=purchased_tickets)

if __name__ == '__main__':
    app.run(debug=True)
