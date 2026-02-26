# Dzien 1: Debugger VS Code + Django ORM

## Czesc 1: Recap Weekend 3 (20 min)

### Co zrobilismy do tej pory

**Weekend 1:** Programowanie proceduralne -> OOP
- Klasy: Pizza, Menu, Customer, VIPCustomer, Order
- Dziedziczenie: Customer -> VIPCustomer

**Weekend 2:** Wyjatki + I/O + Testy
- Hierarchia wyjatkow: PizzeriaError -> ValidationError, NotFoundError
- Serializacja JSON: to_dict(), from_dict(), save_to_file()
- Testy pytest: fixtures, pytest.raises

**Weekend 3:** Git + Django
- Git: init, add, commit, branch, merge, push
- Django: views, templates, formularze, messages
- Pelna aplikacja webowa (menu + klienci + zamowienia)
- Dane w plikach JSON (bez bazy danych)

### Plan tego weekendu

```
Dzien 1: Debugger VS Code + Django ORM
  - Debugowanie kodu w VS Code (breakpoints, krokowanie)
  - ORM: modele Django, migracje, admin panel, QuerySet API
  - Przeniesienie danych z JSON do bazy SQLite

Dzien 2: REST API z Django REST Framework
  - Teoria REST API (HTTP metody, JSON, status codes)
  - Budowanie API endpointow (CRUD)
  - Testowanie API z pytest
```

### Sprawdzenie srodowiska

Upewnij sie ze masz dzialajacy projekt z Weekend 3:

```bash
cd 2801-03-2026/pizzeria_django
python3 manage.py runserver
```

Wejdz na http://127.0.0.1:8000/menu/ - powinienes zobaczyc liste pizz.

Jesli nie masz dzialajacego projektu - uzyj szkieletu `pizzeria_django/` ktory jest przygotowany z rozwiazaniem Weekend 3.

---

## Czesc 2: Debugger VS Code (45 min)

### Teoria: Po co debugger?

Do tej pory debugowalismy kod przez `print()`:

```python
def pizza_list(request):
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    print(f"DEBUG: zaladowano {len(menu)} pizz")    # <- brzydkie!
    print(f"DEBUG: pizzas = {list(menu)}")            # <- trzeba usunac pozniej
    return render(request, 'menu_app/pizza_list.html', {'pizzas': list(menu)})
```

Problemy z `print()`:
- Trzeba dodawac i usuwac recznie
- Nie mozna zatrzymac programu w srodku
- Nie mozna sprawdzic wartosci zmiennych interaktywnie
- Latwo zostawic print() w kodzie produkcyjnym

**Debugger** to narzedzie wbudowane w IDE ktore pozwala:
- **Zatrzymac** program w dowolnym miejscu (breakpoint)
- **Sprawdzic** wartosci wszystkich zmiennych
- **Krokowac** przez kod linia po linii
- **Obserwowac** wyrazenia (watches)
- **Zmienic** wartosci zmiennych w locie

### SHOW: Konfiguracja VS Code debugger (15 min)

#### Krok 1: Otworz projekt w VS Code

```bash
cd 2801-03-2026/pizzeria_django
code .
```

#### Krok 2: Stworz konfiguracje debuggera

Kliknij ikone debuggera w bocznym panelu (ikona z robaczkiem) lub `Ctrl+Shift+D`.

Kliknij "create a launch.json file" i wybierz "Python Debugger" -> "Django".

VS Code stworzy plik `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver", "--noreload"],
            "django": true
        }
    ]
}
```

Wazne opcje:
- `"args": ["runserver", "--noreload"]` - uruchamia serwer Django. `--noreload` wylacza auto-reload zeby debugger dzialal stabilnie.
- `"django": true` - wlacza wsparcie dla szablonow Django

#### Krok 3: Ustaw breakpoint

Otworz plik `menu_app/views.py`. Kliknij na marginesie (na lewo od numeru linii) przy linii `return render(...)` w funkcji `pizza_list`. Pojawi sie czerwona kropka - to jest **breakpoint**.

#### Krok 4: Uruchom debugger

Nacisnij `F5` (lub kliknij zielony trojkat w panelu debuggera).

VS Code uruchomi serwer Django. Otworz przegladarke i wejdz na http://127.0.0.1:8000/menu/

Program zatrzyma sie na breakpoincie! Zobaczysz:

```
Zolta linia na breakpoincie = "tu jestesmy"
```

#### Krok 5: Zbadaj stan programu

W panelu po lewej stronie zobaczysz:

**VARIABLES** - wszystkie zmienne lokalne:
```
request = <WSGIRequest: GET '/menu/'>
menu = <rozwiazanie_weekend2.pizza.Menu object>
```

**WATCH** - dodaj wyrazenia do obserwacji:
- Kliknij "+" i wpisz `len(list(menu))` -> zobaczysz ile pizz jest zaladowanych
- Wpisz `list(menu)[0].name` -> nazwa pierwszej pizzy

**CALL STACK** - stos wywolan (ktorymi funkcjami przeszlismy zeby tu trafic)

#### Krok 6: Krokowanie

Przyciski na gorze ekranu (lub skroty klawiszowe):

| Przycisk | Skrot | Nazwa | Co robi |
|----------|-------|-------|---------|
| ▶️ | F5 | Continue | Kontynuuj do nastepnego breakpointa |
| ⬇️ | F10 | Step Over | Wykonaj linie i przejdz do nastepnej |
| ➡️ | F11 | Step Into | Wejdz do wnetrza funkcji |
| ⬆️ | Shift+F11 | Step Out | Wyjdz z biezacej funkcji |
| 🔄 | Ctrl+Shift+F5 | Restart | Uruchom od nowa |
| ⏹️ | Shift+F5 | Stop | Zatrzymaj debugger |

**Demonstracja:**
1. Ustaw breakpoint na pierwszej linii `pizza_list`
2. `F10` (Step Over) - przejdz linia po linii
3. Obserwuj jak zmienne pojawiaja sie w panelu VARIABLES
4. Po `menu.load_from_file(MENU_FILE)` - sprawdz `len(list(menu))`
5. `F5` (Continue) - pusc dalej

#### Krok 7: Warunkowy breakpoint

Prawy klik na breakpoincie -> "Edit Breakpoint..." -> wpisz warunek:

```python
len(list(menu)) > 3
```

Teraz breakpoint zatrzyma sie TYLKO gdy w menu jest wiecej niz 3 pizze. Przydatne gdy szukasz bledu w specyficznej sytuacji.

### DO: Debugowanie pizza_list view

**Cel:** Uzyj debuggera VS Code zeby zbadac jak dziala Twoj pizza_list view.

**Krok 1:** Stworz `.vscode/launch.json` (jesli nie masz) z konfiguracja Django.

**Krok 2:** Ustaw breakpoint na **pierwszej linii** funkcji `pizza_list` w `menu_app/views.py`.

**Krok 3:** Uruchom debugger (F5) i wejdz na http://127.0.0.1:8000/menu/

**Krok 4:** Gdy program sie zatrzyma:
- Sprawdz `request.method` w panelu VARIABLES -> powinno byc `'GET'`
- Kliknij F10 (Step Over) az do linii `menu.load_from_file(...)`
- Po wykonaniu tej linii sprawdz `list(menu)` w WATCH -> lista obiektow Pizza
- Sprawdz `menu.get_cheapest()` w WATCH -> najtansza pizza
- Kliknij F5 (Continue) zeby dokonczyc

**Krok 5:** Teraz ustaw breakpoint w `pizza_detail` (jesli masz ten view) i wejdz na /menu/Margherita/. Sprawdz wartosc `name` w VARIABLES.

**Krok 6:** Usun breakpointy po zakonczeniu (kliknij na czerwona kropke zeby ja usunac).

### Debugger - podsumowanie

```
KONFIGURACJA
  .vscode/launch.json          Konfiguracja debuggera (raz na projekt)
  Breakpoint (czerwona kropka)  Kliknij na marginesie linii

KROKOWANIE
  F5                           Continue (do nastepnego breakpointa)
  F10                          Step Over (nastepna linia)
  F11                          Step Into (wejdz do funkcji)
  Shift+F11                    Step Out (wyjdz z funkcji)

INSPEKCJA
  VARIABLES                    Panel ze zmiennymi lokalnymi
  WATCH                        Dodaj wyrazenia do obserwacji
  CALL STACK                   Stos wywolan (skad przyszlismy)
  DEBUG CONSOLE                Wpisz wyrazenie Python i zobacz wynik
```

---

## Troubleshooting: Debugger

Jezeli debugger nie startuje lub rzuca bledy, sprawdz ponizsze:

### "Couldn't import Django" / ModuleNotFoundError

Debugger uzywa innego interpretera Python niz ten, w ktorym masz zainstalowane Django.

**Rozwiazanie:** Sprawdz jaki interpreter Python jest wybrany w VS Code. Otworz Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) i wpisz `Python: Select Interpreter`. Wybierz interpreter, w ktorym masz Django. Mozesz sprawdzic w terminalu:

```bash
which python3
python3 -c "import django; print(django.__version__)"
```

Jesli uzywasz virtualenv, upewnij sie ze VS Code uzywa interpretera z tego srodowiska. Mozesz tez dodac sciezke w `launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver", "--noreload"],
            "django": true,
            "python": "/sciezka/do/twojego/python3"
        }
    ]
}
```

### Breakpoint nie zatrzymuje programu

- Upewnij sie ze uzyto `--noreload` w args (bez tego Django odpala 2 procesy i debugger moze nie trafic na wlasciwy)
- Sprawdz czy breakpoint jest ustawiony w kodzie ktory sie wykonuje (nie w importach, nie w komentarzach)

### Port 8000 jest zajety

Jesli poprzedni serwer nadal dziala:

```bash
# Linux/Mac:
lsof -ti:8000 | xargs kill

# Windows:
netstat -ano | findstr :8000
taskkill /PID <numer_pid> /F
```

Albo zmien port w launch.json: `"args": ["runserver", "8001", "--noreload"]`

---

## Czesc 3: Django ORM - Teoria (20 min)

### Czym jest baza danych?

Do tej pory przechowywalismy dane w **plikach JSON**. To dziala dla malych projektow, ale w prawdziwych aplikacjach uzywamy **bazy danych** -- wyspecjalizowanego programu do przechowywania i przeszukiwania danych.

**Baza danych** to osobny program (serwer) ktory:
- Przechowuje dane na dysku w zoptymalizowanym formacie
- Umozliwia szybkie wyszukiwanie (nawet w milionach rekordow)
- Obsluguje wielu uzytkownikow naraz (wspolbieznosc)
- Gwarantuje spojnosc danych (transakcje)

### Rodzaje baz danych

**Relacyjne (SQL)** -- dane w tabelach z wierszami i kolumnami, polaczone relacjami:

| Baza | Opis |
|------|------|
| **SQLite** | Plikowa baza, nie wymaga instalacji serwera. Idealna do nauki i malych projektow. Django uzywa jej domyslnie. |
| **PostgreSQL** | Potezna baza open-source. Standard w produkcji. |
| **MySQL / MariaDB** | Popularna baza, czesto spotykana w hostingach. |

Przyklad tabeli relacyjnej:

```
Tabela: pizza
+----+------------------+-------+
| id | name             | price |
+----+------------------+-------+
|  1 | Margherita       | 25.0  |
|  2 | Pepperoni        | 30.0  |
|  3 | Hawajska         | 32.0  |
+----+------------------+-------+
```

Kazdy wiersz to jeden rekord. Kolumny to pola (atrybuty). `id` to klucz glowny (unikalny identyfikator).

**Nierelacyjne (NoSQL)** -- inne podejscia do przechowywania danych:

| Typ | Przyklad | Dane przechowywane jako |
|-----|----------|------------------------|
| Dokumentowe | MongoDB | Dokumenty JSON (podobne do naszych plikow!) |
| Klucz-wartosc | Redis | Pary klucz: wartosc (szybki cache) |
| Grafowe | Neo4j | Wezly i krawedzie (relacje spoleczne) |

**Na tym kursie uzywamy SQLite** -- relacyjnej bazy plikowej. Nie trzeba nic instalowac -- Django tworzy plik `db.sqlite3` automatycznie. W produkcji zwykle przesiadamy sie na PostgreSQL, ale caly kod Django pozostaje taki sam (zmienia sie tylko ustawienie `DATABASES` w `settings.py`).

### Czym jest ORM?

**ORM** = Object-Relational Mapping = mapowanie obiektow na tabele w bazie danych.

Do tej pory przechowywalismy dane w plikach JSON:

```python
# Weekend 3 - zapis do JSON
menu.save_to_file("menu.json")
menu.load_from_file("menu.json")
```

To dzialalo, ale ma ograniczenia:
- Brak wyszukiwania (trzeba ladowac CALY plik zeby znalezc jedna pizze)
- Brak relacji (zamowienia to surowe ID w JSON)
- Brak wspolbieznosci (dwoch uzytkownikow naraz = problem)
- Brak admin panelu

**Django ORM** pozwala zdefiniowac klase Pythona (model), a Django automatycznie tworzy tabele w bazie danych:

```python
# Django model
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

# Uzycie - Django generuje SQL automatycznie:
Pizza.objects.create(name="Margherita", price=25.0)   # INSERT INTO pizza ...
Pizza.objects.all()                                     # SELECT * FROM pizza
Pizza.objects.filter(price__gt=30)                      # SELECT * WHERE price > 30
Pizza.objects.get(name="Margherita")                    # SELECT * WHERE name = 'Margherita'
```

Nie piszesz SQL - Django robi to za Ciebie!

### Ewolucja projektu: od plikow do bazy danych

Na poprzednich weekendach zbudowalismy klasy Pythona (`Pizza`, `Customer`, `Menu`) ktore przechowywaly dane w plikach JSON. Teraz **zastepujemy** te klasy **modelami Django ORM** -- robia to samo (walidacja, logika biznesowa), ale dodatkowo zapisuja dane do bazy:

```
Weekend 1-2:                     Weekend 4:
  pizza.py (klasa Python)   -->    menu_app/models.py (model Django)
  menu.json (plik)          -->    db.sqlite3 (baza danych)
  save_to_file()            -->    model.save()
  load_from_file()          -->    Model.objects.all()
```

Folder `rozwiazanie_weekend2/` zostaje w projekcie jako referencja, ale **nowy kod bedzie korzystal z modeli Django**.

### Schema bazy danych

Zanim zapiszemy dane w bazie relacyjnej, musimy zdefiniowac **scheme** (strukture) -- czyli jakie tabele istnieja, jakie maja kolumny i jakiego typu sa dane.

Porownaj z plikiem JSON, gdzie mozesz zapisac cokolwiek:

```json
{"name": "Margherita", "price": 25.0}
{"name": "Pepperoni"}
{"cena": "trzydziesci", "extra_field": true}
```

JSON nie wymusza struktury -- kazdy rekord moze wygladac inaczej. W relacyjnej bazie danych musisz **najpierw** zdefiniowac tabele:

```sql
CREATE TABLE pizza (
    id    INTEGER PRIMARY KEY,
    name  VARCHAR(100) NOT NULL UNIQUE,
    price FLOAT NOT NULL
);
```

Dopiero po utworzeniu tabeli mozesz wstawiac dane. Proba wstawienia rekordu bez `price` lub z typem `VARCHAR` zamiast `FLOAT` zakonczy sie bledem. To jest zaleta -- baza **pilnuje** ze dane sa poprawne.

### Migracje -- po co?

Problem: definiujemy modele w Pythonie, ale baza danych rozumie SQL. Ktos musi **przetlumaczyc** model Pythona na komendy SQL (`CREATE TABLE`, `ALTER TABLE` itd.).

Tu wkraczaja **migracje** -- mechanizm Django ktory automatycznie generuje SQL ze zmian w modelach:

```
Model Python           Migracja              Baza danych
class Pizza:    --->   0001_initial.py  ---> CREATE TABLE pizza (...)
  name = Char          (wygenerowany
  price = Float        automatycznie)
```

Gdy pozniej dodasz nowe pole do modelu (np. `description`), Django wygeneruje **kolejna migracje** ktora doda kolumne do istniejącej tabeli (nie tworzy jej od nowa):

```
Dodales pole:          Nowa migracja:        Baza danych:
  description = Text   0002_add_desc.py ---> ALTER TABLE pizza ADD COLUMN description TEXT;
```

Dwie komendy:

```bash
python manage.py makemigrations    # Generuj plik migracji (z modelu -> SQL)
python manage.py migrate           # Zastosuj migracje (wykonaj SQL w bazie)
```

`makemigrations` porownuje Twoje modele z poprzednimi migracjami i generuje plik opisujacy roznice. `migrate` wykonuje te zmiany na bazie. Django pamięta ktore migracje zostaly juz zastosowane, wiec nie wykona tej samej migracji dwa razy.

### SHOW: Konfiguracja projektu pod ORM

Zanim stworzymy pierwszy model, musimy skonfigurowac projekt. Na Weekend 3 celowo wylaczylismy baze danych (`DATABASES = {}`). Teraz ja wlaczamy.

**Krok 1:** Otworz `pizzeria_project/settings.py` i zmien `DATABASES = {}` na:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To mowi Django: "uzyj bazy SQLite, zapisz ja w pliku `db.sqlite3` obok `manage.py`".

**Krok 2:** Dodaj brakujace appy do `INSTALLED_APPS` (potrzebne do migracji i admin):

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'menu_app',
    'customers_app',
    'orders_app',
]
```

Nowe appy:
- `admin` - panel administracyjny (do zarzadzania danymi przez przegladarke)
- `auth` - system uzytkownikow (potrzebny do logowania do admina)
- `contenttypes`, `sessions` - wewnetrzne zaleznosci Django

**Krok 3:** Dodaj `SessionMiddleware` i `AuthenticationMiddleware` do MIDDLEWARE (potrzebne do admin i sesji). Mozesz tez usunac linie `MESSAGE_STORAGE = ...` na dole pliku -- byla potrzebna na Weekend 3 bo nie mielismy sesji, teraz juz mamy:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Krok 4:** Dodaj brakujacy context processor do TEMPLATES:

```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Krok 5:** Sprawdz ze konfiguracja jest poprawna:

```bash
python3 manage.py check
# System check identified no issues (0 silenced).
```

Jesli widzisz bledy - sprawdz czy nie masz literowek w settings.py.

### SHOW: Pierwszy model (GENERIC - ksiazka)

Zobaczmy jak wyglada model Django na prostym przykladzie. Wpisujemy go w pliku `menu_app/models.py` (Django szuka modeli tylko w plikach `models.py` wewnatrz aplikacji zarejestrowanych w `INSTALLED_APPS`):

```python
# menu_app/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    published_year = models.IntegerField(default=2024)

    def __str__(self):
        return f"{self.title} ({self.author})"
```

Tworzenie modelu:
1. Dziedziczymy po `models.Model`
2. Kazde pole to typ z `django.db.models`: `CharField`, `FloatField`, `IntegerField`, `BooleanField`, itd.
3. `__str__` - tekstowa reprezentacja (widoczna w admin panelu i w shell)

Typy pol:
| Typ | Python | Baza danych | Przyklad |
|-----|--------|-------------|---------|
| `CharField(max_length=N)` | str | VARCHAR(N) | nazwa, email |
| `TextField()` | str | TEXT | opis, tresc |
| `IntegerField()` | int | INTEGER | ilosc, rok |
| `FloatField()` | float | REAL | cena |
| `BooleanField()` | bool | BOOLEAN | aktywny, vip |
| `DateTimeField(auto_now_add=True)` | datetime | DATETIME | data utworzenia |

Teraz tworzymy migracje i stosujemy je:

```bash
python manage.py makemigrations
# Migrations for 'menu_app':
#   menu_app/migrations/0001_initial.py
#     - Create model Book

python manage.py migrate
# Applying menu_app.0001_initial... OK
```

I mozemy uzywac modelu w Django shell:

```bash
python manage.py shell
>>> from menu_app.models import Book
>>> Book.objects.create(title="Python Crash Course", author="Eric Matthes", price=49.99)
>>> Book.objects.create(title="Fluent Python", author="Luciano Ramalho", price=59.99)
>>> Book.objects.all()
<QuerySet [<Book: Python Crash Course (Eric Matthes)>, <Book: Fluent Python (Luciano Ramalho)>]>
>>> Book.objects.get(title="Fluent Python")
<Book: Fluent Python (Luciano Ramalho)>
```

---

## Cwiczenie 1: Model Pizza + migracja

**Cel:** Stworz model Django dla pizzy i przetestuj go w Django shell.

**WAZNE:** Na tym weekendzie pracujemy w szkielecie `pizzeria_django/`. Modele tworzymy w **istniejacych appach** (Pizza w `menu_app`, Customer w `customers_app`, Order w `orders_app`). Konfiguracje `settings.py` juz zrobilismy w SHOW powyzej.

**Krok 1:** Usun model Book z `menu_app/models.py` (byl tylko do demonstracji) i stworz model Pizza:

```python
# menu_app/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

    def clean(self):
        """Walidacja domenowa."""
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': f'Nieprawidlowa cena: {self.price} (musi byc > 0)'})
        if not self.name:
            raise ValidationError({'name': 'Nazwa pizzy nie moze byc pusta!'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.price} zl"

    class Meta:
        ordering = ['name']
```

Wyjasnienie:
- `unique=True` na `name` - baza danych pilnuje ze nazwy nie moga sie powtarzac (odpowiednik `DuplicatePizzaError`)
- `clean()` - metoda walidacji Django. Wywolywana przez `full_clean()`. Tutaj sprawdzamy reguly biznesowe (cena > 0, nazwa niepusta).
- `save()` - nadpisujemy zeby **zawsze** walidowac przed zapisem. Domyslnie Django nie wywoluje `clean()` przy `save()` - trzeba to zrobic recznie.
- `class Meta: ordering = ['name']` - domyslne sortowanie po nazwie

**Krok 3:** Stworz migracje i zastosuj je:

```bash
python3 manage.py makemigrations menu_app
python3 manage.py migrate
```

Powinienes zobaczyc cos takiego:
```
Migrations for 'menu_app':
  menu_app/migrations/0001_initial.py
    - Create model Pizza
...
Applying menu_app.0001_initial... OK
```

**Krok 4:** Przetestuj w Django shell:

```bash
python3 manage.py shell
```

```python
>>> from menu_app.models import Pizza

# Stworz pizze
>>> p = Pizza.objects.create(name="Margherita", price=25.0)
>>> p
<Pizza: Margherita: 25.0 zl>
>>> p.id    # Django automatycznie dodaje pole 'id' (auto-increment)
1

# Stworz wiecej
>>> Pizza.objects.create(name="Pepperoni", price=30.0)
>>> Pizza.objects.create(name="Hawajska", price=32.0)

# Pobierz wszystkie
>>> Pizza.objects.all()
<QuerySet [<Pizza: Hawajska: 32.0 zl>, <Pizza: Margherita: 25.0 zl>, <Pizza: Pepperoni: 30.0 zl>]>

# Pobierz jedna
>>> Pizza.objects.get(name="Margherita")
<Pizza: Margherita: 25.0 zl>

# Sprobuj stworzyc z ujemna cena
>>> Pizza.objects.create(name="Zla", price=-10)
# ValidationError: {'price': ['Nieprawidlowa cena: -10 (musi byc > 0)']}

# Sprobuj duplikat
>>> Pizza.objects.create(name="Margherita", price=99)
# IntegrityError: UNIQUE constraint failed: menu_app_pizza.name

>>> exit()
```

Gratulacje - Twoj pierwszy model Django dziala! Dane sa w bazie SQLite (plik `db.sqlite3`).

---

## Czesc 4: Django Admin (25 min)

### SHOW: Admin panel

Django ma wbudowany panel administracyjny - graficzny interfejs do zarzadzania danymi w bazie. Dziala automatycznie z Twoimi modelami.

**Krok 1: Dodaj URL admin do glownego `pizzeria_project/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),    # <- DODAJ
    path('', lambda request: redirect('menu/')),
    path('menu/', include('menu_app.urls')),
    path('klienci/', include('customers_app.urls')),
    path('zamowienia/', include('orders_app.urls')),
]
```

**Krok 2: Stworz konto administratora**

```bash
python3 manage.py createsuperuser
```

Podaj: username (np. `admin`), email (mozesz pominac - Enter), haslo (np. `admin123` - na warsztacie proste haslo jest OK).

**Krok 3: Zarejestruj model w admin**

Otworz `menu_app/admin.py`:

```python
from django.contrib import admin
from .models import Pizza

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
```

Wyjasnienie:
- `@admin.register(Pizza)` - rejestruje model Pizza w panelu admin
- `list_display` - ktore kolumny wyswietlic na liscie
- `search_fields` - po jakich polach mozna szukac

**Krok 4: Otworz admin panel**

```bash
python3 manage.py runserver
```

Wejdz na http://127.0.0.1:8000/admin/ i zaloguj sie danymi superusera.

Zobaczysz:
- Lista modeli (Pizzas)
- Mozesz dodawac, edytowac, usuwac rekordy
- Wyszukiwarka, sortowanie
- Historia zmian

### Cwiczenie 2: Pizza w admin

**Krok 1:** Stworz superusera (jesli jeszcze nie masz):
```bash
python3 manage.py createsuperuser
```

**Krok 2:** Zarejestruj model Pizza w `menu_app/admin.py` (kod powyzej).

**Krok 3:** Wejdz na http://127.0.0.1:8000/admin/ i:
- Zaloguj sie
- Kliknij "Pizzas"
- Dodaj kilka pizz przez formularz admin
- Sprobuj dodac pizze z ujemna cena - powinien byc blad walidacji
- Sprobuj dodac pizze z ta sama nazwa - powinien byc blad unique constraint

**Krok 4:** Zaktualizuj view `pizza_list` w `menu_app/views.py` zeby czytal dane z ORM zamiast z JSON:

**Przed (Weekend 3 - JSON):**
```python
from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.pizza import Menu

MENU_FILE = os.path.join(DATA_DIR, 'menu.json')

def pizza_list(request):
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    return render(request, 'menu_app/pizza_list.html', {'pizzas': list(menu)})
```

**Po (Weekend 4 - ORM):**
```python
from django.shortcuts import render
from .models import Pizza

def pizza_list(request):
    pizzas = Pizza.objects.all()
    return render(request, 'menu_app/pizza_list.html', {'pizzas': pizzas})
```

Roznica:
- Nie importujemy juz `Menu` ani `DATA_DIR` - importujemy model `Pizza` z tego samego appu (`from .models`)
- `Pizza.objects.all()` zamiast `menu.load_from_file()`

**Krok 5:** Wejdz na http://127.0.0.1:8000/menu/ - powinienes zobaczyc pizze ktore wlasnie dodales przez admin panel! Dane pochodza teraz z bazy danych, nie z pliku JSON.

**Krok 6:** Zaktualizuj tez `pizza_add` na ORM. Obecna wersja uzywa `Menu` i `save_to_file()` — zamien na `Pizza.objects.create()`:

```python
from django.core.exceptions import ValidationError
from django.db import IntegrityError

def pizza_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price_str = request.POST.get('price', '').strip()

        errors = []
        if not name:
            errors.append("Nazwa pizzy jest wymagana.")
        if not price_str:
            errors.append("Cena jest wymagana.")

        if not errors:
            try:
                price = float(price_str)
                Pizza.objects.create(name=name, price=price)
                messages.success(request, f"Dodano pizzę: {name}")
                return redirect('pizza_list')
            except (ValueError, TypeError):
                errors.append("Nieprawidlowa cena.")
            except ValidationError as e:
                errors.extend(e.messages)
            except IntegrityError:
                errors.append(f"Pizza '{name}' juz istnieje!")

        return render(request, 'menu_app/pizza_form.html', {
            'errors': errors,
            'name': name,
            'price': price_str,
        })

    return render(request, 'menu_app/pizza_form.html')
```

Przetestuj: wejdz na http://127.0.0.1:8000/menu/dodaj/, dodaj nowa pizze przez formularz, a nastepnie sprawdz w admin panelu (http://127.0.0.1:8000/admin/) ze sie pojawila. Dane plyna w obie strony -- bo oba widoki korzystaja z tej samej bazy danych.

**Bonus:** Jesli masz czas, zaktualizuj tez `pizza_detail`:

---

## Czesc 5: QuerySet API (35 min)

### Teoria: QuerySet - zapytania do bazy

QuerySet to interfejs Django do odpytywania bazy danych. Kazdy model ma manager `objects` z metodami:

```python
# POBIERANIE
Pizza.objects.all()                          # wszystkie rekordy
Pizza.objects.get(name="Margherita")         # dokladnie 1 rekord (rzuca DoesNotExist jesli brak)
Pizza.objects.filter(price__gt=30)           # filtrowanie (WHERE price > 30)
Pizza.objects.exclude(name="Hawajska")       # wykluczenie
Pizza.objects.first()                        # pierwszy rekord
Pizza.objects.last()                         # ostatni rekord
Pizza.objects.count()                        # ile rekordow

# FILTROWANIE - lookups (po podwojnym podkreslniku)
Pizza.objects.filter(price__gt=30)           # price > 30
Pizza.objects.filter(price__gte=30)          # price >= 30
Pizza.objects.filter(price__lt=30)           # price < 30
Pizza.objects.filter(name__contains="a")     # name LIKE '%a%'
Pizza.objects.filter(name__startswith="M")   # name LIKE 'M%'
Pizza.objects.filter(name__icontains="mar")  # case-insensitive contains

# SORTOWANIE
Pizza.objects.order_by('price')              # rosnaco po cenie
Pizza.objects.order_by('-price')             # malejaco po cenie
Pizza.objects.order_by('name')               # alfabetycznie

# TWORZENIE
Pizza.objects.create(name="Diavola", price=34.0)

# AKTUALIZACJA
pizza = Pizza.objects.get(name="Margherita")
pizza.price = 28.0
pizza.save()

# lub masowo:
Pizza.objects.filter(price__lt=30).update(price=30)   # ustaw wszystkie tanie na 30

# USUWANIE
pizza = Pizza.objects.get(name="Hawajska")
pizza.delete()

# lub masowo:
Pizza.objects.filter(price__gt=50).delete()
```

### SHOW: QuerySet w Django shell (GENERIC - ksiazki)

```bash
python3 manage.py shell
```

```python
>>> from menu_app.models import Book

# Stworz dane testowe
>>> Book.objects.create(title="Python Crash Course", author="Eric Matthes", price=49.99)
>>> Book.objects.create(title="Fluent Python", author="Luciano Ramalho", price=59.99)
>>> Book.objects.create(title="Django for Beginners", author="William Vincent", price=39.99)

# Filtrowanie
>>> Book.objects.filter(price__gt=45)
<QuerySet [<Book: Python Crash Course>, <Book: Fluent Python>]>

>>> Book.objects.filter(title__contains="Python")
<QuerySet [<Book: Python Crash Course>, <Book: Fluent Python>]>

# Laczenie filtrow (AND)
>>> Book.objects.filter(price__gt=45, author__contains="Matthes")
<QuerySet [<Book: Python Crash Course>]>

# Sortowanie
>>> Book.objects.order_by('price')         # najtansze najpierw
>>> Book.objects.order_by('-price')        # najdrozsze najpierw

# Agregacja
>>> from django.db.models import Avg, Min, Max
>>> Book.objects.aggregate(Avg('price'))
{'price__avg': 49.99}
>>> Book.objects.aggregate(Min('price'), Max('price'))
{'price__min': 39.99, 'price__max': 59.99}

# Aktualizacja
>>> book = Book.objects.get(title="Fluent Python")
>>> book.price = 54.99
>>> book.save()

# Usuwanie
>>> Book.objects.filter(title="Django for Beginners").delete()
(1, {'api.Book': 1})
```

### Cwiczenie 3: QuerySet cwiczenia w shell

**Cel:** Przetrenuj QuerySet API na modelu Pizza.

Otworz Django shell:
```bash
python3 manage.py shell
```

**Zadanie 1: Dane testowe** - upewnij sie ze masz przynajmniej 4 pizze w bazie:
```python
from menu_app.models import Pizza

# Sprawdz co masz
Pizza.objects.all()

# Dodaj brakujace (jesli potrzeba)
Pizza.objects.get_or_create(name="Margherita", defaults={"price": 25.0})
Pizza.objects.get_or_create(name="Pepperoni", defaults={"price": 30.0})
Pizza.objects.get_or_create(name="Hawajska", defaults={"price": 32.0})
Pizza.objects.get_or_create(name="Quattro Formaggi", defaults={"price": 35.0})
```

`get_or_create` to przydatna metoda - tworzy rekord tylko jesli nie istnieje.

**Zadanie 2: Filtrowanie** - znajdz:
- Pizze drozsze niz 30 zl
- Pizze ktorych nazwa zawiera "a" (case-insensitive)
- Pizze w przedziale cenowym 25-32 zl (uzyj `price__gte` i `price__lte`)

**Zadanie 3: Sortowanie** - posortuj pizze:
- Alfabetycznie po nazwie
- Po cenie malejaco

**Zadanie 4: Agregacja** - oblicz:
```python
from django.db.models import Avg, Min, Max
Pizza.objects.aggregate(Avg('price'))
Pizza.objects.aggregate(Min('price'), Max('price'))
```

**Zadanie 5: Aktualizacja** - zmien cene Margherity na 27.0:
```python
pizza = Pizza.objects.get(name="Margherita")
pizza.price = 27.0
pizza.save()
```

**Zadanie 6: DoesNotExist** - sprobuj znalezc nieistniejaca pizze:
```python
try:
    Pizza.objects.get(name="Carbonara")
except Pizza.DoesNotExist:
    print("Pizza nie znaleziona!")
```

Zwroc uwage: `Pizza.DoesNotExist` to wbudowany wyjatek Django -- kazdy model go ma. Uzywamy go zamiast naszego `PizzaNotFoundError` z Weekend 2.

---

## Czesc 6: Model Customer (40 min)

### Teoria: Pola z ograniczonym wyborem (choices)

Na Weekend 1 mielismy dwie klasy: `Customer` i `VIPCustomer` (dziedziczenie). W Django ORM mozemy to zamodelowac na kilka sposobow. Najprostszym jest **jedno pole `type` z ograniczonymi opcjami**:

```python
class Customer(models.Model):
    CUSTOMER_TYPES = [
        ('regular', 'Zwykly klient'),
        ('vip', 'VIP'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, default='regular')
    discount_percent = models.FloatField(default=0)
    loyalty_points = models.IntegerField(default=0)
```

`choices` to lista krotek `(wartosc_w_bazie, etykieta_dla_czlowieka)`. Django uzywa:
- `wartosc_w_bazie` przy zapisie/odczycie
- `etykieta` w admin panelu i formularzach

Zamiast dwoch klas (Customer + VIPCustomer) mamy jedna tabele z polem `customer_type`. Jesli `customer_type == 'vip'`, to `discount_percent` i `loyalty_points` maja znaczenie.

To uproszczenie - w rzeczywistym projekcie mozna by uzyc dziedziczenia modeli Django, ale na warsztacie jedno pole jest prostsze i latwiejsze do zrozumienia.

### Cwiczenie 4: Model Customer + migracja + admin

**Krok 1:** Dodaj model Customer w `customers_app/models.py`:

```python
# customers_app/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Customer(models.Model):
    CUSTOMER_TYPES = [
        ('regular', 'Zwykly klient'),
        ('vip', 'VIP'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, default='regular')
    discount_percent = models.FloatField(default=0)
    loyalty_points = models.IntegerField(default=0)

    def clean(self):
        if self.customer_type == 'vip' and (self.discount_percent < 0 or self.discount_percent > 100):
            raise ValidationError({'discount_percent': 'Rabat musi byc w zakresie 0-100%'})
        if not self.name:
            raise ValidationError({'name': 'Nazwa klienta nie moze byc pusta!'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_vip(self):
        return self.customer_type == 'vip'

    def __str__(self):
        vip_tag = " (VIP)" if self.is_vip else ""
        return f"{self.name}{vip_tag}"

    class Meta:
        ordering = ['name']
```

**Krok 2:** Stworz migracje i zastosuj:

```bash
python3 manage.py makemigrations customers_app
python3 manage.py migrate
```

**Krok 3:** Zarejestruj w admin (`customers_app/admin.py`):

```python
from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'customer_type', 'discount_percent', 'loyalty_points']
    list_filter = ['customer_type']
    search_fields = ['name']
```

**Krok 4:** Przetestuj w admin panelu - dodaj klienta zwyklego i VIP.

**Krok 5:** Przetestuj w shell:

```bash
python3 manage.py shell
```

```python
from customers_app.models import Customer

# Stworz klientow
Customer.objects.create(name="Jan Kowalski", phone="123-456-789")
Customer.objects.create(name="Anna Nowak", phone="987-654-321", customer_type="vip", discount_percent=15)

# Filtruj VIP-ow
Customer.objects.filter(customer_type="vip")

# Sprawdz property
c = Customer.objects.get(name="Anna Nowak")
c.is_vip    # True
c.discount_percent    # 15.0
```

**Krok 6:** Zaktualizuj view `customer_list` w `customers_app/views.py` na ORM (ten sam wzorzec co dla pizzy):

```python
from django.shortcuts import render
from .models import Customer

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers_app/customer_list.html', {'customers': customers})
```

**Krok 7:** Wejdz na http://127.0.0.1:8000/klienci/ - powinienes zobaczyc klientow dodanych przez admin i shell.

---

## Czesc 7: Model Order z relacjami (40 min)

### Teoria: ForeignKey - relacje miedzy modelami

Zamowienie jest powiazane z klientem (kto zamowil) i z pizzami (co zamowil). W bazie danych relacje tworzy sie przez **klucz obcy** (foreign key):

```python
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
```

`ForeignKey` oznacza: "to zamowienie nalezy do jednego klienta". Django:
- Dodaje kolumne `customer_id` w tabeli zamowien
- Pilnuje ze `customer_id` wskazuje na istniejacego klienta
- `on_delete=models.CASCADE` - jesli klient zostanie usuniety, jego zamowienia tez

**Dostep do relacji:**
```python
order = Order.objects.get(id=1)
order.customer          # -> obiekt Customer
order.customer.name     # -> "Jan Kowalski"

# Odwrotnie - zamowienia klienta:
customer = Customer.objects.get(id=1)
customer.order_set.all()    # -> QuerySet z zamowieniami klienta
```

### Teoria: Zamowienie z pozycjami

Zamowienie sklada sie z **pozycji** (OrderItem). Kazda pozycja to: pizza + ilosc.

```
Order                    OrderItem
+----------+            +----------+----------+----------+
| id       |  1---*     | order    | pizza    | quantity |
| customer |  --------> | (FK)     | (FK)     |          |
| created  |            +----------+----------+----------+
+----------+
```

`1---*` oznacza: jedno zamowienie ma wiele pozycji (relacja one-to-many).

### Cwiczenie 5: Modele Order i OrderItem

**Krok 1:** Dodaj modele w `orders_app/models.py`:

```python
# orders_app/models.py
from django.db import models
from menu_app.models import Pizza
from customers_app.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        """Suma przed rabatem."""
        return sum(item.total_price for item in self.items.all())

    @property
    def discount_amount(self):
        """Kwota rabatu VIP."""
        if self.customer.is_vip:
            return round(self.subtotal * self.customer.discount_percent / 100, 2)
        return 0

    @property
    def total_price(self):
        """Suma po rabacie."""
        return round(self.subtotal - self.discount_amount, 2)

    def __str__(self):
        return f"Zamowienie #{self.id} ({self.customer.name})"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField()

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.pizza.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.pizza.name}"
```

Zwroc uwage na **importy z innych appow**: `from menu_app.models import Pizza` i `from customers_app.models import Customer`. Modele Order/OrderItem sa w `orders_app`, ale uzywaja modeli z `menu_app` i `customers_app` przez ForeignKey.

Wyjasnienie nowych elementow:
- `related_name='items'` - pozwala pisac `order.items.all()` zamiast `order.orderitem_set.all()`
- `auto_now_add=True` - automatycznie ustawia date przy tworzeniu
- `PositiveIntegerField` - tylko liczby > 0
- `unit_price` - zapisujemy cene z momentu zamowienia (gdyby cena pizzy sie zmienila pozniej)
- Property `subtotal`, `discount_amount`, `total_price` - obliczenia analogiczne do klas z Weekend 1, ale teraz wbudowane w model Django

**Krok 2:** Stworz migracje i zastosuj:

```bash
python3 manage.py makemigrations orders_app
python3 manage.py migrate
```

**Krok 3:** Zarejestruj w admin (`orders_app/admin.py`):

```python
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'total_price']
    inlines = [OrderItemInline]
```

`TabularInline` pozwala edytowac pozycje zamowienia (OrderItem) bezposrednio na stronie zamowienia w admin panelu. `extra = 1` - domyslnie pokazuje 1 pusta pozycje do dodania.

**Krok 4:** Przetestuj w admin - stworz zamowienie, dodaj pozycje.

**Krok 5:** Przetestuj w shell:

```python
from menu_app.models import Pizza
from customers_app.models import Customer
from orders_app.models import Order, OrderItem

customer = Customer.objects.first()
pizza = Pizza.objects.get(name="Margherita")

# Stworz zamowienie
order = Order.objects.create(customer=customer)

# Dodaj pozycje
OrderItem.objects.create(order=order, pizza=pizza, quantity=2, unit_price=pizza.price)

# Sprawdz
order.items.all()       # QuerySet z pozycjami
order.subtotal          # 50.0 (2 x 25)
order.total_price       # 50.0 (bez rabatu) lub mniej (z rabatem VIP)
```

---

## Czesc 8: Import danych z JSON do bazy (35 min)

### SHOW: Management command (GENERIC)

Django pozwala tworzyc wlasne komendy CLI (management commands). Przydatne do: importu danych, czyszczenia bazy, generowania raportow.

Komenda to plik Pythona w `<app>/management/commands/<nazwa>.py`:

```
menu_app/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── import_books.py
```

```python
# menu_app/management/commands/import_books.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Importuje ksiazki z pliku'

    def handle(self, *args, **options):
        self.stdout.write("Importuje ksiazki...")
        # ... logika importu ...
        self.stdout.write(self.style.SUCCESS("Zaimportowano!"))
```

Uruchomienie:
```bash
python3 manage.py import_books
```

### Cwiczenie 6: Command import_data

**Cel:** Napisz komende ktora importuje dane z `rozwiazanie_weekend2/data/menu.json` i `customers.json` do bazy Django.

**Krok 1:** Stworz strukture katalogow `menu_app/management/commands/` (razem z plikami `__init__.py`):

```bash
mkdir -p menu_app/management/commands
touch menu_app/management/__init__.py
touch menu_app/management/commands/__init__.py
```

**Krok 2:** Stworz plik `menu_app/management/commands/import_data.py`:

```python
import os
import json
from django.core.management.base import BaseCommand
from menu_app.models import Pizza
from customers_app.models import Customer
from rozwiazanie_weekend2 import DATA_DIR


class Command(BaseCommand):
    help = 'Importuje dane z plikow JSON (rozwiazanie_weekend2) do bazy danych'

    def handle(self, *args, **options):
        self.import_pizzas()
        self.import_customers()

    def import_pizzas(self):
        menu_file = os.path.join(DATA_DIR, 'menu.json')
        try:
            with open(menu_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Plik {menu_file} nie istnieje"))
            return

        created = 0
        for item in data:
            pizza, was_created = Pizza.objects.get_or_create(
                name=item['name'],
                defaults={'price': item['price']}
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Pizze: zaimportowano {created}, juz istnialo {len(data) - created}"))

    def import_customers(self):
        customers_file = os.path.join(DATA_DIR, 'customers.json')
        try:
            with open(customers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Plik {customers_file} nie istnieje"))
            return

        created = 0
        for item in data:
            customer_type = 'vip' if item.get('type') == 'VIPCustomer' else 'regular'
            customer, was_created = Customer.objects.get_or_create(
                name=item['name'],
                defaults={
                    'phone': item['phone'],
                    'customer_type': customer_type,
                    'discount_percent': item.get('discount_percent', 0),
                    'loyalty_points': item.get('loyalty_points', 0),
                }
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Klienci: zaimportowano {created}, juz istnialo {len(data) - created}"))
```

**Krok 3:** Uruchom komende:

```bash
python3 manage.py import_data
```

Powinienes zobaczyc:
```
Pizze: zaimportowano 4, juz istnialo 0
Klienci: zaimportowano 3, juz istnialo 0
```

**Krok 4:** Sprawdz w admin panelu albo w shell ze dane sa w bazie.

---

## Podsumowanie dnia 1

### Co zrobilismy:
1. **Debugger VS Code:** konfiguracja, breakpoints, krokowanie, inspekcja zmiennych
2. **Django ORM:** modele w istniejacych appach (Pizza, Customer, Order)
3. **Django Admin + views:** po kazdym modelu - admin panel + aktualizacja widoku na ORM
4. **QuerySet API:** filtrowanie, sortowanie, agregacja
5. **Relacje:** ForeignKey, related_name, importy miedzy appami
6. **Management command:** import danych z JSON do bazy

### Kluczowe komendy

```bash
python3 manage.py makemigrations    # Generuj migracje z modeli
python3 manage.py migrate           # Zastosuj migracje (stworz tabele)
python3 manage.py createsuperuser   # Stworz konto admin
python3 manage.py shell             # Interaktywny Python z Django
python3 manage.py import_data       # Nasza komenda importu
```

### Kluczowe wzorce

```python
# Model
class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

# QuerySet
Pizza.objects.all()
Pizza.objects.filter(price__gt=30)
Pizza.objects.get(name="Margherita")
Pizza.objects.create(name="Diavola", price=34)

# Relacja
order.items.all()          # related_name
order.customer.name        # ForeignKey
```

### Preview dnia 2

Jutro: REST API z Django REST Framework
- JSON responses zamiast HTML
- Endpointy CRUD (Create, Read, Update, Delete)
- Testowanie API z pytest
