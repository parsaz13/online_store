# 🛒 Online Store — E-commerce Backend with Django, DRF, and React Frontend

## 📌 Overview

This project is a full-stack e-commerce website with a **React** frontend (provided) and a **Django + Django REST Framework (DRF)** backend.
You will develop the backend, including APIs for products, customers, orders, discounts, and more.
You’ll integrate JWT authentication, OTP login, Celery for background tasks, and deploy using Docker and Nginx.

---

## 🚀 Tech Stack

**Backend:**

* Django
* Django REST Framework (DRF)
* PostgreSQL
* Redis (OTP, caching)
* Celery (background tasks)
* RabbitMQ (optional for Celery task queues)
* JWT (authentication)
* Docker & Docker Compose
* Nginx (reverse proxy, static files)

**Frontend:**

* React (pre-built)
* JavaScript, HTML, CSS
* TailwindCSS or Bootstrap (optional)

---

## ✅ Project Phases & Deliverables

### 📅 Phase 1: Project Setup & Initial Backend Development

**Dates:** `14 تیر تا 19 تیر`

**Tasks:**

* Analyze requirements & create an ERD (Entity Relationship Diagram)
* Initialize Git repo with `develop` & `master` branches
* Setup Django project + DRF
* Configure PostgreSQL
* Setup Redis for OTP & caching
* Create models:

  * Customer
  * Address
  * Product
  * Discount
  * Order
  * Order Item
* Implement basic CRUD APIs for products & customers

**Deliverables:**

* ERD in PDF
* GitHub repo with proper commits
* Initial project structure & sample data in Django Admin

---

### 📅 Phase 2: Developing Core Features

**Dates:** `20 تیر تا 26 تیر`

**Tasks:**

* JWT authentication (registration & login)
* OTP-based login via email using Redis
* Product catalog & detail APIs
* Discount system (percent & fixed)
* Category models & hierarchical category APIs
* Shopping cart API (add/remove items)
* Order placement & order item management

**Deliverables:**

* Complete auth & login APIs
* Product, discount, category, order, and cart APIs
* Backend ready to connect with React frontend

---

### 📅 Phase 3: Customer & Order Management

**Dates:** `27 تیر تا 2 مرداد`

**Tasks:**

* Manage customer profiles (view, update)
* Customer order history & status tracking
* Order management APIs (status: pending, shipped, delivered)
* Integrate Celery for order processing (emails for order confirmation)
* Setup Celery with RabbitMQ

**Deliverables:**

* All order/customer management endpoints
* Email notifications via Celery
* Fully connected backend & frontend

---

### 📅 Phase 4: Final Refinements & Deployment

**Dates:** `3 مرداد تا 9 مرداد`

**Tasks:**

* Final debugging & test coverage (>80%)
* Finalize JWT auth (token expiration & refresh)
* Integrate React frontend with backend APIs
* Dockerize the app (Dockerfile, docker-compose)
* Deploy with Nginx as reverse proxy & static file server
* Project documentation & final README

**Deliverables:**

* Live deployment (URL if available)
* Fully integrated React frontend
* Well-tested APIs
* Detailed documentation on GitHub

---

## 🔑 Key Project Requirements

✅ **Git Workflow:**

* Use `develop` for all feature development
* Merge to `master` after each phase

✅ **Testing:**

* Minimum 80% test coverage
* Unit tests for logic & APIs
* End-to-end testing with Selenium (optional)
* TDD approach encouraged

✅ **Multi-language Support:**

* Implement Django internationalization from Phase 1

✅ **Database:**

* Models normalized & related
* Use soft deletes (`delete_logical` pattern) for required models

✅ **Authentication:**

* JWT for login & protected routes
* Frontend handles storing/passing JWT tokens in headers

✅ **Deployment:**

* Use Docker & Docker Compose
* Nginx as reverse proxy + static/media file handling

✅ **GitHub:**

* Private repository
* Instructors added as collaborators
* Well-labeled commits

---

## 🌍 Frontend Integration

* Make sure backend APIs match the React frontend’s expectations
* Handle JWT auth & token refresh in API responses
* Enable CORS for frontend-backend communication
* Return JSON responses that React can consume
* Ensure user flows: add to cart, checkout, orders, profiles

---

## 📝 Final Submission Checklist

✔️ Final code pushed to **private GitHub repo**
✔️ **ERD PDF** included
✔️ Well-documented `README.md`
✔️ Frontend & backend fully connected
✔️ Working deployment (Docker, Nginx)

---

## 🐳 Docker & Deployment

To run the project with Docker:

```bash
docker-compose up --build
```
- The backend will be available at http://localhost:8000
- The API docs are at http://localhost:8000/swagger/
- Nginx will serve at http://localhost/
- Static files: /static/
- Media files: /media/

## 🧪 Testing

To run tests and check coverage:

```bash
pytest --ds=config.settings --cov=store
```

## 📄 ERD

The ERD is located at `/backend/docs/ERD.pdf` (exported from draw.io).

## ⚛️ Frontend

The frontend directory is currently empty. You can scaffold a new React app or place your provided frontend code in the `frontend/` directory.

---

## ⚙️ Local Setup (for developers)

```bash
# Clone repo
git clone <repo_url>
cd <repo_name>

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run Redis & Celery (optional)
# Run the server
python manage.py runserver
```

---

## 📄 ERD

**Location:** `/docs/ERD.pdf`

---

## 🗂️ License

This project is for educational purposes only.

---

## 👥 Collaborators

* Add your instructors as collaborators on the GitHub repo.

---

> *Good luck building your e-commerce backend!* 🚀✨
