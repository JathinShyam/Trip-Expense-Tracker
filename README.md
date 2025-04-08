# Expense Tracker API

A Django REST API for tracking travel expenses and managing trips.

## Features

- Track expenses by category (transport, food, accommodation, misc)
- Associate expenses with specific trips
- Upload and store receipts
- Automatic trip total calculation
- Expense verification system

## API Endpoints

### Expenses
- `GET /api/expenses/` - List all expenses
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense

### Categories
Available expense categories:
- Transport
- Food
- Accommodation 
- Miscellaneous

## Technical Details

Built with:
- Django REST Framework
- PostgreSQL
- Python 3.x

## Upcoming Features

- JWT Authentication
- Automated report generation
- Logging system
- Additional expense analytics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense-tracker-api.git
   cd expense-tracker-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in settings.py

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

The API will be available at http://127.0.0.1:8000/
