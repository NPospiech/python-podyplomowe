# Dzien 2: REST API z Django REST Framework

## Agenda

**Czas trwania:** 8:30 - 15:00 (6h 30min z przerwami)

### Harmonogram

| Czas | Temat | Aktywnosc |
|------|-------|-----------|
| **8:30 - 8:50** | Recap dnia 1 | Sprawdzenie srodowiska |
| **8:50 - 10:30** | REST teoria + DRF setup + Pizza API (GET) | Teoria + cwiczenia |
| **10:30 - 10:40** | **PRZERWA** | 10 minut |
| **10:40 - 12:40** | Pizza CRUD (POST, PUT, DELETE) + testowanie | Cwiczenia |
| **12:40 - 13:10** | **PRZERWA** | 30 minut |
| **13:10 - 15:00** | Testy API + podsumowanie + zadanie domowe | Cwiczenia + testy |

### Co zbudujemy dzisiaj?

REST API dla naszej pizzerii - te same modele ORM i baza danych, ale zamiast stron HTML zwracamy **JSON**:

```
Weekend 3 (HTML):        Weekend 4 (API):
GET /menu/               GET /api/pizzas/
-> strona HTML z lista   -> JSON: [{"name":"Margherita","price":25.0}, ...]
```

Oba interfejsy (HTML i API) wspolistniejaja w jednym projekcie i uzywaja tych samych modeli ORM.

---

## Czesc 1: Recap dnia 1 (20 min)

### Co zrobilismy wczoraj

- **Debugger VS Code:** breakpoints, krokowanie, inspekcja zmiennych
- **Django ORM:** modele Pizza, Customer, Order, OrderItem
- **Migracje:** makemigrations + migrate -> tabele w SQLite
- **Admin panel:** zarzadzanie danymi przez przegladarke
- **QuerySet API:** all(), filter(), get(), create(), order_by()
- **Import danych:** management command import_data (JSON -> baza)

### Sprawdzenie srodowiska

```bash
cd 2801-03-2026/pizzeria_django
python3 manage.py runserver
```

Sprawdz:
1. http://127.0.0.1:8000/menu/ - lista pizz (HTML, dane z ORM)
2. http://127.0.0.1:8000/admin/ - admin panel z danymi

Upewnij sie ze w bazie sa dane (pizze + klienci). Jesli nie - uruchom:
```bash
python3 manage.py import_data
```

---

## Czesc 2: REST API - Teoria (30 min)

### Czym jest REST API?

**API** (Application Programming Interface) = interfejs do komunikacji miedzy programami.

**REST** (Representational State Transfer) = styl architektoniczny dla API webowych.

Do tej pory budowalismy strony HTML dla ludzi. Ale co jesli chcemy zeby **inny program** mogl korzystac z naszych danych? Na przyklad:
- Aplikacja mobilna chce wyswietlic menu pizzerii
- Frontend React/Vue chce pobrac liste zamowien
- Inny serwer chce zlozyc zamowienie programowo

Te programy nie rozumieja HTML - potrzebuja **danych w czystej postaci** (JSON).

### HTML vs JSON

**HTML (dla ludzi):**
```html
<h1>Menu Pizzerii</h1>
<ul>
    <li>Margherita - 25.0 zl</li>
    <li>Pepperoni - 30.0 zl</li>
</ul>
```

**JSON (dla programow):**
```json
[
    {"name": "Margherita", "price": 25.0},
    {"name": "Pepperoni", "price": 30.0}
]
```

### HTTP Metody

REST API uzywa standardowych metod HTTP do roznych operacji:

| Metoda | Cel | Przyklad | SQL equivalent |
|--------|-----|---------|---------------|
| **GET** | Pobierz dane | `GET /api/pizzas/` | SELECT |
| **POST** | Stworz nowy zasob | `POST /api/pizzas/` | INSERT |
| **PUT** | Zaktualizuj zasob | `PUT /api/pizzas/Margherita/` | UPDATE |
| **DELETE** | Usun zasob | `DELETE /api/pizzas/Margherita/` | DELETE |

Te 4 operacje to **CRUD** - Create, Read, Update, Delete.

### Status Codes

Serwer odpowiada kodem statusu HTTP:

| Kod | Nazwa | Znaczenie |
|-----|-------|-----------|
| **200** | OK | Sukces (GET, PUT) |
| **201** | Created | Zasob utworzony (POST) |
| **204** | No Content | Sukces bez danych (DELETE) |
| **400** | Bad Request | Bledne dane w requescie |
| **404** | Not Found | Zasob nie istnieje |
| **405** | Method Not Allowed | Metoda HTTP nie dozwolona |

### Przyklad: typowy flow API

```
1. Klient wysyla:   GET /api/pizzas/
   Serwer odpowiada: 200 OK
   Body: [{"name":"Margherita","price":25.0}, ...]

2. Klient wysyla:   POST /api/pizzas/
   Body: {"name":"Diavola","price":34.0}
   Serwer odpowiada: 201 Created
   Body: {"name":"Diavola","price":34.0}

3. Klient wysyla:   GET /api/pizzas/NieIstniejaca/
   Serwer odpowiada: 404 Not Found
   Body: {"error":"Pizza 'NieIstniejaca' nie znaleziona"}

4. Klient wysyla:   DELETE /api/pizzas/Diavola/
   Serwer odpowiada: 204 No Content
```

---

## Czesc 3: Django REST Framework - Setup (20 min)

### Czym jest DRF?

**Django REST Framework** (DRF) to biblioteka ktora ulatwia budowanie REST API w Django. Dodaje:
- **Serializers** - konwersja modeli Django na JSON i odwrotnie
- **API Views** - widoki zwracajace JSON zamiast HTML
- **Browsable API** - interaktywna strona do testowania API w przegladarce
- **Authentication** - uwierzytelnianie (nie uzyjemy na warsztacie)

### Instalacja

```bash
pip install djangorestframework
```

### Nowy app: api

Na Dniu 1 modele ORM stworzylimy w istniejacych appach (`menu_app`, `customers_app`, `orders_app`). Teraz tworzymy **nowy app** `api` ktory bedzie zawieral tylko kod REST API (serializers, views, urls). Modele importuje z istniejacych appow.

```bash
python3 manage.py startapp api
```

### Konfiguracja

Dodaj `'rest_framework'` i `'api'` do `INSTALLED_APPS` w `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'rest_framework',     # <- DODAJ
    'menu_app',
    'customers_app',
    'orders_app',
    'api',                # <- DODAJ (nowy app)
]
```

### Kluczowe importy DRF

```python
from rest_framework.decorators import api_view          # dekorator dla view
from rest_framework.response import Response             # odpowiedz JSON
from rest_framework import status                        # kody statusu HTTP
from rest_framework import serializers                   # serializery
```

### Teoria: Serializer

**Serializer** to klasa ktora definiuje **jakie dane** maja byc w JSON:

```python
from rest_framework import serializers

class PizzaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
```

Serializery robia dwie rzeczy:
1. **Serializacja** (model -> JSON): bierze obiekt Pythona i zamienia na slownik ktory Django zamieni na JSON
2. **Deserializacja** (JSON -> walidacja): bierze dane z requestu, waliduje je i zwraca czyste dane

Mozna tez uzyc `ModelSerializer` ktory automatycznie generuje pola z modelu Django:

```python
class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['name', 'price']
```

`ModelSerializer` to wygodny skrot - nie musisz recznie definiowac kazdego pola. Na warsztacie bedziemy go uzywac.

### Teoria: @api_view

`@api_view` to dekorator DRF ktory zamienia zwykly view Django na API view:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_api(request):
    return Response({"message": "Witaj w API!"})
```

Roznice wzgledem zwyklego Django view:
- `@api_view(['GET'])` - deklaruje jakie metody HTTP sa dozwolone
- `Response(...)` zamiast `render(...)` - zwraca JSON
- `request.data` zamiast `request.POST` - dane z body (JSON, nie form-encoded)
- Automatycznie obsluguje `Content-Type: application/json`
- Dodaje Browsable API (ladna strona HTML do testowania)

### SHOW: Prosty endpoint (GENERIC - ksiazki)

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    price = serializers.FloatField()

@api_view(['GET'])
def book_list_api(request):
    books = [
        {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'price': 49.99},
        {'title': 'Fluent Python', 'author': 'Luciano Ramalho', 'price': 59.99},
    ]
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
```

```python
# urls.py
path('api/books/', views.book_list_api),
```

Wynik w przegladarce (Browsable API) lub curl:
```json
[
    {"title": "Python Crash Course", "author": "Eric Matthes", "price": 49.99},
    {"title": "Fluent Python", "author": "Luciano Ramalho", "price": 59.99}
]
```

`many=True` mowi serializerowi ze serializujemy **liste** obiektow, nie jeden obiekt.

---

## Cwiczenie 1: PizzaSerializer + GET /api/pizzas/

**Cel:** Stworz pierwszy endpoint API ktory zwraca liste pizz jako JSON.

**Krok 1:** Stworz plik `api/serializers.py`:

```python
# api/serializers.py
from rest_framework import serializers
from menu_app.models import Pizza


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['name', 'price']
```

`ModelSerializer` automatycznie generuje pola z modelu. `fields` okresla ktore pola wyeksponowac w API.

**Krok 2:** Stworz view w `api/views.py`:

```python
# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

from menu_app.models import Pizza
from .serializers import PizzaSerializer


@api_view(['GET'])
def pizza_list_api(request):
    """GET /api/pizzas/ - lista wszystkich pizz."""
    pizzas = Pizza.objects.all()
    serializer = PizzaSerializer(pizzas, many=True)
    return Response(serializer.data)
```

Przejdz przez ten kod:
1. `@api_view(['GET'])` - ten view obsluguje tylko GET
2. `Pizza.objects.all()` - pobierz wszystkie pizze z bazy (ORM z dnia 1)
3. `PizzaSerializer(pizzas, many=True)` - zamien QuerySet na format JSON
4. `Response(serializer.data)` - zwroc JSON

**Krok 3:** Stworz `api/urls.py`:

```python
# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('pizzas/', views.pizza_list_api, name='pizza_list_api'),
]
```

**Krok 4:** Dodaj routing w glownym `pizzeria_project/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('menu/')),
    path('menu/', include('menu_app.urls')),
    path('klienci/', include('customers_app.urls')),
    path('zamowienia/', include('orders_app.urls')),
    path('api/', include('api.urls')),    # <- DODAJ
]
```

**Krok 5:** Sprawdz! Wejdz na http://127.0.0.1:8000/api/pizzas/

Powinienes zobaczyc **Browsable API** - ladna strone HTML z danymi JSON. To DRF automatycznie generuje ten interfejs dla Twojego API.

Mozesz tez uzyc curl z terminala:
```bash
curl http://127.0.0.1:8000/api/pizzas/
```

Wynik:
```json
[
    {"name": "Hawajska", "price": 32.0},
    {"name": "Margherita", "price": 25.0},
    {"name": "Pepperoni", "price": 30.0},
    {"name": "Quattro Formaggi", "price": 35.0}
]
```

---

## Czesc 4: GET detail + 404 (30 min)

### SHOW: Detail endpoint (GENERIC - ksiazka)

```python
from rest_framework import status

@api_view(['GET'])
def book_detail_api(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            {"error": f"Ksiazka o ID {pk} nie znaleziona"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = BookSerializer(book)
    return Response(serializer.data)
```

Roznice wzgledem list:
- `BookSerializer(book)` - **bez** `many=True` (jeden obiekt, nie lista)
- `status.HTTP_404_NOT_FOUND` - kod 404 gdy nie znaleziono
- `return Response({"error": ...}, status=404)` zamiast `raise Http404` - w API zwracamy JSON z bledem

### Cwiczenie 2: GET /api/pizzas/<name>/

**Cel:** Endpoint ktory zwraca szczegoly jednej pizzy.

**Krok 1:** Dodaj view w `api/views.py`:

```python
from rest_framework import status

@api_view(['GET'])
def pizza_detail_api(request, name):
    """GET /api/pizzas/<name>/ - szczegoly pizzy."""
    try:
        pizza = Pizza.objects.get(name=name)
    except Pizza.DoesNotExist:
        return Response(
            {"error": f"Pizza '{name}' nie znaleziona"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = PizzaSerializer(pizza)
    return Response(serializer.data)
```

**Krok 2:** Dodaj URL w `api/urls.py`:

```python
urlpatterns = [
    path('pizzas/', views.pizza_list_api, name='pizza_list_api'),
    path('pizzas/<str:name>/', views.pizza_detail_api, name='pizza_detail_api'),
]
```

**Krok 3:** Sprawdz:
- http://127.0.0.1:8000/api/pizzas/Margherita/ -> JSON z danymi pizzy
- http://127.0.0.1:8000/api/pizzas/NieIstniejaca/ -> JSON z bledem 404

```bash
curl http://127.0.0.1:8000/api/pizzas/Margherita/
# {"name":"Margherita","price":25.0}

curl http://127.0.0.1:8000/api/pizzas/NieIstniejaca/
# {"error":"Pizza 'NieIstniejaca' nie znaleziona"}
```

---

## Czesc 5: POST create + walidacja (30 min)

### Teoria: POST i deserializacja

POST tworzy nowy zasob. Klient wysyla dane JSON w body requestu:

```
POST /api/pizzas/
Content-Type: application/json

{"name": "Diavola", "price": 34.0}
```

W DRF:
1. `request.data` zawiera dane z body (zamiast `request.POST` - DRF obsluguje JSON automatycznie)
2. Serializer **waliduje** dane (deserializacja)
3. Jesli dane sa poprawne -> zapis do bazy
4. Zwroc 201 Created

```python
@api_view(['POST'])
def create_something(request):
    serializer = MySerializer(data=request.data)    # <- deserializacja
    if serializer.is_valid():                        # <- walidacja
        serializer.save()                            # <- zapis do bazy
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

`serializer.errors` to slownik z bledami walidacji, np.:
```json
{"name": ["To pole jest wymagane."], "price": ["Wprowadz poprawna liczbe."]}
```

### SHOW: POST create (GENERIC - ksiazka)

```python
@api_view(['GET', 'POST'])
def book_list_api(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Zwroc uwage: **jeden view obsluguje dwie metody** (GET i POST) na tym samym URL. To typowy wzorzec w REST API - URL `/api/books/` ma rozne zachowanie w zaleznosci od metody HTTP.

### Cwiczenie 3: POST /api/pizzas/

**Cel:** Rozszerz `pizza_list_api` o obsluge POST - tworzenie nowej pizzy.

**Krok 1:** Zaktualizuj view `pizza_list_api` w `api/views.py`:

```python
@api_view(['GET', 'POST'])
def pizza_list_api(request):
    """
    GET  /api/pizzas/ - lista wszystkich pizz
    POST /api/pizzas/ - dodaj nowa pizze
    """
    if request.method == 'GET':
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Krok 2:** Sprawdz! Otworz http://127.0.0.1:8000/api/pizzas/ w przegladarce. Na dole strony Browsable API zobaczysz **formularz** do wysylania POST. Wpisz:

```json
{"name": "Diavola", "price": 34.0}
```

I kliknij "POST". Powinienes zobaczyc odpowiedz 201 Created.

Mozesz tez uzyc curl:
```bash
curl -X POST http://127.0.0.1:8000/api/pizzas/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Diavola", "price": 34.0}'
```

**Krok 3:** Przetestuj walidacje:
```bash
# Pusta nazwa
curl -X POST http://127.0.0.1:8000/api/pizzas/ \
  -H "Content-Type: application/json" \
  -d '{"name": "", "price": 34.0}'
# -> 400 Bad Request

# Duplikat
curl -X POST http://127.0.0.1:8000/api/pizzas/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Margherita", "price": 99}'
# -> 400 Bad Request (unique constraint)
```

---

## Czesc 6: PUT update + DELETE (35 min)

### SHOW: PUT i DELETE (GENERIC - ksiazka)

```python
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_api(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"error": "Nie znaleziono"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Nowe elementy:
- **PUT:** `BookSerializer(book, data=request.data)` - pierwszy argument to istniejacy obiekt do aktualizacji, drugi to nowe dane
- **DELETE:** `book.delete()` + status 204 No Content (sukces bez danych)

### Cwiczenie 4: PUT + DELETE /api/pizzas/<name>/

**Cel:** Rozszerz `pizza_detail_api` o obsluge PUT i DELETE.

**Krok 1:** Zaktualizuj `pizza_detail_api` w `api/views.py`:

```python
@api_view(['GET', 'PUT', 'DELETE'])
def pizza_detail_api(request, name):
    """
    GET    /api/pizzas/<name>/ - szczegoly pizzy
    PUT    /api/pizzas/<name>/ - aktualizuj pizze
    DELETE /api/pizzas/<name>/ - usun pizze
    """
    try:
        pizza = Pizza.objects.get(name=name)
    except Pizza.DoesNotExist:
        return Response(
            {"error": f"Pizza '{name}' nie znaleziona"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = PizzaSerializer(pizza)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PizzaSerializer(pizza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pizza.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Krok 2:** Przetestuj:

```bash
# Aktualizacja ceny
curl -X PUT http://127.0.0.1:8000/api/pizzas/Margherita/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Margherita", "price": 28.0}'
# -> 200 OK, {"name":"Margherita","price":28.0}

# Usuwanie
curl -X DELETE http://127.0.0.1:8000/api/pizzas/Diavola/
# -> 204 No Content

# Sprawdz ze znikla
curl http://127.0.0.1:8000/api/pizzas/Diavola/
# -> 404
```

Mozesz tez testowac przez Browsable API w przegladarce - wejdz na /api/pizzas/Margherita/ i zobaczysz przyciski PUT i DELETE.

### Pizza API - podsumowanie

Masz teraz **pelny CRUD** dla pizzy:

| Metoda | URL | Opis | Status |
|--------|-----|------|--------|
| GET | /api/pizzas/ | Lista pizz | 200 |
| POST | /api/pizzas/ | Dodaj pizze | 201 |
| GET | /api/pizzas/\<name\>/ | Szczegoly | 200 / 404 |
| PUT | /api/pizzas/\<name\>/ | Aktualizuj | 200 / 400 / 404 |
| DELETE | /api/pizzas/\<name\>/ | Usun | 204 / 404 |

---

## Czesc 7: Testowanie API (50 min)

### Teoria: Testowanie API z pytest + DRF

DRF dostarcza `APIClient` - klienta HTTP do testow:

```python
from rest_framework.test import APIClient

client = APIClient()

# GET
response = client.get('/api/pizzas/')
assert response.status_code == 200
assert len(response.data) > 0

# POST
response = client.post('/api/pizzas/', {'name': 'Testowa', 'price': 99.0}, format='json')
assert response.status_code == 201
assert response.data['name'] == 'Testowa'
```

`format='json'` mowi klientowi zeby wyslal dane jako JSON (nie form-encoded).

### SHOW: Prosty test API (GENERIC)

```python
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_book_list(api_client):
    response = api_client.get('/api/books/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_book_create(api_client):
    response = api_client.post('/api/books/', {
        'title': 'Test Book',
        'author': 'Test Author',
        'price': 29.99,
    }, format='json')
    assert response.status_code == 201
    assert response.data['title'] == 'Test Book'
```

`@pytest.mark.django_db` - mowi pytest ze ten test potrzebuje dostepu do bazy danych. Bez tego dostaniesz blad.

### Cwiczenie 5: Testy Pizza API

**Cel:** Napisz testy dla pelnego CRUD pizzy.

**Krok 0:** Upewnij sie ze masz plik `pytest.ini` (lub `setup.cfg`) w katalogu projektu:

Stworz plik `pytest.ini` obok `manage.py`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = pizzeria_project.settings
pythonpath = .
```

Zainstaluj plugin pytest-django:
```bash
pip install pytest-django
```

**Krok 1:** Stworz plik `api/tests.py`:

```python
import pytest
from rest_framework.test import APIClient
from menu_app.models import Pizza


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_pizza():
    return Pizza.objects.create(name="Margherita", price=25.0)


# === Testy Pizza API ===

class TestPizzaAPI:

    @pytest.mark.django_db
    def test_list_empty(self, api_client):
        """GET /api/pizzas/ zwraca pusta liste gdy brak pizz."""
        response = api_client.get('/api/pizzas/')
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.django_db
    def test_list_with_data(self, api_client, sample_pizza):
        """GET /api/pizzas/ zwraca liste pizz."""
        response = api_client.get('/api/pizzas/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Margherita'

    @pytest.mark.django_db
    def test_detail(self, api_client, sample_pizza):
        """GET /api/pizzas/<name>/ zwraca szczegoly pizzy."""
        response = api_client.get('/api/pizzas/Margherita/')
        assert response.status_code == 200
        assert response.data['name'] == 'Margherita'
        assert response.data['price'] == 25.0

    @pytest.mark.django_db
    def test_detail_not_found(self, api_client):
        """GET /api/pizzas/<name>/ zwraca 404 dla nieistniejacej pizzy."""
        response = api_client.get('/api/pizzas/NieIstniejaca/')
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_create(self, api_client):
        """POST /api/pizzas/ tworzy nowa pizze."""
        response = api_client.post('/api/pizzas/', {
            'name': 'Diavola',
            'price': 34.0,
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Diavola'
        assert Pizza.objects.count() == 1

    @pytest.mark.django_db
    def test_create_invalid(self, api_client):
        """POST /api/pizzas/ z blednymi danymi zwraca 400."""
        response = api_client.post('/api/pizzas/', {
            'name': '',
            'price': 34.0,
        }, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_duplicate(self, api_client, sample_pizza):
        """POST /api/pizzas/ z duplikatem nazwy zwraca 400."""
        response = api_client.post('/api/pizzas/', {
            'name': 'Margherita',
            'price': 99.0,
        }, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update(self, api_client, sample_pizza):
        """PUT /api/pizzas/<name>/ aktualizuje pizze."""
        response = api_client.put('/api/pizzas/Margherita/', {
            'name': 'Margherita',
            'price': 28.0,
        }, format='json')
        assert response.status_code == 200
        assert response.data['price'] == 28.0

    @pytest.mark.django_db
    def test_delete(self, api_client, sample_pizza):
        """DELETE /api/pizzas/<name>/ usuwa pizze."""
        response = api_client.delete('/api/pizzas/Margherita/')
        assert response.status_code == 204
        assert Pizza.objects.count() == 0
```

**Krok 2:** Uruchom testy:

```bash
pytest api/tests.py -v
```

Powinienes zobaczyc cos takiego:
```
api/tests.py::TestPizzaAPI::test_list_empty PASSED
api/tests.py::TestPizzaAPI::test_list_with_data PASSED
api/tests.py::TestPizzaAPI::test_detail PASSED
api/tests.py::TestPizzaAPI::test_detail_not_found PASSED
api/tests.py::TestPizzaAPI::test_create PASSED
api/tests.py::TestPizzaAPI::test_create_invalid PASSED
api/tests.py::TestPizzaAPI::test_create_duplicate PASSED
api/tests.py::TestPizzaAPI::test_update PASSED
api/tests.py::TestPizzaAPI::test_delete PASSED
```

Wskazowka: jezeli testy nie przechodza, uzyj debuggera VS Code! Ustaw breakpoint w tescie i uruchom pytest z debuggerem (Run -> "Python: Debug Tests" lub dodaj konfiguracje launch.json dla pytest).

---

## Czesc 8: Podsumowanie weekendu (20 min)

### Progresja calego kursu

```
Weekend 1: proceduralne -> OOP (klasy, dziedziczenie)
Weekend 2: wyjatki -> I/O (JSON) -> testy (pytest)
Weekend 3: Git -> Django (views, templates, forms)
Weekend 4: debugger -> ORM (modele, migracje) -> REST API (DRF)
```

### Co zrobilismy na tym weekendzie

**Dzien 1:**
- Debugger VS Code (breakpoints, krokowanie, inspekcja)
- Django ORM (modele, migracje, QuerySet API)
- Django Admin (panel zarzadzania)
- Ewolucja: modele Django ORM zastepuja klasy z Weekend 1-2
- Import danych z JSON do bazy

**Dzien 2:**
- REST API z Django REST Framework
- Serializery (model -> JSON -> model)
- Pelny CRUD: GET, POST, PUT, DELETE
- Testowanie API z pytest + APIClient

### Kluczowe wzorce

**ORM:**
```python
Pizza.objects.all()                          # lista
Pizza.objects.get(name="X")                  # jeden obiekt
Pizza.objects.create(name="X", price=25)     # tworzenie
Pizza.objects.filter(price__gt=30)           # filtrowanie
```

**REST API view:**
```python
@api_view(['GET', 'POST'])
def my_list_api(request):
    if request.method == 'GET':
        items = MyModel.objects.all()
        serializer = MySerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Test API:**
```python
@pytest.mark.django_db
def test_my_api(api_client):
    response = api_client.get('/api/my-endpoint/')
    assert response.status_code == 200
```

### Pelna struktura URL

| URL | Metoda | Opis | Interfejs |
|-----|--------|------|-----------|
| /menu/ | GET | Lista pizz | HTML |
| /admin/ | GET | Panel admina | HTML |
| /api/pizzas/ | GET, POST | Lista + tworzenie | JSON |
| /api/pizzas/\<name\>/ | GET, PUT, DELETE | CRUD | JSON |

---

## Zadanie domowe (opcjonalne)

### Zadanie 1: Customer API

Zbuduj REST API dla klientow, stosujac ten sam wzorzec co dla pizzy:

1. Stworz `CustomerSerializer` w `api/serializers.py`:
   ```python
   class CustomerSerializer(serializers.ModelSerializer):
       class Meta:
           model = Customer
           fields = ['id', 'name', 'phone', 'customer_type', 'discount_percent', 'loyalty_points']
           read_only_fields = ['id', 'loyalty_points']
   ```

2. Dodaj views: `customer_list_api` (GET + POST) i `customer_detail_api` (GET)

3. Dodaj URL-e: `/api/customers/` i `/api/customers/<int:customer_id>/`

### Zadanie 2: Order API z nested serializers

Zbuduj API dla zamowien - to bardziej zaawansowane zadanie:

1. Stworz `OrderItemSerializer` z `source='pizza.name'` i `SerializerMethodField`
2. Stworz `OrderSerializer` z nested `items = OrderItemSerializer(many=True)`
3. Stworz `OrderCreateSerializer` z innym formatem wejsciowym (customer_id + lista items)
4. Dodaj views: `order_list_api` (GET + POST) i `order_detail_api` (GET + DELETE)

Wskazowka: dane wejsciowe (POST) maja inny format niz wyjsciowe (GET) - to typowy wzorzec.

### Zadanie 3: Wyszukiwanie w API

Dodaj parametr query `?search=` do `pizza_list_api`:

```
GET /api/pizzas/?search=Mar  -> zwraca pizze zawierajace "Mar" w nazwie
```

Wskazowka: `request.query_params.get('search')` + `Pizza.objects.filter(name__icontains=search)`.

### Zadanie 4: Sortowanie w API

Dodaj parametr `?ordering=` do `pizza_list_api`:

```
GET /api/pizzas/?ordering=price     -> sortuj po cenie rosnaco
GET /api/pizzas/?ordering=-price    -> sortuj po cenie malejaco
GET /api/pizzas/?ordering=name      -> sortuj po nazwie
```

Wskazowka: `Pizza.objects.order_by(ordering)`.

### Zadanie 5: Testy Customer i Order API

Napisz testy dla Customer API i Order API (jesli je zbudowales), stosujac wzorzec z Cwiczenia 5.

---

## REST API Cheatsheet

```
DRF SETUP
  pip install djangorestframework
  INSTALLED_APPS += ['rest_framework']

SERIALIZER
  class MySerializer(serializers.ModelSerializer):
      class Meta:
          model = MyModel
          fields = ['field1', 'field2']

VIEW
  @api_view(['GET', 'POST'])
  def my_view(request):
      ...
      return Response(data, status=status.HTTP_200_OK)

STATUS CODES
  200 OK              GET/PUT sukces
  201 Created         POST sukces
  204 No Content      DELETE sukces
  400 Bad Request     Bledne dane
  404 Not Found       Zasob nie istnieje

TESTY
  from rest_framework.test import APIClient
  client = APIClient()
  response = client.get('/api/endpoint/')
  response = client.post('/api/endpoint/', data, format='json')
  assert response.status_code == 200
  assert response.data['key'] == 'value'

CURL
  curl http://localhost:8000/api/pizzas/
  curl -X POST http://localhost:8000/api/pizzas/ \
    -H "Content-Type: application/json" \
    -d '{"name":"Diavola","price":34}'
  curl -X PUT http://localhost:8000/api/pizzas/Margherita/ \
    -H "Content-Type: application/json" \
    -d '{"name":"Margherita","price":28}'
  curl -X DELETE http://localhost:8000/api/pizzas/Margherita/
```
