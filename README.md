# codetutor_athena
# CodeTutor-Athena

## A Generative AI Programming Education Framework

CodeTutor-Athena is a Django-based programming education framework designed to support personalized coding assistance and interactive learning.

The project provides a foundation for building an educational coding platform with learner authentication, dashboards, profile management, Django administration, and an extensible architecture for AI-assisted programming education.

---

## 🚀 Features

- User/Learner authentication
- Learner dashboard
- Learner profile management
- Django Admin portal
- SQLite database
- Session-based authentication
- Modular Django application structure
- Template-based web interface
- Foundation for Generative AI-powered coding assistance
- Designed for personalized programming education and interactive learning

---

## 🛠️ Technology Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML, CSS, Django Templates
- **Authentication:** Django Authentication & Sessions
- **Development Environment:** VS Code / Antigravity IDE
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```text
codetutor_athena/
│
├── codetutor_athena/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analytics_service.py
│   │   └── rag_service.py
│   │
│   └── templates/
│       └── users/
│           ├── base.html
│           ├── dashboard.html
│           ├── login.html
│           └── register.html
│
├── manage.py
├── db.sqlite3
├── .gitignore
└── README.md
