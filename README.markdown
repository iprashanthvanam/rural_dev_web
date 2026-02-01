# Village Development Project

**Full Project Documentation & README**  
**Last updated:** May 2025  
**Author:** Prashanth  
**Location:** Vellore, Tamil Nadu, India

## Project Overview

Village Development is a Django-based web application created to assist rural planning and development. It allows users to:

- Enter detailed village information through a web form
- Automatically generate analytics (growth rate, density, infrastructure score, etc.)
- Produce rule-based AI recommendations for improvement
- Create visual 2D maps highlighting existing + recommended infrastructure
- Generate professionally formatted multi-page PDF reports

The project demonstrates a full-stack rural development planning tool using:

- Django (web framework)
- PostgreSQL + PostGIS (spatial database)
- GeoPandas + Matplotlib (static map generation)
- ReportLab (PDF generation)
- Rule-based recommendation engine

## Features

- Web form for entering comprehensive village data (demographic, infrastructure, geographic, administrative)
- Real-time calculation of key development metrics
- AI-style recommendations across 9+ categories (infrastructure, education, health, sustainability, etc.)
- Static map generation with emoji annotations for existing & suggested facilities
- Multi-page landscape PDF report with header, overview, infrastructure assessment, analysis, recommendations and declaration
- Robust error handling & logging
- Thread-safe Matplotlib usage in server environment

## Tech Stack

| Layer              | Technology                              | Purpose                              |
|---------------------|------------------------------------------|--------------------------------------|
| Backend            | Django 5.2                               | Web framework, ORM, views, routing   |
| Database           | PostgreSQL 15 + PostGIS                  | Relational + spatial data storage    |
| Mapping            | GeoPandas, Matplotlib ('Agg' backend)    | Static 2D map generation             |
| PDF Generation     | ReportLab                                | Professional multi-page PDF reports  |
| Analytics          | Pure Python + Matplotlib                 | Metric calculation & bar charts      |
| Recommendations    | Rule-based logic                         | Actionable suggestions               |
| Logging            | Python logging module                    | Debug & production monitoring        |

## Installation & Setup (Step-by-step)

### 1. Prerequisites

- Python ≥ 3.11 (recommended: 3.13)
- PostgreSQL 15+ with PostGIS extension
- Git (optional)
- Virtual environment tool (venv / virtualenv / conda)

### 2. Clone / Create Project Folder

bash
git clone <your-repo-url> rural-dev-web
cd rural-dev-web/backend

3. Create & Activate Virtual Environment
Bashpython -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

4. Install Dependencies
Bashpip install --upgrade pip
pip install django==5.2 psycopg2-binary geopandas matplotlib reportlab django-geo shapely
Windows users with GeoPandas issues — you may need to install precompiled wheels or use conda:
Bashconda create -n rural-dev python=3.11
conda activate rural-dev
conda install -c conda-forge geopandas
pip install django psycopg2-binary matplotlib reportlab django-geo shapely

5. Database Setup

Install PostgreSQL + PostGIS
Create database:

Bashcreatedb -U postgres village_web_db
psql -U postgres -d village_web_db -c "CREATE EXTENSION postgis;"

Update rural_dev/settings.py:

PythonDATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'village_web_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Apply migrations:

Bashpython manage.py makemigrations
python manage.py migrate

6. GeoJSON File
Place your village features GeoJSON file at:
textC:\Users\<your-username>\Downloads\filtered_output.geojson
Or update the path inside village_app/utils/gis.py

7. Run the Development Server
Bashpython manage.py runserver --insecure
Open browser → http://127.0.0.1:8000/

