# TaskBoard - Aplikacja do zarządzania zadaniami

TaskBoard to aplikacja webowa do zarządzania zadaniami w stylu Kanban, zbudowana przy użyciu Flask.

## Funkcje

### Podstawowe funkcje
- **Tworzenie tablic zadań**: Użytkownicy mogą tworzyć własne tablice zadań
- **Zarządzanie zadaniami**: Dodawanie, edycja i usuwanie zadań
- **System kolumn**: Zadania są organizowane w kolumnach (To Do, In Progress, Done)
- **Drag & Drop**: Intuicyjne przenoszenie zadań między kolumnami
- **Dynamiczne aktualizacje**: Zadania są aktualizowane bez odświeżania strony
- **Dynamiczna widoczność ikon**: Ikony usuwania pojawiają się/znikają w zależności od kontekstu

### System uprawnień
- **Hierarchia ról**: Właściciel > Moderator > Gość
- **Właściciel tablicy**: Pełne uprawnienia do tablicy
- **Moderator**: Może dodawać/edytować zadania, usuwać gości
- **Gość**: Tylko podgląd tablicy

### Zarządzanie uprawnieniami
- **Dodawanie użytkowników**: Właściciel może dodawać użytkowników z określonymi rolami
- **Usuwanie uprawnień**: Hierarchiczne usuwanie uprawnień z wizualnymi wskazówkami
- **Wizualne rozróżnienie**: Kolorowe oznaczenia użytkowników możliwych do usunięcia

### Dynamiczne funkcje UI
- **Bez odświeżania strony**: Przesuwanie zadań nie wymaga przeładowania strony
- **Inteligentne ikony kosza**: Pojawiają się tylko dla zadań w kolumnie "Done" i tylko dla użytkowników z odpowiednimi uprawnieniami
- **Efekty hover**: Ikony kosza pojawiają się przy najechaniu na zadanie
- **Płynne animacje**: Smooth transitions dla wszystkich interakcji
- **Modalne potwierdzenia**: Bezpieczne usuwanie z potwierdzeniem

## Technologie

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Baza danych**: SQLite (development), PostgreSQL (production)
- **Drag & Drop**: SortableJS
- **Konteneryzacja**: Docker

## Struktura projektu

```
TaskBoard/
├── app/
│   ├── __init__.py
│   ├── auth/                 # Moduł uwierzytelniania
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── role/                 # Moduł zarządzania rolami
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── task/                 # Moduł zadań
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── task_board/           # Moduł tablic zadań
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/
│   │   └── task_board/
│   │       └── js/
│   │           ├── task_board.js
│   │           └── task_board_dynamic.js  # Nowy dynamiczny JS
│   ├── templates/
│   │   ├── task_board.html
│   │   ├── login.html
│   │   └── register.html
│   ├── models.py
│   ├── config.py
│   └── decorators.py
├── migrations/
├── main.py
├── requirements.txt
└── README.md
```

## Instalacja i uruchomienie

### Wymagania
- Python 3.8+
- pip
- virtualenv (opcjonalnie)

### Kroki instalacji

1. **Klonowanie repozytorium**
   ```bash
   git clone <repository-url>
   cd TaskBoard
   ```

2. **Tworzenie środowiska wirtualnego**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # lub
   venv\Scripts\activate     # Windows
   ```

3. **Instalacja zależności**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicjalizacja bazy danych**
   ```bash
   flask db upgrade
   ```

5. **Uruchomienie aplikacji**
   ```bash
   python main.py
   ```

   Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

## Uruchomienie z Docker

### Development
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## API Endpoints

### Uwierzytelnianie
- `GET /auth/login` - Strona logowania
- `POST /auth/login` - Logowanie użytkownika
- `GET /auth/register` - Strona rejestracji
- `POST /auth/register` - Rejestracja użytkownika
- `GET /auth/logout` - Wylogowanie użytkownika

### Tablice zadań
- `GET /task_board/dashboard` - Dashboard z listą tablic
- `POST /task_board/add_task_board` - Dodawanie nowej tablicy (JSON)
- `GET /task_board/view_board/<int:board_id>` - Widok tablicy zadań
- `DELETE /task_board/delete/<int:board_id>` - Usuwanie tablicy (JSON)

### Zadania
- `POST /task_boards/<int:board_id>/add_task` - Dodawanie zadania
- `POST /task_boards/<int:board_id>/update_task` - Aktualizacja kolumny zadania (JSON)
- `POST /task_boards/<int:board_id>/delete/<int:task_id>` - Usuwanie zadania

### Zarządzanie rolami
- `POST /task_board/view_board/<int:board_id>/add_role` - Dodawanie roli użytkownika
- `DELETE /task_board/view_board/<int:board_id>/remove_role/<int:user_id>` - Usuwanie roli użytkownika (JSON)

## Konfiguracja

### Zmienne środowiskowe
- `FLASK_ENV` - Środowisko (development/production)
- `SECRET_KEY` - Klucz szyfrowania sesji
- `DATABASE_URL` - URL bazy danych

### Plik konfiguracyjny
Konfiguracja znajduje się w `app/config.py`

## Funkcje bezpieczeństwa

### Uwierzytelnianie i autoryzacja
- **Flask-Login**: Zarządzanie sesjami użytkowników
- **Dekorator `@role_required`**: Kontrola dostępu na poziomie endpointów
- **Hierarchia uprawnień**: Właściciel > Moderator > Gość

### Ochrona CSRF
- **Flask-WTF**: Automatyczna ochrona CSRF dla formularzy
- **Meta tagi**: CSRF token w nagłówkach AJAX

### Walidacja danych
- **WTForms**: Walidacja po stronie serwera
- **Sanityzacja**: Bezpieczne wyświetlanie danych użytkownika

## Dynamiczne funkcje (Nowe)

### Aktualizacje bez odświeżania
- **Przenoszenie zadań**: Zadania są aktualizowane w czasie rzeczywistym
- **Inteligentne przywracanie**: Automatyczne cofanie ruchu przy błędzie
- **Obsługa błędów**: Graceful handling niepowodzeń sieciowych

### Dynamiczne ikony kosza
- **Kontekstowa widoczność**: Ikony pojawiają się tylko gdy są potrzebne
- **Sprawdzanie uprawnień**: Ikony wyświetlane tylko dla użytkowników z odpowiednimi rolami
- **Efekty hover**: Smooth animations przy interakcji

### Architektura JavaScript
- **Klasa TaskBoardManager**: Centralne zarządzanie funkcjonalnością
- **Modularność**: Rozdzielone odpowiedzialności (sortowanie, usuwanie, uprawnienia)
- **Event-driven**: Reaktywne aktualizacje UI

## Rozwój

### Dodawanie nowych funkcji
1. Utwórz nowy blueprint w odpowiednim module
2. Dodaj odpowiednie formularze w `forms.py`
3. Zaimplementuj logikę w `routes.py`
4. Zaktualizuj modele w `models.py` jeśli potrzeba
5. Dodaj testy jednostkowe

### Struktura blueprintów
- **auth**: Uwierzytelnianie użytkowników
- **task**: Operacje na zadaniach
- **task_board**: Zarządzanie tablicami
- **role**: Zarządzanie uprawnieniami użytkowników

## Testowanie

### Testy jednostkowe
```bash
python -m pytest tests/
```

### Testy funkcjonalne
```bash
python -m pytest tests/functional/
```

## Wkład w rozwój

1. Fork repozytorium
2. Utwórz branch dla nowej funkcji (`git checkout -b feature/AmazingFeature`)
3. Commit zmian (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik `LICENSE` dla szczegółów.

## Autor

Twój projekt TaskBoard - System zarządzania zadaniami w stylu Kanban.

---

**Uwaga**: To jest aplikacja demonstracyjna. W środowisku produkcyjnym należy dodatkowo skonfigurować:
- Bezpieczną bazę danych
- HTTPS
- Monitoring i logi
- Backup danych
- Skalowanie poziome 