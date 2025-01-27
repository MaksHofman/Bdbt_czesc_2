from models import *
from flask import session
from sqlalchemy.orm import Session
import io

def save_image(image):
    try:
        binary_data = image.read()
        return binary_data
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

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


def get_aquarium_data(aquarium_id):
    aquarium = db.session.query(Akwarium).filter(Akwarium.id == aquarium_id).first()
    
    if aquarium:
        return aquarium
    else:
        return None

def get_all_aquariums():
    aquariums = db.session.query(Akwarium).all()
    return aquariums

def update_aquarium(aquarium_id, name, capacity, water_type, image):
    aquarium = db.session.query(Akwarium).filter(Akwarium.id == aquarium_id).first()

    if aquarium:
        aquarium.Nazwa = name
        aquarium.Pojemnosc = capacity
        aquarium.Typ_wody = water_type

        if image:
            binary_image = save_image(image)
            if binary_image:
                aquarium.Zdjecie = binary_image
        try:
            db.session.commit()
            return True  
        except Exception as e:
            db.session.rollback()
            print(f"Error updating aquarium: {e}")
            return False
    else:
        return False  

def get_typ_ulgi(user_id):
    uzytkownik = Uzytkownik.query.filter_by(id=user_id).first()
    
    if uzytkownik:
        klient = uzytkownik.klient
        if klient:
            return klient.typ_ulgi
        else:
            return None  
    return None 