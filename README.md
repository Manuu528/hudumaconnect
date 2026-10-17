# HudumaConnect — Public Service Request System

## 1. Overview

HudumaConnect is a Django-based public service request management
system. It allows citizens to report local service issues and track
their progress, while administrators review requests and update
their status.

## 2. Key Features

### Citizen features
- Register an account and log in securely.
- Submit a service request with a category, location and description.
- Attach an optional supporting image.
- View personal requests and their current status.
- View request details and reference numbers.

### Administrator features
- Access a protected administration dashboard.
- View and search submitted service requests.
- Filter requests by category and status.
- Update request statuses: Pending, In Progress and Resolved.
- View request totals and status summaries.
- Manage records through Django administration.

## 3. Service Categories

- Water Supply
- Broken Streetlight
- Garbage Collection
- Road Damage
- Drainage and Sewage
- Other

## 4. Technology Stack

- Python
- Django
- SQLite
- HTML and CSS
- Pillow for image handling

## 5. Project Structure

    public_service_system/
    ├── config/
    │   ├── settings.py
    │   └── urls.py
    ├── requests_app/
    │   ├── migrations/
    │   ├── admin.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── templates/
    │   └── requests_app/
    ├── media/
    ├── manage.py
    └── README.md

## 6. Installation and Setup

Requirements: Python 3 and pip.

1. Navigate to the project directory:

       cd public_service_system

2. Create and activate a virtual environment if one does not exist:

       python3 -m venv venv
       source venv/bin/activate

3. Install dependencies:

       pip install django pillow

4. Apply database migrations:

       python manage.py migrate

5. Create an administrator account if required:

       python manage.py createsuperuser

6. Start the development server:

       python manage.py runserver

7. Open the application:

       http://127.0.0.1:8000/

## 7. Application URLs

- Homepage: /
- Citizen registration: /register/
- Login: /login/
- Citizen dashboard: /dashboard/
- Submit request: /requests/new/
- Administrator dashboard: /admin-dashboard/
- Django administration: /django-admin/

The administrator dashboard requires a staff account.

## 8. Request Status Workflow

1. A newly submitted request receives Pending status.
2. An administrator can change it to In Progress.
3. Once addressed, the administrator can mark it Resolved.
4. Status totals help administrators monitor outstanding work.

## 9. Database

The ServiceRequest model stores a unique reference number, citizen,
category, location, description, optional image, status, creation
time and last-update time.

SQLite is used for local development.

## 10. Testing Checklist

- [ ] Register a citizen account.
- [ ] Log in and log out.
- [ ] Submit a service request.
- [ ] Confirm a new request starts as Pending.
- [ ] Confirm citizens can view their own requests.
- [ ] Confirm administrators can access the admin dashboard.
- [ ] Update a request to In Progress and Resolved.
- [ ] Confirm dashboard totals reflect status changes.
- [ ] Test search and category/status filters.
- [ ] Test optional image upload and request details.
- [ ] Run `python manage.py check`.

## 11. Development and Security Notes

This project is configured for local development. Before production
deployment, configure secure production settings, HTTPS, environment
variables for secrets, appropriate allowed hosts, database backups,
and validated file uploads. Do not use Django's development server
as a production server.

