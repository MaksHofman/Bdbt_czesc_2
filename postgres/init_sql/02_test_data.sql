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
('Michał', 'Zieliński', 'Normalny'),
('Katarzyna', 'Wiśniewska', 'Studencki'),
('as', 'as', 'Studencki');

-- Wstawienie danych do Uzytkownik
INSERT INTO Uzytkownik (Nazwa, Haslo, Email, Id_pracownika, Id_klienta)
VALUES
('qw', 'qw','qw@gmail.com', 1, NULL),
('as', 'as','as@gmail.com', NULL, 3),
('ass', 'ass','qwqqw@gmail.com', NULL, 1),
('pracownik2', 'tajnehaslo','qqwqww@gmail.com', 2, NULL),
('klient2', 'sekretnehaslo','qwqwqw@gmail.com', NULL, 2);

-- Wstawienie danych do Bilet
INSERT INTO Bilet (Id_klienta, Cena)
VALUES
(1, 50.00),
(2, 30.00);

-- Wstawienie danych do Akwaria
INSERT INTO Akwaria (Id_oceanaria, Pojemnosc, Typ_wody, Zdjecie)
VALUES
(1, 5000, 'Słona', pg_read_binary_file('/docker-entrypoint-initdb.d/images/aq2.jpg')),
(1, 3000, 'Słodka', pg_read_binary_file('/docker-entrypoint-initdb.d/images/aq3.jpg'));

-- Wstawienie danych do Ryby
INSERT INTO Ryby (Id_akwaria, Id_oceanaria, Gatunek, Typ_wody, Wiek)
VALUES
(1, 1, 'Rekin Biały', 'Słona', 5),
(2, 1, 'Pirania Czerwona', 'Słodka', 3);
