# Multi-user-Blog-Platform
This is a repository containing the source code for a Multi-user Blog Platform project. (currently in development)

# Multi-User Blog Platform

A scalable, Django-powered blog platform that supports multiple users, allowing them to register, log in, write blog posts, and manage their content—all within a clean and functional web interface.

---

## Configuration

Before running the project, you need to create a `.env` file in the root directory. This file stores environment variables used by Django's settings.

### Sample `.env` file:

\```env
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (default: SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
\```

> ⚠️ Do **not** commit your `.env` file. It's excluded via `.gitignore` to protect sensitive information.

---

## Installation

You can run the project in two ways: using **Docker** or directly with **Python and virtualenv**.

---

### Option 1: Docker (Recommended)

#### Prerequisites:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

#### Steps:

\```bash
git clone https://github.com/ChesterLen/multi-user-blog-platform.git
cd multi-user-blog-platform

# Create a .env file (see Configuration section above)

# Build and run the containers
docker-compose up --build
\```

Visit `http://localhost:8000/` in your browser to access the app.

---

### Option 2: Manual Setup (Python + Virtual Environment)

#### Prerequisites:
- Python 3.8+
- `pip`
- `virtualenv`

#### Steps:

\```bash
git clone https://github.com/ChesterLen/multi-user-blog-platform.git
cd multi-user-blog-platform

# Create a .env file (see Configuration section above)

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
\```

Then open `http://127.0.0.1:8000/` in your browser.

---

## Usage

- Register a new user or log in.
- Create, update, and delete your own blog posts.
- Access the admin panel at `/admin/` (after creating a superuser with `python manage.py createsuperuser`).

> This setup is intended for development purposes. For production use, make sure to configure secure settings, static/media file handling, and a production-ready database.

---
