# Dzien 1: Selenium WebDriver - podstawy

## Agenda

**Czas trwania:** 8:30 - 15:00 (6h 30min z przerwami)

### Harmonogram

| Czas | Temat | Aktywnosc |
|------|-------|-----------|
| **8:30 - 8:50** | Recap Weekend 4 + plan dnia | Wprowadzenie |
| **8:50 - 10:30** | Po co Selenium + setup + pierwszy skrypt | Teoria + cwiczenia |
| **10:30 - 10:40** | **PRZERWA** | 10 minut |
| **10:40 - 12:40** | Lokalizatory + interakcje (klikanie, formularze) | Cwiczenia |
| **12:40 - 13:10** | **PRZERWA** | 30 minut |
| **13:10 - 15:00** | WebDriverWait + integracja z pytest | Cwiczenia + testy |

### Co zbudujemy dzisiaj?

Skrypty Selenium ktore otwieraja prawdziwa przegladarke (Chrome) i automatycznie:
1. Wchodza na strony naszej pizzerii (z Weekend 4)
2. Klikaja w linki, wypelniaja formularze
3. Sprawdzaja co pojawia sie na stronie
4. Pierwsze testy automatyczne w pytest, ktore sterujac przegladarka weryfikuja ze pizzeria dziala

Innymi slowy: zrobimy to, co dotad robil **czlowiek** sprawdzajacy aplikacje recznie - tylko ze automatycznie i powtarzalnie.

---

## Czesc 1: Recap Weekend 4 (20 min)

### Co zrobilismy do tej pory

**Weekend 1:** Programowanie obiektowe
- Klasy: Pizza, Menu, Customer, Order

**Weekend 2:** Wyjatki + I/O + testy pytest
- `pytest`, fixtures, `pytest.raises`, `assert`

**Weekend 3:** Git + Django
- Aplikacja webowa pizzerii (HTML, formularze)

**Weekend 4:** Debugger + Django ORM + REST API
- Modele Pizza, Customer, Order w bazie SQLite
- Admin panel
- REST API: `GET/POST/PUT/DELETE /api/pizzas/`
- Testy API z `APIClient`

### Sprawdzenie srodowiska

Weekend 5 ma wlasna kopie projektu pizzerii (z Weekend 4) w `0910-05-2026/pizzeria_django/`. Bez `db.sqlite3` w repo - musisz uruchomic migracje, zeby zalozyc tabele:

```bash
cd 0910-05-2026/pizzeria_django
python3 manage.py migrate
python3 manage.py runserver
```

Wejdz na http://127.0.0.1:8000/menu/ - powinienes zobaczyc pusta liste pizz. Dodaj kilka przez `/menu/dodaj/` (lub przez admin `/admin/`, jesli zalozysz superusera: `python3 manage.py createsuperuser`).

**Uwaga:** uzywamy projektu z **`0910-05-2026/pizzeria_django/`** - to ta sama baza co Weekend 4, skopiowana zeby Weekend 5 byl samodzielny (nie zalezy od stanu folderu Weekend 4). Stare rozwiazanie z `pizzeria_django_rozwiazanie/` w korzeniu repozytorium **nie ma** `menu_app/models.py` (ladowalo dane z JSON) - polecenia typu `python3 manage.py shell -c "from menu_app.models import Pizza"` na nim nie zadzialaja.

### Plan tego weekendu

```
Dzien 1: Selenium WebDriver - podstawy
  - Setup Selenium + WebDriver Manager
  - Lokalizatory elementow (CSS, XPATH, ID)
  - Interakcje: klikanie, wypelnianie formularzy
  - WebDriverWait (czekanie na zaladowanie elementu)
  - Integracja z pytest

Dzien 2: Page Object Model + testy E2E
  - Pytest fixtures dla Selenium (conftest.py)
  - POM - organizacja kodu testow
  - Pelne scenariusze E2E (uzytkownik zamawia pizze)
  - Headless mode + screenshoty przy bledach
  - Selenium poza testami (scraping)
```

---

## Czesc 2: Po co Selenium? (20 min)

### Jakie testy juz znamy?

| Rodzaj testu | Kiedy uzywamy | Co weryfikuje | Czas |
|--------------|---------------|---------------|------|
| **Unit test** | Weekend 2 | Pojedyncza funkcja, klasa | ms |
| **Integration test** (API) | Weekend 4 | Endpoint REST API + baza | dziesiatki ms |
| **E2E test** (Selenium) | Weekend 5 | Pelny przeplyw uzytkownika w przegladarce | sekundy |

### Po co E2E?

Wyobraz sobie taki bug:

1. Dodales formularz dodawania pizzy
2. Test API (`POST /api/pizzas/`) **przechodzi** - backend zapisuje do bazy
3. Ale w formularzu HTML jest literowka w `name="cena"` zamiast `name="price"`
4. Uzytkownik klika "Dodaj" -> nic sie nie zapisuje (bo pole `price` jest puste)
5. Ani unit test, ani API test tego **nie zlapie** - bo testuja warstwy ponizej

**E2E test** zlapie to natychmiast - bo "klika" formularz dokladnie tak jak uzytkownik.

### Manualny vs automatyczny test

**Manualnie:** otwieram przegladarke, wchodze na `/menu/dodaj/`, wpisuje "Hawajska", "32", klikam "Dodaj", sprawdzam ze widze "Pizza dodana" i pizza pojawia sie na liscie. Powtarzam dla 10 scenariuszy. Czas: 30 minut.

**Automatycznie (Selenium):** uruchamiam `pytest tests_e2e/`, ktore robi to samo - tylko w 10 sekund. I powtorze za miesiac, gdy zmienie cos w kodzie - bez wysilku.

### Czym jest Selenium WebDriver?

**Selenium** to biblioteka do **automatyzacji przegladarki**. Sklada sie z dwoch warstw:

```
Twoj kod Python
      |
      v
Selenium (biblioteka)
      |
      v
WebDriver protokol  <--- standard W3C
      |
      v
Sterownik (ChromeDriver, GeckoDriver)
      |
      v
Przegladarka (Chrome, Firefox, Edge)
```

Twoj skrypt mowi `driver.click()` - Selenium wysyla komende do ChromeDrivera - ChromeDriver mowi Chrome'owi "klinij ten element". Wszystko dzieje sie tak samo jak gdy uzytkownik klika myszka.

### Selenium nie jest jedyne

Inne popularne narzedzia:
- **Playwright** (Microsoft) - nowsza alternatywa, szybsza, prostszy API
- **Cypress** - JavaScript-only, dziala tylko w Chrome
- **Puppeteer** - JavaScript, kontroluje Chrome przez DevTools Protocol

Dlaczego uczymy sie **Selenium**? Bo to **standard W3C**, dziala z kazdym jezykiem (Python, Java, C#, JavaScript), kazda przegladarka.

### Tryb wizualny vs headless

- **Tryb wizualny** - widzisz okno przegladarki, kursor, klikniecia. Dobry do nauki i debugowania.
- **Tryb headless** - przegladarka dziala "w tle", bez interfejsu. Szybsze, mozna uruchomic na serwerze CI/CD bez ekranu.

Na dzien 1 uzywamy trybu wizualnego (widac co sie dzieje). Na dzien 2 wlaczymy headless.

---

## Czesc 3: Setup Selenium (20 min)

### SHOW: Instalacja i pierwszy skrypt

**Krok 1:** Zainstaluj biblioteke Selenium i WebDriver Manager.

```bash
cd 0910-05-2026/pizzeria_django
pip install selenium webdriver-manager
```

**Czemu `webdriver-manager`?** Bez niego musialbys:
1. Sprawdzic wersje swojego Chrome'a
2. Pobrac odpowiedni `chromedriver` z https://chromedriver.chromium.org
3. Polozyc go gdzies w PATH
4. Aktualizowac przy kazdej aktualizacji Chrome'a

`webdriver-manager` robi to wszystko **automatycznie** - przy pierwszym uruchomieniu pobiera odpowiedniego ChromeDrivera i cachuje go lokalnie.

**Krok 2:** Sprawdz instalacje.

```bash
python3 -c "from selenium import webdriver; print(webdriver.__version__)"
```

Powinienes zobaczyc wersje (np. `4.x.x`).

**Krok 3:** Pierwszy skrypt - otworz Google.

Stworz plik `tmp_selenium.py` w korzeniu projektu Django:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Utworz driver - Chrome z automatycznie pobranym ChromeDriverem
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Otworz strone
driver.get("https://www.google.com")

# Wydrukuj tytul
print(f"Tytul strony: {driver.title}")

# Poczekaj 3 sekundy zebysmy zobaczyli okno
import time
time.sleep(3)

# Zamknij przegladarke
driver.quit()
```

Uruchom:

```bash
python3 tmp_selenium.py
```

**Co sie powinno stac:**
1. Otworzy sie nowe okno Chrome'a (dziwny pasek "Chrome jest sterowane przez automatyczne oprogramowanie testowe" - to normalne)
2. Strona Google sie zaladuje
3. W terminalu pojawi sie `Tytul strony: Google`
4. Po 3 sekundach okno sie zamknie

**Wazne!** Zawsze konczymy `driver.quit()` - inaczej zostawimy zombie processy.

### DO: Cw. 1 - Otwarcie pizzerii (25 min)

**Cel:** Napisz skrypt Selenium ktory otwiera strone naszej pizzerii i drukuje jej tytul.

**Krok 1:** Uruchom serwer Django w jednym terminalu:

```bash
cd 0910-05-2026/pizzeria_django
python3 manage.py runserver
```

Sprawdz w przegladarce: http://127.0.0.1:8000/menu/ - widzisz liste pizz.

**Krok 2:** W drugim terminalu (lub w VS Code) stworz plik `tmp_pizzeria_selenium.py`:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# TODO: otworz http://127.0.0.1:8000/menu/

# TODO: wydrukuj driver.title

# TODO: wydrukuj driver.current_url

# TODO: poczekaj 5 sekund

driver.quit()
```

**Krok 3:** Uzupelnij kod tak, zeby skrypt wszedl na strone menu, wydrukowal tytul i URL.

**Oczekiwany wynik w terminalu:**
```
Tytul strony: Menu Pizzerii
URL: http://127.0.0.1:8000/menu/
```

**Bonus:** Dodaj `driver.maximize_window()` zaraz po stworzeniu drivera - okno otworzy sie na pelnym ekranie.

### REVIEW: Najczestsze problemy (10 min)

**Problem 1:** `WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

Nie uzyles `webdriver-manager`. Sprawdz `Service(ChromeDriverManager().install())` - powinno to byc w kodzie.

**Problem 2:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX`

Wersja Chrome'a i ChromeDrivera sie nie zgadzaja. Zaktualizuj `webdriver-manager`:

```bash
pip install --upgrade webdriver-manager
```

**Problem 3:** Okno otwiera sie i od razu zamyka.

Brakuje `time.sleep(...)` lub `driver.quit()` jest wykonywany od razu. Sprawdz czy nie ma exceptiona w kodzie.

**Problem 4:** `ConnectionRefusedError` przy `/menu/`

Serwer Django nie dziala. Uruchom `python3 manage.py runserver` w osobnym terminalu.

---

## Czesc 4: DOM i DevTools (25 min)

### Teoria: Jak przegladarka rozumie strone

Gdy przegladarka dostaje HTML, parsuje go w **DOM** (Document Object Model) - drzewo elementow:

```
<html>
 <body>
  <h1>Menu Pizzerii</h1>
  <ul>
   <li><a href="/menu/Margherita/">Margherita - 25 zl</a></li>
   <li><a href="/menu/Pepperoni/">Pepperoni - 30 zl</a></li>
  </ul>
 </body>
</html>
```

W DOM to drzewo:
```
html
 +- body
     +- h1 ("Menu Pizzerii")
     +- ul
         +- li
         |   +- a (href="/menu/Margherita/", "Margherita - 25 zl")
         +- li
             +- a (href="/menu/Pepperoni/", "Pepperoni - 30 zl")
```

Kazdy element w DOM ma:
- **tag** (`h1`, `a`, `ul`, `li`)
- **atrybuty** (`href="..."`, `id="..."`, `class="..."`)
- **tekst** (zawartosc miedzy `<tag>` a `</tag>`)
- **dzieci** (zagniezdzone elementy)

Selenium pozwala **znalezc** elementy w tym drzewie i z nimi **interaktwowac** (klikac, czytac tekst).

### Inspekcja w DevTools

Otworz pizzerie w Chrome. Nacisnij `F12` (lub prawy klik -> "Zbadaj").

Otworzy sie panel **Developer Tools**. W zakladce **Elements** widzisz cale drzewo HTML.

**Hover** myszka nad linia HTML -> odpowiadajacy element zostanie podswietlony w przegladarce.

**Klikniecie ikony "select element"** (strzalka w lewym gornym rogu DevTools) - mozesz kliknac element na stronie i DevTools podswietli odpowiadajacy HTML.

### DO: Cw. 2 - Inspekcja pizzerii (10 min)

**Krok 1:** Otworz Chrome i wejdz na http://127.0.0.1:8000/menu/

**Krok 2:** Otworz DevTools (`F12`). Przejdz do zakladki **Elements**.

**Krok 3:** Uzyj narzedzia "select element" (strzalka w lewym gornym rogu). Klinij na:
- naglowek "Menu Pizzerii" -> jaki tag? (`h1`, `h2`, ...?)
- "kafelek" pojedynczej pizzy -> jaka klasa? (`.card`, `.pizza-item`, ...?)
- nazwa pizzy w kafelku -> jaki tag i klasa? (`.card-title`?)
- link "Szczegoly" pod kazda pizza -> jaki to element?

**Krok 4:** W projekcie z Weekend 4 template `pizza_list.html` uzywa Bootstrap **kart** (`.card`):
- Kazda pizza jest w `<div class="card">`
- Nazwa w `<h5 class="card-title">{{ pizza.name }}</h5>`
- Cena w `<p class="price">{{ pizza.price }} zl</p>`
- Link szczegolow: `<a class="btn btn-outline-primary btn-sm" href="/menu/<nazwa>/">Szczegoly</a>`

To wazne! Tekst linka to **"Szczegoly"** - nie nazwa pizzy. `By.PARTIAL_LINK_TEXT, "Margherita"` **nie zadziala**.

**Krok 5:** Zapisz w komentarzu w `tmp_pizzeria_selenium.py` co znalazles, np.:
```python
# h1 -> "Menu Pizzerii", brak id
# kafelek pizzy -> <div class="card"> z <h5 class="card-title">
# link szczegolow -> <a class="btn btn-outline-primary"> z text "Szczegoly"
```

**Bonus:** Klikniecie prawym przyciskiem na element w panelu Elements -> "Copy" -> "Copy selector". Daje gotowy CSS selector. Albo "Copy XPath" - daje XPath. Te wartosci moga byc wprost uzyte w Selenium.

---

## Czesc 5: Lokalizatory (40 min)

### Teoria: Selektory By

Selenium wybiera elementy uzywajac klasy `By`. Najczesciej uzywane:

| Lokalizator | Przyklad | Kiedy uzywac |
|-------------|----------|--------------|
| `By.ID` | `By.ID, "submit-btn"` | Najlepszy - `id` jest unikalny |
| `By.NAME` | `By.NAME, "username"` | Dla pol formularza (atrybut `name`) |
| `By.CLASS_NAME` | `By.CLASS_NAME, "pizza-item"` | Element z konkretna klasa CSS |
| `By.TAG_NAME` | `By.TAG_NAME, "h1"` | Element po tagu |
| `By.LINK_TEXT` | `By.LINK_TEXT, "Margherita"` | Link z dokladnym tekstem |
| `By.PARTIAL_LINK_TEXT` | `By.PARTIAL_LINK_TEXT, "Margh"` | Link zawierajacy tekst |
| `By.CSS_SELECTOR` | `By.CSS_SELECTOR, "ul.menu li a"` | Selektor CSS - najuniwersalniejszy |
| `By.XPATH` | `By.XPATH, "//h1[text()='Menu']"` | XPath - najpotezniejszy |

### Hierarchia preferencji

Wybieramy lokalizator wedlug priorytetu:

```
1. By.ID                  <- jesli element ma id, uzyj id
2. By.NAME                <- pola formularza
3. By.CSS_SELECTOR        <- 90% pozostalych przypadkow
4. By.XPATH               <- ostatecznosc, gdy CSS nie wystarczy
```

**Czemu ID najpierw?** Bo `id` powinno byc unikalne na stronie - nie zmienia sie tak czesto i jest szybkie.

**Czemu CSS przed XPATH?** CSS jest bardziej czytelny, szybszy w wykonaniu. XPath sluzy gdy CSS nie wystarczy (np. wybor po tekscie).

### Zaraz, czym wlasciwie jest CSS w lokalizatorze?

Pierwsze skojarzenie: "CSS = kolorki, czcionki, style". I owszem - **glownym** zastosowaniem CSS jest stylowanie strony przez przegladarke. Ale CSS sklada sie z dwoch rzeczy:

1. **Selektor** - opis "ktore elementy" maja byc stylowane (np. `.btn-primary`, `#login-form`, `ul li a`).
2. **Wlasciwosci** - co z nimi zrobic (np. `color: red; font-size: 14px;`).

```css
/* selektor */    /* wlasciwosci */
.btn-primary    { background: blue; color: white; }
```

**Selenium uzywa tylko czesci 1 - selektora.** Zignoruj wlasciwosci. To po prostu jezyk do pytania "ktory element w drzewie HTML?".

```python
# Pytanie do przegladarki: "daj mi przycisk z klasa btn-primary"
driver.find_element(By.CSS_SELECTOR, ".btn-primary")
```

Ten sam jezyk uzywa tez:
- `document.querySelector(".btn-primary")` w JavaScript
- `soup.select(".btn-primary")` w BeautifulSoup
- `$(".btn-primary")` w jQuery

Wiec gdy uczysz sie selektorow CSS, ucisz sie **uniwersalnego sposobu wskazywania elementow w HTML** - przyda sie wszedzie, nie tylko w stylowaniu.

### CSS selektory - krotkie przypomnienie

```css
h1                  /* wszystkie h1 */
.menu               /* element z class="menu" */
#submit             /* element z id="submit" */
ul.menu             /* ul z class="menu" */
ul li               /* wszystkie li wewnatrz ul */
ul > li             /* tylko bezposrednie dzieci */
input[name="cena"]  /* input z atrybutem name="cena" */
li:first-child      /* pierwsze li */
li:nth-child(2)     /* drugie li */
```

### XPath - krotkie wprowadzenie

XPath to "sciezka" przez drzewo XML/HTML:

```
//h1                     element h1 gdziekolwiek
//div[@class='menu']     div z class="menu"
//a[text()='Margherita'] a z dokladnym tekstem "Margherita"
//ul/li[1]               pierwsze li bezposrednio w ul
//div[contains(@class, 'pizza')]  div ktorego class zawiera 'pizza'
```

XPath jest **potezniejszy** od CSS (umie szukac po tekscie), ale **wolniejszy** i mniej czytelny.

### find_element vs find_elements

```python
driver.find_element(By.ID, "submit")    # ZWRACA jeden element (pierwszy)
                                         # Jesli nie ma -> NoSuchElementException

driver.find_elements(By.TAG_NAME, "li") # ZWRACA liste elementow
                                         # Jesli nie ma -> pusta lista []
```

**Uwaga:** `find_element` (singular) rzuca exception, `find_elements` (plural, z "s") zwraca liste.

### SHOW: Lokalizatory na bookstore (15 min)

Zeby pokazac lokalizatory **bez** odpalania prawdziwego serwera ksiegarni, mamy gotowy plik HTML w repo: **`0910-05-2026/dzien1/bookstore_list.html`**. Wystarczy go otworzyc w przegladarce (lub w Selenium przez `file://`).

Struktura strony (skrocona):
```html
<h1 id="page-title">Ksiegarnia online</h1>
<ul class="book-list">
  <li class="book-item">
    <a href="#book-1" class="book-link">Lalka - Boleslaw Prus</a>
    <span class="price">29.90 zl</span>
  </li>
  <li class="book-item">
    <a href="#book-2" class="book-link">Quo Vadis - Henryk Sienkiewicz</a>
    <span class="price">34.50 zl</span>
  </li>
  ...
</ul>
<button id="show-more">Pokaz wiecej</button>
```

Kod Selenium szukajacy elementow (uruchamiany **prosto z repo**):

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Zaladuj plik HTML wprost przez file://
html_path = Path("0910-05-2026/dzien1/bookstore_list.html").resolve()
driver.get(f"file://{html_path}")

# 1. Tytul strony - po ID
title = driver.find_element(By.ID, "page-title")
print(title.text)                       # "Ksiegarnia online"

# 2. Wszystkie ksiazki - po klasie (lista)
books = driver.find_elements(By.CLASS_NAME, "book-item")
print(f"Znaleziono {len(books)} ksiazek")

# 3. Pierwsza ksiazka - po CSS selector
first_book = driver.find_element(By.CSS_SELECTOR, ".book-list .book-item:first-child .book-link")
print(first_book.text)                  # "Lalka - Boleslaw Prus"

# 4. Wszystkie ceny - po CSS
prices = driver.find_elements(By.CSS_SELECTOR, ".price")
for p in prices:
    print(p.text)

# 5. Link konkretnej ksiazki - po LINK_TEXT
quo_vadis = driver.find_element(By.LINK_TEXT, "Quo Vadis - Henryk Sienkiewicz")
print(quo_vadis.get_attribute("href"))  # konczy sie na "#book-2"

# 6. Po XPath - element zawierajacy tekst "Lalka"
lalka = driver.find_element(By.XPATH, "//a[contains(text(), 'Lalka')]")
print(lalka.text)

driver.quit()
```

### DO: Cw. 3 - Lokalizatory na pizzerii (25 min)

**Cel:** Napisz skrypt ktory znajdzie kluczowe elementy na stronie `/menu/` pizzerii.

**Krok 1:** Otworz pizzerie w przegladarce. Otworz DevTools (`F12`) i potwierdz strukture (z Cw. 2):
- naglowek -> `<h1>`
- kazda pizza -> `<div class="card">` z `<h5 class="card-title">`
- link szczegolow -> `<a class="btn btn-outline-primary btn-sm" href="/menu/...">Szczegoly</a>`
- cena -> `<p class="price">`

Jesli w bazie SQLite masz pizze (z Weekend 4) - powinienes widziec kafelki. Jesli baza jest pusta, dodaj pierwsza pizze przez `/menu/dodaj/` zanim odpalisz skrypt.

**Krok 2:** Stworz plik `tmp_lokalizatory.py`. Zacznij od boilerplate:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://127.0.0.1:8000/menu/")

# Cw. 3a: Znajdz naglowek strony (h1) i wydrukuj jego tekst
# Wskazowka: By.TAG_NAME, "..."


# Cw. 3b: Znajdz wszystkie kafelki pizz i wydrukuj ich liczbe
# Wskazowka: kafelek to <div class="card"> -> By.CSS_SELECTOR, "..."
# Pamietaj: find_elementS (z "s") zwraca liste


# Cw. 3c: Dla kazdego kafelka wydrukuj nazwe i cene
# Wskazowka: wewnatrz kafelka szukaj .card-title i .price


# Cw. 3d: Znajdz link "Szczegoly" pierwszej pizzy i wydrukuj jego href
# UWAGA: text linka to "Szczegoly" - nie nazwa pizzy!
# Wskazowka: a.btn-outline-primary wewnatrz .card; uzyj get_attribute("href")


# Cw. 3e: Znajdz link do pizzy "Margherita" przez atrybut href (jesli istnieje)
# Wskazowka: CSS attribute selector "a[href$='Margherita/']"
# (operator $= = "konczy sie na...")


driver.quit()
```

**Krok 3:** Twoim zadaniem jest **uzupelnic kazdy z punktow Cw. 3a-3e** uzywajac odpowiednich selektorow. Po kazdym punkcie uruchom skrypt i sprawdz output.

**Bonus 1:** Wydrukuj nazwy pizz drozszych niz 30 zl. Wskazowka: cena to tekst typu "30.0 zl" - sparsuj liczbe (`float(tekst.split()[0])`).

**Bonus 2:** Uzyj XPath zeby znalezc kafelek pizzy "Pepperoni":
```python
pepperoni_card = driver.find_element(
    By.XPATH, "//div[contains(@class, 'card') and .//h5[text()='Pepperoni']]"
)
```

### REVIEW: Wybor lokalizatora (10 min)

**Pytanie:** Co lepiej, `By.CLASS_NAME, "btn-primary"` czy `By.CSS_SELECTOR, ".btn-primary"`?

**Odpowiedz:** Praktycznie to samo. `By.CSS_SELECTOR` jest bardziej uniwersalny (mozna laczyc w bardziej zlozone selektory: `.btn-primary[type='submit']`), wiec wiele zespolow standardyzuje na CSS_SELECTOR.

**Pytanie:** Co gdy element nie ma id ani klasy?

**Odpowiedz:** Mozliwosci:
1. Dodaj atrybut `data-testid="..."` w HTML i znajdz przez `[data-testid='...']`. To jest **najlepsza praktyka** - `data-testid` istnieje wylacznie do testow i nie zmienia sie z designem.
2. Uzyj XPath po tekscie: `By.XPATH, "//button[text()='Dodaj']"`
3. Uzyj kontekstu: `form#order input[type='submit']`


**NoSuchElementException** - co robic?

```python
from selenium.common.exceptions import NoSuchElementException

try:
    el = driver.find_element(By.ID, "nieistniejacy")
except NoSuchElementException:
    print("Nie znaleziono!")
```

Albo uzyj `find_elements` (lista) - jesli pusta to nie ma:

```python
ele = driver.find_elements(By.ID, "nieistniejacy")
if not ele:
    print("Nie znaleziono!")
```

---

## Czesc 6: Interakcje z elementami (50 min)

### Teoria: Co mozna zrobic z elementem?

Po znalezieniu elementu (`element = driver.find_element(...)`) mozna:

| Operacja | Metoda | Przyklad |
|----------|--------|----------|
| Klikniecie | `.click()` | `button.click()` |
| Wpisanie tekstu | `.send_keys("text")` | `input.send_keys("Margherita")` |
| Wyczyszczenie pola | `.clear()` | `input.clear()` |
| Pobranie tekstu | `.text` | `print(h1.text)` |
| Pobranie atrybutu | `.get_attribute("name")` | `link.get_attribute("href")` |
| Sprawdzenie widocznosci | `.is_displayed()` | `if button.is_displayed():` |
| Sprawdzenie aktywnosci | `.is_enabled()` | `if button.is_enabled():` |
| Sprawdzenie zaznaczenia | `.is_selected()` | dla checkbox/radio |

### Specjalne klawisze

```python
from selenium.webdriver.common.keys import Keys

input_field.send_keys("tekst")
input_field.send_keys(Keys.ENTER)        # Enter
input_field.send_keys(Keys.TAB)          # Tab
input_field.send_keys(Keys.ARROW_DOWN)   # Strzalka w dol
input_field.send_keys(Keys.CONTROL, "a") # Ctrl+A
```

### Submit formularza

Dwa sposoby:
```python
# 1. Klinij przycisk submit
driver.find_element(By.ID, "submit-btn").click()

# 2. Wcisnij Enter w polu
driver.find_element(By.NAME, "username").send_keys(Keys.ENTER)
```

### SHOW: Logowanie w bookstore (15 min)

Tak jak przy lokalizatorach, gotowy plik HTML w repo: **`0910-05-2026/dzien1/bookstore_login.html`**. Maly skrypt JavaScript w pliku przejmuje submit formularza i pokazuje komunikat powitalny - dzieki temu nie potrzebujemy backendu.

Struktura strony (skrocona):
```html
<form id="login-form">
  <input name="username" id="username" type="text">
  <input name="password" id="password" type="password">
  <button id="login-btn" type="submit">Zaloguj</button>
</form>

<div id="welcome-area" class="hidden">
  <p class="welcome-message"></p>
</div>

<!-- JS: po submit pokazuje "Witaj, <username>!" w .welcome-message -->
```

Kod Selenium (uruchamiany **prosto z repo**):

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
html_path = Path("0910-05-2026/dzien1/bookstore_login.html").resolve()
driver.get(f"file://{html_path}")

# Wpisz login i haslo
username = driver.find_element(By.ID, "username")
username.clear()                      # Wyczysc pole (gdyby cos juz tam bylo)
username.send_keys("jan@example.com")

password = driver.find_element(By.ID, "password")
password.send_keys("Tajne123")

# Klinij "Zaloguj"
driver.find_element(By.ID, "login-btn").click()

# Po submit JS pokazuje .welcome-message - sprawdzmy ze sie pojawila
welcome = driver.find_element(By.CSS_SELECTOR, ".welcome-message")
print(welcome.text)                   # "Witaj, jan@example.com!"

driver.quit()
```

**Wzorzec:** wypelnij pola (`.send_keys`) -> klinij submit (`.click`) -> sprawdz nowy stan strony.

### DO: Cw. 4 - Formularz dodawania pizzy (20 min)

**Cel:** Wypelnij formularz `/menu/dodaj/` i dodaj pizze.

**Krok 1:** Otworz `/menu/dodaj/` w przegladarce. Otworz DevTools i sprawdz:
- Jak nazywaja sie pola formularza? (`<input name="?">`)
- Jak nazywa sie przycisk submit? (`<button>` lub `<input type="submit">`)

**Krok 2:** Stworz `tmp_dodaj_pizze.py`. Boilerplate gotowy - reszte uzupelnij sam:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://127.0.0.1:8000/menu/dodaj/")

# Wpisz nazwe pizzy - dostosuj `By.NAME` do faktycznej nazwy w HTML


# Wpisz cene


# Klinij submit (przycisk lub input type="submit")


# Poczekaj 2 sekundy zebysmy zobaczyli wynik
time.sleep(2)

# Wypisz aktualny URL i tytul


driver.quit()
```

**Krok 3:** Uruchom skrypt. Powinno sie:
1. Otworzyc okno
2. Wejsc na formularz
3. Pojawic sie tekst "Selenium Special" w polu nazwy
4. Pojawic sie "42" w polu ceny
5. Klinij submit -> przekierowanie na liste pizz
6. Pojawic sie nowa pizza "Selenium Special - 42 zl"

**Krok 4:** Uruchom drugi raz - prawdopodobnie zobaczysz blad walidacji ("Pizza o tej nazwie juz istnieje"). Zmien nazwe na unikalna lub usun pizze z bazy. **Wazne:** musi byc to projekt `0910-05-2026/pizzeria_django/` (kopia Weekend 4 z ORM) - tylko tam istnieje `menu_app.models.Pizza`:

```bash
cd 0910-05-2026/pizzeria_django
python3 manage.py shell -c "from menu_app.models import Pizza; Pizza.objects.filter(name='Selenium Special').delete()"
```

Jesli widzisz `ModuleNotFoundError: No module named 'menu_app.models'` - jestes w zlym katalogu (najprawdopodobniej w `pizzeria_django_rozwiazanie/`, gdzie `models.py` nie istnieje).

**Bonus:** Po dodaniu sprawdz w skrypcie ze pizza pojawila sie na liscie. **UWAGA:** `By.PARTIAL_LINK_TEXT, "Selenium Special"` **nie zadziala** - text linka to "Szczegoly", nie nazwa pizzy! Wybierz po `card-title`:
```python
driver.get("http://127.0.0.1:8000/menu/")
nazwy = [t.text for t in driver.find_elements(By.CSS_SELECTOR, ".card-title")]
assert "Selenium Special" in nazwy, f"Brak pizzy w liscie: {nazwy}"
print(f"OK, pizza na liscie. Wszystkie: {nazwy}")
```

### REVIEW: Czego nauczylismy sie z formularza (5 min)

**Wzorzec submission formularza:** `find` pole -> `send_keys(...)` -> `find` przycisk -> `click()`.

**Glowna pulapka, na ktora zaraz wpadniemy:** klikniesz submit i od razu szukasz nowego elementu - ale strona moze nie zdazyc sie zaladowac. Selenium rzuci `NoSuchElementException`. Zaraz nauczymy sie temu zaradzic uzywajac **WebDriverWait** (czesc 7).

**Drobiazg na pamiec:** `send_keys` nie czysci pola przed wpisaniem - jesli formularz miał juz jakis tekst, dopisze. Czyscimy `input.clear()` przed `send_keys(...)`.

---

## Czesc 7: WebDriverWait - czekanie na elementy (40 min)

### Teoria: Po co czekac?

Strony nowoczesne sa **dynamiczne**:
- Klikniesz "Dodaj" -> pojawia sie spinner -> dopiero potem komunikat "Dodano"
- Klikniesz link -> JS animuje przejscie -> dopiero potem nowa strona
- AJAX laduje dane -> tabela jest pusta przez 0.5s

Jesli skrypt Selenium szuka elementu **zanim** sie pojawi, dostanie `NoSuchElementException`.

### Trzy sposoby czekania

**1. `time.sleep(n)`** - czekaj `n` sekund. **Zlo!**
```python
driver.find_element(By.ID, "btn").click()
time.sleep(5)                            # <- nadzieja, ze 5s wystarczy
driver.find_element(By.ID, "result")
```
- Jesli element pojawi sie po 0.1s -> tracisz 4.9s
- Jesli element pojawi sie po 6s -> blad

**2. Implicit wait** - "czekaj **do** N sekund **kazdym razem** gdy szukasz elementu":
```python
driver.implicitly_wait(10)               # globalnie - na caly skrypt
driver.find_element(By.ID, "btn").click()
driver.find_element(By.ID, "result")     # <- automatycznie czeka do 10s
```
- Mniej zle, ale czeka na **istnienie** elementu, nie na **widocznosc** czy **klikalnosc**.

**3. Explicit wait (WebDriverWait + expected_conditions)** - "czekaj az **konkretny warunek** bedzie spelniony":
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)         # max 10 sekund
wait.until(EC.visibility_of_element_located((By.ID, "result")))
```
- Sprawdza co 0.5s
- Konczy gdy warunek spelniony (np. po 1s)
- Rzuca `TimeoutException` po 10s

**Explicit wait to standard.** Implicit wait jest "leniwy", explicit jest precyzyjny.

### Najczestsze expected_conditions

| Warunek | Co sprawdza |
|---------|-------------|
| `presence_of_element_located` | Element jest w DOM (moze byc niewidoczny) |
| `visibility_of_element_located` | Element jest w DOM **i widoczny** |
| `element_to_be_clickable` | Element jest widoczny **i klikalny** |
| `text_to_be_present_in_element` | Element zawiera dany tekst |
| `url_contains` | URL zawiera dany fragment |
| `title_contains` | Tytul strony zawiera dany fragment |
| `alert_is_present` | Pojawil sie alert popup |

### SHOW: Czekanie na wyniki wyszukiwania (15 min)

Zeby pokazac czekanie **bez zaleznosci od backendu** (zadnego AJAX, zadnej bazy) przygotowalismy maly plik HTML ktory ma `setTimeout(3000)` w JavaScripcie. Wyglada tak: wpisujesz haslo, klikasz "Szukaj", przez 3 sekundy widac "Trwa wyszukiwanie...", potem pojawiaja sie wyniki.

**Plik:** `0910-05-2026/dzien1/wait_demo.html` (gotowy w repo).

**Krok 1:** Otworz plik wprost w przegladarce (jako `file://...`):
```bash
# Linux:
xdg-open 0910-05-2026/dzien1/wait_demo.html
# macOS:
open 0910-05-2026/dzien1/wait_demo.html
```
Wpisz cokolwiek i klinij "Szukaj" - zobacz ze przez ~3s widac "Trwa wyszukiwanie..." a potem pojawia sie 3 wyniki.

**Krok 2:** Skrypt Selenium ktory **bez** czekania wyrzuci błąd:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Zaladuj plik HTML wprost przez file://
html_path = Path("0910-05-2026/dzien1/wait_demo.html").resolve()
driver.get(f"file://{html_path}")

driver.find_element(By.ID, "search-input").send_keys("Sienkiewicz")
driver.find_element(By.ID, "search-btn").click()

# WERSJA NAIWNA - bez czekania:
results = driver.find_elements(By.CSS_SELECTOR, "#search-results .book-item")
print(f"Znaleziono {len(results)} ksiazek")    # <- 0 ksiazek! (jeszcze ukryte)

driver.quit()
```

**Krok 3:** Wersja **z** WebDriverWait:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
html_path = Path("0910-05-2026/dzien1/wait_demo.html").resolve()
driver.get(f"file://{html_path}")

driver.find_element(By.ID, "search-input").send_keys("Sienkiewicz")
driver.find_element(By.ID, "search-btn").click()

# Czekaj az pierwszy book-item pojawi sie w DOM
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search-results .book-item")))

results = driver.find_elements(By.CSS_SELECTOR, "#search-results .book-item")
print(f"Znaleziono {len(results)} ksiazek")    # <- 3 ksiazki

driver.quit()
```

Roznica: pierwsza wersja po klikniecie szuka **natychmiast** - wynikow jeszcze nie ma. Druga **czeka** az kontener stanie sie widoczny (max 10s) - potem zliczy. To wlasnie jest wzorzec `wait.until`.

**Wzorzec:** akcja (klikniecie) -> `wait.until(...)` -> dalsze operacje.

### DO: Cw. 5 - Czekanie na komunikat sukcesu (25 min)

**Cel:** Po dodaniu pizzy poczekaj az pojawi sie komunikat "Pizza dodana" (Django messages).

**Krok 1:** Sprawdz w DevTools jak pojawia sie messages w Twoim projekcie. W projekcie z Weekend 4 messages renderuja sie jako Bootstrap alerty:
```html
<div class="alert alert-success alert-dismissible fade show">
  Dodano pizze: Margherita
  <button type="button" class="btn-close" ...></button>
</div>
```

Selector w Selenium: `.alert.alert-success` (sukces) lub `.alert-danger` (blad walidacji w formularzu).

**Krok 2:** Stworz `tmp_dodaj_z_wait.py`. Boilerplate (importy + driver + wait) gotowy - **uzupelnij sam** kazdy z punktow:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Wejdz na formularz
driver.get("http://127.0.0.1:8000/menu/dodaj/")

nazwa = "Selenium Wait Test"

# Wypelnij formularz (pole name, pole price)


# Klinij submit


# CZEKAJ az URL zmieni sie z /menu/dodaj/ na /menu/ (bez /dodaj/)
# UWAGA: prosty url_contains("/menu/") byl by trywialnie spelniony - bo /menu/dodaj/ tez go zawiera!
# Wskazowka: EC.url_to_be("http://127.0.0.1:8000/menu/")


# CZEKAJ az pojawi sie komunikat sukcesu
# Wskazowka: .alert-success (Bootstrap), uzyj EC.visibility_of_element_located


# Sprawdz ze nowa pizza jest na liscie pizz
# Wskazowka: zbierz teksty z .card-title i sprawdz `assert nazwa in nazwy`


driver.quit()
```

**Krok 3:** Pamietaj ze pizza musi byc unikalna - jesli juz dodales, usun:
```bash
cd 0910-05-2026/pizzeria_django
python3 manage.py shell -c "from menu_app.models import Pizza; Pizza.objects.filter(name='Selenium Wait Test').delete()"
```

**Krok 4:** Uruchom. Skrypt powinien:
1. Otworzyc formularz
2. Wypelnic pola
3. Klikniecie submit -> czekanie na zmiane URL na liste
4. Wypisac komunikat sukcesu
5. Wypisac liste pizz i potwierdzic ze nowa jest na niej

**Bonus:** Co sie stanie gdy podasz duplikat? Formularz nie redirect-uje, tylko zwraca strone z `<div class="alert-danger">` zawierajacym blad. Twoj `wait.until(EC.url_to_be(...))` rzuci `TimeoutException` - bo URL **nie zmienil sie**. Zlap exception i sprawdz komunikat bledu z `.alert-danger`.

---

## Czesc 8: Selenium + pytest (40 min)

### Teoria: Po co testy automatyczne?

Skrypt `tmp_dodaj_z_wait.py` to **manualnie uruchamiany skrypt**. Ma kilka problemow:

1. **Brak asercji** - tylko drukuje, nie sprawdza czy jest dobrze
2. **Trzeba uruchamiac recznie**
3. **Trzeba sprzatac dane** (usuwac pizze z bazy)
4. **Nie integruje sie z CI/CD**

**Pytest + Selenium** rozwiazuje wszystkie te problemy:
- `assert` -> automatyczna weryfikacja
- `pytest tests_e2e/` -> jedna komenda uruchamia wszystkie testy
- `@pytest.fixture` -> setup i cleanup automatyczne
- Latwy do podpiecia w GitHub Actions

### SHOW: Pierwszy test pytest + Selenium (15 min)

Generyczny test ksiegarni uruchamiany **na pliku z dysku** (`bookstore_list.html` - ten sam, ktorego uzylismy przy lokalizatorach):

```python
# tests_e2e/test_bookstore.py
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BOOKSTORE_URL = "file://" + str(
    Path(__file__).resolve().parents[2] / "0910-05-2026" / "dzien1" / "bookstore_list.html"
)


@pytest.fixture
def driver():
    """Tworzy WebDrivera dla pojedynczego testu i sprzata po nim."""
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield drv
    drv.quit()


def test_strona_glowna_ma_tytul(driver):
    driver.get(BOOKSTORE_URL)
    h1 = driver.find_element(By.TAG_NAME, "h1")
    assert "Ksiegarnia" in h1.text


def test_lista_ksiazek_nie_jest_pusta(driver):
    driver.get(BOOKSTORE_URL)
    books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
    assert len(books) > 0
```

Uruchomienie:
```bash
pytest tests_e2e/test_bookstore.py -v
```

(`parents[2]` zalezy od tego gdzie umiescisz `test_bookstore.py` - dostosuj liczbe poziomow do swojej struktury katalogow, albo po prostu uzyj `Path("0910-05-2026/dzien1/bookstore_list.html").resolve()` jesli odpalasz pytest z korzenia repo.)

**Co tu sie dzieje:**
1. `@pytest.fixture` definiuje "fixture" - cos co pytest tworzy przed testem
2. `yield drv` - przekazuje drivera do testu
3. Po skonczeniu testu wykonuje sie kod **po** `yield` - tu `drv.quit()`
4. Test dostaje `driver` jako parametr (pytest dopasowuje po nazwie)
5. `assert` - jesli falsze, test fail

**Zaleta:** Kazdy test dostaje **swojego** drivera, sprzatany po sobie. Brak wycieku zasobow.

### DO: Cw. 6 - Pierwszy test pizzerii (25 min)

**Cel:** Napisz pytest test ktory sprawdza ze na `/menu/` sa pizze.

**Krok 1:** Utworz folder `tests_e2e/` w projekcie pizzerii:

```bash
cd 0910-05-2026/pizzeria_django
mkdir tests_e2e
touch tests_e2e/__init__.py
```

**Krok 2:** Upewnij sie ze masz przynajmniej 2 pizze w bazie. Jesli nie:
```bash
python3 manage.py shell -c "from menu_app.models import Pizza; Pizza.objects.get_or_create(name='Margherita', defaults={'price': 25.0}); Pizza.objects.get_or_create(name='Pepperoni', defaults={'price': 30.0})"
```

**Krok 3:** Stworz plik `tests_e2e/test_pizza_list.py`. Boilerplate (importy + fixture) gotowy - **uzupelnij sam** kazdy z testow:

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield drv
    drv.quit()


def test_pizza_list_displays_pizzas(driver):
    """Strona /menu/ wyswietla co najmniej jedna pizze (kafelek .card)."""
    # Wejdz na http://127.0.0.1:8000/menu/

    # Znajdz wszystkie kafelki .card

    # Asercja: powinny byc co najmniej 1
    pass


def test_pizza_list_has_naglowek(driver):
    """Strona /menu/ ma naglowek h1 zawierajacy slowo 'Menu'."""
    # Wejdz na http://127.0.0.1:8000/menu/

    # Znajdz h1

    # Asercja: "Menu" w h1.text
    pass
```

**Krok 4:** Upewnij sie ze serwer Django dziala:
```bash
python3 manage.py runserver
```

**Krok 5:** W drugim terminalu uruchom testy:
```bash
pytest tests_e2e/test_pizza_list.py -v
```

**Oczekiwany wynik:**
```
tests_e2e/test_pizza_list.py::test_pizza_list_displays_pizzas PASSED
tests_e2e/test_pizza_list.py::test_pizza_list_has_naglowek PASSED
```

**Krok 6:** Dodaj test ktory celowo failuje (np. szuka tytulu "Ksiegarnia" na pizzerii). Sprawdz jak wyglada output bledu:

```python
def test_celowy_bledny(driver):
    driver.get("http://127.0.0.1:8000/menu/")
    h1 = driver.find_element(By.TAG_NAME, "h1")
    assert "Ksiegarnia" in h1.text  # <- zostanie fail
```

**Bonus:** Dodaj test sprawdzajacy ze klikniecie na "Szczegoly" pierwszej pizzy otwiera strone detalu (URL zmienia sie na `/menu/<nazwa>/`). Wskazowka: link "Szczegoly" wybierzesz przez `By.CSS_SELECTOR, ".card a.btn-outline-primary"`.

**Uwaga o pizza_detail:** widok detalu w projekcie z Weekend 4 (`menu_app/views.py: pizza_detail`) wciaz laduje pizze z pliku `menu.json` (legacy z Weekend 3) - **nie z ORM**. Pizza dodana przez formularz nie pojawi sie w detalu. Jesli bonus failuje na `Http404` - to znany problem projektu, nie Twojego testu.

### REVIEW: Co dalej? (10 min)

W tym momencie masz **dzialajace testy E2E**. Ale:
- W kazdym tescie powtarzasz `driver.get("http://127.0.0.1:8000/menu/")`
- W kazdym tescie powtarzasz selektory `By.CSS_SELECTOR, ".card"`
- Jesli zmienisz template (zamiast Bootstrap kart dasz np. `<table>`), trzeba poprawic w **wielu** miejscach

**Jutro** rozwiazemy te problemy uzywajac **Page Object Model**.

---

## Czesc 9: Podsumowanie dnia 1 (5 min)

### Co umiesz po dziu 1

- Instalacja Selenium + webdriver-manager
- Otwieranie strony, drukowanie tytulu/URL
- Inspekcja HTML w DevTools
- Lokalizatory: ID, NAME, CSS_SELECTOR, XPATH, LINK_TEXT
- `find_element` vs `find_elements`
- Interakcje: `click()`, `send_keys()`, `clear()`, `text`, `get_attribute()`
- WebDriverWait + expected_conditions
- Pierwszy pytest test ze Selenium

### Najwazniejsze wzorce

```python
# Wzorzec 1: znalezienie elementu
element = driver.find_element(By.CSS_SELECTOR, ".some-class")

# Wzorzec 2: wypelnienie formularza i submit
driver.find_element(By.NAME, "field").send_keys("value")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Wzorzec 3: czekanie na zmiane stanu
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "result")))

# Wzorzec 4: pytest fixture
@pytest.fixture
def driver():
    drv = webdriver.Chrome(...)
    yield drv
    drv.quit()
```

### Czego nie omowilismy (jutro!)

- Page Object Model - jak organizowac kod testow
- Headless mode + screenshoty
- Pelne scenariusze E2E (uzytkownik zamawia pizze)
- Selenium poza testami (scraping)

### Preview dnia 2

Jutro przeksztalcimy nasze rozproszone testy w czytelna strukture POM:

```python
# Zamiast tego (rozsiane lokalizatory):
driver.find_element(By.NAME, "name").send_keys("Margherita")
driver.find_element(By.NAME, "price").send_keys("25")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Bedzie to (Page Object):
add_pizza_page.add_pizza("Margherita", 25)
```

### Cwiczenie domowe (opcjonalne)

Napisz test E2E dla detali pizzy:
1. Wejdz na `/menu/`
2. Klinij na pierwsza pizze
3. Sprawdz ze URL zawiera `/menu/<nazwa>/`
4. Sprawdz ze na stronie detalu jest cena pizzy

---

## Troubleshooting

### "ChromeDriver only supports Chrome version XX"

```bash
pip install --upgrade webdriver-manager selenium
```

### "Connection refused" przy `127.0.0.1:8000`

Serwer Django nie dziala. W osobnym terminalu:
```bash
python3 manage.py runserver
```

### Test failuje z "NoSuchElementException" choc element jest na stronie

1. Sprawdz selector w DevTools (`Ctrl+F` w panelu Elements)
2. Element moze byc w iframe - trzeba `driver.switch_to.frame(...)`
3. Element ladowal sie dynamicznie - dodaj `WebDriverWait`

### "ElementNotInteractableException" przy click()

Element jest widoczny w DOM ale niedostepny (zaslony, disabled, animowany). Dodaj:
```python
wait.until(EC.element_to_be_clickable((By.ID, "btn")))
```

### Skrypt zostawia okna Chrome

Brak `driver.quit()`. Najlepiej uzywac `try/finally`:
```python
try:
    # ... twoj kod
finally:
    driver.quit()
```

Albo uzywac fixture pytest - automatycznie sprzatnie.
