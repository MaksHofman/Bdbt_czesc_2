from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Oceanaria(Base):
    __tablename__ = 'Oceanaria'

    Id_oceanaria = Column(Integer, primary_key=True)
    Nazwa = Column(String(255), nullable=False)
    Adress = Column(String(255), nullable=False)
    Telefon = Column(String(20))
    Email = Column(String(255))

    akwaria = relationship('Akwaria', back_populates='oceanarium')
    ryby = relationship('Ryby', back_populates='oceanarium')

class Pracownik(Base):
    __tablename__ = 'Pracownik'

    Id_pracownika = Column(Integer, primary_key=True)
    Imie = Column(String(100), nullable=False)
    Nazwisko = Column(String(100), nullable=False)
    Stopien_naukowy = Column(String(100))
    Data_zatrudnienia = Column(Date, nullable=False)
    Placa = Column(Numeric(10, 2), nullable=False)
    Zdjecie = Column(LargeBinary)

    uzytkownik = relationship('Uzytkownik', back_populates='pracownik')

class Klient(Base):
    __tablename__ = 'Klient'

    Id_klienta = Column(Integer, primary_key=True)
    Imie = Column(String(100), nullable=False)
    Nazwisko = Column(String(100), nullable=False)
    Typ_ulgi = Column(String(50))

    uzytkownik = relationship('Uzytkownik', back_populates='klient')
    bilety = relationship('Bilet', back_populates='klient')

class Uzytkownik(Base):
    __tablename__ = 'Uzytkownik'

    Id_uzytkownika = Column(Integer, primary_key=True)
    Nazwa = Column(String(100), nullable=False)
    Haslo = Column(String(255), nullable=False)
    Id_pracownika = Column(Integer, ForeignKey('Pracownik.Id_pracownika', ondelete='SET NULL'))
    Id_klienta = Column(Integer, ForeignKey('Klient.Id_klienta', ondelete='SET NULL'))

    pracownik = relationship('Pracownik', back_populates='uzytkownik')
    klient = relationship('Klient', back_populates='uzytkownik')

class Bilet(Base):
    __tablename__ = 'Bilet'

    Id_biletu = Column(Integer, primary_key=True)
    Id_klienta = Column(Integer, ForeignKey('Klient.Id_klienta', ondelete='CASCADE'), nullable=False)
    Cena = Column(Numeric(10, 2), nullable=False)

    klient = relationship('Klient', back_populates='bilety')

class Akwaria(Base):
    __tablename__ = 'Akwaria'

    Id_akwaria = Column(Integer, primary_key=True)
    Id_oceanaria = Column(Integer, ForeignKey('Oceanaria.Id_oceanaria', ondelete='CASCADE'), nullable=False)
    Pojemnosc = Column(Numeric(10, 2), nullable=False)
    Typ_wody = Column(String(50), nullable=False)
    Zdjecie = Column(LargeBinary)

    oceanarium = relationship('Oceanaria', back_populates='akwaria')
    ryby = relationship('Ryby', back_populates='akwarium')

class Ryby(Base):
    __tablename__ = 'Ryby'

    Id_ryby = Column(Integer, primary_key=True)
    Id_akwaria = Column(Integer, ForeignKey('Akwaria.Id_akwaria', ondelete='CASCADE'), nullable=False)
    Id_oceanaria = Column(Integer, ForeignKey('Oceanaria.Id_oceanaria', ondelete='CASCADE'))
    Gatunek = Column(String(100), nullable=False)
    Typ_wody = Column(String(50), nullable=False)
    Wiek = Column(Integer)
    Zdjecie = Column(LargeBinary)

    akwarium = relationship('Akwaria', back_populates='ryby')
    oceanarium = relationship('Oceanaria', back_populates='ryby')
