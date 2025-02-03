# Hiring Test for Backend Developers

## Overview

Welcome to the Backend Developer Hiring Test! This test evaluates your ability to design, implement, and document a backend system using Django. Your solution should include a well-structured API, multilingual support, caching, and code best practices.

## Technology Stack
- Backend: Django/Python
- Database: SQLite (default)
- Caching: Redis 
- API: RESTful API with proper authentication
- Editor Support: WYSIWYG integration using django-ckeditor
- Translation: Google Translate API / googletrans (for automated multilingual support)
- Testing: pytest

## Features
- Create, read, update, and delete FAQs.
- Multilingual translation support.
- REST API for fetching FAQs with language filtering.
- Caching with Redis for performance optimization.
- Django admin panel for easy management.
- Docker support for deployment.

## API Endpoints
- Fetch All FAQs: GET /api/faqs/
- Review ALL THE FAQs: GET /admin
- Fetch FAQs in a Specific Language: GET /api/faqs/?lang={lang}

### response
``` bash
[
    {
        "id": 1,
        "question": "What is Django?",
        "answer": "Django is a Python-based web framework."
    }
]
```
### Fetch FAQs in a Specific Language
```bash
[
    {
        "id": 1,
        "question": "Django क्या है?",
        "answer": "Django एक पायथन-आधारित वेब फ्रेमवर्क है।"
    }
]

```



## steps to Install (with python)
- Clone the Repository
```bash
git clone https://github.com/miharshrajput1/BharatFD
cd BharatFD
```
- Create and Activate a Virtual Environment
```bash
 python -m venv venv
 source venv/bin/activate  # For macOS/Linux
 venv\Scripts\activate      # For Windows
 ```
- Install Dependencies
```bash
pip install -r requirements.txt
 ```

- Apply Migrations
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
 ```

- Create a Superuser (for admin panel)
```bash
python manage.py createsuperuser
 ```

- Start the Development Server
```bash
python manage.py runserver 127.0.0.1/8000
```


## Deployment with Docker
- Clone the Repository
```bash
git clone https://github.com/miharshrajput1/BharatFD
cd BharatFD
```
- Build Docker Images
```bash 
docker-compose build
```
- Run the Containers
```bash
 docker-compose up -d
```
- Apply Migrations
 ```bash
 docker-compose exec web python manage.py migrate
 ```
- Create a Superuser (Optional)
 ```bash
 docker-compose exec web python manage.py createsuperuser
 ```


- Stopping the Containers
```bash
docker-compose down
 ```

- Restarting the Containers
If you need to restart your app:
```bash
docker-compose restart
```

- Docker Container Overview:
1. web → Django application (Runs on port 8000)
2. redis → Redis service (Runs on port 6379)

  

