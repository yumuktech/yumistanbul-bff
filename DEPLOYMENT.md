# Yum Istanbul BFF - Deployment Guide

## Vercel Deployment Instructions

### Prerequisites
1. Vercel account connected to GitHub
2. PostgreSQL database (recommended: Vercel Postgres or Neon)

### Environment Variables
Set these in your Vercel project settings:

**Required:**
- `DJANGO_SECRET_KEY` - Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DATABASE_URL` - PostgreSQL connection string (format: `postgresql://user:password@host:port/dbname`)
- `DJANGO_DEBUG` - Set to `0` for production
- `DJANGO_ALLOWED_HOSTS` - Your frontend domain(s), comma-separated (e.g., `yourapp.vercel.app,yourdomain.com`)

**Auto-set by Vercel:**
- `VERCEL_URL` - Automatically provided by Vercel

### CORS Configuration
Update `CORS_ALLOWED_ORIGINS` in `bff/settings.py` to include your frontend URL:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://your-frontend.vercel.app',  # Add your production frontend
]
```

Also update `CSRF_TRUSTED_ORIGINS` similarly.

### Deployment Steps

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will auto-detect the Python project

3. **Configure Environment:**
   - Add all environment variables listed above
   - Connect or create a PostgreSQL database

4. **Deploy:**
   - Vercel will run the build automatically
   - The `build.sh` script handles migrations and static files

5. **Post-Deployment:**
   - Run taxonomy seeding if needed (first deploy):
     ```bash
     vercel env pull
     python manage.py seed_taxonomy
     ```
   - Create superuser for admin access:
     ```bash
     python manage.py createsuperuser
     ```

### API Endpoints
Your BFF will be available at: `https://your-project.vercel.app/api/`

- `GET /api/restaurants/` - List restaurants
- `GET /api/restaurants/{id}/` - Restaurant detail
- `GET /api/districts/` - List districts
- `GET /api/features/` - List features
- `GET /api/additional-filters/` - List filters
- `GET /api/search/suggestions/?q=` - Search suggestions
- `POST /api/auth/token/` - Obtain JWT
- `POST /api/auth/token/refresh/` - Refresh JWT

### Troubleshooting

**CORS Issues:**
- Ensure your frontend domain is in `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`
- Verify `DJANGO_ALLOWED_HOSTS` includes your Vercel domain

**Database Issues:**
- Verify `DATABASE_URL` format is correct
- Check database connection from Vercel dashboard
- Ensure migrations ran successfully in build logs

**Static Files:**
- Static files are collected to `staticfiles/` during build
- Admin assets should work automatically

### Local Development

1. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up database:
   ```bash
   python manage.py migrate
   python manage.py seed_taxonomy
   ```

4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```

5. Run server:
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000/admin/` and `http://localhost:8000/api/`
