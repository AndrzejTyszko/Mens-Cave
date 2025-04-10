Men's Cave - Platforma Wynajmu Warsztatów 


📄 Opis Projektu

Men's Cave to nowoczesna aplikacja webowa i mobilna do wynajmu przestrzeni warsztatowych. Pozwala:

🙋 Najemcom: wyszukiwać, filtrować i rezerwować warsztaty,

👨‍💼 Właścicielom: dodawać swoje warsztaty do systemu,

📅 Zarządzać kalendarzem i dostępnością, - Nie dodane

⭐ Wystawiać opinie i komentarze,

📢 Prowadzić komunikację przez chat, -- Nie dodane

🔍 Korzystać z zaawansowanej filtracji i sortowania ofert.

🚀 Stack technologiczny

Backend

Python 3.10 + Django + Django REST Framework

PostgreSQL jako baza danych

JWT (SimpleJWT) do autoryzacji

ratelimit - ochrona endpointów logowania i rejestracji

Testy: APITestCase (8 testów funkcjonalnych)

Bezpieczeństwo: walidacja dat, uprawnienia dostępu, zabezpieczenia CSRF, hashowanie haseł

Frontend

Vue 3 + Vite + Tailwind CSS (SPA)

Vue Router do nawigacji

Axios do komunikacji z API

Komponenty UI: Heroicons, animacje z transition, efekty hover, modale, dropdowny

Responsywność: dopasowanie do mobile / desktop

Autoryzacja: JWT + localStorage

Mobilny Frontend (Ready-to-extend)

React Native z Axios (podpięcie do tego samego API)

Widoki kompatybilne z backendem + responsywne formularze logowania/rejestracji

🌐 Funkcje aplikacji

🔐 Użytkownik (najemca)

Rejestracja i logowanie (JWT)

Wyszukiwanie warsztatów po lokalizacji, cenie, wyposażeniu

Filtrowanie i sortowanie wyników

Rezerwacja online z kalkulacją ceny

Historia rezerwacji + formularz opinii

💼 Właściciel warsztatu

Dodawanie warsztatów (opis, cennik, zdjęcia, lokalizacja)

Kalendarz dostępności + zarządzanie rezerwacjami -- Nie dodane

Panel edycji / usuwania ofert

Podgląd opinii i statystyk

🔧 Administrator (API + Panel admina Django) -- Tylko backend

Moderacja treści, zgłoszeń

Podgląd użytkowników, rezerwacji i opinii


🌟 Przykładowe widoki

Rejestracja i logowanie
![image](https://github.com/user-attachments/assets/6f11a3a5-fd49-4d1b-8724-bf876c277754)


Dodawanie warsztatu
![image](https://github.com/user-attachments/assets/013b6d36-82f6-4a3c-9d92-316c9103e803)



Rezerwacja i komentarz
![image](https://github.com/user-attachments/assets/90c8bfc1-3bc3-4ad5-9591-5b4257a53f1f)


📦 Uruchomienie projektu

Backend:

cd menscave_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Frontend:

cd frontend
npm install
npm run dev

📉 Testy backendu

python manage.py test

Testy pokrywają:

rejestrację,

dodanie warsztatu,

rezerwacje,

opiniowanie (także błędne przypadki),

listowanie warsztatów.

🚫 Licencja

MIT

Projekt stworzony jako praca dyplomowa przez [Andrzej Tyszko]

