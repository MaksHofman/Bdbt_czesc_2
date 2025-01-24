-- Tworzenie tabeli Oceanaria
CREATE TABLE Oceanaria (
    Id_oceanaria SERIAL PRIMARY KEY,
    Nazwa VARCHAR(255) NOT NULL,
    Adress VARCHAR(255) NOT NULL,
    Telefon VARCHAR(20),
    Email VARCHAR(255)
);

-- Tworzenie tabeli Pracownik
CREATE TABLE Pracownik (
    Id_pracownika SERIAL PRIMARY KEY,
    Imie VARCHAR(100) NOT NULL,
    Nazwisko VARCHAR(100) NOT NULL,
    Stopien_naukowy VARCHAR(100),
    Data_zatrudnienia DATE NOT NULL,
    Placa NUMERIC(10, 2) NOT NULL,
    Zdjecie BYTEA
);

-- Tworzenie tabeli Klient
CREATE TABLE Klient (
    Id_klienta SERIAL PRIMARY KEY,
    Imie VARCHAR(100) NOT NULL,
    Nazwisko VARCHAR(100) NOT NULL,
    Typ_ulgi VARCHAR(50)
);

-- Tworzenie tabeli Uzytkownik
CREATE TABLE Uzytkownik (
    Id_uzytkownika SERIAL PRIMARY KEY,
    Nazwa VARCHAR(100) NOT NULL,
    Haslo VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Id_pracownika INT,
    Id_klienta INT,
    FOREIGN KEY (Id_pracownika) REFERENCES Pracownik(Id_pracownika) ON DELETE SET NULL,
    FOREIGN KEY (Id_klienta) REFERENCES Klient(Id_klienta) ON DELETE SET NULL
);

-- Tworzenie tabeli Bilet
CREATE TABLE Bilet (
    Id_biletu SERIAL PRIMARY KEY,
    Id_klienta INT NOT NULL,
    Cena NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (Id_klienta) REFERENCES Klient(Id_klienta) ON DELETE CASCADE
);

-- Tworzenie tabeli Akwaria
CREATE TABLE Akwaria (
    Id_akwaria SERIAL PRIMARY KEY,
    Id_oceanaria INT NOT NULL,
    Pojemnosc NUMERIC(10, 2) NOT NULL,
    Typ_wody VARCHAR(50) NOT NULL,
    Zdjecie BYTEA,
    FOREIGN KEY (Id_oceanaria) REFERENCES Oceanaria(Id_oceanaria) ON DELETE CASCADE
);

-- Tworzenie tabeli Ryby
CREATE TABLE Ryby (
    Id_ryby SERIAL PRIMARY KEY,
    Id_akwaria INT NOT NULL,
    Id_oceanaria INT,
    Gatunek VARCHAR(100) NOT NULL,
    Typ_wody VARCHAR(50) NOT NULL,
    Wiek INT,
    Zdjecie BYTEA,
    FOREIGN KEY (Id_akwaria) REFERENCES Akwaria(Id_akwaria) ON DELETE CASCADE,
    FOREIGN KEY (Id_oceanaria) REFERENCES Oceanaria(Id_oceanaria) ON DELETE CASCADE
);