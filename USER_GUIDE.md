# Enterprise CRM — System Workflow & Operational User Guide

Welcome to the **Enterprise Small-Business CRM Platform**. This documentation explains the complete lifecycle of customer data, business sales workflows, role permissions, and step-by-step instructions on how to access and manage every section of the system.

---

## 📌 Table of Contents
1. [Core Architecture & CRM Lifecycle](#1-core-architecture--crm-lifecycle)
2. [User Roles & Access Levels](#2-user-roles--access-levels)
3. [Quick Start & Accessing the System](#3-quick-start--accessing-the-system)
4. [Step-by-Step Workflow Guides](#4-step-by-step-workflow-guides)
   - [A. Executive Dashboard & Analytics](#a-executive-dashboard--analytics)
   - [B. Lead Generation & Kanban Pipeline](#b-lead-generation--kanban-pipeline)
   - [C. 1-Click Lead-to-Customer Conversion](#c-1-click-lead-to-customer-conversion)
   - [D. Customer Account & Contact Management](#d-customer-account--contact-management)
   - [E. Opportunity & Deal Tracking](#e-opportunity--deal-tracking)
   - [F. Tasks, Activities & Overdue Follow-ups](#f-tasks-activities--overdue-follow-ups)
   - [G. User Profiles & System Settings](#g-user-profiles--system-settings)
5. [Top Navigation, Shortcuts & Global Search](#5-top-navigation-shortcuts--global-search)
6. [Django REST Framework API Access](#6-django-rest-framework-api-access)
7. [Developer & Deployment Reference](#7-developer--deployment-reference)

---

## 1. Core Architecture & CRM Lifecycle

The application automates the sales journey from first prospect contact to closing deals and retaining long-term customer accounts.

```mermaid
graph TD
    A[New Lead / Inquiry] -->|Sales Rep Outreach| B(Contacted)
    B -->|Discovery & Budget Check| C(Qualified)
    C -->|Send Proposal & Quote| D(Proposal)
    D -->|Contract Review| E(Negotiation)
    E -->|Deal Won!| F[1-Click Lead Conversion]
    E -->|Deal Lost| L[Mark Lost]
    F -->|Atomic Database Transaction| G[(Active Customer Record)]
    G --> H[Primary & Secondary Contacts]
    G --> I[Sales Opportunities / Deals]
    G --> J[Follow-up Tasks, Calls & Meetings]
    G --> K[Meeting Notes & Activity Timeline]
```

### Data Relationship Highlights
- **Leads**: Top-of-funnel prospects. They can be tracked through 7 distinct pipeline stages on a visual Kanban board or list table.
- **Conversion**: When a lead reaches `WON`, a 1-click atomic transaction converts the lead into an active **Customer** record and creates their **Primary Contact**.
- **Customer 360°**: Customer records hold linked contacts, communication notes, monetary opportunities, and scheduled activities.
- **Opportunities (Deals)**: Revenue-generating projects tied to customer accounts with deal values ($), win probabilities (%), and target closing dates.
- **Tasks**: Time-sensitive action items (Calls, Meetings, Follow-ups, Tasks) with automatic overdue detection based on server time.

---

## 2. User Roles & Access Levels

The CRM implements Role-Based Access Control (RBAC) via a custom user model:

| Role | Default Access Scope | Capabilities |
| :--- | :--- | :--- |
| 🛡️ **Admin** | System-wide | Full operational rights across all accounts, leads, deals, tasks, plus direct access to the **Django Admin Portal** (`/admin/`). |
| 💼 **Manager** | Team & Pipeline Oversight | Full visibility into all customer accounts, team pipeline values, stage transitions, and managerial analytics. |
| 👤 **Sales Rep** | Assigned Accounts & Daily Sales | Day-to-day operations: managing assigned prospects, moving leads through stages, updating customer records, creating deals, and logging follow-up tasks. |

### Demo Credentials
| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` |
| **Manager** | `manager1` | `manager123` |
| **Sales Rep** | `sales1` | `sales123` |

---

## 3. Quick Start & Accessing the System

### 1. Launch the Server
Ensure the virtual environment is activated and the Django server is running:
```powershell
.\venv\Scripts\activate
python manage.py runserver
```

### 2. Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```
If you are not authenticated, you will automatically be redirected to the **Sign In** page (`/accounts/login/`).

---

## 4. Step-by-Step Workflow Guides

### A. Executive Dashboard & Analytics
- **URL**: `http://127.0.0.1:8000/dashboard/`
- **Purpose**: High-level executive overview of sales velocity and urgent tasks.
- **Key Features**:
  - **4 KPI Metric Cards**:
    - **Total Accounts**: Total customer accounts currently in the CRM.
    - **Active Prospects**: Number of active leads in qualification.
    - **Won Revenue**: Real-time sum of closed-won opportunities + total pipeline valuation.
    - **Pending Tasks**: Active action items, with immediate visual badges if any task is **Overdue**.
  - **Lead Pipeline Distribution**: Interactive doughnut chart displaying the proportion of prospects in each stage.
  - **Deal Valuation by Stage**: Bar chart aggregating monetary values ($) by deal stage.
  - **Live Feeds**: Recent client accounts, incoming leads, and upcoming action items with direct links.

---

### B. Lead Generation & Kanban Pipeline
- **List View**: `http://127.0.0.1:8000/leads/`
- **Kanban Board**: `http://127.0.0.1:8000/leads/pipeline/`

#### 1. Adding a New Lead
1. Click the **`+ New`** button in the top navbar or on the Leads page and choose **`New Lead`**.
2. Complete the lead details:
   - **Title**: Short summary of the prospect opportunity (e.g. `Cloud Migration Project`).
   - **Contact Name & Company**: First name, last name, and organization.
   - **Email & Phone**: Primary communication channel.
   - **Lead Source**: Website, Referral, Cold Call, LinkedIn, Event, or Other.
   - **Stage**: New, Contacted, Qualified, Proposal, Negotiation, Won, or Lost.
   - **Priority**: Low, Medium, or High.
   - **Estimated Value ($)**: Projected contract size.
   - **Assigned Representative**: Sales rep responsible for the prospect.
   - **Follow-up Date**: Target next touchpoint.
3. Click **Save Lead**.

#### 2. Visual Kanban Board
Navigate to **Leads & Pipeline** → **Kanban Pipeline** (`/leads/pipeline/`):
- Columns group leads across the 7 pipeline stages.
- Each card displays lead title, company, priority tag, monetary value, and quick-action buttons.
- Click the pencil icon to update a lead's stage or click the arrow icon to trigger 1-click conversion.

---

### C. 1-Click Lead-to-Customer Conversion
When a prospect agrees to terms and is marked **WON**:
1. From the Lead Detail page or Kanban card, click **`Convert to Customer`**.
2. You will be prompted with a confirmation screen summarizing the customer record to be generated.
3. Click **`Confirm Conversion`**.
4. The system executes a database transaction (`transaction.atomic()`):
   - Creates a new active **Customer** profile (or links to an existing customer if the email matches).
   - Generates a **Primary Contact** under that customer with the lead's contact details.
   - Sets the lead's status to `WON`.
   - Redirects you straight to the newly created Customer 360° profile.

---

### D. Customer Account & Contact Management
- **Customer List**: `http://127.0.0.1:8000/customers/`
- **Customer Detail**: `http://127.0.0.1:8000/customers/<id>/`

#### 1. Finding & Filtering Customers
- Use the **Search bar** on the customer list page to filter by name, company, email, or phone.
- Use the **Status dropdown** to filter by `Active Customer`, `Lead`, or `Inactive`.

#### 2. Customer 360° Profile
Opening any customer record displays:
- **Customer Overview**: Company name, status badge, email, phone, office address, and assigned sales rep.
- **Linked Contacts**: List of all stakeholders at the company. Click **`Add Contact`** to add additional contacts with custom designations (e.g. CTO, Finance Director).
- **Communication & Meeting Notes**: Timeline of notes logged by sales reps. Type meeting minutes into the note box and submit to append to the client history.
- **Deals & Opportunities**: All active or historical sales opportunities tied to this client.
- **Scheduled Tasks**: Calls, meetings, or reminders specifically linked to this customer account.

---

### E. Opportunity & Deal Tracking
- **URL**: `http://127.0.0.1:8000/opportunities/`

#### 1. Creating a Deal
1. Click **`+ New`** in the top navbar → **`New Deal`** (or navigate to Opportunities → Add Opportunity).
2. Specify:
   - **Deal Name**: e.g., `Enterprise SaaS Subscription — 100 Seats`.
   - **Customer**: Select the parent customer organization.
   - **Amount ($)**: Total deal valuation.
   - **Stage**: Qualification, Needs Analysis, Proposal / Price Quote, Negotiation, Closed Won, or Closed Lost.
   - **Win Probability (%)**: Estimated percentage chance of closing (0–100%).
   - **Target Closing Date**: Expected contract signature date.
   - **Assigned Representative**: Owner of the deal.
3. Click **Save Opportunity**.

#### 2. Financial Metrics
The Opportunity page automatically calculates:
- **Total Pipeline Valuation**: Aggregate monetary sum of all open deals.
- **Closed Won Revenue**: Sum of all deals reaching the `Closed Won` stage.

---

### F. Tasks, Activities & Overdue Follow-ups
- **URL**: `http://127.0.0.1:8000/tasks/`

#### 1. Scheduling an Activity
1. Click **`+ New`** in the top navbar → **`New Task`**.
2. Fill in:
   - **Task Title**: Description of the activity (e.g., `Demo Presentation Call`).
   - **Activity Type**: Phone Call, Meeting, Follow-up, or General Task.
   - **Priority**: Low, Medium, or High.
   - **Due Date & Time**: Target deadline for completion.
   - **Related Record**: Optionally link the task to a specific **Customer**, **Lead**, or **Opportunity**.
3. Click **Create Task**.

#### 2. Completing & Toggling Tasks
- Tasks can be toggled between `Pending` and `Completed` directly by clicking the status circle icon on the task table.
- Any task past its `due_date` that is still `Pending` or `In Progress` is automatically flagged as **Overdue** with an alert badge and highlighted in red on both the list and the dashboard.

---

### G. User Profiles & System Settings
- **URL**: `http://127.0.0.1:8000/accounts/profile/`
- View your operational role, assigned customer account counts, active leads, and pending tasks.
- Update your First Name, Last Name, Email Address, Phone Number, and Bio.

---

## 5. Top Navigation, Shortcuts & Global Search

The top header is pinned across all pages and provides the following features:

| Feature | How to Use |
| :--- | :--- |
| **Global Omni-Search** | Click the search box or press **`Ctrl+K`** (or `⌘K` on Mac) to immediately focus and search records across the system. |
| **`+ New` Quick Create** | Click the primary dropdown button in the top right to instantly create a Lead, Customer, Deal, or Task from anywhere. |
| **Theme Toggle (Sun/Moon)** | Click the sun/moon button to switch between **Light Mode** and **Dark Mode**. Your preference is saved in your browser. |
| **User Profile Dropdown** | Click your user initials/avatar in the top right to access **Account Settings**, **My Activities**, or **Sign Out**. |
| **Mobile Drawer** | On mobile or tablet devices, click the hamburger icon (`☰`) to open the sliding navigation drawer. |

---

## 6. Django REST Framework API Access

The application includes a REST API powered by Django REST Framework (DRF):

### Authentication
API endpoints support both **Session Authentication** (browser cookies) and **Basic Authentication** (`Authorization: Basic <base64>`).

### Key Endpoints
| Resource | URL Endpoint | Supported Methods | Description |
| :--- | :--- | :--- | :--- |
| **Users** | `/api/users/` | `GET` | List CRM users and assigned roles |
| **Customers** | `/api/customers/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | Full CRUD operations for client accounts |
| **Leads** | `/api/leads/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | Full CRUD operations for sales leads |
| **Opportunities** | `/api/opportunities/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD operations for deals & financials |
| **Tasks** | `/api/tasks/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD operations for follow-up activities |

### Interactive Browsable API
Log into the web application, then navigate directly to:
```
http://127.0.0.1:8000/api/
```
You can inspect schemas, send `POST` payloads, and test filters directly in your browser.

---

## 7. Developer & Deployment Reference

### Running System Tests
Run the automated test suite covering models, roles, conversions, and API responses:
```powershell
.\venv\Scripts\activate
python manage.py test
```

### Running Django Deployment Security Checks
```powershell
python manage.py check --deploy
```

### Applying Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

---

*Enterprise CRM Documentation — Built with Django 5+, Bootstrap 5.3, Chart.js, and Django REST Framework.*
