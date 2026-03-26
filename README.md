# Climatology Lab Website

A comprehensive, Django-based dynamic website and administrative dashboard built for the **Climatology Lab at IIT Roorkee** (Department of Architecture and Planning). This platform serves as the central hub for the lab's digital presence, showcasing research projects, team profiles, publications, and workshop announcements, while providing a powerful, authenticated dashboard for content management.

---

## 🚀 Features & Functionalities

- **Public-Facing Website:**
  - **Dynamic Homepage:** Real-time statistics, laboratory overview, and recent highlights.
  - **Research Portfolios:** Detailed pages for ongoing and completed projects, including investigator tracking.
  - **Interactive Team Directory:** Profiles for PIs, Co-PIs, researchers, and alumni.
  - **Publications Hub:** A comprehensive library of research papers, journal articles, and book chapters.
  - **Notice Board / Workshops:** Announcements for upcoming events and workshops.
  - **Contact & Feedback:** Integrated contact form with email routing and submission tracking.
  - **Responsive Design:** A polished UI built with Bootstrap 5, optimized for mobile and desktop viewing.

- **Administrative Dashboard (`/dashboard/`):**
  - **Secure Authentication:** OTP-enabled password reset, robust session management (24-hour persistence), and localized role-based access.
  - **Full CRUD Management:** Create, read, update, and delete entries for all public-facing modules (Projects, Team, Publications, Workshops).
  - **Data Import/Export:** Bulk import via CSV and export features for Publications and other key metrics.
  - **Media Management:** Direct integration with AWS S3 / Supabase for secure, scalable image and document hosting.

---

## 🛠 Tech Stack

- **Backend:** Python 3.12+, Django 5.2.10
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Crispy Forms (`crispy-bootstrap5`)
- **Database:** SQLite (Development) / PostgreSQL (Production ready vi `dj-database-url`)
- **Web Servers / Tools:** 
  - Waitress (Windows App Server)
  - Nginx (Reverse Proxy & SSL termination)
  - Whitenoise (Static file serving)
- **Cloud & External Services:**
  - AWS SES (Simple Email Service) for SMTP
  - Supabase / AWS S3 (via `django-storages` and `boto3`) for media storage
- **Libraries:** Pillow (image processing), pandas/tablib (data export), BeautifulSoup4.

---

## ⚙️ Installation & Setup Instructions

### Prerequisites
- Python 3.12+ installed
- Git
- PowerShell (if deploying on Windows Server)

### Local Development Setup (Step-by-Step)

1. **Clone the Repository**
   ```powershell
   git clone <repository_url>
   cd "C:\ClimatologyLab" # or your local path
   ```

2. **Create and Activate Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Environment Variables Configuration**
   Duplicate `.env.production` (or create a new `.env` file) in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-local-secret-key-development
   ALLOWED_HOSTS=*
   ```

5. **Apply Database Migrations**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create an Admin User**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```powershell
   python manage.py runserver
   ```
   *Access the site at `http://localhost:8000/`*

---

## 📖 Usage Guide

- **Public Visitors:** Navigate to the root URL (`/`) to browse lab statistics, publications, and projects. Use the Contact tab to get in touch with the lab.
- **Lab Administrators:**
  1. Navigate to `http://localhost:8000/accounts/login/` (or `/dashboard/`).
  2. Log in using the superuser credentials.
  3. Use the sidebar to navigate between managing Team Members, Publications, Workshops, and dynamic Homepage Statistics.
  4. To add publications in bulk, click on "Import" inside the Publications dashboard view.

---

## 📂 Project Structure

```text
Lab/
├── config/              # Central Django settings, core configurations, and root URL routing
├── core/                # Frontend web application (views for homepage, context processors)
├── dashboard/           # Comprehensive secure backend dashboard (forms, CRUD views, templates)
├── team/                # App handling team member models and public team listing
├── projects/            # App handling research projects and grants
├── publications/        # App handling publications, citations, and CSV imports
├── workshops/           # App handling the notice board and workshop registrations
├── contact/             # Form logic, email dispatching, and admin tracking for queries
├── templates/           # Global HTML templates (Base layouts, navbars, footers)
├── static/              # Global CSS, JS, and static frontend assets
├── media/               # Local storage directory for file/image uploads (Dev only)
├── .env                 # Environment variables configuration (ignored in git)
├── manage.py            # Django command-line utility
└── requirements.txt     # Complete list of Python dependencies
```

---

## 🔗 Main Endpoints & Routes

While not a headless REST API, the application relies on strict URL routing for navigation and operations:

- **Public Routes:**
  - `/` - Homepage
  - `/projects/` - Research Projects Gallery
  - `/team/` - Team Directory
  - `/publications/` - Publications Database
  - `/contact/` - Contact Form

- **Secure Dashboard Routes (Requires Auth):**
  - `/dashboard/` - Admin Overview
  - `/dashboard/projects/` - Portfolio Management
  - `/dashboard/publications/` - Publications CRUD & Import/Export
  - `/dashboard/team/` - Team Member Management
  - `/dashboard/password-reset/` - OTP Password Recovery Utility
  - `/management-console/` - Default Django Admin (renamed for security constraints)

---

## 🖼 UI Description

- **Frontend Website:** Modern, research-focused aesthetic prioritizing whitespace, crisp typography, and high-quality imagery. Employs a primary blue/white color scheme consistent with IIT Roorkee's branding guidelines. Features responsive grids for publications and card-based layouts for team members.
- **Admin Dashboard:** A streamlined, functional dark-sidebar interface built on Bootstrap 5. It features tabular data views, modal popups for quick edits, and Crispy Forms for elegant, error-validated data entry.

---

## ⚠️ Known Issues / Limitations

- **Media Storage in Production:** The application relies on external S3/Supabase storage in production. If the environment variables (`SUPABASE_S3_ENDPOINT`, etc.) are omitted, image uploads will fall back to local storage which may be ephemeral depending on the hosting provider.
- **Email Delivery Restrictions:** AWS SES is strictly configured. If the `EMAIL_HOST_USER` is not verified in AWS or sandbox mode is active, the contact form may fail to dispatch emails.

---

## 🔮 Future Improvements

- Fully transition the frontend to a headless REST/GraphQL architecture (e.g., Django Ninja or DRF paired with React/Next.js) for greater interactivity.
- Implement Elasticsearch or PostgreSQL Full-Text Search for deep querying across the publications database.
- Add an automated BibTeX parser/importer for dynamic bibliography generation.

---

## 🧑‍💻 Author Details

**Developed By:** Chanchal Suthar  
**Maintained For:** Climatology Lab, Department of Architecture and Planning, IIT Roorkee  
**Contact:** climatologylab@ar.iitr.ac.in

---

## 📄 License

Created exclusively for the Climatology Lab, IIT Roorkee. All rights reserved. Do not distribute or replicate without explicit authorization from the principal investigators.
