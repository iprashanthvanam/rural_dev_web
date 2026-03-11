## Rural Development Model

##Live preview :
- https://rural-dev-web-rai3.onrender.com/

### Project Overview

Village Development is a Django-based web application created to assist rural planning and development. It allows users to:

- Enter detailed village information through a web form
- Automatically generate analytics (growth rate, density, infrastructure score, etc.)
- Produce rule-based AI recommendations for improvement
- Create visual 2D maps highlighting existing + recommended infrastructure
- Generate professionally formatted multi-page PDF reports
---

### Features

- **Data Entry:** Web form for entering comprehensive village data (demographic, infrastructure, geographic, administrative).
- **Analytics:** Real-time calculation of key development metrics.
- **AI Recommendations:** Rule-based suggestions across 9+ categories (infrastructure, education, health, sustainability, etc.).
- **Mapping:** Static map generation with emoji annotations for existing & suggested facilities.
- **Reporting:** Multi-page landscape PDF report with header, overview, infrastructure assessment, analysis, recommendations, and declaration.
- **Reliability:** Robust error handling, logging, and thread-safe Matplotlib usage.

---

### Tech Stack

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


### Installation & Setup (Step-by-step)

#### Prerequisites

- Python ≥ 3.11 (recommended: 3.13)
- PostgreSQL 15+ with PostGIS extension
- Git (optional)
- Virtual environment tool (venv / virtualenv / conda)


#### Clone & Enter Project

```bash
git clone [<your-repo-url>](https://github.com/iprashanthvanam/rural_dev_web.git
cd rural-dev-web/backend
```

For windows
```
python -m venv venv
venv\Scripts\activate
```

For Linux/Mac
```
python3 -m venv venv
source venv/bin/activate
```


#### Install Dependencies
```
pip install --upgrade pip
pip install django==5.2 psycopg2-binary geopandas matplotlib reportlab django-geo shapely
Simply : pip install -r requirements.txt
```



#### Windows (GeoPandas issues – Conda recommended)
```
conda create -n rural-dev python=3.11
conda activate rural-dev
conda install -c conda-forge geopandas
pip install django psycopg2-binary matplotlib reportlab django-geo shapely
```


#### Database Setup
```
createdb -U postgres village_web_db
psql -U postgres -d village_web_db -c "CREATE EXTENSION postgis;"
```

Update rural_dev/settings.py:
```
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
```



#### Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```



#### GeoJSON File Configuration

Place your village GeoJSON file at:

- C:\Users\<your-username>\Downloads\filtered_output.geojson

- OR update the path inside:

- village_app/utils/gis.py



#### Run Development Server
```
python manage.py runserver --insecure
```
### Open browser:
```
👉 http://127.0.0.1:8000
```
---

### Application Workflow

- User enters village data
- Backend validates & stores information
- Analytics engine computes metrics
- Rule-based logic generates recommendations
- GIS module creates annotated village map
- ReportLab generates multi-page PDF
- User downloads final development report
---

### Project Highlights

- Full-stack Django application
- GIS-enabled spatial processing
- Automated analytics & reporting
- Production-grade PDF output
- Clean, modular architecture
- Real-world rural planning use case

<h3 align="center">Village Demographic Data Entry Form</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture1.png" width="30%" />
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture2.png" width="30%" />
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture3.png" width="30%" />
</p>
<h3 align="center">Village Development Map</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture4.png" width="70%" />
</p>
<h3 align="center">Village Development Report – Overview</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture5.png" width="45%" />
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture6.png" width="45%" />
</p>
<h3 align="center">Village Development Report – Analysis & Recommendations</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture7.png" width="45%" />
  <img src="https://raw.githubusercontent.com/iprashanthvanam/rural_dev_web/main/images/Picture8.png" width="45%" />
</p>













