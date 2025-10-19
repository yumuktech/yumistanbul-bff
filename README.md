# Yum Istanbul BFF

This repository contains a Django-based backend-for-frontend (BFF) that powers the Yum Istanbul frontend application. The service exposes REST endpoints for restaurant discovery, taxonomy lookups, editor workflows, and lightweight search suggestions.

## Getting started

1. Create and activate a virtual environment.
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations and seed baseline taxonomy data.
   ```bash
   python manage.py migrate
   python manage.py seed_taxonomy
   ```
4. Create an editor user (optional for local testing).
   ```bash
   python manage.py createsuperuser
   python manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.get_or_create(name='editors')"
   ```
5. Start the development server.
   ```bash
   python manage.py runserver
   ```

## Key endpoints

- `GET /api/restaurants/` — list restaurants with filters (`district`, `feature`, `additional`, pagination, ordering).
- `GET /api/restaurants/<uuid|slug>/` — retrieve restaurant detail.
- `POST /api/restaurants/` — create restaurant (editors only).
- `PATCH /api/restaurants/<uuid|slug>/` — update restaurant (editors only).
- `GET /api/districts/`
- `GET /api/features/`
- `GET /api/additional-filters/`
- `GET /api/search/suggestions/?q=` — lightweight search for restaurants and districts.
- `POST /api/auth/token/` — obtain JWT for editor workflows.
- `POST /api/auth/token/refresh/`

Run `python manage.py test` to execute the app's automated test suite.
# yumistanbul-bff
