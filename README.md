## Setup

git clone https://github.com/adnanmaksic/408-tracker.git project
cd project
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env

Add your own values to values to `.env`:

CANVAS_BASE_URL=https://boisestatecanvas.instructure.com
CANVAS_API_TOKEN=your_canvas_token
DJANGO_SECRET_KEY=your_django_secret_key

To run the app:

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Reflection

I learned how to authenticate with a REST API, parse JSON, handle pagination, and display API data with Django templates.
Keeping API tokens and secret keys in `.env` also reinforced the importance of protecting secrets.
The most challenging part was handling errors and pagination.