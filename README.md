# NUB Journal
**DBMS Course Project — Northern University Bangladesh**
A lightweight Django MVT blog publishing platform.

## Setup

```bash
# 1. Create & activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install Django
pip install django

# 3. Apply database migrations
python manage.py migrate

# 4. (Optional) Create a superuser for /admin
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Modules

| Module | URLs | Description |
|--------|------|-------------|
| Authentication | /register/ /login/ /logout/ | Register, login, logout |
| Blog CRUD | /create/ /edit/<pk>/ /delete/<pk>/ | Owner-scoped create, edit, delete |
| Publish & Read | /my-posts/ (toggle) / /post/<slug>/ | Draft ↔ Published toggle; public listing |

## Database Schema

**Users** — Django's built-in `auth_user` table (user_id PK, username, email, password hash, etc.)

**Blog** — `blog_blog` table
- `blog_id` — PK
- `user_id` — FK → Users (CASCADE)
- `title`, `slug` (unique), `content`
- `status` — 'draft' | 'published'
- `created_at`, `updated_at`, `published_at`

## Tech Stack
- **Backend:** Django 5+ (MVT pattern)
- **Database:** SQLite (django.db.backends.sqlite3)
- **Frontend:** Django Templates + Bootstrap 5 (CDN)
- **Auth:** Django's built-in session auth + bcrypt password hashing
