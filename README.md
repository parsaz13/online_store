# Online Store Project

## Overview
This project is an e-commerce platform developed with a Django/DRF backend and a React frontend. It includes features for customer management, product catalog, order processing, and seller dashboards, deployed using Docker and Nginx.

## Technologies
- **Backend**: Django, Django REST Framework (DRF), PostgreSQL, Redis, Celery, JWT Authentication, Docker, Nginx.
- **Frontend**: React, Vite, TailwindCSS, Axios, pnpm.
- **Tools**: Git, docker-compose, Swagger (drf_yasg).

## Setup

### Prerequisites
- Python 3.12
- Node.js 18+
- Docker Desktop
- PostgreSQL
- Redis

### Installation

1. **Clone the Repository**
git clone <your-repo-url>
cd online_store</your-repo-url>


2. **Backend Setup**
- Create and activate a virtual environment:

- Install dependencies:
pip install -r backend/requirements.txt

- Apply migrations:
cd backend
python manage.py migrate

- Create a superuser:
python manage.py createsuperuser


3. **Frontend Setup**
- Install dependencies:
cd frontend
pnpm i

- Run the development server:
pnpm dev


4. **Docker Setup**
- Build and run with Docker Compose:
docker-compose up --build

- Access the app at `http://localhost`.

## Run Tests
- Run backend tests:
cd backend
python manage.py test
- Test coverage is 83%, reported using `coverage.py`.

## Deployment
- The application is containerized with Docker and served via Nginx.
- Deployed live URL: <insert-live-url-here> (after deployment on a server like DigitalOcean).
- Use `docker-compose.yml` and `nginx.conf` for production setup.

## API Documentation
- API endpoints are documented using Swagger (drf_yasg).
- Access at `http://localhost:8000/api/docs/` (when backend is running).

## ERD
- Entity Relationship Diagram is available as `erd.pdf` in the repository.

## Project Structure
- `backend/`: Django project with apps (users, products, store, orders, etc.).
- `frontend/`: React app with components and hooks.
- `docker-compose.yml`: Defines services for backend, frontend, database, and Nginx.

## Features
- **Authentication**: JWT-based login and registration with OTP via email.
- **Customer Management**: Profile management, multiple addresses.
- **Product Management**: CRUD for products, categories (hierarchical), discounts, best seller/price APIs.
- **Order Management**: Cart, order placement, status tracking, email notifications via Celery.
- **Seller Dashboard**: Manage store, products, categories, and orders (restricted to owners).

## Contributing
- Use `develop` branch for development, merge to `main` after each phase.
- Submit pull requests with detailed descriptions.

## License
- This project is for educational purposes only.

## Contact
- For questions, contact the team via GitHub issues.
