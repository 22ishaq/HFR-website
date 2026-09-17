# Deploying the HFR website

Everything below assumes the code is on the server (or PaaS) with Python 3.12+
and the dependencies from `requirements.txt` installed.

## 1. Environment variables (required)

| Variable | What to set |
| --- | --- |
| `DJANGO_SECRET_KEY` | A long random string. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. The site refuses to start in production with the dev key. |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | The domain(s), comma separated, e.g. `hfr.gla.ac.uk,www.hfr.gla.ac.uk` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Same domains with scheme, e.g. `https://hfr.gla.ac.uk` |

## 2. Email (required for password resets)

| Variable | What to set |
| --- | --- |
| `DJANGO_EMAIL_HOST` | SMTP server |
| `DJANGO_EMAIL_PORT` | Usually `587` (default) |
| `DJANGO_EMAIL_USER` / `DJANGO_EMAIL_PASSWORD` | SMTP credentials |
| `DJANGO_DEFAULT_FROM_EMAIL` | e.g. `HFR <hfr@glasgow.ac.uk>` (default) |

In development no setup is needed; reset emails print to the runserver console.

## 3. First deploy

```
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
gunicorn hfr_site.wsgi
```

## 4. Before opening the doors

- **Never reuse the development `db.sqlite3`.** It contains test accounts
  (including a superuser) with a public password. Start from a fresh database,
  or if one was ever copied across, run `python manage.py seed_test_users --delete`.
  The seed command itself refuses to run when `DEBUG` is off.
- In the admin, set **Recruitment settings**: the open/closed toggle and the
  (informational) close date shown on the register page.
- Check the file storage locations `media/` (public: avatars) and
  `private_media/` (applicant CVs, served only to team leads through the app)
  are on a persistent disk and included in backups, along with the database.

## 5. Sanity checks

```
DJANGO_DEBUG=0 DJANGO_SECRET_KEY=<key> python manage.py check --deploy
```

Expect no errors. W004/W008 style warnings about HSTS and SSL redirect should
be gone; the hardening switches on automatically when `DJANGO_DEBUG=0`.
