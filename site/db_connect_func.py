from models import *
from flask import session
from sqlalchemy.orm import Session


def get_and_save_oceanarium_by_id(oceanarium_id: int):
    oceanarium = Oceanarium.query.filter(Oceanarium.id == oceanarium_id).first()
    if oceanarium:
        session['oceanarium'] = {
            "id": oceanarium.id,
            "nazwa": oceanarium.nazwa,
            "adress": oceanarium.adress,
            "telefon": oceanarium.telefon,
            "email": oceanarium.email,
        }
        return True
    else:
        session.pop('oceanarium', None)
        return False

def get_user_info(user_id: int):
    user = Uzytkownik.query.filter(Uzytkownik.id == user_id).first()
    if user:
        # Prepare user information
        user_info = {
            "id": user.id,
            "nazwa": user.nazwa,
            "id_pracownika": user.id_pracownika,
            "id_klienta": user.id_klienta,
            "is_employee": user.id_pracownika is not None,  # True if the user is an employee
        }

        # Add detailed information about employee if exists
        if user.id_pracownika:
            user_info["pracownik"] = {
                "imie": user.pracownik.imie,
                "nazwisko": user.pracownik.nazwisko,
                "stopien_naukowy": user.pracownik.stopien_naukowy,
                "data_zatrudnienia": user.pracownik.data_zatrudnienia,
                "placa": float(user.pracownik.placa),
            }

        # Add detailed information about client if exists
        if user.id_klienta:
            user_info["klient"] = {
                "imie": user.klient.imie,
                "nazwisko": user.klient.nazwisko,
                "typ_ulgi": user.klient.typ_ulgi,
            }

        return user_info
    else:
        return None
