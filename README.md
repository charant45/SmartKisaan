# SmartKisaan 🌱

An agricultural marketplace platform connecting farmers with buyers and equipment rental services, featuring AI-powered crop suggestions.

## Key Features
- Buy/Sell agricultural produce  
- Rent farming equipment  
- AI-based crop suggestion system  
- User authentication system  
- Responsive web interface  

## Project Structure
```
smartkisaan/
├── djangoproject/
│   ├── myproject/             # Main Django project
│   │   ├── __init__.py
│   │   ├── settings.py        # Project configuration
│   │   ├── urls.py            # Main URL routing
│   │   └── wsgi.py            # WSGI configuration
│   │
│   └── myapp/                 # Django application
│       ├── migrations/        # Database migrations
│       ├── static/
│       │   └── myapp/         # App-specific static files
│       │       ├── css/
│       │       │   ├── style.css
│       │       │   └── base.css
│       │       └── images/    # All application images
│       ├── templates/         # HTML templates
│       ├── admin.py           # Admin configuration
│       ├── apps.py
│       ├── forms.py           # Django forms
│       ├── models.py          # Database models
│       ├── tests.py
│       ├── urls.py            # App URL routing
│       └── views.py           # Application logic
│
├── ai_model/                  # ML models directory
│   └── predictor.py           # Prediction logic
│
├── requirements.txt           # Project dependencies
├── manage.py                  # Django CLI
└── .env                       # Environment variables
```

## Installation

### Prerequisites
- Python 3.11+  
- pip  
- Virtualenv (recommended)  

### Setup Instructions

1. **Clone Repository**
```bash
git clone https://github.com/charant45/SmartKisaan.git
cd SmartKisaan
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**  
Create a `.env` file in the root directory:
```env
SECRET_KEY='your-django-secret-key'
DEBUG=0  # Set to 1 for development
DATABASE_URL='postgres://user:password@localhost/dbname'
```

5. **Database Setup**
```bash
python manage.py migrate
```

6. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

7. **Run Development Server**
```bash
python manage.py runserver
```

## Deployment

For production deployment (e.g., Render.com):
```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

## Configuration

Update `settings.py` with the following:
```python
ALLOWED_HOSTS = ['your-domain.com', 'localhost']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## License

MIT License
