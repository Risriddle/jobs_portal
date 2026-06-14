# JobBoard

A full-stack Job Management application built using **Vue.js**, **Django REST Framework**, and **PostgreSQL**. The platform allows users to create, manage, filter, edit, duplicate, and analyze job postings through a modern dashboard interface.

---

## Features

### Job Management
- Create new job postings
- Edit existing jobs
- Delete jobs
- Duplicate jobs
- Upload profile/job images
- Assign multiple statuses and categories
- Manage location details (Address, City, State)
- Track start and end dates

### Dashboard
- Responsive job card layout
- Search jobs by title
- Filter jobs by status
- Real-time updates after CRUD operations

### Analytics
- Status Distribution Pie Chart
- Jobs by City Bar Chart
- Jobs by State Bar Chart
- Interactive visualizations using Chart.js

### Validation & UX
- Frontend form validation
- Date range validation
- Error handling for API failures
- Loading states and empty-state views

---

## Tech Stack

### Frontend
- Vue 3 (Composition API)
- Vue Router
- Axios
- Chart.js
- Vue-ChartJS
- CSS

### Backend
- Django
- Django REST Framework
- Django Filter
- PostgreSQL
- Pillow


---

## Project Structure

```text
job-portal/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── JobCard.vue
│   │   │   └── JobForm.vue
│   │   │
│   │   ├── views/
│   │   │   ├── DashboardView.vue
│   │   │   └── AnalyticsView.vue
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── css/
│   │   └── router/
│   │
│   └── package.json
│
├── backend/
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── jobs/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
└── README.md
```

---

## Database Design

### Job

| Field | Type |
|---------|---------|
| title | CharField |
| description | TextField |
| profile_picture | ImageField |
| address | CharField |
| city | CharField |
| state | CharField |
| start_date | DateField |
| end_date | DateField |

### Status

| Field | Type |
|---------|---------|
| name | CharField |

### Category

| Field | Type |
|---------|---------|
| name | CharField |

### Relationships

```text
Job
├── ManyToMany → Status
└── ManyToMany → Category
```

---

## API Endpoints

### Jobs

| Method | Endpoint | Description |
|----------|------------|--------------|
| GET | `/api/jobs/` | Get all jobs |
| POST | `/api/jobs/` | Create a job |
| PUT | `/api/jobs/<id>/` | Update a job |
| DELETE | `/api/jobs/<id>/` | Delete a job |
| POST | `/api/jobs/<id>/duplicate/` | Duplicate a job |

### Status

| Method | Endpoint |
|----------|------------|
| GET | `/api/statuses/` |

### Categories

| Method | Endpoint |
|----------|------------|
| GET | `/api/categories/` |

### Analytics

| Method | Endpoint |
|----------|------------|
| GET | `/api/analytics/` |

---

##  Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/Risriddle/job-portal.git
cd job-portal
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

Configure PostgreSQL in `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Start backend server:

```bash
python manage.py runserver
```

Backend:

```text
http://localhost:8000
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

##  Analytics Dashboard

The analytics page provides visual insights into the current job database:

- Status Distribution (Pie Chart)
- Jobs by City (Bar Chart)
- Jobs by State (Bar Chart)

Built using Chart.js and Vue-ChartJS.

---

## Admin Panel

Django Admin is available for managing jobs, statuses, and categories.

```text
http://localhost:8000/admin/
```

Create a superuser using:

```bash
python manage.py createsuperuser
```

---


