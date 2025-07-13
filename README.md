# TaskBoard - Aplikacja do Zarządzania Zadaniami

TaskBoard to aplikacja webowa inspirowana Trello, napisana w Flask, która umożliwia użytkownikom tworzenie tablic zadań, zarządzanie zadaniami w systemie kolumn (To Do, In Progress, Done) oraz współpracę z innymi użytkownikami poprzez system uprawnień.

## 🔗 Linki

- 🌐 **[Demo na żywo](https://michalszubaonline.cv)** - Zobacz aplikację w działaniu
- 📁 **[Repozytorium GitHub](https://github.com/WcaleNieMichal/TaskBoard.git)** - Kod źródłowy projektu

> **Uwaga:** Wersja produkcyjna może różnić się od aktualnego kodu w repozytorium.

## 📋 Spis treści

- [Funkcjonalności](#-funkcjonalności)
- [Technologie](#-technologie)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Uruchomienie](#-uruchomienie)
- [Użycie Docker](#-użycie-docker)
- [Struktura projektu](#-struktura-projektu)
- [Modele danych](#-modele-danych)
- [System uprawnień](#-system-uprawnień)
- [API Endpoints](#-api-endpoints)

## ✨ Funkcjonalności

### Zarządzanie użytkownikami
- ✅ Rejestracja i logowanie użytkowników
- ✅ Bezpieczne hasła (hashowanie)
- ✅ Sesje użytkowników z Flask-Login

### Zarządzanie tablicami zadań
- ✅ Tworzenie własnych tablic zadań
- ✅ Usuwanie tablic zadań
- ✅ Udostępnianie tablic innym użytkownikom
- ✅ System uprawnień (właściciel, moderator, gość)

### Zarządzanie zadaniami
- ✅ Dodawanie nowych zadań
- ✅ Przenoszenie zadań między kolumnami (drag & drop)
- ✅ Usuwanie zakończonych zadań
- ✅ Trzy kolumny: To Do, In Progress, Done

### Współpraca
- ✅ Udostępnianie tablic innym użytkownikom
- ✅ Role użytkowników: Moderator (pełne uprawnienia), Gość (tylko podgląd)
- ✅ Zarządzanie uprawnieniami przez właściciela tablicy

## 🚀 Technologie

### Backend
- **Flask** - framework webowy
- **Flask-SQLAlchemy** - ORM do bazy danych
- **Flask-Login** - zarządzanie sesjami użytkowników
- **Flask-WTF** - obsługa formularzy i CSRF
- **Flask-Migrate** - migracje bazy danych
- **Werkzeug** - hashowanie haseł

### Frontend
- **Bootstrap 5** - framework CSS
- **Bootstrap Icons** - ikony
- **SortableJS** - drag & drop dla zadań
- **Vanilla JavaScript** - interakcje

### Baza danych
- **SQLite** - domyślna baza danych (rozwój)
- Możliwość konfiguracji PostgreSQL/MySQL (produkcja)

### Inne
- **Docker** - konteneryzacja
- **Alembic** - migracje bazy danych

## 📋 Wymagania

- Python 3.11+
- pip (menedżer pakietów Python)
- Opcjonalnie: Docker i Docker Compose

## 🔧 Instalacja

### 1. Klonowanie repozytorium
```bash
git clone <url-repozytorium>
cd TaskBoard
```

### 2. Utworzenie środowiska wirtualnego
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate     # Windows
```

### 3. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 4. Konfiguracja bazy danych
```bash
flask db upgrade
```

## ▶️ Uruchomienie

### Lokalne uruchomienie
```bash
python main.py
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

### Zmienne środowiskowe (opcjonalne)
```bash
export SECRET_KEY="twoj-sekretny-klucz"
export DATABASE_URL="sqlite:///instance/taskboard.db"
```

## 🐳 Użycie Docker

### Docker Compose (zalecane)
```bash
docker-compose up --build
```

### Ręczne budowanie
```bash
docker build -t taskboard .
docker run -p 5000:5000 taskboard
```

## 📁 Struktura projektu

```
TaskBoard/
├── app/                          # Pakiet główny aplikacji
│   ├── __init__.py              # Factory aplikacji Flask
│   ├── config.py                # Konfiguracja aplikacji
│   ├── models.py                # Modele SQLAlchemy
│   ├── routes.py                # Główne routy
│   ├── decorators.py            # Dekoratory (system uprawnień)
│   ├── extensions.py            # Inicjalizacja rozszerzeń Flask
│   ├── auth/                    # Moduł uwierzytelniania
│   │   ├── routes.py           # Routy logowania/rejestracji
│   │   └── forms.py            # Formularze auth
│   ├── task/                    # Moduł zadań
│   │   ├── routes.py           # Operacje na zadaniach
│   │   └── forms.py            # Formularze zadań
│   ├── task_board/              # Moduł tablic zadań
│   │   ├── routes.py           # Operacje na tablicach
│   │   └── forms.py            # Formularze tablic
│   ├── templates/               # Szablony HTML
│   │   ├── dash_board.html     # Panel główny
│   │   ├── task_board.html     # Widok tablicy
│   │   ├── login.html          # Strona logowania
│   │   └── register.html       # Strona rejestracji
│   └── static/                  # Pliki statyczne
│       └── task_board/js/       # JavaScript
├── migrations/                   # Migracje bazy danych
├── instance/                    # Pliki instancji (baza SQLite)
├── main.py                      # Punkt wejścia aplikacji
├── requirements.txt             # Zależności Python
├── Dockerfile                   # Konfiguracja Docker
└── docker-compose.yml          # Docker Compose
```

## 🗄️ Modele danych

### User (Użytkownik)
- `id` - klucz główny
- `email` - unikalny adres email
- `password` - zahashowane hasło
- Relacje: własne tablice, uprawnienia do tablic

### TaskBoard (Tablica zadań)
- `id` - klucz główny
- `name` - nazwa tablicy (unikalna per użytkownik)
- `owner_id` - właściciel tablicy
- Relacje: zadania, uprawnienia użytkowników

### Task (Zadanie)
- `id` - klucz główny
- `description` - opis zadania
- `column` - kolumna (todo/inprogress/done)
- `task_board_id` - ID tablicy
- Relacja: tablica zadań

### TaskBoardPermission (Uprawnienia)
- `user_id` + `task_board_id` - klucz złożony
- `role` - rola (moderator/viewer)
- Relacje: użytkownik, tablica

## 🔐 System uprawnień

### Role użytkowników:
1. **Właściciel** - pełne uprawnienia do swojej tablicy
2. **Moderator** - może dodawać/edytować/usuwać zadania, nie może zarządzać uprawnieniami
3. **Gość (Viewer)** - tylko podgląd tablicy

### Dekorator `@role_required`
- Automatyczna weryfikacja uprawnień do tablicy
- Obsługa różnych ról w jednym dekoratorze
- Zwraca odpowiednie błędy dla API i web interface

## 🌐 API Endpoints

### Uwierzytelnianie
- `GET/POST /auth/login` - logowanie
- `GET/POST /auth/register` - rejestracja
- `GET /auth/logout` - wylogowanie

### Tablice zadań
- `GET /task_board/` - panel główny z listą tablic
- `POST /task_board/add_task_board` - dodanie nowej tablicy (JSON)
- `GET /task_board/view_board/<board_id>` - widok tablicy
- `DELETE /task_board/delete/<board_id>` - usunięcie tablicy
- `POST /task_board/view_board/<board_id>/add_role` - dodanie uprawnień użytkownika

### Zadania
- `POST /task_boards/<board_id>/add_task` - dodanie zadania
- `POST /task_boards/<board_id>/update_task` - aktualizacja kolumny zadania (JSON)
- `POST /task_boards/<board_id>/delete/<task_id>` - usunięcie zadania

## 🎯 Najważniejsze funkcje

### Drag & Drop
- Wykorzystuje bibliotekę SortableJS
- Automatyczne zapisywanie zmian w bazie danych
- Obsługa błędów i powiadomień użytkownika

### Bezpieczeństwo
- CSRF protection we wszystkich formularzach
- Hashowanie haseł z Werkzeug
- Weryfikacja uprawnień na poziomie backend

### Responsywność
- Bootstrap 5 zapewnia responsywny design
- Optymalizacja dla urządzeń mobilnych

---

**Autor:** Michal  
**Licencja:** MIT  
**Wersja:** 1.0.0 
