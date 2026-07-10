# 🚀 Zyvora — Scalable E-Commerce Backend

A production-style RESTful E-Commerce Backend built using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. The project follows a layered architecture and is designed with scalability in mind. It implements core backend engineering concepts such as authentication, authorization, database normalization, caching, pagination, and containerization.

---

# ✨ Features

## 🔐 Authentication & Authorization

- User Registration
- User Login
- JWT Authentication
- Password Hashing
- Role-Based Access Control (Admin & Customer)
- Protected Routes

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

---

## 🛒 Shopping Cart

- Add Product to Cart
- View Cart
- Update Product Quantity
- Remove Product from Cart

---

## 📋 Order Management

- Place Order
- Cancel Order

---

## Redis Caching

Implemented Redis Cache for:

- Product Listing
- Product Details

Cache-Aside Pattern is used to reduce database load and improve response time.

---

## 🐳 Docker

Containerized the application using Docker.

Services include:

- FastAPI Application
- PostgreSQL
- Redis

Managed using Docker Compose.

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
POST   /signup
POST   /login
```

---

## Products

```
POST    /products
GET     /products
GET     /products/{id}
PATCH   /products/{id}
DELETE  /products/{id}
```

## Categories

```
POST    /categories
GET     /categories
PATCH   /categories/{id}
DELETE  /categories/{id}
```

---

## Cart

```
POST    /cart/items
GET     /cart
PATCH   /cart/items/{id}
DELETE  /cart/items/{id}
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

### Testing

- Pytest

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
- Docker Containerization

---

# 🚀 Future Enhancements

- Microservices Architecture
- Apache Kafka
- Event-Driven Communication
- API Gateway


---

## ⭐ If you found this project useful, consider giving it a star!
