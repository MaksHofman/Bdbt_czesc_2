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

def get_aquarium_data(aquarium_id):
    # Query the database to get the aquarium data by its ID
    aquarium = db.session.query(Akwarium).filter(Akwarium.id == aquarium_id).first()
    
    if aquarium:
        # Return the aquarium data as a dictionary or object
        return aquarium
    else:
        # Handle the case where no aquarium is found
        return None

def get_all_aquariums():
    # Query all aquariums from the database
    aquariums = db.session.query(Akwarium).all()
    return aquariums

def update_aquarium(aquarium_id, name, capacity, water_type, image):
    # Retrieve the aquarium record from the database using the aquarium_id
    aquarium = db.session.query(Akwarium).filter(Akwarium.id == aquarium_id).first()

    if aquarium:
        # Update the aquarium fields with the new data
        aquarium.Nazwa = name
        aquarium.Pojemnosc = capacity
        aquarium.Typ_wody = water_type
        
        # If an image is provided, handle the image (you can store the file or update the path)
        if image:
            # Assuming you're saving the image to a static folder and storing the path in the database
            image_path = save_image(image)  # Implement the image saving function
            aquarium.Zdjecie = image_path  # Or store the byte data if you're saving images directly to the database

        # Commit the changes to the database
        db.session.commit()
        return True  # Successfully updated
    else:
        return False  # Aquarium not found    