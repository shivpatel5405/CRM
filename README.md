# Enterprise Small-Business Django CRM System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)
![REST API](https://img.shields.io/badge/DRF-REST%20API-red?logo=django)
![License](https://img.shields.io/badge/License-MIT-green)

A production-grade, full-stack **Customer Relationship Management (CRM) System** built with Python, Django, SQLite, Bootstrap 5, Chart.js, and Django REST Framework. 

Designed specifically to demonstrate real-world backend engineering, role-based security, relational database modeling, business workflow automation, interactive data visualization, and RESTful API architecture.

---

## 🌟 Key Features

### 1. 🔐 Authentication & Role-Based Access Control (RBAC)
* **Custom User Model**: Extends `AbstractUser` with operational roles (`ADMIN`, `MANAGER`, `SALES_REP`), phone, and bio.
* **Role-Based Security**: Custom view decorators (`@admin_required`, `@manager_required`) and CBV mixins.
* **User Profiles**: Personal dashboard displaying assigned customer accounts, leads, and task metrics.

### 2. 👥 Customer & Contact Management
* **Customer Records**: Track company details, status (`Active`, `Lead`, `Inactive`), and assigned sales representatives.
* **Linked Contacts**: 1-to-many relationship supporting primary and secondary organizational contact persons.
* **Activity Notes**: Timeline feed of client meeting notes and communications.
* **Search & Filter**: Multi-field search (`Q` objects) and paginated listing optimized with `select_related`.

### 3. 📈 Lead Pipeline & 1-Click Conversion
* **7-Stage Sales Pipeline**: `New` → `Contacted` → `Qualified` → `Proposal` → `Negotiation` → `Won` / `Lost`.
* **Visual Kanban Board**: Drag-and-drop style stage column layout grouping active prospects.
* **1-Click Lead Conversion**: Atomic transaction (`transaction.atomic()`) that converts a `WON` lead directly into an active `Customer` and `Contact` record.

### 4. 💼 Sales Opportunity & Deal Tracking
* **Monetary Deal Tracking**: Track deal amounts ($), win probabilities (%), and target closing dates.
* **Financial Aggregation**: Real-time pipeline total values and closed-won revenue metrics calculated via Django ORM (`Sum`).

### 5. ⏱️ Task & Activity Management
* **Activities**: Schedule Calls, Meetings, Follow-ups, and Tasks linked to Customers or Deals.
* **Overdue Tracking**: Automatic calculation of overdue activities using timezone-aware datetimes.
* **1-Click Toggle**: Quick status completion toggle directly from list tables.

### 6. 📊 Executive Dashboard & Visualizations
* **KPI Metrics**: Real-time total counts for Customers, Active Leads, Won Revenue, and Pending Tasks.
* **Interactive Chart.js Visuals**:
  * **Lead Pipeline Breakdown**: Doughnut chart rendering prospect stage distribution.
  * **Opportunity Value Chart**: Bar chart displaying deal monetary values per stage.

### 7. 🌐 RESTful API Layer (Django REST Framework)
* **API Endpoints**: Full CRUD endpoints for `/api/customers/`, `/api/leads/`, `/api/opportunities/`, `/api/tasks/`, `/api/users/`.
* **Features**: ModelSerializers with nested child relations, `PageNumberPagination`, `SearchFilter`, and Session/Basic Authentication.

### 8. 🧪 Automated Testing
* Comprehensive unit test suite using Django `TestCase` and DRF `APIClient` covering models, RBAC permissions, conversion workflows, and API responses.

---

## 📐 Database Entity-Relationship (ER) Architecture

```text
+-------------------+          +-------------------+          +--------------------+
|   accounts.User   |          | customer.Customer |          |  customers.Contact |
+-------------------+          +-------------------+          +--------------------+
| id (PK)           |<--------1| id (PK)           |<--------1| id (PK)            |
| username          |  assigned| name              |   belongs| customer_id (FK)   |
| email             |          | email             |          | first_name         |
| role (ADMIN/...)  |          | company           |          | last_name          |
| phone             |          | status            |          | email              |
+-------------------+          +-------------------+          +--------------------+
    |         |                          |                              
    |         |                          |                              
    |assigned |assigned                  |customer                      
    v         v                          v                              
+-------------------+          +-------------------+          +--------------------+
|     leads.Lead    |          |  opportunities.Op |          |     tasks.Task     |
+-------------------+          +-------------------+          +--------------------+
| id (PK)           |          | id (PK)           |          | id (PK)            |
| title             |          | name              |          | title              |
| status (NEW/WON..) |          | amount            |          | task_type          |
| estimated_value   |          | stage             |          | due_date           |
+-------------------+          +-------------------+          +--------------------+
```

---

## 🛠️ Project Directory Structure

```text
CRM/
├── manage.py                # Django CLI utility
├── db.sqlite3               # Local SQLite database
├── requirements.txt         # Project dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Excluded git files
│
├── config/                  # Core project configuration
│   ├── settings.py          # Settings & INSTALLED_APPS
│   └── urls.py              # Root URL routing table
│
├── accounts/                # User authentication & RBAC roles
├── customers/               # Customer CRUD, Contacts & Notes
├── leads/                   # Lead pipeline & 1-Click conversion
├── opportunities/           # Deals, stage tracking & financial metrics
├── tasks/                   # Activity tracking & overdue logic
├── dashboard/               # Analytics & Chart.js integration
├── api/                     # DRF REST API serializers & viewsets
│
├── templates/               # Global Bootstrap 5 HTML templates
└── static/                  # Custom CSS stylesheets & assets
```

---

## 🚀 Local Installation & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** and **Git** installed.

### 2. Clone Repository
```cmd
git clone https://github.com/your-username/django-crm.git 
cd django-crm
```

### 3. Create & Activate Virtual Environment
```cmd
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```cmd
python manage.py migrate
```


### 6. Run Local Server
```cmd
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Pre-Configured Demo Credentials

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Full System & Django Admin Access |
| **Manager** | `manager1` | `manager123` | Managerial Pipeline & Team Access |
| **Sales Rep** | `sales1` | `sales123` | Sales Representative Operations |

---

## 📡 REST API Reference

Authentication required via Session (`cookie`) or Basic Auth.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/users/` | `GET` | List all user profiles |
| `/api/customers/` | `GET`, `POST`, `PUT`, `DELETE` | CRUD Customer records |
| `/api/leads/` | `GET`, `POST`, `PUT`, `DELETE` | CRUD Lead records |
| `/api/opportunities/` | `GET`, `POST`, `PUT`, `DELETE` | CRUD Sales Opportunities |
| `/api/tasks/` | `GET`, `POST`, `PUT`, `DELETE` | CRUD Tasks & Activities |

---

## 🧪 Running Automated Tests

Run the full Django unit test suite:
```cmd
python manage.py test
```


## 📄 License
This project is open-source under the [MIT License](LICENSE).
