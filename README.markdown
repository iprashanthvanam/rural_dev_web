# Village Development Project

**Full Project Documentation & README**  
**Last updated:** May 2025  
**Author:** Prashanth  
**Location:** Hyderabad, Telangana, India  

---

## Project Overview

Village Development is a Django-based web application created to assist rural planning and development. It allows users to:

- Enter detailed village information through a web form
- Automatically generate analytics (growth rate, density, infrastructure score, etc.)
- Produce rule-based AI recommendations for improvement
- Create visual 2D maps highlighting existing + recommended infrastructure
- Generate professionally formatted multi-page PDF reports

The project demonstrates a full-stack rural development planning tool using:

- **Django** (web framework)
- **PostgreSQL + PostGIS** (spatial database)
- **GeoPandas + Matplotlib** (static map generation)
- **ReportLab** (PDF generation)
- **Rule-based recommendation engine**

---

## Features

- **Data Entry:** Web form for entering comprehensive village data (demographic, infrastructure, geographic, administrative).
- **Analytics:** Real-time calculation of key development metrics.
- **AI Recommendations:** Rule-based suggestions across 9+ categories (infrastructure, education, health, sustainability, etc.).
- **Mapping:** Static map generation with emoji annotations for existing & suggested facilities.
- **Reporting:** Multi-page landscape PDF report with header, overview, infrastructure assessment, analysis, recommendations, and declaration.
- **Reliability:** Robust error handling, logging, and thread-safe Matplotlib usage.

---

## Tech Stack

| Layer | Technology | Purpose |
|------|------------|---------|
| **Backend** | Django 5.2 | Web framework, ORM, views, routing |
| **Database** | PostgreSQL 15 + PostGIS | Relational + spatial data storage |
| **Mapping** | GeoPandas, Matplotlib ('Agg') | Static 2D map generation |
| **PDF Gen** | ReportLab | Professional multi-page PDF reports |
| **Analytics** | Pure Python + Matplotlib | Metric calculation & bar charts |
| **Logic** | Rule-based logic | Actionable suggestions |
| **Logging** | Python logging module | Debug & production monitoring |

---


---

## Installation & Setup (Step-by-step)

### 1. Prerequisites

- Python ≥ 3.11 (recommended: 3.13)
- PostgreSQL 15+ with PostGIS extension
- Git (optional)
- Virtual environment tool (venv / virtualenv / conda)

---

### 2. Clone & Enter Project

```bash
git clone <your-repo-url>
cd rural-dev-web/backend

For windows:
python -m venv venv
venv\Scripts\activate

For Linux/Mac
python3 -m venv venv
source venv/bin/activate

---

### 3. Install Dependencies

pip install --upgrade pip
pip install django==5.2 psycopg2-binary geopandas matplotlib reportlab django-geo shapely
Simply : pip install -r requirements.txt

---

### 4. Windows (GeoPandas issues – Conda recommended)

conda create -n rural-dev python=3.11
conda activate rural-dev
conda install -c conda-forge geopandas
pip install django psycopg2-binary matplotlib reportlab django-geo shapely

---

### 5. Database Setup

createdb -U postgres village_web_db
psql -U postgres -d village_web_db -c "CREATE EXTENSION postgis;"

Update rural_dev/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'village_web_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


---

### 6. Apply Migrations

python manage.py makemigrations
python manage.py migrate


---

### 7. GeoJSON File Configuration

Place your village GeoJSON file at:
C:\Users\<your-username>\Downloads\filtered_output.geojson

OR update the path inside:
village_app/utils/gis.py

---

### 8. Run Development Server

python manage.py runserver --insecure
Open browser:
👉 http://127.0.0.1:8000/




















