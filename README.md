# Enterprise Small-Business Django CRM System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)
![REST API](https://img.shields.io/badge/DRF-REST%20API-red?logo=django)
![License](https://img.shields.io/badge/License-MIT-green)

A production-grade, full-stack **Customer Relationship Management (CRM) System** built with Python, Django, SQLite, Bootstrap 5, Chart.js, and Django REST Framework. Features an executive analytics dashboard, interactive lead Kanban pipeline, 1-click lead-to-customer conversion, full contact/opportunity/task tracking, a public marketing landing page with interactive ROI calculator, and a fully customized enterprise Django Admin portal.

📖 **For detailed operational workflows, UI navigation, and user instructions, see the [Complete User & Operational Guide](USER_GUIDE.md).**

---

## 🌟 Key Features

### 1. 🌐 Public SaaS Landing Page (`/`)
* **Enterprise Showcase**: Modern marketing homepage highlighting CRM capabilities, feature pillars, live customer metrics, and client testimonials.
* **Interactive ROI Calculator**: Dynamic client-side widget allowing visitors to calculate projected annual revenue lift and time saved based on sales team size and deal volume.
* **Seamless Onboarding**: Unauthenticated visitors explore the platform and navigate directly to Sign In or Registration. Authenticated users are automatically routed to the Executive Dashboard.
* **Dual Theme Support**: Fully responsive design with immediate Dark Mode and Light Mode switching.

### 2. 🔐 Authentication & Role-Based Access Control (RBAC)
* **Custom User Model**: Extends `AbstractUser` with operational roles (`ADMIN`, `MANAGER`, `SALES_REP`), phone, and bio.
* **Role-Based Security**: Custom view decorators (`@admin_required`, `@manager_required`) and class-based view mixins.
* **Modernized Login Experience**: Glassmorphic authentication card with password visibility toggles, remember-me support, and **1-Click Demo Login pills** (`Admin`, `Manager`, `Sales Rep`) for instant testing.
* **User Profiles**: Personal dashboard displaying assigned customer accounts, leads, and task metrics.

### 3. 👥 Customer & Contact Management
* **Customer Records**: Track company details, operational status (`Active Customer`, `Lead`, `Inactive`), and assigned sales representatives.
* **Linked Contacts**: 1-to-many relationship supporting primary and secondary organizational contact persons with custom designations.
* **Activity Notes**: Timeline feed of client meeting minutes and logged communications.
* **Search & Filter**: Multi-field search (`Q` objects) and paginated listing optimized with `select_related`.

### 4. 📈 Lead Pipeline & 1-Click Conversion
* **7-Stage Sales Pipeline**: `New` → `Contacted` → `Qualified` → `Proposal` → `Negotiation` → `Won` / `Lost`.
* **Visual Kanban Board**: Drag-and-drop style column layout grouping active prospects with priority tags and valuation badges.
* **1-Click Lead Conversion**: Atomic transaction (`transaction.atomic()`) that converts a `WON` lead directly into an active `Customer` and `Contact` record.

### 5. 💼 Sales Opportunity & Deal Tracking
* **Monetary Deal Tracking**: Track deal amounts ($), win probabilities (%), and target closing dates.
* **Financial Aggregation**: Real-time pipeline total values and closed-won revenue metrics calculated via Django ORM (`Sum`).
* **Overdue Warnings**: Dynamic indicators highlighting opportunities past their target close date.

### 6. ⏱️ Task & Activity Management
* **Activities**: Schedule Calls, Meetings, Follow-ups, and Tasks linked to Customers, Leads, or Deals.
* **Overdue Tracking**: Automatic calculation of overdue activities using timezone-aware datetimes with visual alerts (`🚨 OVERDUE`).
* **1-Click Toggle**: Quick status completion toggle directly from list tables.

### 7. 📊 Executive Dashboard & Visualizations
* **Real-time KPI Metrics**: Live counters with percentage trends for Total Accounts, Active Prospects, Won Revenue, and Pending Tasks.
* **Interactive Chart.js Visuals**:
  * **Lead Pipeline Breakdown**: Doughnut chart rendering prospect stage distribution with theme-aware colors.
  * **Opportunity Value Chart**: Bar chart displaying deal monetary values per stage.
* **Live Feeds**: Recent client accounts, incoming leads, and upcoming action items with direct links.

### 8. 🛠️ Customized Enterprise Django Admin Portal (`/admin/`)
* **Enterprise Branding**: Styled with `Enterprise CRM Administration` branding, Google Fonts (*Plus Jakarta Sans* & *Inter*), and dark navy header styling.
* **Integrated Navigation**: Header quick-launch links between the **Django Admin**, the **CRM Dashboard** (`/dashboard/`), and the public **Website** (`/`).
* **Rich ModelAdmins**:
  * **User Admin**: Color-coded role badges, full name display, and bulk role assignment actions.
  * **Customer Admin**: Status badges, linked contacts count, total won revenue calculation, and inline contacts/notes.
  * **Lead Admin**: 7-stage status pills, priority badges, formatted valuations, and pipeline advancement actions.
  * **Opportunity Admin**: Visual probability progress bars, weighted valuation calculations, and closing date alerts.
  * **Task Admin**: Task type icons (`📞 Call`, `👥 Meeting`, etc.), priority pills, overdue alert tags, and status actions.

### 9. 🌐 RESTful API Layer (Django REST Framework)
* **API Endpoints**: Full CRUD endpoints for `/api/customers/`, `/api/leads/`, `/api/opportunities/`, `/api/tasks/`, `/api/users/`.
* **Features**: ModelSerializers with nested child relations, `PageNumberPagination`, `SearchFilter`, and Session/Basic Authentication.
* **Browsable API**: Interactive DRF web interface at `/api/` for testing payloads.

### 10. 🧪 Automated Testing
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
├── README.md                # Project overview and setup documentation
├── USER_GUIDE.md            # Comprehensive operational & user guide
│
├── config/                  # Core project configuration
│   ├── settings.py          # Settings & INSTALLED_APPS
│   ├── urls.py              # Root URL routing & Admin site branding
│   └── wsgi.py              # WSGI entry point
│
├── accounts/                # User authentication, profiles & RBAC roles
│   ├── models.py            # User model with Role choices
│   ├── views.py             # Login, register, profile views
│   └── admin.py             # CustomUserAdmin with role badges & actions
│
├── customers/               # Customer CRUD, Contacts & Notes
│   ├── models.py            # Customer, Contact, Note models
│   └── admin.py             # CustomerAdmin with revenue metrics & inlines
│
├── leads/                   # Lead pipeline & 1-Click conversion
│   ├── models.py            # Lead model with 7 pipeline stages
│   └── admin.py             # LeadAdmin with stage pills & pipeline actions
│
├── opportunities/           # Deals, stage tracking & financial metrics
│   ├── models.py            # Opportunity model
│   └── admin.py             # OpportunityAdmin with progress bars & weighted values
│
├── tasks/                   # Activity tracking & overdue logic
│   ├── models.py            # Task model with overdue property
│   └── admin.py             # TaskAdmin with type badges & overdue alerts
│
├── dashboard/               # Analytics & Chart.js integration
│   └── views.py             # Aggregated KPI and chart metrics
│
├── api/                     # DRF REST API serializers & viewsets
│   ├── serializers.py       # Model serializers
│   └── views.py             # ModelViewSets with permissions & filters
│
├── templates/               # Global HTML templates
│   ├── base.html            # Base layout with navbar, theme toggle & shortcuts
│   ├── landing/             # Public marketing landing page & ROI calculator
│   ├── admin/               # Custom Django Admin base template & branding
│   ├── accounts/            # Sign in, registration & profile templates
│   ├── dashboard/           # Executive analytics dashboard
│   ├── customers/           # Customer list, detail, and form views
│   ├── leads/               # Lead list, form, and Kanban pipeline views
│   ├── opportunities/       # Deal list and form views
│   └── tasks/               # Task list and form views
│
└── static/                  # Static assets & stylesheets
    ├── css/
    │   └── style.css        # Enterprise design system (Light & Dark theme)
    ├── admin/
    │   └── css/
    │       └── custom_admin.css # Custom Django Admin stylesheet
    └── js/
        └── dashboard.js     # Chart.js initialization & dynamic theme switcher
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
**Windows (PowerShell / Command Prompt):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```cmd
python manage.py migrate
```

### 6. Run Local Development Server
```cmd
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Pre-Configured Demo Credentials

The login screen (`/accounts/login/`) includes **1-Click Demo Login pills** to instantly autofill these credentials:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| 🛡️ **Admin** | `admin` | `admin123` | Full System Governance & Django Admin (`/admin/`) |
| 💼 **Manager** | `manager1` | `manager123` | Pipeline Oversight, Analytics & Team Accounts |
| 👤 **Sales Rep** | `sales1` | `sales123` | Day-to-Day Leads, Customers, Deals & Tasks |

---

## 📡 REST API Reference

Authentication is supported via **Session Authentication** (browser cookies) or **Basic Authentication** (`Authorization: Basic <base64>`).

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/users/` | `GET` | List all user profiles and roles |
| `/api/customers/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | Full CRUD operations for customer records |
| `/api/leads/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | Full CRUD operations for sales leads |
| `/api/opportunities/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD operations for deals & financials |
| `/api/tasks/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD operations for tasks & activities |

An interactive browsable API is available at `http://127.0.0.1:8000/api/`.

---

## 🧪 Running Automated Tests

Run the comprehensive Django unit test suite:
```powershell
python manage.py test
```

All 7 core automated test suites validate RBAC security, lead-to-customer conversion atomicity, financial aggregations, and REST API endpoints.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
