# Dzien 2: Page Object Model + testy E2E

## Agenda

**Czas trwania:** 8:30 - 15:00 (6h 30min z przerwami)

### Harmonogram

| Czas | Temat | Aktywnosc |
|------|-------|-----------|
| **8:30 - 8:50** | Recap dnia 1 | Sprawdzenie srodowiska |
| **8:50 - 10:30** | Pytest fixtures + conftest.py + POM teoria | Teoria + cwiczenia |
| **10:30 - 10:40** | **PRZERWA** | 10 minut |
| **10:40 - 12:40** | POM dla pizzerii + testy CRUD | Cwiczenia |
| **12:40 - 13:10** | **PRZERWA** | 30 minut |
| **13:10 - 15:00** | E2E scenariusz + headless + scraping | Cwiczenia + demo |

### Co zbudujemy dzisiaj?

Przeksztalcimy "luzne" testy z dnia 1 w **profesjonalna strukture**:

- `conftest.py` z fixtura `driver` (oraz `live_server` z `pytest-django`) - jeden raz, uzywane w kazdym tescie
- Page Object Model: `MenuPage` + `AddPizzaPage` - jedna klasa = jedna strona aplikacji
- Pelne testy E2E: scenariusz "admin zarzadza menu" (CRUD pizzy) od poczatku do konca
- Headless mode + automatyczne screenshoty przy fail
- Bonus: Selenium do scrapingu strony spoza pizzerii

> **Uwaga o stanie projektu:** ORM ma tylko model `Pizza`. Klasy `Customer` i `Order` z poprzednich weekendow nadal trzymaja dane w plikach JSON (folder `rozwiazanie_weekend2/`). Dlatego wszystkie cwiczenia tego dnia kreca sie wokol **pizz** - bo to jedyna domena z pelnym ORM.

---

## Czesc 1: Recap dnia 1 (20 min)

### Co umiemy z dnia 1

- Setup `selenium` + `webdriver-manager`
- Lokalizatory: `By.ID`, `By.CSS_SELECTOR`, `By.XPATH`, `By.LINK_TEXT`
- Interakcje: `click()`, `send_keys()`, `clear()`, `text`, `get_attribute()`
- `WebDriverWait` + `expected_conditions`
- Pierwszy test pytest + Selenium

### Sprawdzenie srodowiska

Jesli wczoraj `runserver` byl uruchomiony - dzis tez go uruchom (na chwile, do dopiero co napisanych testow z dnia 1):

```bash
cd 0910-05-2026/pizzeria_django
python3 manage.py runserver
```

Test z dnia 1 (`tests_e2e/test_pizza_list.py`) zawiera lokalna fixture `driver`. Dzis przeniesiemy ja do `conftest.py` i zaczniemy uzywac `live_server` zamiast `runserver`. **Nim to zrobimy** - usun lokalna fixture z pliku testu (inaczej zasloni nowa z conftest.py).

### Dlaczego potrzebujemy POM?

Wyobraz sobie 10 testow ktore wszystkie zaczynaja sie podobnie:

```python
def test_pizza_dodana_pojawia_sie_na_liscie(driver):
    driver.get("http://127.0.0.1:8000/menu/dodaj/")
    driver.find_element(By.NAME, "name").send_keys("Margherita")
    driver.find_element(By.NAME, "price").send_keys("25")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    # ...

def test_pizza_z_ujemna_cena_zwraca_blad(driver):
    driver.get("http://127.0.0.1:8000/menu/dodaj/")
    driver.find_element(By.NAME, "name").send_keys("ZlaPizza")
    driver.find_element(By.NAME, "price").send_keys("-5")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    # ...

# i tak 8 razy wiecej...
```

**Problem 1:** Powtarzanie kodu (`driver.find_element(By.NAME, "name")` w 10 miejscach).

**Problem 2:** Jesli developer zmieni `name="name"` na `name="pizza_name"` w HTML - poprawiac w 10 miejscach.

**Problem 3:** Test wyglada jak instrukcja "kliknij to, wpisz tamto" - **trudno przeczytac** co test sprawdza biznesowo.

POM rozwiazuje wszystkie trzy.

---

## Czesc 2: Pytest fixtures - przyspieszenie (40 min)

### Teoria: Fixture scope (20 min)

Fixture moze miec rozne **zasiegi** (scope) - ile razy jest tworzona:

| Scope | Tworzona... | Kiedy uzywac |
|-------|-------------|--------------|
| `function` (domyslny) | przed kazdym testem | gdy test musi miec **swiezy** stan |
| `class` | raz na klase testowa | gdy testy w klasie wspoldziela stan |
| `module` | raz na plik | rzadko |
| `session` | raz na cale uruchomienie pytest | gdy stworzenie zasobu jest **drogie** |

**Selenium driver** jest drogi (start Chrome ~1-2s). Jesli mamy 50 testow, scope='function' = 50 razy 1.5s = 75 sekund **tylko na start drivera**!

Opcja 1: `scope='session'` - jeden driver na wszystkie testy. **Ryzyko:** stan z poprzedniego testu wycieka.

Opcja 2: `scope='function'` z driver per test. **Ryzyko:** wolne, ale izolowane.

### conftest.py - wspolne fixtures

`conftest.py` to specjalny plik pytest. Fixtury z niego sa **automatycznie dostepne** we wszystkich testach w tym folderze (i podfolderach).

```
tests_e2e/
  conftest.py           <- definicja fixture driver
  test_menu.py          <- moze uzywac fixture driver
  test_zamowienia.py    <- tez moze uzywac
  pages/
    test_inny.py        <- tez (folder ponizej)
```

**Bez `conftest.py`:** musisz definiowac fixture w **kazdym** pliku testowym albo importowac.

### live_server - serwer Django dla testow

W dniu 1 musielismy **recznie** uruchamiac `python manage.py runserver`. Niewygodne i zawodne (a jak ktos ma juz 8000 zajete?).

**`pytest-django`** daje fixture `live_server` ktory:
1. Automatycznie startuje serwer Django **w tle**
2. Daje URL (`live_server.url`) - np. `http://localhost:38291/`
3. Po skonczeniu testow zatrzymuje serwer
4. Automatycznie tworzy **pusta** baze (test database)

```python
def test_cos(live_server, driver):
    driver.get(f"{live_server.url}/menu/")
    # ...
```

**Wazne:** `live_server` wymaga `pytest-django` + `pytest.ini` z konfiguracja DJANGO_SETTINGS_MODULE.

### SHOW: Generyczny conftest.py (20 min)

Generyczny `conftest.py` z fixtura `driver` - to jedyna fixtura ktora bedzie potrzebna we **wszystkich** testach Selenium tego dnia:

```python
# tests_e2e/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """WebDriver dla pojedynczego testu - czysty stan, sprzatany po fail."""
    options = Options()
    # options.add_argument("--headless=new")  # wlaczymy pozniej

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    # Bez implicit_wait. POM uzywa jawnych WebDriverWait - mieszanie
    # implicit + explicit prowadzi do nieprzewidywalnych timeoutow.
    yield drv
    drv.quit()
```

I przyklad testu - **uruchamialny** na pliku z dnia 1 (`bookstore_list.html`):

```python
# tests_e2e/test_homepage.py
from pathlib import Path
from selenium.webdriver.common.by import By

PAGE_URL = "file://" + str(
    Path("0910-05-2026/dzien1/bookstore_list.html").resolve()
)


def test_homepage_ma_tytul(driver):
    driver.get(PAGE_URL)
    h1 = driver.find_element(By.TAG_NAME, "h1")
    assert "Ksiegarnia" in h1.text


def test_homepage_ma_liste_ksiazek(driver):
    driver.get(PAGE_URL)
    books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
    assert len(books) > 0
```

**Zauwaz:** Test dostaje `driver` automatycznie (pytest dopasowuje po nazwie). Brak `import` fixtury - dziala bo `conftest.py` jest w tym samym folderze.

### DO: Cw. 1 - conftest.py dla pizzerii (25 min)

**Cel:** Zbuduj `conftest.py` dla projektu pizzerii z fixtura `driver` (oraz wbudowana `live_server` z `pytest-django`).

**Krok 1:** Zainstaluj `pytest-django` (Weekend 4 nie wymagal go - DRF ma swoj wbudowany `APIClient`):

```bash
pip install pytest-django
```

**Krok 2:** Sprawdz `pytest.ini` w projekcie pizzerii. Powinien zawierac:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = pizzeria_project.settings
python_files = test_*.py
```

Jesli go nie ma - utworz go w `pizzeria_django/pytest.ini`.

**Krok 3:** Najpierw **usun** lokalna fixture `driver` z pliku `tests_e2e/test_pizza_list.py` (z dnia 1). Inaczej zasloni nowa z conftest.

**Krok 4:** Stworz `tests_e2e/conftest.py`:

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless=new")  # wlaczymy pod koniec dnia

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    # NIE mieszamy implicit + explicit wait. POM uzywa jawnych WebDriverWait,
    # implicit_wait moglby zaklocic timeouty. Zostawiamy tylko explicit.
    yield drv
    drv.quit()
```

**Krok 5:** `live_server` jest wbudowane w `pytest-django` - nie trzeba go definiowac samemu. Jest dostepne **wszedzie** gdzie masz `pytest-django`.

**Krok 6:** Test ktory uzywa obu fixtur. Boilerplate gotowy - **cialo testu uzupelniasz sam**:

```python
# tests_e2e/test_menu_z_live_server.py
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.django_db
def test_menu_dziala_z_live_server(live_server, driver):
    """live_server uruchamia Django automatycznie - nie trzeba runserver."""
    # 1. Wejdz pod f"{live_server.url}/menu/"
    # 2. Znajdz h1 (By.TAG_NAME, "h1")
    # 3. Asercja: h1.text nie jest pusty
    pass
```

**Krok 7:** Uruchom **bez** `python manage.py runserver` (`live_server` zrobi to sam):

```bash
pytest tests_e2e/test_menu_z_live_server.py -v
```

**Co sie powinno stac:**
1. Pytest startuje
2. `live_server` w tle uruchamia Django na losowym porcie
3. `driver` startuje Chrome
4. Test wchodzi na `live_server.url + /menu/` - widzi pusta liste pizz (bo testowa baza jest pusta)
5. `assert h1.text != ""` - pass (bo h1 istnieje, choc liste pusta)
6. Driver zamyka, serwer zatrzymuje sie

**Krok 8:** Zauwaz: w bazie testowej **nie ma** pizz! `live_server` tworzy **pusta** baze testowa. Nasze pizze z dev'owej bazy `db.sqlite3` nie sa widoczne.

To jest dobre - testy maja **kontrolowany** stan. Ale musimy nauczyc sie **wstawiac dane** do bazy testowej:

```python
@pytest.mark.django_db
def test_z_pizza_w_bazie(live_server, driver):
    from menu_app.models import Pizza
    Pizza.objects.create(name="TestPizza", price=20.0)

    driver.get(f"{live_server.url}/menu/")
    # Tekst nazwy pizzy jest w <h5 class="card-title">, nie w <a>
    karty = driver.find_elements(By.CSS_SELECTOR, ".card-title")
    nazwy = [k.text for k in karty]
    assert "TestPizza" in nazwy
```

`@pytest.mark.django_db` mowi pytest-django: "ten test korzysta z bazy". Po tescie baza jest **automatycznie czyszczona** - kazdy test dostaje swieza pusta baze (transactional rollback).

**Bonus:** Stworz fixture `pizza_factory` ktora pomaga tworzyc pizze w bazie. Pytest-django udostepnia juz fixture `db` jako bramke do bazy - mozna ja "pociagnac" w naszym fixture przez parametr:

```python
@pytest.fixture
def pizza_factory(db):
    from menu_app.models import Pizza
    def _factory(name, price=20.0):
        return Pizza.objects.create(name=name, price=price)
    return _factory
```

I test (uwaga: `pizza_factory` juz pociagnal `db`, wiec `@pytest.mark.django_db` na tescie nie jest tu konieczne - ale dla czytelnosci zwykle dodajemy):

```python
@pytest.mark.django_db
def test_lista_zawiera_dodana_pizze(live_server, driver, pizza_factory):
    pizza_factory("Hawajska", 32)
    driver.get(f"{live_server.url}/menu/")
    karty = driver.find_elements(By.CSS_SELECTOR, ".card-title")
    assert "Hawajska" in [k.text for k in karty]
```

---

## Czesc 3: Page Object Model - teoria (20 min)

### Czym jest POM?

**Page Object Model** to wzorzec projektowy: kazda strona aplikacji = jedna klasa Pythona.

```
Strona w aplikacji        ->    Klasa POM
http://.../menu/           ->    MenuPage
http://.../menu/dodaj/     ->    AddPizzaPage
http://.../menu/<nazwa>/   ->    PizzaDetailPage
http://.../admin/login/    ->    AdminLoginPage  (zad. domowe)
```

Klasa POM zawiera:
- **Lokalizatory** (gdzie sa elementy) - jako atrybuty klasy
- **Akcje** (co mozna zrobic na stronie) - jako metody

### Bez POM vs Z POM

**Bez POM** (rozsiane lokalizatory w testach):

```python
def test_dodaj_pizze(driver, live_server):
    driver.get(f"{live_server.url}/menu/dodaj/")
    driver.find_element(By.NAME, "name").send_keys("Margherita")
    driver.find_element(By.NAME, "price").send_keys("25")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be(f"{live_server.url}/menu/"))  # nie url_contains - byloby trywialne
    assert "Margherita" in driver.page_source
```

**Z POM** (logika strony w klasie):

```python
def test_dodaj_pizze(driver, live_server):
    add_page = AddPizzaPage(driver, live_server.url)
    menu_page = add_page.open().add_pizza("Margherita", 25)
    assert "Margherita" in menu_page.pizza_names()
```

Test stal sie **biznesowo czytelny**: "otworz strone dodawania, dodaj pizze, sprawdz ze jest na liscie".

### Struktura klasy POM

```python
class MenuPage:
    URL_PATH = "/menu/"

    # 1. Lokalizatory (Bootstrap karty - z Weekend 4)
    NAGLOWEK = (By.TAG_NAME, "h1")
    PIZZA_TITLES = (By.CSS_SELECTOR, ".card-title")
    PIZZA_DETAIL_LINKS = (By.CSS_SELECTOR, ".card a.btn-outline-primary")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    # 2. Nawigacja
    def open(self):
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait.until(EC.visibility_of_element_located(self.NAGLOWEK))
        return self

    # 3. Asercje (zapytania)
    def pizza_names(self):
        elements = self.driver.find_elements(*self.PIZZA_TITLES)
        return [e.text for e in elements]

    # 4. Akcje (klikniecia)
    def click_pizza_detail(self, name):
        # tekst linka to "Szczegoly", wiec szukamy po href
        link = self.driver.find_element(By.CSS_SELECTOR, f"a[href$='{name}/']")
        link.click()
        # PizzaDetailPage - import wewnatrz funkcji zeby uniknac cyklu
        from .pizza_detail_page import PizzaDetailPage
        return PizzaDetailPage(self.driver, self.base_url)
```

### Kluczowe wzorce

**1. Lokalizatory jako tuple `(By, "selector")`:**
```python
NAGLOWEK = (By.TAG_NAME, "h1")
# uzycie z gwiazdka:
self.driver.find_element(*self.NAGLOWEK)
```

**2. Metody zwracaja `self` (fluent interface) lub nastepna strone:**
```python
def open(self):
    ...
    return self                    # mozemy chainowac: page.open().pizza_names()

def click_pizza(self, name):
    ...
    return PizzaDetailPage(...)    # przejscie do innej strony
```

**3. Wait wbudowany w POM:**
```python
def open(self):
    self.driver.get(...)
    self.wait.until(EC.visibility_of_element_located(self.NAGLOWEK))  # <-- czekanie ZAWSZE
    return self
```

Test nie musi pisac `WebDriverWait` - POM to robi za niego.

### SHOW: LoginPage dla bookstore (15 min)

Zeby pokazac POM **na czyms uruchamialnym** - wracamy do `bookstore_login.html` z dnia 1. To pojedynczy plik HTML z formularzem i kawalkiem JS, ktory po submit pokazuje `.welcome-message`. Idealne do POM-a:

```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """POM dla bookstore_login.html z dnia 1.
    base_url to file:// URL pliku HTML - w realnym projekcie byloby
    np. "http://localhost:8000" + URL_PATH = "/login/".
    """
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.ID, "login-btn")
    WELCOME_MSG = (By.CSS_SELECTOR, ".welcome-message")

    def __init__(self, driver, page_url):
        self.driver = driver
        self.page_url = page_url
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.page_url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        return self

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BTN).click()
        # Po submit JS pokazuje .welcome-message - czekamy na nia.
        self.wait.until(EC.visibility_of_element_located(self.WELCOME_MSG))
        return self

    def welcome_text(self):
        return self.driver.find_element(*self.WELCOME_MSG).text
```

Test (rzeczywiscie dziala - mozesz uruchomic):

```python
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PAGE_URL = "file://" + str(
    Path("0910-05-2026/dzien1/bookstore_login.html").resolve()
)


def test_login_pokazuje_komunikat_powitalny():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        login = LoginPage(driver, PAGE_URL).open()
        login.login("jan@example.com", "Tajne123")
        assert login.welcome_text() == "Witaj, jan@example.com!"
    finally:
        driver.quit()
```

Zauwaz: test operuje na **abstrakcji biznesowej** (`login(...)`), nie na lokalizatorach. Lokalizatory siedza wylacznie w `LoginPage`.

---

## Czesc 4: POM dla pizzerii (90 min)

### DO: Cw. 2 - MenuPage (30 min)

**Cel:** Stworz pierwsza klase POM dla strony `/menu/` pizzerii.

**Krok 1:** Stworz strukture folderow:

```bash
cd 0910-05-2026/pizzeria_django/tests_e2e
mkdir pages
touch pages/__init__.py
touch pages/base_page.py
touch pages/menu_page.py
```

**Krok 2:** `pages/base_page.py` - klasa bazowa dla wszystkich Page Objectow:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Wspolne funkcjonalnosci dla wszystkich stron."""
    URL_PATH = ""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, 10)

    def url(self):
        return f"{self.base_url}{self.URL_PATH}"

    def go(self):
        self.driver.get(self.url())

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
```

**Krok 3:** `pages/menu_page.py`:

```python
from selenium.webdriver.common.by import By
from tests_e2e.pages.base_page import BasePage


class MenuPage(BasePage):
    URL_PATH = "/menu/"

    # Lokalizatory - Bootstrap karty z Weekend 4
    NAGLOWEK = (By.TAG_NAME, "h1")
    PIZZA_CARDS = (By.CSS_SELECTOR, ".card")
    PIZZA_TITLES = (By.CSS_SELECTOR, ".card-title")
    PIZZA_PRICES = (By.CSS_SELECTOR, ".card .price")
    DODAJ_LINK = (By.LINK_TEXT, "Dodaj pizze")

    def open(self):
        self.go()
        self.wait_for_visible(self.NAGLOWEK)
        return self

    def title(self):
        return self.driver.find_element(*self.NAGLOWEK).text

    def pizza_count(self):
        return len(self.driver.find_elements(*self.PIZZA_CARDS))

    def pizza_names(self):
        return [e.text for e in self.driver.find_elements(*self.PIZZA_TITLES)]

    def has_pizza(self, name):
        return name in self.pizza_names()

    def click_dodaj(self):
        self.driver.find_element(*self.DODAJ_LINK).click()
        # AddPizzaPage - import wewnatrz funkcji zeby uniknac cyklu (stworzymy w Cw. 3)
        from tests_e2e.pages.add_pizza_page import AddPizzaPage
        return AddPizzaPage(self.driver, self.base_url)
```

> **Uwaga o importach:** uzywamy importow **bezwzglednych** (`from tests_e2e.pages...`), nie wzglednych (`from .pages...`). Pytest z domyslna konfiguracja zbiera testy z roznych folderow i wzgledne importy w plikach testow czesto rzucaja `ImportError: attempted relative import with no known parent package`. Bezwzgledne sa stabilne. Wymaga to pliku `tests_e2e/__init__.py` (juz utworzony w dniu 1).

**Krok 4:** Testy uzywajace MenuPage. Boilerplate gotowy - **cialo kazdego testu uzupelniasz sam**:

```python
# tests_e2e/test_menu.py
import pytest
from tests_e2e.pages.menu_page import MenuPage


@pytest.mark.django_db
def test_menu_jest_puste_w_swiezej_bazie(live_server, driver):
    """live_server tworzy pusta baze testowa - menu powinno byc puste."""
    # 1. Otworz MenuPage
    # 2. Asercja: pizza_count() == 0
    pass


@pytest.mark.django_db
def test_menu_pokazuje_pizze_z_bazy(live_server, driver):
    """Pizze stworzone przez ORM pojawiaja sie na liscie."""
    # 1. Stworz dwie Pizze przez ORM (Pizza.objects.create(...))
    #    Wskazowka: from menu_app.models import Pizza
    # 2. Otworz MenuPage
    # 3. Asercje: pizza_count() == 2, has_pizza("Margherita"), has_pizza("Pepperoni")
    pass


@pytest.mark.django_db
def test_menu_ma_naglowek(live_server, driver):
    """Strona ma naglowek <h1> zawierajacy slowo 'Menu'."""
    # 1. Otworz MenuPage
    # 2. Asercja: "Menu" w menu.title()
    pass
```

**Krok 5:** Uruchom:

```bash
pytest tests_e2e/test_menu.py -v
```

3 testy powinny przejsc.

**Bonus:** Dodaj metode `pizza_prices()` ktora zwraca liste cen jako floaty (parsuj `.card .price` text typu "25.0 zl"). Nastepnie metode `cheapest_pizza()` zwracajaca nazwe najtanszej.

### REVIEW: Dlaczego to dziala (10 min)

Patrz na test:
```python
menu = MenuPage(driver, live_server.url).open()
assert menu.pizza_count() == 2
```

vs to samo bez POM:
```python
driver.get(f"{live_server.url}/menu/")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
items = driver.find_elements(By.CSS_SELECTOR, ".card")
assert len(items) == 2
```

**POM:**
- Krocej
- Czytelniej (`pizza_count()` mowi WHAT, nie HOW)
- Lokalizatory tylko w jednym miejscu (`MenuPage.PIZZA_CARDS`)
- Jesli zmienimy template (np. zamiast Bootstrap kart dasz table) - poprawiamy 1 miejsce w `MenuPage`

### DO: Cw. 3 - AddPizzaPage z fluent interface (30 min)

**Cel:** Stworz POM dla formularza `/menu/dodaj/` z metoda `add_pizza(name, price)` ktora **zwraca** MenuPage po sukcesie.

**Krok 1:** `pages/add_pizza_page.py`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tests_e2e.pages.base_page import BasePage
from tests_e2e.pages.menu_page import MenuPage


class AddPizzaPage(BasePage):
    URL_PATH = "/menu/dodaj/"

    NAME_INPUT = (By.NAME, "name")
    PRICE_INPUT = (By.NAME, "price")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    # Bledy walidacji formularza pojawiaja sie w <div class="alert alert-danger">
    ERROR_MSG = (By.CSS_SELECTOR, ".alert-danger")

    def open(self):
        self.go()
        self.wait_for_visible(self.NAME_INPUT)
        return self

    def fill_name(self, name):
        field = self.driver.find_element(*self.NAME_INPUT)
        field.clear()
        field.send_keys(name)
        return self

    def fill_price(self, price):
        field = self.driver.find_element(*self.PRICE_INPUT)
        field.clear()
        field.send_keys(str(price))
        return self

    def submit_expecting_success(self):
        self.driver.find_element(*self.SUBMIT_BTN).click()
        # Po sukcesie redirect z /menu/dodaj/ na /menu/. UWAGA: nie url_contains
        # bo "/menu/" jest podlancuchem "/menu/dodaj/" - byloby trywialnie spelnione.
        self.wait.until(EC.url_to_be(f"{self.base_url}/menu/"))
        return MenuPage(self.driver, self.base_url)

    def submit_expecting_error(self):
        self.driver.find_element(*self.SUBMIT_BTN).click()
        self.wait_for_visible(self.ERROR_MSG)
        return self

    def add_pizza(self, name, price):
        """Helper: wypelnij + submit + zwroc MenuPage."""
        return (
            self.fill_name(name)
                .fill_price(price)
                .submit_expecting_success()
        )

    def get_error(self):
        try:
            return self.driver.find_element(*self.ERROR_MSG).text
        except Exception:
            return None
```

**Krok 2:** Testy. Boilerplate gotowy - **cialo kazdego testu uzupelniasz sam**:

```python
# tests_e2e/test_dodawanie_pizzy.py
import pytest
from tests_e2e.pages.add_pizza_page import AddPizzaPage


@pytest.mark.django_db
def test_dodaj_pizze_pojawia_sie_w_bazie(live_server, driver):
    """Dodanie pizzy przez formularz tworzy rekord w bazie i pizza widoczna na liscie."""
    # 1. Otworz AddPizzaPage
    # 2. Wywolaj add_pizza("Hawajska", 32) - dostaniesz MenuPage
    # 3. Asercja UI: menu_page.has_pizza("Hawajska")
    # 4. Asercja bazy: Pizza.objects.filter(name="Hawajska").exists()
    #    Wskazowka: from menu_app.models import Pizza
    pass


@pytest.mark.django_db
def test_dodaj_duplicate_pizze_pokazuje_blad(live_server, driver):
    """Pizza o tej samej nazwie nie moze byc dodana drugi raz."""
    # 1. Stworz Pizze przez ORM (np. "Margherita", 25)
    # 2. Otworz AddPizzaPage
    # 3. fill_name("Margherita").fill_price(28).submit_expecting_error()
    # 4. Asercja: get_error() nie jest None i zawiera "juz istnieje" (lub podobne)
    pass
```

> **Uwaga o pustej nazwie:** Pole `name` w formularzu ma atrybut HTML `required`. Browser **zablokuje** submit zanim zapytanie pojdzie do serwera - wtedy `submit_expecting_error()` zacznie czekac na `.alert-danger`, ktory nigdy sie nie pojawi (bo zaden POST nie poszedl). Pomijamy ten przypadek - testowanie HTML-owej walidacji `required` to inna kategoria. Skupiamy sie na walidacji **serwerowej** (duplikat, ujemna cena - ktorej `min="0.01"` browser tez moze blokowac, ale ServerSide ValidationError ja zlapie tak czy inaczej).

**Krok 3:** Uruchom: `pytest tests_e2e/test_dodawanie_pizzy.py -v`

**Krok 4:** Zwroc uwage na **dwie warstwy asercji** w `test_dodaj_pizze_pojawia_sie_w_bazie`:
1. UI: `menu_page.has_pizza("Hawajska")` - klient widzi pizze
2. Baza: `Pizza.objects.filter(...).exists()` - rekord faktycznie sie zapisal

To wazne - sama asercja UI moze byc bledna (np. backend pokazuje pizze ale jej nie zapisuje).

**Bonus:** Sprawdz w DevTools czy formularz ma `min="0.01"` na polu price. Jesli tak - wpisanie ujemnej liczby zablokuje submit po stronie HTML. Sprobuj obejsc to przez `driver.execute_script("arguments[0].removeAttribute('min')", price_input)` zeby wymusic POST i przetestowac walidacje serwerowa (`InvalidPriceError`).

### REVIEW: Fluent interface (10 min)

Zauwaz wzorzec w `AddPizzaPage`:

```python
def fill_name(self, name):
    ...
    return self           # <- zwraca siebie
```

Pozwala chainowac:

```python
add_page.fill_name("X").fill_price(20).submit_expecting_success()
```

vs bez chainowania:
```python
add_page.fill_name("X")
add_page.fill_price(20)
add_page.submit_expecting_success()
```

Pierwsza wersja jest bardziej zwarta. Druga jasniejsza dla niektorych. **Wybor stylu** zalezy od zespolu.

### DO: Cw. 4 - PizzaDetailPage + nawigacja miedzy stronami (25 min)

**Cel:** Stworz prosty `PizzaDetailPage` ktory reprezentuje strone `/menu/<nazwa>/` i przetestuj nawigacje `MenuPage -> PizzaDetailPage`.

> **Uwaga:** widok `pizza_detail` w projekcie z Weekend 4 wciaz laduje pizze z **pliku JSON** (`menu.json`) - nie z ORM. Pizza dodana przez `live_server` (do bazy testowej) **nie pojawi sie** w detalu. Dlatego ten test musi seedowac dane do JSON-a, albo testowac `Http404` dla pizzy ktorej nie ma w JSON-ie. Wybieramy drugi wariant - prostszy.

**Krok 1:** `pages/pizza_detail_page.py`:

```python
from selenium.webdriver.common.by import By
from tests_e2e.pages.base_page import BasePage


class PizzaDetailPage(BasePage):
    # URL_PATH dynamiczny - zalezy od nazwy pizzy
    NAGLOWEK = (By.TAG_NAME, "h1")
    BODY = (By.TAG_NAME, "body")

    def open(self, pizza_name):
        self.driver.get(f"{self.base_url}/menu/{pizza_name}/")
        self.wait_for_visible(self.BODY)
        return self

    def is_404(self):
        # DEBUG=True w settings.py -> Django pokazuje techniczna strone 404
        # z tekstem "Page not found (404)" w body. Sprawdzamy oba warianty.
        body_text = self.driver.find_element(*self.BODY).text
        return "404" in body_text or "Page not found" in body_text

    def heading(self):
        return self.driver.find_element(*self.NAGLOWEK).text
```

**Krok 2:** Test. Boilerplate gotowy - **cialo testu uzupelniasz sam**:

```python
# tests_e2e/test_pizza_detail.py
import pytest
from tests_e2e.pages.pizza_detail_page import PizzaDetailPage


@pytest.mark.django_db
def test_pizza_z_bazy_ale_nie_z_json_zwraca_404(live_server, driver):
    """
    Pizza istnieje w ORM (baza), ale widok detalu wciaz laduje JSON
    z Weekend 3 - wiec dla pizzy spoza JSON-a dostaniemy 404.
    Ten test dokumentuje znane ograniczenie projektu.
    """
    # 1. Stworz Pizze "OrmOnly" przez ORM
    #    Wskazowka: from menu_app.models import Pizza
    # 2. Otworz PizzaDetailPage dla "OrmOnly"
    # 3. Asercja: detail.is_404()
    pass
```

**Krok 3:** Uruchom: `pytest tests_e2e/test_pizza_detail.py -v`

**Krok 4:** Test passuje, bo dokumentuje **rzeczywiste** zachowanie projektu - nie idealne, ale honest.

**Bonus 1:** Napraw widok `pizza_detail` w `menu_app/views.py` zeby uzywal ORM zamiast JSON. Po naprawie test bedzie failowal - to dobre, bo znaczy ze 404 juz nie wystepuje. Zmien test na `assert detail.heading() == "OrmOnly"`.

**Bonus 2:** Selenium IDE - rozszerzenie do Chrome/Firefox ktore "nagrywa" Twoje klikniecia i eksportuje je jako kod Selenium. Przydatne na poczatek. Zainstaluj z https://www.selenium.dev/selenium-ide/ , nagraj prosty scenariusz "wejdz na /menu/, klinij Szczegoly", wyeksportuj jako Python pytest. Porownaj z Twoim POM-em - co jest lepsze, co gorsze?

---

## Czesc 5: Test E2E - pelny scenariusz (30 min)

### Teoria: Pyramida testow (15 min)

```
        /\
       /  \      E2E (Selenium)        - duzo, wolne, kompletne
      /----\
     /      \    Integration (API)     - sredni
    /--------\
   /          \  Unit                  - duzo, szybkie
  /____________\
```

**Reguly piramidy:**

| Warstwa | Liczba testow | Czas pojedynczego | Co lapie |
|---------|--------------|--------------------|----------|
| Unit | 1000+ | <10ms | Bledy w pojedynczych funkcjach |
| Integration | 100 | <100ms | Bledy w komunikacji modulow |
| E2E | 10 | sekundy | Bledy w pelnym przeplywie |

**Anti-pattern: ice-cream cone** - duzo E2E, malo unit. Powolne, niestabilne testy.

**Praktyka:** Selenium E2E rezerwujemy na **kluczowe scenariusze biznesowe** ("admin dodaje pizze do menu", "klient zamawia pizze") - nie na wszystkie kombinacje walidacji.

### DO: Cw. 5 - Pelny scenariusz E2E "admin zarzadza menu" (30 min)

**Cel:** Napisz pelny test E2E ktory wykonuje pelny przeplyw zarzadzania menu z perspektywy administratora.

**Scenariusz biznesowy:**
1. Admin wchodzi na puste menu pizzerii
2. Klika "Dodaj pizze" -> trafia na formularz
3. Dodaje pierwsza pizze ("Margherita", 25 zl)
4. Wraca na liste -> pizza widoczna
5. Probuje dodac duplikat -> formularz odrzuca
6. Dodaje druga pizze ("Pepperoni", 30 zl) -> widoczna na liscie
7. Sprawdzenie konsystencji UI <-> baza ORM

**Krok 1:** `tests_e2e/test_e2e_admin_menu.py`. Boilerplate (importy + dekorator + sygnatura) gotowy - kazdy z 7 krokow scenariusza **uzupelniasz sam**. Sprawdz co masz w `MenuPage` i `AddPizzaPage` - to wszystko czego potrzebujesz.

```python
import pytest
from tests_e2e.pages.menu_page import MenuPage
from tests_e2e.pages.add_pizza_page import AddPizzaPage


@pytest.mark.django_db
def test_e2e_admin_zarzadza_menu(live_server, driver):
    """
    Pelny scenariusz biznesowy: admin buduje menu od zera.
    """
    from menu_app.models import Pizza

    # KROK 1: Wejdz na puste menu (utworz MenuPage, .open())
    # Asercja: menu.pizza_count() == 0


    # KROK 2: Admin klika "Dodaj pizze" -> trafia na formularz
    # Wskazowka: menu.click_dodaj() zwraca AddPizzaPage


    # KROK 3: Dodaj pierwsza pizze ("Margherita", 25)
    # Wskazowka: add_page.add_pizza(...) zwraca MenuPage
    # Asercja: menu.has_pizza("Margherita"), menu.pizza_count() == 1


    # KROK 4: Sprobuj dodac duplikat ("Margherita") - powinno sie nie powiesc
    # Wskazowka: AddPizzaPage(...).open(), fill_name + fill_price + submit_expecting_error
    # Asercja: add_page.get_error() jest niepusty


    # KROK 5: Dodaj DRUGA pizze ("Pepperoni", 30) na tym samym AddPizzaPage
    # (nie trzeba ponownie .open() - wystarczy fill_name/fill_price/submit_expecting_success)
    # Asercja: menu.pizza_count() == 2, has_pizza("Margherita") i has_pizza("Pepperoni")


    # KROK 6: Asercja na poziomie bazy - rzeczywiscie sa 2 rekordy
    # Wskazowka: Pizza.objects.count(), Pizza.objects.values_list("name", flat=True)


    pass  # usun gdy uzupelnisz wszystkie kroki
```

**Krok 2:** Uruchom:

```bash
pytest tests_e2e/test_e2e_admin_menu.py -v
```

**Krok 3:** Patrz na okno przegladarki - widzisz **caly scenariusz** odgrywany krok po kroku. To jest moc E2E - widac dokladnie co robi uzytkownik.

**Krok 4:** Dodaj `print()` w kazdym kroku - zauwaz jak Selenium "klika" i "pisze" automatycznie.

**Bonus 1:** Zmierz czas trwania testu (`-v` pokazuje czas). Porownaj z testem unit z Weekend 4 (~10ms vs sekundy E2E).

**Bonus 2:** Czemu ten test traktujemy jako **jeden** scenariusz, a nie 6 osobnych? Zaleta: testuje **przeplyw** - "z menu mozna przejsc do formularza, dodac pizze i wrocic do menu". Wada: gdy pierwszy krok pada, kolejne nie sa wykonane (no diagnostic).

**Bonus 3:** Co bys zrobil zeby test zamawiania (klient -> wybor pizzy -> zamowienie) bylo mozliwe? Wskazowka: trzeba przeniesc Customer i Order z plikow JSON do ORM (zadanie domowe).

---

## Czesc 6: Headless mode + screenshoty (30 min)

### Teoria: Headless

**Headless** = przegladarka bez GUI. Korzysci:
- **Szybsze** (nie renderuje pikseli na ekran)
- **Mozna na CI/CD** (serwery nie maja monitora)
- **Mozna w tle** (nie przeszkadza)

Wada: nie widzisz co sie dzieje. Stosujemy **dopiero** gdy testy sa juz dopracowane.

### Screenshot na fail

Jesli test E2E **fail** w CI - co poszlo nie tak? Headless = nie widzisz okna.

Rozwiazanie: **automatyczny screenshot** w momencie bledu.

```python
driver.save_screenshot("/tmp/fail.png")
```

Ale lepiej zrobic to **automatycznie** dla kazdego failujacego testu - przez **pytest hook** `pytest_runtest_makereport`.

### SHOW: pytest hook (15 min)

Dodaj do `conftest.py`:

```python
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Po failujacym tescie zrob screenshot z drivera."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            import os
            os.makedirs(screenshot_dir, exist_ok=True)
            path = f"{screenshot_dir}/{item.name}.png"
            driver.save_screenshot(path)
            print(f"\n[SCREENSHOT] {path}")
```

Co tu sie dzieje:
- `pytest_runtest_makereport` - hook uruchamiany po **kazdym** kroku testu (setup, call, teardown)
- `report.when == "call"` - filtrujemy tylko faze wlasciwego testu
- `report.failed` - tylko gdy fail
- `item.funcargs.get("driver")` - bierzemy driver z fixture
- `driver.save_screenshot(path)` - zapis pliku PNG

### DO: Cw. 6 - Headless + screenshoty (15 min)

**Krok 1:** W `conftest.py` zmien fixture `driver` zeby uzywal headless:

```python
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")           # WLACZ headless
    options.add_argument("--window-size=1920,1080")  # rozdzielczosc (responsive CSS!)

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    yield drv
    drv.quit()
```

> Pamietaj: NIE dodajemy `implicit_wait` - mieszanie z explicit waits powoduje nieprzewidywalne timeouty.

**Krok 2:** Dodaj hook screenshotu z SHOW (powyzej).

**Krok 3:** Uruchom testy:

```bash
pytest tests_e2e/ -v
```

Testy beda **szybsze**, ale nie zobaczysz okien.

**Krok 4:** Dodaj test ktory celowo failuje:

```python
@pytest.mark.django_db
def test_celowy_fail(live_server, driver):
    driver.get(f"{live_server.url}/menu/")
    assert "TextKtoryNieIstnieje" in driver.page_source
```

**Krok 5:** Uruchom - test failuje, w terminalu widzisz `[SCREENSHOT] screenshots/test_celowy_fail.png`.

**Krok 6:** Otworz plik PNG - widzisz **dokladnie** co bylo na ekranie w momencie fail. To bezcenne w CI/CD.

**Bonus:** Dodaj do nazwy screenshota timestamp zeby kolejne uruchomienia nie nadpisywaly:

```python
from datetime import datetime
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
path = f"{screenshot_dir}/{ts}_{item.name}.png"
```

---

## Czesc 7: Selenium poza testami - scraping (15 min)

### SHOW: Pobranie menu z innej pizzerii

Selenium nie jest **tylko** do testow. Mozna nim **scrape'owac** strony - wyciagac dane z aplikacji ktore nie maja API.

Przyklad: chcesz sciagnac menu konkurencyjnej pizzerii (ktora ma tylko strone HTML, brak API).

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json


def scrape_menu(url):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    try:
        driver.get(url)
        items = driver.find_elements(By.CSS_SELECTOR, ".pizza-item")
        result = []
        for item in items:
            name = item.find_element(By.CSS_SELECTOR, ".name").text
            price = item.find_element(By.CSS_SELECTOR, ".price").text
            result.append({"name": name, "price": price})
        return result
    finally:
        driver.quit()


if __name__ == "__main__":
    menu = scrape_menu("https://example-pizzeria.local/menu/")
    print(f"Pobrano {len(menu)} pozycji")
    with open("scraped_menu.json", "w") as f:
        json.dump(menu, f, indent=2, ensure_ascii=False)
```

**Wazne** - prawne i etyczne aspekty:
- **Sprawdz `robots.txt`** strony zrodlowej (np. `https://example.com/robots.txt`)
- **Respektuj `Terms of Service`** - niektore strony zabraniaja scrapingu
- **Nie obciazaj serwera** - dodaj `time.sleep(1)` miedzy requestami
- **API > Scraping** - jesli strona ma API, uzyj go zamiast scrapingu

**Kiedy scraping ma sens:**
- Strona nie ma API
- Dane sa publiczne i ich uzycie zgodne z TOS
- Maly wolumen (nie skanujesz milionow stron)

**Kiedy NIE:**
- Mozesz uzyc oficjalnego API
- Naruszasz TOS
- Robisz to masowo bez zgody wlasciciela

### Alternatywy do Selenium do scrapingu

| Narzedzie | Kiedy uzywac |
|-----------|--------------|
| `requests` + `BeautifulSoup` | Statyczne strony (HTML bez JavaScriptu) |
| `selenium` / `playwright` | Strony z dynamicznym JS (SPA, AJAX) |
| `scrapy` | Projekty scrapingowe na duza skale |

Selenium wybieramy gdy strona **renderuje sie po stronie klienta** (React, Vue) i tresc pojawia sie dopiero po wykonaniu JavaScriptu.

---

## Czesc 8: Podsumowanie weekendu (15 min)

### Co umiesz po weekendzie 5

**Dzien 1:**
- Setup Selenium + WebDriver Manager
- Lokalizatory: ID, NAME, CSS, XPATH, LINK_TEXT
- Interakcje: click, send_keys, clear, text, get_attribute
- WebDriverWait + expected_conditions
- Pierwszy test pytest + Selenium

**Dzien 2:**
- pytest fixtures, scope, conftest.py
- pytest-django + live_server
- Page Object Model: BasePage + konkretne strony
- Fluent interface (return self)
- Pelne testy E2E
- Headless mode + screenshoty na fail
- Scraping z Selenium

### Caly kurs - podsumowanie

```
Weekend 1: Procedural -> OOP
Weekend 2: Wyjatki + I/O + pytest unit testy
Weekend 3: Git + Django (HTML, formularze)
Weekend 4: Debugger + Django ORM + REST API
Weekend 5: Selenium E2E + POM
```

Mamy **pelny stack** do budowania i testowania aplikacji webowej:
- Klasy Pythona z walidacja
- Persystencja w bazie SQL przez ORM
- API REST do komunikacji programistycznej
- Testy na 3 poziomach: unit, integration, E2E

### Selenium w CI/CD

Twoje testy E2E moga uruchamiac sie automatycznie:

**GitHub Actions** (`.github/workflows/tests.yml`):
```yaml
name: tests
on: [push, pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: pytest tests_e2e/ -v
```

GitHub Actions ma **Chrome zainstalowanego** - testy headless dziala bez konfiguracji.

### Alternatywy do Selenium

| Narzedzie | Plusy | Minusy |
|-----------|-------|--------|
| **Selenium** | Standard W3C, wszystkie przegladarki, wszystkie jezyki | Wolniejsze, wiecej kodu |
| **Playwright** (Microsoft) | Szybsze, prostszy API, auto-wait | Mlodsze, mniejsza spolecznosc |
| **Cypress** | Bardzo prostszy, dobre dev tools | Tylko Chrome, tylko JavaScript |

Po opanowaniu Selenium **latwo przejdziesz** na Playwright - koncepcje sa te same.

### Cwiczenia domowe (opcjonalne)

1. **Customer i Order do ORM:** Dotychczas klasy `Customer` i `Order` z Weekendu 1-2 trzymaja dane w plikach JSON. Przenies je do ORM (modele Django) analogicznie jak `Pizza` w Weekend 4. Po tym dodaj POM `CustomerPage`, `AddCustomerPage` i testy CRUD.
2. **AdminLoginPage:** Dodaj POM logowania do `/admin/`. Wymaga utworzenia uzytkownika w `live_server` (`User.objects.create_superuser(...)` w fixturze) i przeprowadzenia logowania przez formularz Django admin.
3. **Naprawa pizza_detail:** Widok detalu wciaz uzywa `menu.json`. Przepisz na ORM (`Pizza.objects.get(name=name)`) i dopisz test E2E ktory potwierdza ze pizza dodana przez UI ma dzialajacy detal.
4. **GitHub Actions:** Skonfiguruj workflow `.github/workflows/tests.yml` ktory uruchamia testy E2E w trybie headless w CI.
5. **Playwright:** Przepisz jeden test E2E w Playwright (`pip install playwright`) i porownaj API.

### Q&A + zakonczenie

Pytania? Komentarze?

Dzieki za caly kurs! Sukcesu w pisaniu Python web apps.

---

## Troubleshooting

### `live_server` nie startuje

Sprawdz `pytest.ini`:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = pizzeria_project.settings
```

I czy `pytest-django` jest zainstalowany:
```bash
pip install pytest-django
```

### Testy z `@pytest.mark.django_db` failuja z "DB not allowed"

Brakuje `pytest-django`. Lub `DJANGO_SETTINGS_MODULE` jest zly.

### Headless test "widzi" inne dane niz wizualny

Sprawdz `--window-size`. Niektore CSS media queries odpalaja na malych ekranach.
```python
options.add_argument("--window-size=1920,1080")
```

### Screenshot nie zapisuje sie

Sprawdz uprawnienia do folderu (`screenshots/`). Hook ktory dodalismy wymaga ze folder istnieje (lub `os.makedirs(..., exist_ok=True)`).

### POM ma cyrkularny import

Jesli `MenuPage` zwraca `PizzaDetailPage`, a `PizzaDetailPage` zwraca `MenuPage` (np. po klikniecu "Wstecz") - cyrkularny import.

Rozwiazanie: importuj **wewnatrz funkcji**:
```python
def click_pizza(self, name):
    from .pizza_detail_page import PizzaDetailPage
    self.driver.find_element(...).click()
    return PizzaDetailPage(self.driver, self.base_url)
```

### Test failuje raz na 5 uruchomien (flaky)

Najprawdopodobniej **wyscig** z czasem ladowania. Dodaj/popraw `WebDriverWait`:
```python
self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BTN))
self.driver.find_element(*self.SUBMIT_BTN).click()
```

Nigdy `time.sleep(0.5)` jako "fix" - tylko explicit waits.
