# Weekend 4: Debugger + ORM + REST API - Harmonogram szczegolowy

## Informacje ogolne

- **Daty:** 28-29 marca 2026
- **Godziny:** 8:30 - 15:00 (kazdy dzien)
- **Temat:** Debugger VS Code + Django ORM (dzien 1) + REST API z DRF (dzien 2)
- **Wymagania wstepne:** Weekend 1 (OOP) + Weekend 2 (wyjatki + testy) + Weekend 3 (Git + Django)

## Struktura dnia

- **Blok 1:** 8:30 - 10:30 (120 min)
- **Przerwa:** 10:30 - 10:40 (10 min)
- **Blok 2:** 10:40 - 12:40 (120 min)
- **Przerwa obiadowa:** 12:40 - 13:10 (30 min)
- **Blok 3:** 13:10 - 15:00 (110 min)

**Czas roboczy:** ~5h 50min / dzien

---

## DZIEN 1: Debugger VS Code + Django ORM

### Blok 1 (8:30-10:30) - Debugger + ORM Intro + First Model - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 8:30-8:50 | 20 min | Powitanie, recap Weekend 3, plan weekendu 4 | Intro |
| 8:50-9:05 | 15 min | Teoria: Debugger VS Code - po co, czym rozni sie od print() | Wyklad |
| 9:05-9:20 | 15 min | **SHOW:** Konfiguracja launch.json, breakpoints, step over/into/out, variables, watches | Live coding |
| 9:20-9:35 | 15 min | **DO:** Debugowanie pizza_list view - breakpoint w view, inspekcja request i context | Cwiczenie |
| 9:35-9:55 | 20 min | Teoria: bazy danych, schema, Django ORM, modele, migracje | Wyklad |
| 9:55-10:10 | 15 min | **SHOW:** Pierwszy model Django (GENERIC: Book w menu_app) + makemigrations + migrate | Live coding |
| 10:10-10:30 | 20 min | **DO:** Cw. 1: Model Pizza w menu_app + migracja + Django shell (Pizza.objects.create, .all, .get) | Cwiczenie |

### Przerwa (10:30-10:40) - 10 min

### Blok 2 (10:40-12:40) - Admin + QuerySets + Customer Model - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 10:40-10:55 | 15 min | **SHOW:** Django Admin - rejestracja modelu, createsuperuser, przegladanie danych | Live coding |
| 10:55-11:15 | 20 min | **DO:** Cw. 2: Pizza w admin + aktualizacja pizza_list view na ORM + weryfikacja w przegladarce | Cwiczenie |
| 11:15-11:35 | 20 min | Teoria: QuerySet API - all(), filter(), get(), create(), update(), delete(), order_by() | Wyklad |
| 11:35-11:50 | 15 min | **SHOW:** QuerySet w praktyce - Django shell (GENERIC: Book.objects.filter, exclude, order_by) | Live coding |
| 11:50-12:05 | 15 min | **DO:** Cw. 3: QuerySet cwiczenia w shell - filtrowanie pizz, sortowanie, agregacja | Cwiczenie |
| 12:05-12:15 | 10 min | Teoria: Relacje w modelach - ForeignKey, choices. Model Customer z polem type | Wyklad |
| 12:15-12:40 | 25 min | **DO:** Cw. 4: Model Customer w customers_app + migracja + admin + aktualizacja customer_list view | Cwiczenie |

### Przerwa obiadowa (12:40-13:10) - 30 min

### Blok 3 (13:10-15:00) - Order Model + Import danych - 110 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 13:10-13:25 | 15 min | Teoria: ForeignKey - relacje miedzy modelami, on_delete, related_name | Wyklad |
| 13:25-14:00 | 35 min | **DO:** Cw. 5: Modele Order + OrderItem w orders_app z ForeignKey do Pizza i Customer + admin | Cwiczenie |
| 14:00-14:15 | 15 min | **SHOW:** Management command - import danych z JSON do bazy (GENERIC przyklad) | Live coding |
| 14:15-14:40 | 25 min | **DO:** Cw. 6: Napisz command `import_data` w menu_app ktory importuje menu.json i customers.json do DB | Cwiczenie |
| 14:40-14:50 | 10 min | Bufor: dodatkowy czas na cwiczenia / Q&A | Praktyka |
| 14:50-15:00 | 10 min | Podsumowanie dnia 1. Preview: REST API jutro. | Outro |

---

## DZIEN 2: REST API z Django REST Framework

### Blok 1 (8:30-10:30) - REST Concepts + Pizza API (GET) - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 8:30-8:50 | 20 min | Recap dnia 1 - ORM dziala, dane w bazie, admin panel | Intro |
| 8:50-9:10 | 20 min | Teoria: REST API - czym jest, HTTP metody (GET/POST/PUT/DELETE), JSON, status codes | Wyklad |
| 9:10-9:25 | 15 min | Teoria: DRF - instalacja, `startapp api`, Serializer, @api_view, Response, status | Wyklad |
| 9:25-9:40 | 15 min | **SHOW:** Prosty serializer + GET list (GENERIC: Book API) | Live coding |
| 9:40-10:00 | 20 min | **DO:** Cw. 1: PizzaSerializer + pizza_list_api (GET /api/pizzas/) | Cwiczenie |
| 10:00-10:15 | 15 min | **SHOW:** GET detail z parametrem URL + 404 response (GENERIC: Book detail) | Live coding |
| 10:15-10:30 | 15 min | **DO:** Cw. 2: pizza_detail_api (GET /api/pizzas/<name>/) | Cwiczenie |

### Przerwa (10:30-10:40) - 10 min

### Blok 2 (10:40-12:40) - Pizza CRUD (POST, PUT, DELETE) - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 10:40-10:55 | 15 min | Teoria: POST create + walidacja w serializerze + status 201 | Wyklad |
| 10:55-11:10 | 15 min | **SHOW:** POST create (GENERIC: Book create) | Live coding |
| 11:10-11:30 | 20 min | **DO:** Cw. 3: POST /api/pizzas/ - tworzenie pizzy przez API | Cwiczenie |
| 11:30-11:50 | 20 min | **SHOW:** PUT update + DELETE (GENERIC: Book update/delete) | Live coding |
| 11:50-12:15 | 25 min | **DO:** Cw. 4: PUT + DELETE /api/pizzas/<name>/ - pelny CRUD pizzy | Cwiczenie |
| 12:15-12:40 | 25 min | Eksperymentowanie: testowanie API przez Browsable API i curl, walidacja bledow | Praktyka |

### Przerwa obiadowa (12:40-13:10) - 30 min

### Blok 3 (13:10-15:00) - Testowanie API + Podsumowanie - 110 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 13:10-13:30 | 20 min | Teoria: Testowanie API - APIClient, pytest-django, @pytest.mark.django_db | Wyklad |
| 13:30-13:40 | 10 min | **SHOW:** Prosty test API (GENERIC: Book test) | Live coding |
| 13:40-14:20 | 40 min | **DO:** Cw. 5: Testy Pizza API - test list, detail, create, update, delete | Cwiczenie |
| 14:20-14:40 | 20 min | Podsumowanie weekendu 4 + calego kursu. Kluczowe wzorce. | Wyklad |
| 14:40-14:55 | 15 min | Omowienie zadan domowych (Customer API, Order API, wyszukiwanie, sortowanie) | Wyklad |
| 14:55-15:00 | 5 min | Q&A, pozegnanie | Outro |

---

## Przyklady SHOW vs DO

| Sekcja | SHOW (przyklad) | DO (zadanie) |
|--------|----------------|--------------|
| Debugger | Breakpoint w hello view | Debugowanie pizza_list view |
| Pierwszy model | Book model w menu_app + migracja | Pizza model w menu_app + shell |
| Admin | Rejestracja Book w admin | Pizza w admin + superuser |
| QuerySet | Book.objects.filter/order_by | Filtrowanie pizz w shell |
| Serializer + GET list | BookSerializer + book_list_api | PizzaSerializer + pizza_list_api |
| GET detail + 404 | book_detail_api | pizza_detail_api |
| POST create | Book create API | Pizza create API |
| PUT + DELETE | Book update/delete | Pizza update/delete |
| Test API | Test Book API | Test Pizza API |

---

## Struktura URL (rozwiazanie)

### HTML Views (z Weekend 3 - nadal dzialaja)

```
/menu/                         -> pizza_list (HTML)
/menu/<str:name>/              -> pizza_detail (HTML)
/menu/dodaj/                   -> pizza_add (HTML form)
/klienci/                      -> customer_list (HTML)
/klienci/dodaj/                -> customer_add (HTML form)
/zamowienia/                   -> order_list (HTML)
/zamowienia/<int:order_id>/    -> order_detail (HTML)
/zamowienia/nowe/              -> order_create (HTML form)
/admin/                        -> Django admin panel
```

### REST API (nowe - na zajeciach)

```
GET    /api/pizzas/              -> lista pizz (JSON)
POST   /api/pizzas/              -> dodaj pizze
GET    /api/pizzas/<name>/       -> szczegoly pizzy
PUT    /api/pizzas/<name>/       -> aktualizuj cene
DELETE /api/pizzas/<name>/       -> usun pizze
```

### REST API (zadanie domowe)

```
GET    /api/customers/           -> lista klientow
POST   /api/customers/           -> dodaj klienta
GET    /api/customers/<id>/      -> szczegoly klienta

GET    /api/orders/              -> lista zamowien
POST   /api/orders/              -> zloz zamowienie
GET    /api/orders/<id>/         -> szczegoly zamowienia
DELETE /api/orders/<id>/         -> anuluj zamowienie
```

---

## Ewolucja projektu

### ORM zastepuje engine

Na Weekend 1-2 studenci zbudowali klasy Pythona (Pizza, Customer, Menu) z walidacja i persystencja w plikach JSON. Na Weekend 4 **zastepujemy** te klasy modelami Django ORM:

```
Weekend 1-2:                     Weekend 4:
  pizza.py (klasa Python)   -->    menu_app/models.py (model Django)
  menu.json (plik)          -->    db.sqlite3 (baza danych)
  save_to_file()            -->    model.save()
  load_from_file()          -->    Model.objects.all()
```

Folder `rozwiazanie_weekend2/` zostaje w projekcie jako referencja kodu z poprzednich weekendow. Nowy kod korzysta z modeli Django.
