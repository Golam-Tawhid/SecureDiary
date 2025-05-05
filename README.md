# Secure Diary

Secure Diary is a Flask-based web application that allows users to securely create, view, edit, and delete personal diary entries. The application features user registration and login, encrypted data handling, and a user-friendly interface to manage diary entries privately.

This project was developed as part of the "Cryptography and Cryptanalysis" course during my undergraduate degree.

## Features

- User registration and authentication with secure password handling
- Create, read, update, and delete (CRUD) diary entries
- User-specific diary entries with access control
- Encryption support for sensitive data
- Responsive and clean UI with Flask templates
- PostgreSQL database backend with SQLAlchemy ORM

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd SecureDiary
```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables:

- `SESSION_SECRET`: Secret key for Flask sessions (default used if not set)
- `DATABASE_URL`: PostgreSQL database connection URI (default: `postgresql://postgres:postgres1234@localhost:5432/social_diary`)

Example (Linux/macOS):

```bash
export SESSION_SECRET='your_secret_key'
export DATABASE_URL='your_database_uri'
```

## Usage

1. Initialize the database (tables are created automatically on app start).

2. Run the Flask application:

```bash
flask run
```

or if using `main.py` directly:

```bash
python main.py
```

3. Open your browser and navigate to `http://localhost:5000` to access the app.

## Folder Structure

- `app.py` - Main Flask application setup and initialization
- `config.py` - Configuration settings for the app
- `models.py` - Database models (User, DiaryEntry)
- `routes/` - Flask blueprints for authentication and diary entry routes
- `templates/` - HTML templates for rendering pages
- `static/` - Static files (CSS, JavaScript, images)
- `forms.py` - WTForms definitions for user input forms
- `utils/` - Utility modules for encryption and key management
- `requirements.txt` - Python dependencies list

## License

This project is licensed under the MIT License. See the LICENSE file for details.
