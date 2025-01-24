from datetime import date, datetime, timedelta
from models import *
import re

__login_check = r'^[A-Za-z]+$'
__password_check = r'^[A-Za-z0-9]+$'

def get_user_from_db(username):
    user = Uzytkownik.query.filter_by(username=username).first()
    if user:
        return user.username, 
    else:
        return None, None, None, None, None, None, None

def anti_sql_injection_login_check(login, password) -> bool:
    if re.match(__login_check, login) and re.match(__password_check, password):
        return True
    else:
        return False

# Checks if an email is already in use
def check_email_exists(email: str) -> bool:
    return Uzytkownik.query.filter_by(email=email).first() is not None


# Checks if login credentials are correct
def checking_if_login_correct(login: str, password: str) -> bool:
    user = Uzytkownik.query.filter_by(username=login, password=password).first()
    return user is not None


# Adds a user to the database
def add_user_to_db(login: str, password: str, email: str):
    try:
        # Check if the login already exists
        existing_user = Uzytkownik.query.filter_by(nazwa=login).first()
        if existing_user:
            return False

        # Create the user entry
        new_user = Uzytkownik(
            nazwa=login,
            haslo=password,
            email=email,
            id_pracownika=None,  # No relation to Pracownik
            id_klienta=None      # No relation to Klient
        )
        db.session.add(new_user)
        db.session.commit()

        return True
    
    except Exception as e:
        db.session.rollback()  # Rollback in case of failure
        return {"success": False, "message": f"An error occurred: {str(e)}"}

# Utility functions
def check_if_email_correct(email: str) -> bool:
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None


