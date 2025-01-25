-- Dodanie danych testowych do tabel

-- Wstawienie danych do Oceanaria
INSERT INTO Oceanaria (Nazwa, Adress, Telefon, Email)
VALUES
('Oceanarium Gdańsk', 'Gdańsk, ul. Morska 12', '123456789', 'kontakt@oceanariumgdansk.pl');

-- Wstawienie danych do Pracownik
INSERT INTO Pracownik (Imie, Nazwisko, Stopien_naukowy, Data_zatrudnienia, Placa)
VALUES
('Jan', 'Kowalski', 'Magister Biologii', '2020-05-01', 4500.00),
('Anna', 'Nowak', 'Doktor Biologii', '2019-03-15', 5500.00);

-- Wstawienie danych do Klient
INSERT INTO Klient (Imie, Nazwisko, Typ_ulgi)
VALUES
('Michał', 'Zieliński', 'Rodzinny'),
('Katarzyna', 'Wiśniewska', 'Studencki');

-- Wstawienie danych do Uzytkownik
INSERT INTO Uzytkownik (Nazwa, Haslo, Id_pracownika, Id_klienta)
VALUES
('qw', 'qw', 1, NULL),
('klient1', 'haslo321', NULL, 1),
('pracownik2', 'tajnehaslo', 2, NULL),
('klient2', 'sekretnehaslo', NULL, 2);

-- Wstawienie danych do Bilet
INSERT INTO Bilet (Id_klienta, Cena)
VALUES
(1, 50.00),
(2, 45.00);

-- Wstawienie danych do Akwaria
INSERT INTO Akwaria (Id_oceanaria, Pojemnosc, Typ_wody, Zdjecie)
VALUES
(1, 5000.00, 'Słona', NULL),
(1, 3000.00, 'Słodka', NULL);

-- Wstawienie danych do Ryby
INSERT INTO Ryby (Id_akwaria, Id_oceanaria, Gatunek, Typ_wody, Wiek)
VALUES
(1, 1, 'Rekin Biały', 'Słona', 5),
(2, 1, 'Pirania Czerwona', 'Słodka', 3);
