# Climatology Lab Website

A Django-based website for the Climatology Lab at IIT Roorkee, Department of Architecture and Planning.

## Features

- Homepage with dynamic statistics
- Notice board for workshops and events
- Team members management
- Research projects showcase
- Publications repository
- Contact form with submission tracking
- Fully responsive design
- Comprehensive admin panel

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone or navigate to the project directory**
```bash
cd "c:\Users\Gourav\OneDrive\Desktop\Internship IITR\Lab"
```

2. **Activate virtual environment**
```bash
.\venv\Scripts\activate
```

3. **The dependencies are already installed**
- Django 5.2.10
- Pillow

### Database

The database is already set up and migrated. To reset or create migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin User

A superuser has been created:
- Username: `admin`
- Email: `admin@climatologylab.com`

Set the password:
```bash
python manage.py changepassword admin
```

## Running the Application

```bash
python manage.py runserver
```

Visit:
- Homepage: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/

## Project Structure

```
Lab/
├── config/              # Project settings
├── core/                # Main app (homepage, static pages)
├── team/                # Team members
├── projects/            # Research projects
├── publications/        # Publications
├── workshops/           # Notice board
├── contact/             # Contact form
├── templates/           # HTML templates
├── static/             # CSS, JavaScript, images
├── media/              # Uploaded files
└── manage.py
```

## Apps

### Core
- Site settings
- Homepage statistics (publications, projects, outreach count)
- Homepage content

### Workshops
- Notice board entries
- Workshop announcements

### Team
- Team member profiles
- Photos and bios
- Research interests

### Projects
- Research projects
- Principal investigators
- Co-investigators
- Project status tracking

### Publications
- Research publications
- Journal articles
- Conference papers
- PDF uploads

### Contact
- Contact form submissions
- Admin tracking

## Admin Panel

Access at `/admin/` to manage:
- Site settings
- Homepage statistics
- Workshops and notices
- Team members
- Research projects
- Publications
- Contact submissions

## Design

The website preserves the original design exactly:

### Colors
- Primary Blue: #4A90E2
- Dark Blue: #1E3A5F (footer)
- Light Blue: #B8D4F1
- Red: #E74C3C
- Yellow: #F1C40F
- Green: #2ECC71 (submit button)
- Black: #000000

### Layout
- Responsive grid design
- Stats section with circular badges
- Notice board with card layout
- Two-tone footer with contact form

## URLs

| Page | URL |
|------|-----|
| Homepage | `/` |
| Projects | `/projects/` |
| Team | `/team/` |
| Publications | `/publications/` |
| Learn | `/learn/` |
| Impact | `/impact/` |
| Contact | `/contact/` |
| Admin | `/admin/` |

## Development

### Adding Content

Use the admin panel to add:
1. Homepage statistics
2. Workshop notices
3. Team members
4. Research projects
5. Publications

### Customization

- **Templates**: Edit files in `templates/`
- **Styling**: Modify `static/css/main.css`
- **JavaScript**: Edit `static/js/main.js`
- **Models**: Update `models.py` in each app

### Deployment

For production:
1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL recommended)
4. Configure email backend for contact form
5. Collect static files: `python manage.py collectstatic`
6. Use a production server (Gunicorn, uWSGI)
7. Set up HTTPS

## Technologies

- **Backend**: Django 5.2.10
- **Database**: SQLite (development), PostgreSQL (recommended for production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Image Processing**: Pillow

## License

Created for the Climatology Lab, IIT Roorkee.

Designed by Anush Rana, Created by Abhishek Saini.

## Support

For issues or questions, contact the development team.
