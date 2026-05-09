# Weekend 5: Python + Selenium - Harmonogram szczegolowy

## Informacje ogolne

- **Daty:** 9-10 maja 2026
- **Godziny:** 8:30 - 15:00 (kazdy dzien)
- **Temat:** Selenium WebDriver - automatyzacja przegladarki (dzien 1) + Page Object Model + testy E2E (dzien 2)
- **Wymagania wstepne:** Weekend 1 (OOP) + Weekend 2 (wyjatki + pytest) + Weekend 3 (Git + Django) + Weekend 4 (Pizza model w ORM + REST API)

> **Uwaga o stanie projektu po Weekend 4:** ORM ma tylko model `Pizza`. `Customer` i `Order` nadal sa klasami Pythona z `rozwiazanie_weekend2/` i danymi w plikach JSON. Dlatego wszystkie cwiczenia Weekendu 5 dotycza **wylacznie pizz** (CRUD przez UI).

## Struktura dnia

- **Blok 1:** 8:30 - 10:30 (120 min)
- **Przerwa:** 10:30 - 10:40 (10 min)
- **Blok 2:** 10:40 - 12:40 (120 min)
- **Przerwa obiadowa:** 12:40 - 13:10 (30 min)
- **Blok 3:** 13:10 - 15:00 (110 min)

**Czas roboczy:** ~5h 50min / dzien

---

## DZIEN 1: Selenium WebDriver - podstawy

### Blok 1 (8:30-10:30) - Wprowadzenie + Setup + Pierwszy test - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 8:30-8:50 | 20 min | Powitanie, recap Weekend 4, plan weekendu 5 (po co Selenium) | Intro |
| 8:50-9:10 | 20 min | Teoria: Czym jest Selenium, WebDriver, manualny vs automatyczny test, przegladarki headless | Wyklad |
| 9:10-9:30 | 20 min | **SHOW:** Instalacja `selenium`, `webdriver-manager`, struktura projektu testow, pierwszy skrypt (otworz google.com) | Live coding |
| 9:30-9:55 | 25 min | **DO:** Cw. 1: Zainstaluj Selenium, napisz skrypt ktory otwiera strone pizzerii (`/menu/`) i drukuje tytul | Cwiczenie |
| 9:55-10:05 | 10 min | **REVIEW:** Omowienie - PATH problemy, Chrome vs Firefox, webdriver-manager | Review |
| 10:05-10:20 | 15 min | Teoria: Jak przegladarka renderuje strone (DOM), inspekcja elementow w DevTools | Wyklad |
| 10:20-10:30 | 10 min | **DO:** Cw. 2: Otworz DevTools (F12) na stronie pizzerii, znajdz element `<h1>`, lista pizz, link do detalu | Cwiczenie |

### Przerwa (10:30-10:40) - 10 min

### Blok 2 (10:40-12:40) - Lokalizatory + Interakcje - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 10:40-11:00 | 20 min | Teoria: Lokalizatory `By` (ID, NAME, CLASS_NAME, TAG_NAME, CSS_SELECTOR, XPATH, LINK_TEXT) | Wyklad |
| 11:00-11:15 | 15 min | **SHOW:** `find_element` vs `find_elements` na stronie ksiazek (GENERIC) - znajdz tytul, liste, link | Live coding |
| 11:15-11:40 | 25 min | **DO:** Cw. 3: Znajdz na `/menu/` h1, wszystkie nazwy pizz (lista), link do pierwszej pizzy | Cwiczenie |
| 11:40-11:50 | 10 min | **REVIEW:** Omowienie - kiedy ID, kiedy CSS, kiedy XPATH, NoSuchElementException | Review |
| 11:50-12:05 | 15 min | Teoria: Interakcje - `click()`, `send_keys()`, `clear()`, `text`, `get_attribute()` | Wyklad |
| 12:05-12:20 | 15 min | **SHOW:** Wypelnienie formularza logowania (GENERIC: bookstore login) + submit | Live coding |
| 12:20-12:40 | 20 min | **DO:** Cw. 4: Wypelnij formularz `/menu/dodaj/` (nazwa + cena pizzy) i kliknij "Dodaj" | Cwiczenie |

### Przerwa obiadowa (12:40-13:10) - 30 min

### Blok 3 (13:10-15:00) - Czekanie na elementy + Asercje + Zadanie - 110 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 13:10-13:30 | 20 min | Teoria: Problem czekania - implicit vs explicit wait, `WebDriverWait`, `expected_conditions` | Wyklad |
| 13:30-13:45 | 15 min | **SHOW:** WebDriverWait do oczekiwania na element po klikniecu (GENERIC: bookstore search) | Live coding |
| 13:45-14:10 | 25 min | **DO:** Cw. 5: Otworz pizzerie, dodaj pizze i poczekaj `WebDriverWait` az pojawi sie message.success | Cwiczenie |
| 14:10-14:25 | 15 min | **SHOW:** Pierwszy test pytest + Selenium - struktura test_*.py, fixture `driver`, asercje | Live coding |
| 14:25-14:45 | 20 min | **DO:** Cw. 6: Napisz `test_pizza_list_displays_pizzas` - sprawdz ze na `/menu/` jest >= 1 pizza | Cwiczenie |
| 14:45-14:55 | 10 min | **REVIEW:** Omowienie - assert vs Selenium, czemu testy automatyczne | Review |
| 14:55-15:00 | 5 min | Podsumowanie dnia 1, preview: jutro POM + E2E | Outro |

---

## DZIEN 2: Page Object Model + Testy E2E

### Blok 1 (8:30-10:30) - Pytest fixtures + Page Object Model - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 8:30-8:50 | 20 min | Recap dnia 1 - lokalizatory, czekanie, pierwszy test | Intro |
| 8:50-9:10 | 20 min | Teoria: Pytest fixtures w testach E2E - scope, conftest.py, headless, screenshot na fail | Wyklad |
| 9:10-9:30 | 20 min | **SHOW:** `conftest.py` z fixturem `driver` (GENERIC: ksiazka test) - scope=session vs function | Live coding |
| 9:30-9:55 | 25 min | **DO:** Cw. 1: Zbuduj `conftest.py` dla pizzerii - fixture `driver`, fixture `live_server` (Django) | Cwiczenie |
| 9:55-10:15 | 20 min | Teoria: Page Object Model - po co, struktura klasy Page, lokalizatory jako atrybuty, akcje jako metody | Wyklad |
| 10:15-10:30 | 15 min | **SHOW:** `LoginPage` (GENERIC: bookstore) - klasa Page z lokalizatorami i metoda `login(user, pw)` | Live coding |

### Przerwa (10:30-10:40) - 10 min

### Blok 2 (10:40-12:40) - POM dla pizzerii + testy CRUD - 120 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 10:40-11:10 | 30 min | **DO:** Cw. 2: Stworz `MenuPage` z metodami `open()`, `pizza_names()`, `click_pizza(name)` | Cwiczenie |
| 11:10-11:20 | 10 min | **REVIEW:** Omowienie - dlaczego POM zmniejsza duplikacje, fluent interface (return self) | Review |
| 11:20-11:35 | 15 min | **SHOW:** Test z uzyciem POM (GENERIC: BookListPage + test) - czytelnosc | Live coding |
| 11:35-12:05 | 30 min | **DO:** Cw. 3: Stworz `AddPizzaPage` z metoda `add_pizza(name, price)` + `test_dodaj_pizze_zapisuje_w_bazie` | Cwiczenie |
| 12:05-12:15 | 10 min | **REVIEW:** Omowienie - jak laczyc strony (return next_page) | Review |
| 12:15-12:40 | 25 min | **DO:** Cw. 4: `PizzaDeletePage` (przez admin) lub negatywne testy formularza (duplikaty, ujemna cena) | Cwiczenie |

### Przerwa obiadowa (12:40-13:10) - 30 min

### Blok 3 (13:10-15:00) - E2E scenariusz + Headless + Selenium poza testami - 110 min

| Czas | Czas trwania | Temat | Typ |
|------|-------------|-------|-----|
| 13:10-13:25 | 15 min | Teoria: Test E2E vs unit/integration. Co E2E lapie, co przepuszcza. Pyramid testow. | Wyklad |
| 13:25-13:55 | 30 min | **DO:** Cw. 5: Pelny scenariusz E2E "admin zarzadza menu" - dodanie pizzy -> weryfikacja na liscie -> blokada duplikatu -> walidacja ujemnej ceny | Cwiczenie |
| 13:55-14:10 | 15 min | **SHOW:** Headless mode + screenshot przy bledzie (GENERIC: pytest hook `pytest_runtest_makereport`) | Live coding |
| 14:10-14:25 | 15 min | **DO:** Cw. 6: Wlacz headless w `conftest.py` + dodaj automatyczny screenshot przy fail teste | Cwiczenie |
| 14:25-14:40 | 15 min | **SHOW:** Selenium do scrapingu (poza testami) - przyklad: pobierz menu z innej pizzerii i zapisz do JSON | Live coding |
| 14:40-14:50 | 10 min | Podsumowanie weekendu 5 + calego kursu. Selenium w CI/CD, alternatywy (Playwright, Cypress). | Wyklad |
| 14:50-14:55 | 5 min | Omowienie zadania domowego - testy E2E dla klientow + admin login | Wyklad |
| 14:55-15:00 | 5 min | Q&A, pozegnanie | Outro |

---

## Przyklady SHOW vs DO

Zgodnie z ustalonym wzorcem: SHOW uzywa innej domeny (bookstore, generyczne strony) niz DO (pizzeria_django).

| Sekcja | SHOW (przyklad) | DO (zadanie) |
|--------|----------------|--------------|
| Pierwszy skrypt | Otworz google.com, wydrukuj tytul | Otworz `/menu/` pizzerii i wydrukuj tytul |
| Lokalizatory | Bookstore - znajdz tytul + liste ksiazek | Pizzeria - znajdz h1 + liste pizz |
| Interakcje (formularz) | Bookstore login (login + haslo) | Formularz dodawania pizzy (`/menu/dodaj/`) |
| WebDriverWait | Bookstore search - czekaj na wyniki | Pizzeria - czekaj na message.success po dodaniu |
| Pytest + Selenium | Test bookstore - sprawdz tytul | `test_pizza_list_displays_pizzas` |
| conftest.py + fixtures | Generyczny `driver` fixture | `driver` + `live_server` dla pizzerii |
| Page Object Model | `LoginPage` (bookstore) | `MenuPage` + `AddPizzaPage` (CRUD pizzy) |
| Headless + screenshots | pytest hook GENERIC | Wlacz dla pizzerii, screenshot przy fail |
| Scraping | Pobierz menu z innej pizzerii | (pokaz, bez DO) |

---

## Struktura projektu testow

```
0910-05-2026/pizzeria_django/         # projekt Django (Weekend 4)
  manage.py
  pizzeria_project/
  menu_app/
  customers_app/
  orders_app/
  api/
  tests_e2e/                          # NOWE - testy Selenium
    __init__.py
    conftest.py                       # fixture driver (live_server z pytest-django)
    pages/                            # Page Object Model
      __init__.py
      base_page.py                    # klasa bazowa Page
      menu_page.py                    # MenuPage (lista pizz)
      add_pizza_page.py               # AddPizzaPage (formularz)
    test_menu.py                      # testy listy pizz
    test_dodawanie_pizzy.py           # testy formularza (sukces + walidacja)
    test_e2e_admin_menu.py            # test E2E pelny scenariusz CRUD pizzy
  pytest.ini                          # konfiguracja pytest
```

---

## Zaleznosci techniczne

```bash
pip install selenium                  # WebDriver biblioteka (>= 4.6)
pip install webdriver-manager         # automatyczne pobieranie ChromeDriver
pip install pytest-django             # NOWE - integracja pytest z Django (live_server, db fixtures)
```

> Weekend 4 uzywal DRF `APIClient` (wbudowane w Django) do testow API - nie wymagal `pytest-django`. Dzisiaj instalujemy go po raz pierwszy, zeby skorzystac z fixtury `live_server`.

Wymagania systemowe:
- Google Chrome lub Chromium zainstalowany lokalnie (WebDriver Manager pobierze odpowiedni ChromeDriver)
- Alternatywa: Firefox + GeckoDriver

---

## Kluczowe decyzje pedagogiczne

### Po co Selenium?

Studenci znaja juz testy jednostkowe (Weekend 2) i testy API (Weekend 4). Selenium uzupelnia ten obraz:
- **Unit test** -> czy funkcja zwraca dobra wartosc
- **API test** -> czy endpoint zwraca dobry JSON
- **E2E test (Selenium)** -> czy uzytkownik przejdzie pelny scenariusz w przegladarce

### Pizzeria_django jako System Under Test

Uzywamy gotowego projektu z Weekend 4 - studenci nie pisza nowej aplikacji, tylko **testuja istniejaca**. To realistyczne - w pracy najczesciej dostajesz aplikacje i piszesz dla niej testy.

### Page Object Model od poczatku

Po pierwszym dniu wprowadzania API Selenium - drugiego dnia od razu organizujemy kod w POM. To pokazuje **profesjonalny standard** - nie pisac kazdy test od zera, tylko budowac warstwe abstrakcji.

### Headless dopiero w drugiej polowie dnia 2

W dniu 1 i pierwszej polowie dnia 2 widac przegladarke - studenci widza ze test "klika i pisze". Dopiero gdy juz rozumieja co sie dzieje, wlaczamy headless (szybciej, mozna w CI).

---

## Czas na poszczegolne aktywnosci

| Aktywnosc | Dzien 1 | Dzien 2 | Razem |
|-----------|---------|---------|-------|
| Intro/Outro | 25 min | 20 min | 45 min |
| Wyklad | 75 min | 55 min | 130 min |
| Live coding (SHOW) | 60 min | 65 min | 125 min |
| Cwiczenie (DO) | 165 min | 175 min | 340 min |
| Review | 25 min | 20 min | 45 min |
| **Razem roboczy** | **350 min** | **335 min** | **685 min** |
| Przerwy | 40 min | 40 min | 80 min |
| **Razem** | **390 min** | **375 min** | **765 min** |

---

## Checkpointy

### Dzien 1
- [ ] 9:55 - Wszyscy maja dzialajacy `selenium` + `webdriver-manager`?
- [ ] 11:40 - Wszyscy znajduja element po CSS i XPATH?
- [ ] 12:40 - Wszyscy potrafia wypelnic formularz?
- [ ] 14:55 - Wszyscy maja pierwszy test `test_pizza_list_displays_pizzas` zielony?

### Dzien 2
- [ ] 9:55 - Wszyscy maja `conftest.py` z fixturem `driver`?
- [ ] 12:05 - Wszyscy maja dzialajacy `MenuPage` + test?
- [ ] 13:55 - Wszyscy przechodza scenariusz E2E "admin zarzadza menu"?
- [ ] 14:55 - Wszyscy uruchamiaja testy w trybie headless?
