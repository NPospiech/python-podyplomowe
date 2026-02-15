# Dzien 2: Django - Pelna aplikacja webowa

## Agenda

**Czas trwania:** 8:30 - 15:00 (6h 30min z przerwami)

### Harmonogram

| Czas | Temat | Aktywnosc |
|------|-------|-----------|
| **8:30 - 8:50** | Recap dnia 1 | Sprawdzenie srodowiska, pytania |
| **8:50 - 10:30** | Detail views, static files, formularze | Teoria + cwiczenia |
| **10:30 - 10:40** | **PRZERWA** | 10 minut |
| **10:40 - 12:40** | Budowanie pelnej aplikacji | customers_app + orders_app |
| **12:40 - 13:10** | **PRZERWA** | 30 minut |
| **13:10 - 15:00** | Formularz zamowien, messages, integracja | Finalizacja + testy + podsumowanie |

### Co zbudujemy dzisiaj?

Pelna aplikacje webowa do zarzadzania pizzeria:
- **Detail views** - strona szczegolow pizzy z parametrem URL
- **Dziedziczenie szablonow** - wspolny wyglad z base.html + Bootstrap
- **Formularze HTML** - dodawanie pizz, klientow, zamowien
- **Error handling** - polaczenie wyjatkow z Weekend 2 z Django views
- **Messages** - komunikaty uzytkownikowi (sukces/blad)

### Czego sie nauczysz?

- Parametry w URL-ach (`<str:name>`, `<int:id>`)
- Dziedziczenie szablonow (`extends`, `block`)
- HTTP GET vs POST i wzorzec POST-Redirect-GET
- Ochrona CSRF w formularzach
- Obsluga bledow w views (try/except + Http404)
- Django messages framework

---

## Czesc 1: Recap dnia 1 (20 min)

### Co zrobilismy wczoraj

- **Git:** init, add, commit, branch, merge, push
- **GitHub:** fork, clone, push na forka
- **Django:** otworzylimy szkielet projektu `pizzeria_django/`
- **Pierwszy app:** `startapp menu_app` + rejestracja w INSTALLED_APPS + urls.py
- **Integracja:** skopiowalismy `rozwiazanie_weekend2/` do projektu Django
- **pizza_list:** view ladujacy dane z JSON i wyswietlajacy je w template

### Sprawdzenie srodowiska

Upewnij sie ze masz dzialajacy serwer:

```bash
cd 1415-02-2026/pizzeria_django
python3 manage.py runserver
```

Wejdz na http://127.0.0.1:8000/menu/ - powinienes zobaczyc liste pizz.

Przypomnij sobie kluczowe importy:
```python
from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.pizza import Pizza, Menu
```

---

## Czesc 2: Detail views - parametry w URL (45 min)

### Teoria: Czym sa parametry URL?

Do tej pory nasze URL-e byly statyczne:
- `/menu/` - zawsze ten sam widok (lista pizz)

Ale co jesli chcemy wyswietlic **szczegoly konkretnej pizzy**? Na przyklad:
- `/menu/Margherita/` - szczegoly Margherity
- `/menu/Pepperoni/` - szczegoly Pepperoni

Potrzebujemy sposobu zeby **wyciagnac czesc URL-a** (nazwe pizzy) i przekazac ja do view jako argument. Do tego sluza **parametry URL**.

### Skladnia parametrow URL w Django

```python
# urls.py
path('<str:name>/', views.pizza_detail, name='pizza_detail'),
```

`<str:name>` to **konwerter URL** - mowi Django:
- **`str`** - typ parametru (tekst). Inne typy: `int` (liczba calkowita), `slug` (tekst-z-myslnikami)
- **`name`** - nazwa argumentu, ktory zostanie przekazany do view

**Jak to dziala w praktyce:**

```
URL: /menu/Margherita/

path('<str:name>/', views.pizza_detail)
      ^^^^^^^^^^
      name = "Margherita"
                   |
                   v
def pizza_detail(request, name):    # name = "Margherita"
```

Przyklad z liczbami:
```
URL: /zamowienia/42/

path('<int:order_id>/', views.order_detail)
      ^^^^^^^^^^^^^^^
      order_id = 42 (int, nie string!)
```

### Teoria: Http404 - co robic gdy zasob nie istnieje?

Co jesli ktos wejdzie na `/menu/NieIstniejacaPizza/`? Musimy zwrocic blad **404 Not Found**.

W Django rzucamy specjalny wyjatek `Http404`:

```python
from django.http import Http404

def pizza_detail(request, name):
    # ... szukamy pizzy ...
    if not found:
        raise Http404(f"Pizza '{name}' nie znaleziona")
```

Django przechwyci ten wyjatek i wyswietli strone bledu 404. W trybie `DEBUG=True` zobaczysz ladna strone z opisem bledu.

**Polaczenie z Weekend 2:** Nasz engine rzuca `PizzaNotFoundError` gdy pizza nie istnieje. Mozemy go zamienic na `Http404`:

```python
from rozwiazanie_weekend2.exceptions import PizzaNotFoundError

try:
    pizza = menu.find_pizza(name)
except PizzaNotFoundError:
    raise Http404(f"Pizza '{name}' nie znaleziona")
```

### Demonstracja: Detail view (GENERIC - ksiazka)

Zobaczmy jak wyglada detail view na przykladzie listy ksiazek:

```python
# views.py
from django.http import Http404
from django.shortcuts import render

def book_detail(request, pk):
    books = {
        1: {'title': 'Python Crash Course', 'author': 'Eric Matthes'},
        2: {'title': 'Fluent Python', 'author': 'Luciano Ramalho'},
    }
    book = books.get(pk)
    if not book:
        raise Http404("Ksiazka nie znaleziona")
    return render(request, 'books/book_detail.html', {'book': book})
```

```python
# urls.py
path('books/<int:pk>/', views.book_detail, name='book_detail'),
```

```html
<!-- templates/books/book_detail.html -->
<h1>{{ book.title }}</h1>
<p>Autor: {{ book.author }}</p>
<a href="/books/">Powrot do listy</a>
```

Zwroc uwage na caly flow:
1. URL `/books/1/` -> Django wyciaga `pk=1` (jako int)
2. View `book_detail(request, pk=1)` -> szuka ksiazki w slowniku
3. Jesli znaleziona -> renderuje template z danymi
4. Jesli nie -> `Http404`

### Cwiczenie 1: pizza_detail view

**Cel:** po kliknieciu na nazwe pizzy w liscie, zobaczysz strone ze szczegolami tej pizzy.

**Krok 1:** Dodaj nowy view w `menu_app/views.py`:

```python
# menu_app/views.py - dodaj do istniejacego pliku
from django.http import Http404
from rozwiazanie_weekend2.exceptions import PizzaNotFoundError

def pizza_detail(request, name):
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    try:
        pizza = menu.find_pizza(name)
    except PizzaNotFoundError:
        raise Http404(f"Pizza '{name}' nie znaleziona")
    return render(request, 'menu_app/pizza_detail.html', {'pizza': pizza})
```

**Krok 2:** Stworz template `menu_app/templates/menu_app/pizza_detail.html`:

```html
<!DOCTYPE html>
<html>
<head><title>{{ pizza.name }}</title></head>
<body>
    <h1>{{ pizza.name }}</h1>
    <p>Cena: {{ pizza.price }} zl</p>
    <a href="/menu/">Powrot do menu</a>
</body>
</html>
```

Na razie uzywamy prostego HTML (tak jak w pizza_list z dnia 1). W nastepnym cwiczeniu dodamy base.html i przelaczymy na `{% extends %}`.

**Krok 3:** Dodaj URL w `menu_app/urls.py`:

```python
# menu_app/urls.py
path('<str:name>/', views.pizza_detail, name='pizza_detail'),
```

`<str:name>` oznacza: "wez cokolwiek z URL i przekaz jako argument `name` do view".
Np. URL `/menu/Margherita/` -> `pizza_detail(request, name='Margherita')`.

**Krok 4:** Dodaj linki w `pizza_list.html` zeby mozna bylo kliknac na pizze:

```html
{% for pizza in pizzas %}
    <li><a href="/menu/{{ pizza.name }}/">{{ pizza.name }}</a> - {{ pizza.price }} zl</li>
{% endfor %}
```

**Krok 5:** Sprawdz! Wejdz na /menu/, kliknij na nazwe pizzy. Sprobuj tez wejsc na /menu/NieIstniejaca/ - powinienes zobaczyc 404.

---

## Czesc 3: Dziedziczenie szablonow + Bootstrap (30 min)

### Teoria: Problem duplikacji w szablonach

Teraz mamy dwa szablony (`pizza_list.html` i `pizza_detail.html`) i kazdy ma caly `<!DOCTYPE html>...`. Gdybysmy chcieli dodac nawigacje na gorze strony, musielibysmy ja dodac w **kazdym** szablonie osobno. Przy 10 stronach to koszmar.

Rozwiazanie: **dziedziczenie szablonow** (template inheritance).

### Teoria: extends i block

Idea jest prosta - tworzymy **szablon bazowy** (`base.html`) ze wspolnymi elementami (nawigacja, naglowek, stopka) i oznaczamy **dziury** (`block`), ktore szablony potomne wypelnia trescia:

```
base.html (szablon bazowy):
+---------------------------+
| <nav> Menu | Klienci </nav>|     <- wspolne dla wszystkich stron
|                           |
| {% block content %}       |     <- "dziura" - tu wejdzie tresc
| {% endblock %}            |
|                           |
| <footer>Pizzeria</footer> |     <- wspolne dla wszystkich stron
+---------------------------+

pizza_list.html (szablon potomny):
{% extends "base.html" %}         <- "uzyj base.html jako szkieletu"
{% block content %}               <- "wypelnij dziure trescia:"
  <h1>Menu</h1>
  <ul>...</ul>
{% endblock %}
```

**Wynik:** Django wstawia tresc z `pizza_list.html` w miejsce `{% block content %}` w `base.html`. Nawigacja, CSS, JavaScript - wszystko jest w jednym miejscu (`base.html`) i nie trzeba tego powtarzac.

**Kluczowe tagi:**
- `{% extends "base.html" %}` - MUSI byc **pierwsza linia** szablonu potomnego
- `{% block nazwa %}...{% endblock %}` - definiuje blok do nadpisania
- Mozna miec wiele blokow: `title`, `content`, `extra_css`, itp.

### Teoria: Pliki statyczne (CSS, JS, obrazki)

Django obsluguje pliki statyczne (CSS, JavaScript, obrazki) przez system `staticfiles`.

**Konfiguracja** (juz gotowa w szkielecie):
```python
# settings.py
STATIC_URL = 'static/'              # URL pod ktorym dostepne sa pliki statyczne
STATICFILES_DIRS = [BASE_DIR / 'static']   # Gdzie Django szuka plikow
```

**Uzycie w szablonie:**
```html
{% load static %}                                      <!-- zaladuj tag 'static' -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">   <!-- uzyj go -->
```

`{% load static %}` musi byc na poczatku szablonu (po `{% extends %}` jesli jest).
`{% static 'css/style.css' %}` generuje poprawny URL do pliku, np. `/static/css/style.css`.

### Przegladnij base.html w szkielecie

Otworz plik `templates/base.html` w swoim projekcie - jest juz gotowy w szkielecie:

```html
{% load static %}
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Pizzeria{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/menu/">Pizzeria</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/menu/">Menu</a>
                <a class="nav-link" href="/klienci/">Klienci</a>
                <a class="nav-link" href="/zamowienia/">Zamowienia</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

Zwroc uwage na:
- **`{% block title %}Pizzeria{% endblock %}`** - blok z domyslna wartoscia "Pizzeria". Szablony potomne moga go nadpisac.
- **`{% block content %}{% endblock %}`** - pusty blok na tresc strony
- **Bootstrap CDN** - biblioteka CSS dajaca ladne style (przyciski, tabele, nawigacja)
- **Sekcja messages** - wyswietla komunikaty (uzyjesz pozniej)
- **`{% load static %}`** i **`{% static 'css/style.css' %}`** - ladowanie naszego CSS

### Cwiczenie 2: Ostyluj pizza pages

**Cel:** zaktualizuj swoje szablony zeby korzystaly z `base.html` zamiast pisac caly HTML od zera.

**Krok 1:** Zmien `pizza_list.html` zeby uzywal base.html:

```html
{% extends "base.html" %}

{% block title %}Menu{% endblock %}

{% block content %}
<h1>Menu Pizzerii</h1>
<ul>
{% for pizza in pizzas %}
    <li><a href="/menu/{{ pizza.name }}/">{{ pizza.name }}</a> - {{ pizza.price }} zl</li>
{% endfor %}
</ul>
{% endblock %}
```

**Krok 2:** Zmien tez `pizza_detail.html` - zastap caly prosty HTML na:

```html
{% extends "base.html" %}

{% block title %}{{ pizza.name }}{% endblock %}

{% block content %}
<h1>{{ pizza.name }}</h1>
<p>Cena: {{ pizza.price }} zl</p>
<a href="/menu/">Powrot do menu</a>
{% endblock %}
```

Porownaj z wersja z poprzedniego cwiczenia - zamiast calego `<!DOCTYPE html>...` mamy tylko tresc strony. Reszta (head, nav, bootstrap) jest w `base.html`.

**Krok 3:** Sprawdz! Odswiez strone - powinienes zobaczyc ciemna nawigacje na gorze i ostylowana tresc.

Jesli widzisz blad "TemplateDoesNotExist: base.html" - sprawdz czy w `settings.py` masz:
```python
TEMPLATES = [{'DIRS': [BASE_DIR / 'templates'], ...}]
```
(To juz powinno byc skonfigurowane w szkielecie)

---

## Czesc 4: Formularze HTML (45 min)

### Teoria: HTTP GET vs POST

Do tej pory uzywalismy tylko **GET** - przegladarka prosi o strone, serwer ja zwraca:

```
Przegladarka  --GET /menu/-->  Django  --HTML-->  Przegladarka
              "daj mi liste pizz"     "oto lista"
```

Ale co jesli uzytkownik chce **wyslac dane** do serwera (np. dodac nowa pizze)? Do tego sluzy **POST**:

```
Przegladarka  --POST /menu/dodaj/-->  Django  --redirect-->  Przegladarka
              "oto dane nowej pizzy"   "OK, dodano"          --GET /menu/-->
```

**Roznice:**
| | GET | POST |
|---|---|---|
| **Cel** | Pobranie danych | Wyslanie danych |
| **Dane** | W URL (np. `?q=pizza`) | W body requestu (niewidoczne) |
| **Bezpieczenstwo** | Dane widoczne w URL | Dane ukryte |
| **Uzycie** | Wyswietlanie stron | Formularze, logowanie, zamowienia |

### Teoria: Formularz HTML

Formularz HTML to sposob na zebranie danych od uzytkownika:

```html
<form method="post" action="/menu/dodaj/">
    <input type="text" name="pizza_name">
    <input type="number" name="price">
    <button type="submit">Wyslij</button>
</form>
```

Gdy uzytkownik kliknie "Wyslij":
1. Przegladarka zbiera dane ze wszystkich pol (`name="pizza_name"`, `name="price"`)
2. Wysyla je jako POST na adres z `action` (lub na biezacy URL jesli brak `action`)
3. Django odbiera dane w `request.POST`:

```python
def pizza_add(request):
    if request.method == 'POST':
        name = request.POST.get('pizza_name')     # wartosc z inputa name="pizza_name"
        price = request.POST.get('price')          # wartosc z inputa name="price"
```

### Teoria: CSRF - ochrona formularzy

**CSRF** (Cross-Site Request Forgery) to atak gdzie zlosliwa strona wysyla formularz w Twoim imieniu. Django wymaga tokena CSRF w kazdym formularzu POST:

```html
<form method="post">
    {% csrf_token %}          <!-- WYMAGANE! Django odrzuci formularz bez tego -->
    <input type="text" name="name">
    <button type="submit">Wyslij</button>
</form>
```

`{% csrf_token %}` generuje ukryty input z unikalnym tokenem. Django sprawdza ten token przy kazdym POST - jezeli go nie ma lub jest nieprawidlowy, zwraca blad 403 Forbidden.

**Zasada:** Kazdy `<form method="post">` w Django MUSI miec `{% csrf_token %}`.

### Teoria: Wzorzec POST-Redirect-GET

Co sie stanie jesli po wyslaniu formularza uzytkownik kliknie F5 (odswiez strone)? Przegladarka wyslalaby formularz **ponownie** - np. dodajac pizze drugi raz!

Rozwiazanie: **POST-Redirect-GET** (PRG):

```
1. Uzytkownik wysyla formularz      -> POST /menu/dodaj/
2. Serwer przetwarza dane           -> dodaje pizze do JSON
3. Serwer zwraca REDIRECT           -> redirect('/menu/')
4. Przegladarka robi GET /menu/     -> wyswietla liste (z nowa pizza)
5. Uzytkownik klika F5              -> GET /menu/ (bezpieczne!)
```

W Django:
```python
from django.shortcuts import redirect

def pizza_add(request):
    if request.method == 'POST':
        # ... przetworzenie danych ...
        return redirect('pizza_list')     # <- przekierowanie po sukcesie
    return render(request, 'pizza_form.html')   # <- GET: pokaz formularz
```

### Wzorzec view z formularzem

Kazdy view obslugujacy formularz ma **ta sama strukture**:

```python
def my_form_view(request):
    if request.method == 'POST':
        # 1. Odczytaj dane z formularza
        name = request.POST.get('name', '').strip()

        # 2. Waliduj dane
        errors = []
        if not name:
            errors.append("Pole jest wymagane.")

        # 3. Jesli OK - przetworz i przekieruj
        if not errors:
            try:
                # ... zapis do pliku, bazy, itp ...
                return redirect('success_page')
            except SomeError as e:
                errors.append(str(e))

        # 4. Jesli bledy - pokaz formularz ponownie z bledami
        return render(request, 'form.html', {
            'errors': errors,
            'name': name,         # zachowaj wpisane dane
        })

    # GET: pokaz pusty formularz
    return render(request, 'form.html')
```

Ten wzorzec powtarza sie w **kazdym** formularzu. Zapamietaj go - uzyjesz go wielokrotnie dzisiaj.

### Demonstracja: Formularz kontaktowy (GENERIC)

```python
# views.py
from django.shortcuts import render, redirect

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Przetwarzanie...
        return redirect('contact_success')
    return render(request, 'contact_form.html')
```

```html
<!-- contact_form.html -->
<form method="post">
    {% csrf_token %}
    <input type="text" name="name" required>
    <input type="email" name="email" required>
    <textarea name="message" required></textarea>
    <button type="submit">Wyslij</button>
</form>
```

### Cwiczenie 3: Formularz dodawania pizzy

**Cel:** stworz strone /menu/dodaj/ z formularzem do dodawania nowej pizzy do menu.

**Krok 1:** Stworz template `menu_app/templates/menu_app/pizza_form.html`:

```html
{% extends "base.html" %}

{% block title %}Dodaj pizze{% endblock %}

{% block content %}
<h1>Dodaj nowa pizze</h1>

{% if errors %}
<div style="color: red;">
    {% for error in errors %}
    <p>{{ error }}</p>
    {% endfor %}
</div>
{% endif %}

<form method="post">
    {% csrf_token %}
    <div>
        <label>Nazwa:</label>
        <input type="text" name="name" value="{{ name }}" required>
    </div>
    <div>
        <label>Cena (zl):</label>
        <input type="number" name="price" step="0.01" value="{{ price }}" required>
    </div>
    <button type="submit">Dodaj</button>
</form>

<a href="/menu/">Powrot do menu</a>
{% endblock %}
```

Zwroc uwage:
- `{% csrf_token %}` - **WYMAGANE** w kazdym formularzu POST w Django
- `method="post"` - dane ida w body requestu, nie w URL
- `value="{{ name }}"` - zachowuje wpisana wartosc gdy formularz sie nie powiedzie (zeby uzytkownik nie musial wpisywac od nowa)

**Krok 2:** Dodaj view w `menu_app/views.py`:

```python
from django.shortcuts import redirect
from rozwiazanie_weekend2.pizza import Pizza, Menu
from rozwiazanie_weekend2.exceptions import InvalidPriceError, DuplicatePizzaError

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
                pizza = Pizza(name, price)
                menu = Menu()
                menu.load_from_file(MENU_FILE)
                menu.add_pizza(pizza)
                menu.save_to_file(MENU_FILE)
                return redirect('pizza_list')
            except (ValueError, TypeError) as e:
                errors.append(str(e))
            except InvalidPriceError as e:
                errors.append(str(e))
            except DuplicatePizzaError as e:
                errors.append(str(e))

        return render(request, 'menu_app/pizza_form.html', {
            'errors': errors,
            'name': name,
            'price': price_str,
        })

    return render(request, 'menu_app/pizza_form.html')
```

Przejdz przez ten kod i rozpoznaj wzorzec z teorii:
- `if request.method == 'POST'` - formularz zostal wyslany -> przetwarzaj dane
- `else` (GET) - uzytkownik dopiero wchodzi na strone -> pokaz pusty formularz
- `redirect('pizza_list')` - PRG: po sukcesie przekieruj na liste
- `except` - przy bledzie pokaz formularz ponownie z komunikatem bledu
- Walidacja `if not name` - sprawdzenie PRZED proba zapisu

Zwroc uwage na obsluge **wyjatkow z Weekend 2**: `InvalidPriceError` (cena <= 0), `DuplicatePizzaError` (pizza juz istnieje). Zamiast crashowac serwer, lapiesz wyjatek i wyswietlasz czytelny komunikat.

**Krok 3:** Dodaj URL w `menu_app/urls.py`:

```python
path('dodaj/', views.pizza_add, name='pizza_add'),
```

**WAZNE:** `dodaj/` musi byc PRZED `<str:name>/` w liscie URL, bo inaczej Django potraktuje "dodaj" jako nazwe pizzy!

```python
# menu_app/urls.py - poprawna kolejnosc
urlpatterns = [
    path('', views.pizza_list, name='pizza_list'),
    path('dodaj/', views.pizza_add, name='pizza_add'),        # PRZED <str:name>
    path('<str:name>/', views.pizza_detail, name='pizza_detail'),
]
```

**Krok 4:** Dodaj link w `pizza_list.html`:

```html
<a href="/menu/dodaj/">Dodaj nowa pizze</a>
```

**Krok 5:** Sprawdz! Wejdz na /menu/dodaj/, wypelnij formularz, kliknij "Dodaj". Nowa pizza powinna pojawic sie na liscie.

**Bonus - przetestuj obsluge bledow:**
- Wyslij pusty formularz -> "Nazwa pizzy jest wymagana."
- Wpisz cene -5 -> blad z `InvalidPriceError`
- Wpisz nazwe pizzy ktora juz istnieje (np. "Margherita") -> blad z `DuplicatePizzaError`

---

## Czesc 5: Customer Views (40 min)

### Teoria: Budowanie kolejnego appa

Teraz powtorz caly proces tworzenia appa, ktory poznales wczoraj dla `menu_app`:

1. `python manage.py startapp <nazwa>` - stworz app
2. Dodaj do `INSTALLED_APPS` w settings.py - zarejestruj go
3. Dodaj `include()` w glownym urls.py - podlacz routing
4. Napisz views.py - logika
5. Stworz urls.py w appie - mapowanie URL -> view
6. Stworz templates - szablony HTML

Ten wzorzec powtarza sie przy kazdym nowym appie. Do konca dnia zrobisz go jeszcze dwa razy - za kazdym razem powinno isc szybciej.

### Cwiczenie 4: Pelne customers_app

**Cel:** zbuduj nowy app do zarzadzania klientami - lista klientow + formularz dodawania (z wyborem typu regular/VIP).

**Krok 1:** Stworz nowy app:

```bash
python3 manage.py startapp customers_app
```

**WAZNE - 2 kroki konfiguracji (tak samo jak dla menu_app):**

**A)** Dodaj `'customers_app'` do `INSTALLED_APPS` w `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'menu_app',
    'customers_app',    # <- DODAJ
]
```

**B)** Dodaj routing w glownym `pizzeria_project/urls.py`:

```python
urlpatterns = [
    path('menu/', include('menu_app.urls')),
    path('klienci/', include('customers_app.urls')),    # <- DODAJ
]
```

**Krok 2:** Stworz `customers_app/views.py`:

```python
import os
from django.shortcuts import render, redirect
from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.customer import Customer, VIPCustomer, CustomerManager

CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers.json')

def customer_list(request):
    manager = CustomerManager()
    manager.load_from_file(CUSTOMERS_FILE)
    return render(request, 'customers_app/customer_list.html', {
        'customers': list(manager),
    })

def customer_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        customer_type = request.POST.get('type', 'regular')

        errors = []
        if not name:
            errors.append("Imie klienta jest wymagane.")
        if not phone:
            errors.append("Numer telefonu jest wymagany.")

        if not errors:
            manager = CustomerManager()
            manager.load_from_file(CUSTOMERS_FILE)

            if customer_type == 'vip':
                discount = float(request.POST.get('discount', 10))
                customer = VIPCustomer(name, phone, discount)
            else:
                customer = Customer(name, phone)

            manager.add_customer(customer)
            manager.save_to_file(CUSTOMERS_FILE)
            return redirect('customer_list')

        return render(request, 'customers_app/customer_form.html', {
            'errors': errors,
            'name': name,
            'phone': phone,
        })

    return render(request, 'customers_app/customer_form.html')
```

Zwroc uwage na nowy element: **wybor typu klienta**. Formularz wysyla `type` ('regular' lub 'vip') i na tej podstawie tworzymy `Customer` lub `VIPCustomer` z Weekend 1. Dziedziczenie, ktore pisalismy na Weekend 1, teraz dziala w aplikacji webowej!

**Krok 3:** Stworz `customers_app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('dodaj/', views.customer_add, name='customer_add'),
]
```

Routing glowny (`pizzeria_project/urls.py`) juz podpielismy w Kroku 1B.

**Krok 4:** Stworz katalog na templates i plik `customers_app/templates/customers_app/customer_list.html`:

```bash
mkdir -p customers_app/templates/customers_app
```

```html
{% extends "base.html" %}

{% block title %}Klienci{% endblock %}

{% block content %}
<h1>Lista klientow</h1>
<a href="/klienci/dodaj/">Dodaj klienta</a>

<table>
    <tr><th>ID</th><th>Imie</th><th>Telefon</th><th>Typ</th></tr>
    {% for customer in customers %}
    <tr>
        <td>{{ customer.id }}</td>
        <td>{{ customer.name }}</td>
        <td>{{ customer.phone }}</td>
        <td>{% if customer.discount_percent is not None %}VIP ({{ customer.discount_percent }}%){% else %}Zwykly{% endif %}</td>
    </tr>
    {% empty %}
    <tr><td colspan="4">Brak klientow</td></tr>
    {% endfor %}
</table>
{% endblock %}
```

Uwaga: `customer.discount_percent` istnieje tylko na `VIPCustomer` - dla zwyklego klienta bedzie `None`.

**Krok 5:** Stworz template `customers_app/templates/customers_app/customer_form.html`:

```html
{% extends "base.html" %}

{% block title %}Dodaj klienta{% endblock %}

{% block content %}
<h1>Dodaj klienta</h1>

{% if errors %}
<div style="color: red;">
    {% for error in errors %}
    <p>{{ error }}</p>
    {% endfor %}
</div>
{% endif %}

<form method="post">
    {% csrf_token %}
    <div>
        <label>Imie:</label>
        <input type="text" name="name" value="{{ name }}" required>
    </div>
    <div>
        <label>Telefon:</label>
        <input type="text" name="phone" value="{{ phone }}" required>
    </div>
    <div>
        <label>Typ:</label>
        <select name="type">
            <option value="regular">Zwykly klient</option>
            <option value="vip">VIP</option>
        </select>
    </div>
    <div>
        <label>Rabat VIP (%):</label>
        <input type="number" name="discount" value="10" min="1" max="50">
        <small>(tylko dla VIP)</small>
    </div>
    <button type="submit">Dodaj</button>
</form>

<a href="/klienci/">Powrot do listy</a>
{% endblock %}
```

Nowy element HTML: **`<select>`** - lista rozwijana. `<option value="vip">VIP</option>` oznacza: wyswietl tekst "VIP", a wysylaj wartosc `"vip"` w `request.POST.get('type')`.

**Krok 6:** Sprawdz! Wejdz na /klienci/ - zobaczysz istniejacych klientow z pliku JSON. Dodaj nowego przez formularz.

---

## Czesc 6: Order Views (50 min)

### Teoria: Zamowienia - zlozonosc rosnie

Zamowienia to najzlozniejsza czesc aplikacji, bo lacza dane z **dwoch zrodel**:
- Menu (pizze) - `rozwiazanie_weekend2/data/menu.json`
- Klienci - `rozwiazanie_weekend2/data/customers.json`

Dodatkowo zamowienia musimy zapisywac recznie w JSON, bo nasz engine z Weekend 2 nie mial `OrderManager.save_to_file()`. To dobry przyklad jak laczyc istniejacy kod z nowym.

**Struktura zamowienia w JSON:**
```json
{
    "id": 1,
    "customer_id": 2,
    "items": [
        {"pizza_name": "Margherita", "pizza_price": 25.0, "quantity": 2}
    ],
    "discount_percent": 15
}
```

`discount_percent` jest `null` dla zwyklych klientow, a dla VIP przechowuje rabat.

### Cwiczenie 5: Order list + detail views

**Cel:** zbuduj app do wyswietlania zamowien.

**Krok 1:** Stworz nowy app:

```bash
python3 manage.py startapp orders_app
```

**WAZNE - 2 kroki konfiguracji (tak samo jak poprzednio):**

**A)** Dodaj `'orders_app'` do `INSTALLED_APPS` w `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'menu_app',
    'customers_app',
    'orders_app',    # <- DODAJ
]
```

**B)** Dodaj routing w glownym `pizzeria_project/urls.py`:

```python
urlpatterns = [
    path('menu/', include('menu_app.urls')),
    path('klienci/', include('customers_app.urls')),
    path('zamowienia/', include('orders_app.urls')),    # <- DODAJ
]
```

**Krok 2:** Stworz `orders_app/views.py` - zacznij od helperow do odczytu/zapisu zamowien:

```python
import os
import json
from django.shortcuts import render, redirect
from django.http import Http404
from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.pizza import Menu
from rozwiazanie_weekend2.customer import CustomerManager
from rozwiazanie_weekend2.exceptions import CustomerNotFoundError, PizzaNotFoundError

MENU_FILE = os.path.join(DATA_DIR, 'menu.json')
CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

def _load_orders():
    """Wczytuje zamowienia z pliku JSON."""
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_orders(orders_data):
    """Zapisuje zamowienia do pliku JSON."""
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders_data, f, indent=2, ensure_ascii=False)
```

Funkcje `_load_orders()` i `_save_orders()` to **helpery** (prywatne funkcje, przedrostek `_`) uzywane przez inne views. Uzywamy surowego `json.load/dump` bo nasz engine nie mial zapisu zamowien do plikow.

**Krok 3:** Dodaj view listy zamowien:

```python
def order_list(request):
    orders_data = _load_orders()
    customer_mgr = CustomerManager()
    customer_mgr.load_from_file(CUSTOMERS_FILE)

    orders_display = []
    for order_data in orders_data:
        # Znajdz nazwe klienta
        customer_name = f"Klient #{order_data['customer_id']}"
        try:
            customer = customer_mgr.find_customer(order_data['customer_id'])
            customer_name = customer.name
        except CustomerNotFoundError:
            pass

        # Oblicz sume
        total = sum(item['pizza_price'] * item['quantity'] for item in order_data['items'])
        if order_data.get('discount_percent'):
            total = total * (1 - order_data['discount_percent'] / 100)

        orders_display.append({
            'id': order_data['id'],
            'customer_name': customer_name,
            'items_count': len(order_data['items']),
            'total': round(total, 2),
            'is_vip': order_data.get('discount_percent') is not None,
        })

    return render(request, 'orders_app/order_list.html', {'orders': orders_display})
```

Zwroc uwage: view przygotowuje dane **specjalnie pod template** (`orders_display`). Zamiast przekazywac surowe dane JSON, tworzy slowniki z gotowymi wartosciami do wyswietlenia (nazwa klienta zamiast ID, obliczona suma). To dobra praktyka - template powinien byc prosty, logika w views.

**Krok 4:** Dodaj view szczegulow zamowienia:

```python
def order_detail(request, order_id):
    orders_data = _load_orders()
    customer_mgr = CustomerManager()
    customer_mgr.load_from_file(CUSTOMERS_FILE)

    # Znajdz zamowienie
    order_data = None
    for o in orders_data:
        if o['id'] == order_id:
            order_data = o
            break

    if order_data is None:
        raise Http404(f"Zamowienie #{order_id} nie znalezione")

    # Nazwa klienta
    customer_name = f"Klient #{order_data['customer_id']}"
    try:
        customer = customer_mgr.find_customer(order_data['customer_id'])
        customer_name = customer.name
    except CustomerNotFoundError:
        pass

    # Pozycje i sumy
    items = []
    subtotal = 0
    for item in order_data['items']:
        item_total = item['pizza_price'] * item['quantity']
        subtotal += item_total
        items.append({
            'pizza_name': item['pizza_name'],
            'pizza_price': item['pizza_price'],
            'quantity': item['quantity'],
            'total': item_total,
        })

    discount_percent = order_data.get('discount_percent')
    discount_amount = 0
    total = subtotal
    if discount_percent:
        discount_amount = round(subtotal * discount_percent / 100, 2)
        total = round(subtotal - discount_amount, 2)

    return render(request, 'orders_app/order_detail.html', {
        'order_id': order_data['id'],
        'customer_name': customer_name,
        'items': items,
        'subtotal': subtotal,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'total': total,
    })
```

Tu znowu widzisz `raise Http404(...)` z Czesci 2 - ten sam wzorzec: szukamy zasobu, jesli go nie ma -> 404.

**Krok 5:** Stworz `orders_app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
```

`<int:order_id>` - parametr URL jako liczba calkowita (pamietasz teorie z Czesci 2?).

**Krok 6:** Stworz katalog i templates:

```bash
mkdir -p orders_app/templates/orders_app
```

Stworz `orders_app/templates/orders_app/order_list.html`:

```html
{% extends "base.html" %}

{% block title %}Zamowienia{% endblock %}

{% block content %}
<h1>Zamowienia</h1>

{% if orders %}
<table>
    <tr><th>#</th><th>Klient</th><th>Pozycje</th><th>Suma</th></tr>
    {% for order in orders %}
    <tr>
        <td><a href="/zamowienia/{{ order.id }}/">#{{ order.id }}</a></td>
        <td>{{ order.customer_name }} {% if order.is_vip %}(VIP){% endif %}</td>
        <td>{{ order.items_count }}</td>
        <td>{{ order.total }} zl</td>
    </tr>
    {% endfor %}
</table>
{% else %}
<p>Brak zamowien. <a href="/zamowienia/nowe/">Zloz pierwsze zamowienie</a></p>
{% endif %}
{% endblock %}
```

Stworz `orders_app/templates/orders_app/order_detail.html`:

```html
{% extends "base.html" %}

{% block title %}Zamowienie #{{ order_id }}{% endblock %}

{% block content %}
<h1>Zamowienie #{{ order_id }}</h1>
<p>Klient: {{ customer_name }}</p>

<table>
    <tr><th>Pizza</th><th>Cena</th><th>Ilosc</th><th>Razem</th></tr>
    {% for item in items %}
    <tr>
        <td>{{ item.pizza_name }}</td>
        <td>{{ item.pizza_price }} zl</td>
        <td>{{ item.quantity }}</td>
        <td>{{ item.total }} zl</td>
    </tr>
    {% endfor %}
</table>

<p>Suma: {{ subtotal }} zl</p>
{% if discount_percent %}
<p>Rabat VIP ({{ discount_percent }}%): -{{ discount_amount }} zl</p>
{% endif %}
<p><strong>Do zaplaty: {{ total }} zl</strong></p>

<a href="/zamowienia/">Powrot do listy</a>
{% endblock %}
```

**Krok 7:** Na razie lista zamowien bedzie pusta (nie mamy jeszcze formularza tworzenia). To OK - formularz dodamy w nastepnym cwiczeniu.

---

## Czesc 7: Formularz zamowienia (40 min)

### Teoria: Formularz z danymi z wielu zrodel

Formularz zamowienia jest bardziej zlozony niz poprzednie formularze, bo zamiast wolnego pola tekstowego (jak nazwa pizzy) mamy **listy wyboru** (select):

- Wybierz klienta -> z listy klientow z JSON
- Wybierz pizze -> z menu z JSON

To oznacza ze view musi **zaladowac dane** (liste klientow, liste pizz) ZANIM wyrenderuje formularz - zeby wypelnic `<select>`:

```python
def order_create(request):
    # Zaladuj dane do wypelnienia select-ow
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    customer_mgr = CustomerManager()
    customer_mgr.load_from_file(CUSTOMERS_FILE)

    # Przekaz dane do template (zarowno dla GET jak i POST z bledami)
    return render(request, 'order_form.html', {
        'pizzas': list(menu),
        'customers': list(customer_mgr),
    })
```

**Element HTML `<select>`** generuje liste rozwijana:
```html
<select name="customer_id">
    {% for customer in customers %}
    <option value="{{ customer.id }}">{{ customer.name }}</option>
    {% endfor %}
</select>
```

Kazdy `<option>` ma:
- `value` - wartosc wysylana w POST (np. ID klienta)
- Tekst miedzy tagami - to co widzi uzytkownik (np. imie klienta)

### Cwiczenie 6: Order creation form

**Cel:** stworz formularz na /zamowienia/nowe/ gdzie mozna wybrac klienta, pizze i ilosc.

**Krok 1:** Dodaj view `order_create` w `orders_app/views.py`:

```python
def order_create(request):
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    customer_mgr = CustomerManager()
    customer_mgr.load_from_file(CUSTOMERS_FILE)

    if request.method == 'POST':
        customer_id_str = request.POST.get('customer_id', '')
        pizza_name = request.POST.get('pizza_name', '')
        quantity_str = request.POST.get('quantity', '1')

        errors = []
        if not customer_id_str:
            errors.append("Wybierz klienta.")
        if not pizza_name:
            errors.append("Wybierz pizze.")

        if not errors:
            try:
                customer_id = int(customer_id_str)
                customer = customer_mgr.find_customer(customer_id)
                pizza = menu.find_pizza(pizza_name)
                quantity = int(quantity_str)

                # Oblicz rabat VIP
                discount_percent = None
                if hasattr(customer, 'discount_percent'):
                    discount_percent = customer.discount_percent

                # Zapisz zamowienie
                orders_data = _load_orders()
                next_id = max((o['id'] for o in orders_data), default=0) + 1
                new_order = {
                    'id': next_id,
                    'customer_id': customer.id,
                    'items': [{
                        'pizza_name': pizza.name,
                        'pizza_price': pizza.price,
                        'quantity': quantity,
                    }],
                    'discount_percent': discount_percent,
                }
                orders_data.append(new_order)
                _save_orders(orders_data)

                return redirect('order_detail', order_id=next_id)
            except CustomerNotFoundError:
                errors.append("Wybrany klient nie istnieje.")
            except PizzaNotFoundError:
                errors.append("Wybrana pizza nie istnieje.")
            except ValueError:
                errors.append("Nieprawidlowe dane.")

        return render(request, 'orders_app/order_form.html', {
            'errors': errors,
            'pizzas': list(menu),
            'customers': list(customer_mgr),
        })

    return render(request, 'orders_app/order_form.html', {
        'pizzas': list(menu),
        'customers': list(customer_mgr),
    })
```

Zwroc uwage na:
- `hasattr(customer, 'discount_percent')` - sprawdzamy czy klient to VIP (ma atrybut z Weekend 1)
- `redirect('order_detail', order_id=next_id)` - `redirect()` moze przyjac **argumenty URL** (tu `order_id`) zeby przekierowac na strone szczegulow nowego zamowienia
- View **laduje dane na poczatku** (przed `if POST`) bo potrzebuje ich zarowno do wyswietlenia formularza (GET) jak i do przetworzenia (POST)

**Krok 2:** Dodaj URL w `orders_app/urls.py`:

```python
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('nowe/', views.order_create, name='order_create'),        # PRZED <int:order_id>
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
```

**Krok 3:** Stworz template `orders_app/templates/orders_app/order_form.html`:

```html
{% extends "base.html" %}

{% block title %}Nowe zamowienie{% endblock %}

{% block content %}
<h1>Zloz zamowienie</h1>

{% if errors %}
<div style="color: red;">
    {% for error in errors %}
    <p>{{ error }}</p>
    {% endfor %}
</div>
{% endif %}

<form method="post">
    {% csrf_token %}
    <div>
        <label>Klient:</label>
        <select name="customer_id" required>
            <option value="">-- Wybierz klienta --</option>
            {% for customer in customers %}
            <option value="{{ customer.id }}">{{ customer.name }}</option>
            {% endfor %}
        </select>
    </div>
    <div>
        <label>Pizza:</label>
        <select name="pizza_name" required>
            <option value="">-- Wybierz pizze --</option>
            {% for pizza in pizzas %}
            <option value="{{ pizza.name }}">{{ pizza.name }} ({{ pizza.price }} zl)</option>
            {% endfor %}
        </select>
    </div>
    <div>
        <label>Ilosc:</label>
        <input type="number" name="quantity" min="1" value="1" required>
    </div>
    <button type="submit">Zloz zamowienie</button>
</form>

<a href="/zamowienia/">Powrot do listy</a>
{% endblock %}
```

**Krok 4:** Sprawdz! Wejdz na /zamowienia/nowe/, wybierz klienta i pizze, zloz zamowienie. Po zlozeniu powinienes zobaczyc szczegoly zamowienia z suma. Jezeli wybrales klienta VIP - powinien byc naliczony rabat.

---

## Czesc 8: Django Messages (15 min)

### Teoria: Komunikaty dla uzytkownika

Po dodaniu pizzy czy zlozeniu zamowienia uzytkownik jest przekierowywany na liste. Ale skad wie, ze operacja sie powiodla? Jedyne co widzi to lista - moze nie zauwazy zmian.

Django ma wbudowany **messages framework** - mechanizm do wyswietlania jednorazowych komunikatow:

```python
from django.contrib import messages

def pizza_add(request):
    if request.method == 'POST':
        # ... obsluga formularza ...
        messages.success(request, f"Dodano pizze: {name}")     # <- komunikat
        return redirect('pizza_list')
```

Komunikat jest zapisywany w sesji (cookie) i wyswietlany **dokladnie raz** - po odswieszeniu strony znika.

Typy komunikatow:
- `messages.success(request, "...")` - sukces (zielony)
- `messages.error(request, "...")` - blad (czerwony)
- `messages.warning(request, "...")` - ostrzezenie (zolty)
- `messages.info(request, "...")` - informacja (niebieski)

Wyswietlanie w template (juz jest w naszym `base.html`!):

```html
{% if messages %}
{% for message in messages %}
<div class="alert alert-{{ message.tags }}">{{ message }}</div>
{% endfor %}
{% endif %}
```

`message.tags` to klasa CSS odpowiadajaca typowi komunikatu (`success`, `error`, itp.). Bootstrap stylizuje je automatycznie.

### Cwiczenie 7: Dodaj messages do swoich views

**Zadanie:** Dodaj komunikaty sukcesu do:
- `pizza_add` - po dodaniu pizzy
- `customer_add` - po dodaniu klienta
- `order_create` - po zlozeniu zamowienia

Przyklad dla `pizza_add`:

```python
from django.contrib import messages

def pizza_add(request):
    if request.method == 'POST':
        # ... cala obsluga formularza ...
        if not errors:
            try:
                # ... zapis ...
                messages.success(request, f"Dodano pizze: {name}")   # <- DODAJ
                return redirect('pizza_list')
            except ...
```

Sprawdz - po dodaniu pizzy powinienes zobaczyc zielony komunikat na gorze strony.

---

## Czesc 9: Pelna integracja (25 min)

### Cwiczenie 8: Przetestuj caly flow

Pora przetestowac cala aplikacje end-to-end. Przejdz przez ten scenariusz:

1. **Menu:** Przegladaj menu (/menu/) - kliknij na pizze, zobacz szczegoly
2. **Dodaj pizze:** Wejdz na /menu/dodaj/, dodaj "Diavola" za 34 zl
3. **Dodaj klienta:** Wejdz na /klienci/dodaj/, dodaj klienta VIP z rabatem 20%
4. **Zloz zamowienie:** Wejdz na /zamowienia/nowe/, wybierz nowego klienta VIP i pizze
5. **Sprawdz rabat:** Zobacz szczegoly zamowienia - rabat VIP powinien sie naliczac
6. **Przetestuj bledy:**
   - Sprobuj dodac pizze z ujemna cena
   - Sprobuj dodac pizze ktora juz istnieje
   - Wejdz na /menu/NieIstniejaca/ - powinien byc 404

Jezeli wszystko dziala - gratulacje! Masz pelna aplikacje webowa zbudowana na Django, ktora uzywa kodu z Weekend 1 i 2 jako backend.

---

## Czesc 10: Podsumowanie weekendu (10 min)

### Progresja kursu

```
Weekend 1: proceduralne -> OOP (klasy, dziedziczenie)
Weekend 2: wyjatki -> I/O (JSON) -> testy (pytest)
Weekend 3: Git -> Django (views, templates, forms)
Weekend 4: REST API -> wiecej Django
```

### Co zrobilismy dzisiaj

- **Detail views** z parametrami URL (`<str:name>`, `<int:id>`)
- **Dziedziczenie szablonow** (`extends`, `block`) + Bootstrap
- **Formularze HTML** z obsluga POST + CSRF + walidacja
- **Wzorzec POST-Redirect-GET** - bezpieczne formularze
- **Error handling** - polaczenie wyjatkow z Weekend 2 z Django views
- **Messages framework** - komunikaty uzytkownikowi
- **Pelna aplikacja webowa** bez bazy danych!

### Kluczowe wzorce do zapamietania

1. **Nowy app:** `startapp` -> `INSTALLED_APPS` -> `include()` w urls.py
2. **View z formularzem:** `if POST` -> walidacja -> zapis -> redirect | `else` -> pusty formularz
3. **Parametr URL:** `<typ:nazwa>` w urls.py -> argument w view
4. **Http404:** `raise Http404(...)` gdy zasob nie istnieje
5. **CSRF:** `{% csrf_token %}` w kazdym `<form method="post">`

### Co dalej (Weekend 4)

- REST API z Django REST Framework
- JSON responses zamiast HTML
- Testowanie API
- Deployment

---

## Zadanie domowe (opcjonalne)

Ponizsze zadania mozesz zrobic samodzielnie po zajeciach. Nie ma prowadzenia krok po kroku - musisz sam/sama znalezc rozwiazanie. Uzyj wiedzy z dzisiejszego dnia.

Kazde zadanie wymaga tego samego wzorca co na zajeciach: **view + template + URL**. Pamietaj o `{% csrf_token %}` w formularzach POST i o wzorcu POST-Redirect-GET.

**Podpowiedz:** Zajrzyj do plikow `rozwiazanie_weekend2/pizza.py`, `customer.py`, `order.py` - znajdziesz tam metody, ktore nie byly uzywane na zajeciach. Warto je przeczytac.

---

### Zadanie 1: Usuwanie pizzy z menu

**Cel:** Na stronie `/menu/` obok kazdej pizzy powinien byc przycisk "Usun". Po kliknieciu pizza znika z menu.

**Wymagania:**
- Usuwanie musi byc operacja POST (nie GET!) - bo zmienia dane na serwerze
- Po usunieciu przekieruj na `/menu/` z komunikatem `messages.warning()`
- Obsluz `PizzaNotFoundError` gdyby pizza juz nie istniala

**Z czego skorzystac w engine:**
- `menu.remove_pizza(name)` - metoda Menu, ktora usuwa pizze po nazwie

**Wskazowka do implementacji:** Mozesz dodac maly formularz obok kazdej pizzy w `pizza_list.html`:
```html
<form method="post" action="/menu/usun/" style="display:inline;">
    {% csrf_token %}
    <input type="hidden" name="name" value="{{ pizza.name }}">
    <button type="submit">Usun</button>
</form>
```

Potrzebujesz: nowy view `pizza_delete` + URL `path('usun/', ...)`.

---

### Zadanie 2: Sortowanie i statystyki menu

**Cel:** Na stronie `/menu/` dodaj:
- Linki do sortowania: "Po nazwie", "Po cenie (rosnaco)", "Po cenie (malejaco)"
- Statystyki na dole strony: najtansza pizza, najdrozsza pizza, srednia cena

**Wymagania:**
- Sortowanie przez **URL query parameters**: `/menu/?sort=price_asc`
- Statystyki widoczne pod lista pizz

**Z czego skorzystac w engine:**
- `menu.get_cheapest()` - zwraca najtansza pizze
- `menu.get_most_expensive()` - zwraca najdrozsza pizze
- `menu.get_average_price()` - zwraca srednia cene

**Nowa koncepcja - query parameters:**

Query parameters to dane po `?` w URL. W Django odczytujesz je inaczej niz parametry URL:
```python
# URL: /menu/?sort=price_asc
sort_by = request.GET.get('sort', 'name')    # domyslnie sortuj po nazwie
```

`request.GET` (nie `request.POST`!) to slownik z parametrami z URL. Uzyj go w view `pizza_list` do sortowania listy przed przekazaniem do template.

Linki w template:
```html
<a href="/menu/?sort=name">Po nazwie</a>
<a href="/menu/?sort=price_asc">Cena (rosnaco)</a>
<a href="/menu/?sort=price_desc">Cena (malejaco)</a>
```

---

### Zadanie 3: Strona klienta z punktami lojalnosciowymi

**Cel:** Po kliknieciu na imie klienta w `/klienci/` otwiera sie strona `/klienci/<int:customer_id>/` z szczegolami. Dla klientow VIP widoczne sa punkty lojalnosciowe i formularz do ich dodawania.

**Wymagania:**
- Nowy detail view: `customer_detail(request, customer_id)`
- Template wyswietla: imie, telefon, typ (zwykly/VIP)
- Dla VIP: dodatkowa sekcja z `loyalty_points` i formularzem POST do dodawania punktow
- Linki w `customer_list.html` kierujace na strone klienta

**Z czego skorzystac w engine:**
- `customer_mgr.find_customer(customer_id)` - znajdz klienta po ID
- `VIPCustomer.loyalty_points` - aktualna liczba punktow
- `VIPCustomer.add_loyalty_points(points)` - dodaj punkty

**Wskazowka:** Sprawdz czy klient jest VIP w template:
```html
{% if customer.discount_percent is not None %}
    <p>Punkty lojalnosciowe: {{ customer.loyalty_points }}</p>
    <!-- formularz dodawania punktow -->
{% endif %}
```

Po dodaniu punktow musisz zapisac zmienionego klienta do pliku (`customer_mgr.save_to_file()`).

---

### Zadanie 4: Anulowanie zamowienia

**Cel:** Na stronie szczegulow zamowienia (`/zamowienia/<id>/`) dodaj przycisk "Anuluj zamowienie". Po kliknieciu zamowienie znika z listy.

**Wymagania:**
- Anulowanie to operacja POST (zmienia dane!)
- Po anulowaniu przekieruj na `/zamowienia/` z komunikatem `messages.warning()`
- Obsluz sytuacje gdy zamowienie nie istnieje (404)

**Z czego skorzystac:**
- W tym cwiczeniu nie uzyjesz `OrderManager` z engine (bo zamowienia przechowujesz w surowym JSON)
- Musisz samodzielnie: zaladowac `orders.json`, usunac zamowienie o danym ID, zapisac z powrotem

**Wskazowka:** Uzyj list comprehension do filtrowania:
```python
orders_data = [o for o in orders_data if o['id'] != order_id]
```

---

### Checklista po zadaniach domowych

Jesli zrobiles wszystkie 4 zadania, Twoja aplikacja powinna miec te URL-e:

| URL | Opis |
|-----|------|
| `/menu/` | Lista pizz z sortowaniem i statystykami |
| `/menu/<str:name>/` | Szczegoly pizzy |
| `/menu/dodaj/` | Formularz dodawania |
| `/menu/usun/` | Usuwanie pizzy (POST) |
| `/klienci/` | Lista klientow z linkami |
| `/klienci/<int:customer_id>/` | Szczegoly klienta + punkty VIP |
| `/klienci/dodaj/` | Formularz dodawania |
| `/zamowienia/` | Lista zamowien |
| `/zamowienia/<int:order_id>/` | Szczegoly + przycisk anulowania |
| `/zamowienia/nowe/` | Formularz zamowienia |

---

## Materialy dodatkowe

### Struktura finalna projektu

```
pizzeria_django/
├── manage.py
├── pizzeria_project/              # Konfiguracja
│   ├── settings.py
│   ├── urls.py                    # Glowny routing -> 3 appy
│   └── wsgi.py
├── rozwiazanie_weekend2/          # Engine z Weekend 1+2
│   ├── pizza.py, customer.py, order.py, exceptions.py
│   └── data/
│       ├── menu.json, customers.json, orders.json
├── menu_app/                      # App: menu pizz
│   ├── views.py                   # pizza_list, pizza_detail, pizza_add
│   ├── urls.py
│   └── templates/menu_app/
├── customers_app/                 # App: klienci
│   ├── views.py                   # customer_list, customer_add
│   ├── urls.py
│   └── templates/customers_app/
├── orders_app/                    # App: zamowienia
│   ├── views.py                   # order_list, order_detail, order_create
│   ├── urls.py
│   └── templates/orders_app/
├── templates/
│   └── base.html                  # Szablon bazowy z Bootstrap
└── static/
    └── css/style.css
```

### Kluczowe URL-e

| URL | View | Opis |
|-----|------|------|
| `/menu/` | pizza_list | Lista pizz |
| `/menu/<str:name>/` | pizza_detail | Szczegoly pizzy |
| `/menu/dodaj/` | pizza_add | Formularz dodawania |
| `/klienci/` | customer_list | Lista klientow |
| `/klienci/dodaj/` | customer_add | Formularz dodawania |
| `/zamowienia/` | order_list | Lista zamowien |
| `/zamowienia/<int:order_id>/` | order_detail | Szczegoly zamowienia |
| `/zamowienia/nowe/` | order_create | Formularz zamowienia |
