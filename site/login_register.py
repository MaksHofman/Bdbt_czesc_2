from datetime import date, datetime, timedelta
from models import *
import re

__login_check = r'^[A-Za-z]+$'
__password_check = r'^[A-Za-z0-9]+$'


def anti_sql_injection_login_check(login, password) -> bool:
    if re.match(__login_check, login) and re.match(__password_check, password):
        return True
    else:
        return False

def check_email_exists(email: str) -> bool:
    return Uzytkownik.query.filter_by(email=email).first() is not None


def checking_if_login_correct(login: str, password: str) -> bool:
    user = Uzytkownik.query.filter_by(nazwa=login, haslo=password).first()
    return user is not None


def add_user_to_db(login: str, password: str, email: str):
    try:
        existing_user = Uzytkownik.query.filter_by(nazwa=login).first()
        if existing_user:
            return False

        # Create the user entry
        new_user = Uzytkownik(
            nazwa=login,
            haslo=password,
            email=email,
            id_pracownika=None,  
            id_klienta=None     
        )
        db.session.add(new_user)
        db.session.commit()

        return True
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"An error occurred: {str(e)}"}

def check_if_email_correct(email: str) -> bool:
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None


def get_user_info(user_id: int):
    user = Uzytkownik.query.filter(Uzytkownik.id == user_id).first()
    if user:
        user_info = {
            "id": user.id,
            "nazwa": user.nazwa,
            "id_pracownika": user.id_pracownika,
            "id_klienta": user.id_klienta,
            "is_employee": user.id_pracownika is not None, 
        }

        if user.id_pracownika:
            user_info["pracownik"] = {
                "imie": user.pracownik.imie,
                "nazwisko": user.pracownik.nazwisko,
                "stopien_naukowy": user.pracownik.stopien_naukowy,
                "data_zatrudnienia": user.pracownik.data_zatrudnienia,
                "placa": float(user.pracownik.placa),
            }

        if user.id_klienta:
            user_info["klient"] = {
                "imie": user.klient.imie,
                "nazwisko": user.klient.nazwisko,
                "typ_ulgi": user.klient.typ_ulgi,
            }

        return user_info
    else:
        return None

def get_user_from_db(login: str):
    try:
        user = Uzytkownik.query.filter_by(nazwa=login).first()

        if not user:
            return False

        user_info = {
            "id": user.id,
            "Nazwa": user.nazwa,
            "Email": user.email,
            "czyPracownik": user.id_pracownika is not None  
        }

        return user_info

    except Exception as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}
