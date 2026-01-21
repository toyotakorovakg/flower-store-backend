# Secure Flower Store Backend

This repository contains a FastAPI backend designed to work with a hardened
PostgreSQL database schema.  It provides endpoints for user authentication,
product and order management, messaging, and support features.  The emphasis
is on **security**: sensitive information is encrypted, row–level security
policies are enforced in the database, and the application is configured
through environment variables to avoid hard‑coding secrets.

## Local setup

Follow these steps to get the backend running locally:

1. **Clone the repository** and create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -U pip
   # Install required packages from pyproject.toml or requirements.txt
   pip install -r requirements.txt
   ```

2. **Copy the environment template** and fill in real values:

   ```sh
   cp .env.example .env
   # then edit .env to set DB credentials and secrets
   ```

   The application expects either a full `DATABASE_URL` using the
   `postgresql+asyncpg` dialect【734863252372453†L1700-L1718】 (e.g. provided by Supabase) or
   individual `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and
   `DB_PASSWORD` variables.  Additionally you must set `ENCRYPTION_KEY`,
   `EMAIL_PEPPER` and `JWT_SECRET_KEY` to strong, randomly generated
   strings. See the **Secrets** section below for generation commands.

3. **Generate secrets**: create strong random strings for the secrets. For
   example:

   ```sh
   # Generate a 32-byte base64 key for Fernet encryption
   python -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"

   # Generate a 16-byte hex pepper for email hashing
   python -c "import secrets; print(secrets.token_hex(16))"

   # Generate a 32-byte hex string for the JWT secret
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   Copy the outputs into your `.env` file as `ENCRYPTION_KEY`,
   `EMAIL_PEPPER` and `JWT_SECRET_KEY` respectively.

4. **Run the API**:

   ```sh
   uvicorn app.main:app --reload
   ```

   On startup the application will attempt to connect to the database using
   the provided configuration.  If the connection fails, it will log an
   error and abort.  Ensure that your database is reachable and that row
   level security policies are enabled as defined in the SQL schema.

## Database connection

The backend uses SQLAlchemy’s async engine with `asyncpg` as the driver.
The DSN is constructed from the environment settings defined in
`app/core/settings.py`.  For example, if using [Supabase](https://supabase.com/),
your `.env` might include:

```env
DATABASE_URL=postgresql+asyncpg://postgres:<YOUR-PASSWORD>@db.<project-ref>.supabase.co:5432/postgres
ENCRYPTION_KEY=<32-byte-random-string>
EMAIL_PEPPER=<16-byte-random-pepper>
JWT_SECRET_KEY=<32-byte-random-string>
```

Replace `<YOUR-PASSWORD>` and `<project-ref>` with the credentials from your
Supabase project.  Never commit these secrets to version control.

## Extending the API

The current implementation provides only placeholders for endpoints.  To
implement full functionality:

* Define SQLAlchemy ORM models in `app/db/models/*` to mirror your
  PostgreSQL tables, referencing the RLS policies.
* Implement service layers in `app/services/` to encapsulate business logic.
* Replace stubbed endpoints in `app/api/v1/endpoints/` with real
  query/update logic, using dependencies from `app/api/v1/deps.py` to
  provide sessions and enforce authentication.

Pull requests and contributions that improve security and functionality are
welcome.
