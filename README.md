# 🛒 E-commerce Platform Backend with Django & DRF

## 📌 Description

This is a fully-featured e-commerce backend system built with Django and Django REST Framework. It supports user management, product catalog, shopping cart, orders, and store functionalities. It is designed to work with a React frontend and is ready for future deployment using Docker and Nginx.

---

## 🚀 Features

- ✅ JWT-based authentication with OTP verification (via Redis)
- ✅ Role-based access: Admin, Store Owner, Customer
- ✅ Multi-address support per customer
- ✅ Product management and hierarchical categories
- ✅ Shopping cart and order placement
- ✅ Order status tracking (pending, shipped, delivered, canceled)
- ✅ Celery task queue for sending order confirmation emails
- ✅ Soft-delete system for key models
- ✅ Swagger/OpenAPI documentation with drf-yasg

---

## 🧱 Tech Stack

- Python 3.x
- Django 5.x
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- SimpleJWT
- Docker (coming soon)

---

## ⚙️ Installation Guide

### 1. Clone the repository

```bash
git clone <repo-url>
cd <project-folder>
