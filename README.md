# 🚀 Zyvora — Scalable E-Commerce Backend

A production-style RESTful E-Commerce Backend built using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. The project follows a layered architecture and is designed with scalability in mind. It implements core backend engineering concepts such as authentication, authorization, database normalization, caching, safe concurrent ordering, and containerization.

---

# ✨ Features

## 🔐 Authentication & Authorization

- User Registration
- User Login
- JWT Authentication
- Password Hashing
- Role-Based Access Control (Admin & Customer)
- Protected Routes
- User Profile

---

## 📦 Product Management

- Create Product
- Update Product
- Delete Product
- View Products
- Product Details

---

## 📂 Category Management

- Create Category
- Update Category
- Delete Category
- View Categories
- View Products in a Category

---

## 🛒 Shopping Cart

- Add Product to Cart
- View Cart
- Update Product Quantity
- Remove Product from Cart
- Clear Cart

---

## 📋 Order Management

- Place Order
- View Orders
- Cancel Order
- Safe concurrent ordering: stock is checked and reduced in one atomic SQL update, so two customers can never buy the last unit
- Exact money: prices and totals are stored as `NUMERIC(10, 2)` and calculated with Python `Decimal`, never `float`. The API returns money as a string, e.g. `"19.99"`

---

## Redis Caching

Implemented Redis Cache for:

- Product Listing
- Product Details

Cache-Aside Pattern is used to reduce database load and improve response time.

---

## 🚦 Rate Limiting

Redis-based rate limiting per client IP (1000 requests per 60 seconds).

---

## 🐳 Docker

Containerized the application using Docker.

Services include:

- FastAPI Application
- PostgreSQL
- Redis

Managed using Docker Compose.

```bash
docker compose up --build
```

---

## 🗃️ Database Migrations

The database schema is managed with **Alembic** (`alembic/versions/`). The app never creates tables by itself.

- When the app container starts, it runs `alembic upgrade head` first, then starts the server. A new or old database is always brought up to date automatically.
- After changing a model, create a migration, **read it**, then apply it:

```bash
docker compose exec app alembic revision --autogenerate -m "describe the change"
docker compose exec app alembic upgrade head
```

---

# 🏗️ Architecture

```
                Client
                   │
                   ▼
              FastAPI Router
                   │
                   ▼
              Service Layer
                   │
                   ▼
            Repository Layer
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
   PostgreSQL            Redis Cache
```

---

# 🗄️ Database Design

The application follows a normalized relational database design.

### Tables

- Users
- Categories
- Products
- Carts
- Cart Items
- Orders
- Order Items
  
---

# 🌐 REST APIs

## Authentication

```
POST    /auth/signup
POST    /auth/login
GET     /auth/profile
```

---

## Admin

```
GET     /admin/dashboard
```

---

## Products

```
POST    /products
GET     /products
GET     /products/{id}
PUT     /products/{id}
DELETE  /products/{id}
```

---

## Categories

```
POST    /categories
GET     /categories
GET     /categories/{id}
PUT     /categories/{id}
DELETE  /categories/{id}
GET     /categories/{id}/products
```

---

## Cart

```
POST    /cart/add
GET     /cart
PUT     /cart/item/{id}
DELETE  /cart/item/{id}
DELETE  /cart/clear
```

---

## Orders

```
POST    /orders
GET     /orders
GET     /orders/{id}
PATCH   /orders/{id}/cancel
```

---

# 🛠️ Tech Stack

### Backend

- FastAPI
- Python

### Database

- PostgreSQL
- SQLAlchemy
- Alembic (migrations)

### Authentication

- JWT
- OAuth2
- Passlib

### Validation

- Pydantic

### Cache

- Redis

### Containerization

- Docker
- Docker Compose

---

# 📚 Backend Concepts Implemented

- REST API Design
- CRUD Operations
- JWT Authentication
- Role-Based Authorization
- Password Hashing
- Request Validation
- Layered Architecture
- Database Normalization
- Entity Relationships
- HTTP Status Codes
- Error Handling
- Redis Cache (Cache-Aside Pattern)
- Rate Limiting
- Atomic Stock Updates for Concurrent Orders
- Database Migrations (Alembic)
- Exact Decimal Money Handling
- Docker Containerization

---

# 🚀 Future Enhancements

- Microservices Architecture
- Event-Driven Communication
- API Gateway


---

## ⭐ If you found this project useful, consider giving it a star!
