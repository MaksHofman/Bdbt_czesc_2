from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Oceanarium(db.Model):
    __tablename__ = 'oceanaria'

    id = db.Column('id_oceanaria', db.Integer, primary_key=True)  # Maps to Id_oceanaria
    nazwa = db.Column('nazwa', db.String(255), nullable=False)
    adress = db.Column('adress', db.String(255), nullable=False)
    telefon = db.Column('telefon', db.String(20))
    email = db.Column('email', db.String(255))

    akwaria = db.relationship('Akwarium', back_populates='oceanarium', cascade='all, delete')
    ryby = db.relationship('Ryba', back_populates='oceanarium', cascade='all, delete')


class Pracownik(db.Model):
    __tablename__ = 'pracownik'

    id = db.Column('id_pracownika', db.Integer, primary_key=True)  # Maps to Id_pracownika
    imie = db.Column('imie', db.String(100), nullable=False)
    nazwisko = db.Column('nazwisko', db.String(100), nullable=False)
    stopien_naukowy = db.Column('stopien_naukowy', db.String(100))
    data_zatrudnienia = db.Column('data_zatrudnienia', db.Date, nullable=False)
    placa = db.Column('placa', db.Numeric(10, 2), nullable=False)
    zdjecie = db.Column('zdjecie', db.LargeBinary)

    uzytkownik = db.relationship('Uzytkownik', back_populates='pracownik')


class Klient(db.Model):
    __tablename__ = 'klient'

    id = db.Column('id_klienta', db.Integer, primary_key=True)  # Maps to Id_klienta
    imie = db.Column('imie', db.String(100), nullable=False)
    nazwisko = db.Column('nazwisko', db.String(100), nullable=False)
    typ_ulgi = db.Column('typ_ulgi', db.String(50))

    uzytkownik = db.relationship('Uzytkownik', back_populates='klient')
    bilety = db.relationship('Bilet', back_populates='klient', cascade='all, delete')


class Uzytkownik(db.Model):
    __tablename__ = 'uzytkownik'

    id = db.Column('id_uzytkownika', db.Integer, primary_key=True)  # Maps to Id_uzytkownika
    nazwa = db.Column('nazwa', db.String(100), nullable=False)
    haslo = db.Column('haslo', db.String(255), nullable=False)
    email = db.Column('email', db.String(255), nullable=True)
    id_pracownika = db.Column('id_pracownika', db.Integer, db.ForeignKey('pracownik.id_pracownika', ondelete='SET NULL'))
    id_klienta = db.Column('id_klienta', db.Integer, db.ForeignKey('klient.id_klienta', ondelete='SET NULL'))

    pracownik = db.relationship('Pracownik', back_populates='uzytkownik')
    klient = db.relationship('Klient', back_populates='uzytkownik')


class Bilet(db.Model):
    __tablename__ = 'bilet'

    id = db.Column('id_biletu', db.Integer, primary_key=True)  # Maps to Id_biletu
    id_klienta = db.Column('id_klienta', db.Integer, db.ForeignKey('klient.id_klienta', ondelete='CASCADE'), nullable=False)
    cena = db.Column('cena', db.Numeric(10, 2), nullable=False)

    klient = db.relationship('Klient', back_populates='bilety')


class Akwarium(db.Model):
    __tablename__ = 'akwaria'

    id = db.Column('id_akwaria', db.Integer, primary_key=True)  # Maps to Id_akwaria
    id_oceanaria = db.Column('id_oceanaria', db.Integer, db.ForeignKey('oceanaria.id_oceanaria', ondelete='CASCADE'), nullable=False)
    pojemnosc = db.Column('pojemnosc', db.Numeric(10, 2), nullable=False)
    typ_wody = db.Column('typ_wody', db.String(50), nullable=False)
    zdjecie = db.Column('zdjecie', db.LargeBinary)

    oceanarium = db.relationship('Oceanarium', back_populates='akwaria')
    ryby = db.relationship('Ryba', back_populates='akwarium', cascade='all, delete')


class Ryba(db.Model):
    __tablename__ = 'ryby'

    id = db.Column('id_ryby', db.Integer, primary_key=True)  # Maps to Id_ryby
    id_akwaria = db.Column('id_akwaria', db.Integer, db.ForeignKey('akwaria.id_akwaria', ondelete='CASCADE'), nullable=False)
    id_oceanaria = db.Column('id_oceanaria', db.Integer, db.ForeignKey('oceanaria.id_oceanaria', ondelete='CASCADE'))
    gatunek = db.Column('gatunek', db.String(100), nullable=False)
    typ_wody = db.Column('typ_wody', db.String(50), nullable=False)
    wiek = db.Column('wiek', db.Integer)
    zdjecie = db.Column('zdjecie', db.LargeBinary)

    akwarium = db.relationship('Akwarium', back_populates='ryby')
    oceanarium = db.relationship('Oceanarium', back_populates='ryby')
