from models import Oceanaria, Pracownik, Klient, Uzytkownik, Bilet, Akwaria, Ryby
from flask import session
from sqlalchemy.orm import Session


def get_and_save_oceanarium_by_id(session_db: Session, oceanarium_id: int):
    """
    Fetches a row from the Oceanaria table by its ID and saves it to Flask's session.

    :param session_db: SQLAlchemy session object.
    :param oceanarium_id: ID of the oceanarium to retrieve.
    :return: True if the data is saved to Flask's session, False if not found.
    """
    oceanarium = session_db.query(Oceanaria).filter(Oceanaria.Id_oceanaria == oceanarium_id).first()
    if oceanarium:
        # Save the oceanarium data into the Flask session
        session['oceanarium'] = {
            "Id_oceanaria": oceanarium.Id_oceanaria,
            "Nazwa": oceanarium.Nazwa,
            "Adress": oceanarium.Adress,
            "Telefon": oceanarium.Telefon,
            "Email": oceanarium.Email,
        }
        return True
    else:
        # Clear the session data if not found
        session.pop('oceanarium', None)
        return False
