# Smart E-Commerce Backend

A backend system for a Smart E-Commerce application built using **FastAPI, Django Admin, MySQL, SQLAlchemy, Alembic, JWT authentication, Stripe, WebSockets, and email notifications**.

The project provides customer-facing REST APIs through FastAPI and an administrative management panel through Django Admin.

---

## 1. Project Overview

The Smart E-Commerce system provides the backend functionality required for an online shopping platform.

### Customer Features

* User registration
* User login
* JWT authentication
* Role-based access control
* Product browsing
* Product details
* Shopping cart management
* Order checkout
* Order history
* Order status tracking
* Stripe payment integration
* In-app notifications
* Real-time WebSocket notifications
* Email notifications

### Admin Features

* Django Admin panel
* Customer management
* Category management
* Product management
* Order management
* Payment management
* Notification management
* Sales analytics
* Revenue trends
* Top-selling products
* Low-stock products
* CSV sales reports
* PDF sales reports

---

# 2. Technology Stack

| Component            | Technology                 |
| -------------------- | -------------------------- |
| Customer Backend     | FastAPI                    |
| Admin Panel          | Django Admin               |
| Programming Language | Python                     |
| Database             | MySQL                      |
| ORM                  | SQLAlchemy                 |
| Migration            | Alembic                    |
| Authentication       | JWT                        |
| Password Hashing     | Passlib + bcrypt           |
| Payment              | Stripe                     |
| Notifications        | Email + WebSocket + In-App |
| API Documentation    | Swagger / OpenAPI          |
| API Testing          | Postman                    |
| Reports              | CSV / PDF                  |

---

# 3. System Architecture

```text
                    Smart E-Commerce
                           |
             +-------------+-------------+
             |                           |
             v                           v
       FastAPI Backend             Django Admin
             |                           |
             |                           |
             +-------------+-------------+
                           |
                           v
                         MySQL
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
        Stripe          Email          WebSocket
       Payments       Notifications   Notifications
```

### FastAPI

FastAPI handles:

* Authentication
* Products
* Cart
* Orders
* Payments
* Notifications
* WebSockets
* Customer APIs

### Django Admin

Django provides:

* Administrative CRUD operations
* Product management
* Customer management
* Order management
* Analytics
* Reports

Both applications work with the same MySQL database.

---

# 4. Project Structure

```text
smart_ecommerce/
│
├── fastapi_app/
│   │
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env
│
├── django_admin/
│   │
│   ├── config/
│   ├── store/
│   ├── manage.py
│   └── requirements.txt
│
├── database/
│   └── ecommerce.sql
│
├── postman/
│   └── Smart_Ecommerce.postman_collection.json
│
├── docs/
│   └── Smart_Ecommerce_Documentation.pdf
│
└── README.md
```

---

# 5. Prerequisites

Before running the project, install:

* Python 3.x
* MySQL 8.0.x
* Git
* Postman
* Stripe CLI (only for Stripe webhook testing)

Verify Python:

```bash
python --version
```

Verify MySQL:

```bash
mysql --version
```

---

# 6. Database Setup

Create the MySQL database:

```sql
CREATE DATABASE ecommerce
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Select the database:

```sql
USE ecommerce;
```

---

# 7. FastAPI Setup

Go to the FastAPI project:

```bash
cd C:\Users\subramanyam\smart_ecommerce\fastapi_app
```

Create the virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 8. FastAPI Environment Configuration

Create a `.env` file inside:

```text
fastapi_app/.env
```

Example:

```env
DATABASE_URL=mysql+pymysql://root:<PASSWORD>@127.0.0.1:3306/ecommerce

JWT_SECRET_KEY=<YOUR_SECRET_KEY>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

STRIPE_SECRET_KEY=sk_test_<YOUR_STRIPE_KEY>
STRIPE_WEBHOOK_SECRET=whsec_<YOUR_WEBHOOK_SECRET>

STRIPE_SUCCESS_URL=http://localhost:3000/payment/success
STRIPE_CANCEL_URL=http://localhost:3000/payment/cancel

SMTP_HOST=<SMTP_HOST>
SMTP_PORT=587
SMTP_USERNAME=<SMTP_USERNAME>
SMTP_PASSWORD=<SMTP_PASSWORD>
SMTP_FROM_EMAIL=no-reply@example.com
SMTP_USE_TLS=true

CORS_ORIGINS=http://localhost:3000
```

### Important

Do not commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 9. MySQL Password with Special Characters

If the MySQL password contains special characters such as:

```text
@
```

the character must be URL encoded.

For example:

```text
@  →  %40
```

Therefore:

```text
mypassword@123
```

becomes:

```text
mypassword%40123
```

The database URL would be:

```env
DATABASE_URL=mysql+pymysql://root:mypassword%40123@127.0.0.1:3306/ecommerce
```

---

# 10. Database Migration

The project uses **Alembic** for database migrations.

Activate the FastAPI environment:

```bash
cd C:\Users\subramanyam\smart_ecommerce\fastapi_app
venv\Scripts\activate
```

Run migrations:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

The database contains tables such as:

```text
users
categories
products
cart_items
orders
order_items
payments
notifications
```

---

# 11. Start FastAPI

Run:

```bash
uvicorn app.main:app --reload --port 8001
```

If `uvicorn` is not recognized, use:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

FastAPI will run at:

```text
http://127.0.0.1:8001
```

---

# 12. Swagger API Documentation

Open:

```text
http://127.0.0.1:8001/docs
```

This provides Swagger UI.

ReDoc is available at:

```text
http://127.0.0.1:8001/redoc
```

Swagger can be used to test all FastAPI endpoints.

---

# 13. Authentication

## Register

```http
POST /api/auth/register
```

Example:

```json
{
    "name": "Test User",
    "email": "user@example.com",
    "password": "Password123"
}
```

---

## Login

```http
POST /api/auth/login
```

Example:

```json
{
    "email": "user@example.com",
    "password": "Password123"
}
```

Successful login returns:

```json
{
    "access_token": "eyJ...",
    "token_type": "bearer"
}
```

---

# 14. JWT Authorization

Protected APIs require a JWT.

In Swagger:

1. Click **Authorize**
2. Enter the JWT token
3. Click **Authorize**
4. Click **Close**

Use only the token value.

Do not manually add:

```text
Bearer
```

when Swagger's HTTP Bearer security scheme is configured to add it automatically.

---

# 15. Authentication Endpoints

| Method | Endpoint             | Description      |
| ------ | -------------------- | ---------------- |
| POST   | `/api/auth/register` | Register user    |
| POST   | `/api/auth/login`    | Login            |
| GET    | `/api/auth/me`       | Get current user |

---

# 16. Product APIs

| Method | Endpoint                     | Description               |
| ------ | ---------------------------- | ------------------------- |
| GET    | `/api/products`              | List products             |
| GET    | `/api/products/{product_id}` | Get product               |
| POST   | `/api/products`              | Create product            |
| PUT    | `/api/products/{product_id}` | Update product            |
| DELETE | `/api/products/{product_id}` | Delete/deactivate product |

Administrative product operations require the appropriate role.

---

# 17. Role-Based Access Control

The system uses roles to control access.

Example roles:

```text
customer
admin
staff
```

Customers can perform normal shopping operations.

Admins/staff can access administrative functionality according to the configured permissions.

Check user roles in MySQL:

```sql
USE ecommerce;

SELECT id, name, email, role
FROM users;
```

To change a user's role:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'user@example.com';
```

After changing the role, the user must **log in again** because the role is included in the JWT.

---

# 18. Cart APIs

| Method | Endpoint                    | Description     |
| ------ | --------------------------- | --------------- |
| GET    | `/api/cart`                 | View cart       |
| POST   | `/api/cart/items`           | Add item        |
| PUT    | `/api/cart/items/{item_id}` | Update quantity |
| DELETE | `/api/cart/items/{item_id}` | Remove item     |

Example add-to-cart request:

```json
{
    "product_id": 1,
    "quantity": 2
}
```

---

# 19. Order APIs

| Method | Endpoint                  | Description         |
| ------ | ------------------------- | ------------------- |
| POST   | `/api/orders/checkout`    | Create order        |
| GET    | `/api/orders`             | Order history       |
| GET    | `/api/orders/{id}`        | Get order           |
| PUT    | `/api/orders/{id}/status` | Update order status |

Typical order flow:

```text
Browse Products
       ↓
Add Product to Cart
       ↓
View Cart
       ↓
Checkout
       ↓
Create Order
       ↓
Create Payment
       ↓
Stripe Checkout
       ↓
Payment Success
       ↓
Order Status Updated
       ↓
Notification Sent
```

---

# 20. Stripe Payment

Stripe is configured using test-mode credentials.

Example:

```env
STRIPE_SECRET_KEY=sk_test_<YOUR_KEY>
```

Create a payment session:

```http
POST /api/payments/create/{order_id}
```

Stripe returns a checkout session/URL.

For webhook testing, install Stripe CLI and run:

```bash
stripe listen --forward-to localhost:8001/api/payments/webhook
```

Copy the generated:

```text
whsec_...
```

into:

```env
STRIPE_WEBHOOK_SECRET=whsec_<YOUR_SECRET>
```

Restart FastAPI after changing environment variables.

### Stripe Test Card

Use:

```text
Card Number: 4242 4242 4242 4242
Expiry: Any future date
CVC: Any 3 digits
```

Use Stripe test mode only during development.

---

# 21. Payment APIs

| Method | Endpoint                          | Description            |
| ------ | --------------------------------- | ---------------------- |
| POST   | `/api/payments/create/{order_id}` | Create Stripe checkout |
| POST   | `/api/payments/webhook`           | Stripe webhook         |

---

# 22. Notifications

The application supports:

* In-app notifications
* Email notifications
* Real-time WebSocket notifications

Notification examples:

```text
Order Confirmation
Payment Success
Payment Failure
Order Shipped
Order Status Updated
```

Get notifications:

```http
GET /api/notifications
```

---

# 23. WebSocket Notifications

WebSocket endpoint:

```text
/api/notifications/ws/{user_id}
```

Example:

```text
ws://127.0.0.1:8001/api/notifications/ws/1
```

WebSockets allow notifications to be delivered in real time without repeatedly polling the API.

---

# 24. Email Notifications

SMTP configuration is stored in `.env`.

Example:

```env
SMTP_HOST=<SMTP_HOST>
SMTP_PORT=587
SMTP_USERNAME=<SMTP_USERNAME>
SMTP_PASSWORD=<SMTP_PASSWORD>
SMTP_FROM_EMAIL=no-reply@example.com
SMTP_USE_TLS=true
```

Email notifications can be generated for:

* Order confirmation
* Payment status
* Shipping/order status
* Other configured order events

---

# 25. Django Admin Setup

Open a second terminal.

Go to:

```bash
cd C:\Users\subramanyam\smart_ecommerce\django_admin
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Check Django:

```bash
python -m django --version
```

Run Django system checks:

```bash
python manage.py check
```

---

# 26. Django Admin Superuser

Create a Django administrator:

```bash
python manage.py createsuperuser
```

Enter:

```text
Username
Email
Password
```

---

# 27. Start Django Admin

Run:

```bash
python manage.py runserver 8000
```

Open:

```text
http://127.0.0.1:8000/admin/
```

Login using the superuser credentials.

---

# 28. Django Admin Features

The Admin Panel provides management for:

### Customers

* View customers
* Manage customer information
* Manage user roles

### Categories

* Create category
* Update category
* Delete category

### Products

* Add products
* Edit products
* Delete/deactivate products
* Manage stock
* Manage price
* Manage category
* Manage product image URL

### Orders

* View orders
* View order items
* Update order status

### Payments

* View payment records
* Check payment status

### Notifications

* View notification records
* Check notification status

---

# 29. Analytics

Analytics page:

```text
http://127.0.0.1:8000/analytics/
```

The dashboard provides information such as:

* Total sales
* Total revenue
* Top-selling products
* Revenue trends
* Low-stock products

---

# 30. Sales Reports

## CSV Report

```text
http://127.0.0.1:8000/reports/sales.csv
```

## PDF Report

```text
http://127.0.0.1:8000/reports/sales.pdf
```

These reports can be used as project demonstration evidence.

---

# 31. Postman Testing

The recommended testing sequence is:

```text
1. Register
       ↓
2. Login
       ↓
3. Copy JWT
       ↓
4. Set Bearer Token
       ↓
5. Products
       ↓
6. Cart
       ↓
7. Checkout
       ↓
8. Payment
       ↓
9. Orders
       ↓
10. Notifications
```

Login request:

```http
POST http://127.0.0.1:8001/api/auth/login
```

Body:

```json
{
    "email": "user@example.com",
    "password": "Password123"
}
```

For protected APIs:

```text
Authorization
    ↓
Bearer Token
    ↓
Paste JWT
```

---

# 32. Complete Local Startup

For normal development, run these services.

### Terminal 1 — MySQL

Make sure MySQL Server is running.

### Terminal 2 — FastAPI

```bash
cd C:\Users\subramanyam\smart_ecommerce\fastapi_app
venv\Scripts\activate
uvicorn app.main:app --reload --port 8001
```

### Terminal 3 — Django

```bash
cd C:\Users\subramanyam\smart_ecommerce\django_admin
venv\Scripts\activate
python manage.py runserver 8000
```

### Application URLs

| Application  | URL                                     |
| ------------ | --------------------------------------- |
| FastAPI      | http://127.0.0.1:8001                   |
| Swagger      | http://127.0.0.1:8001/docs              |
| ReDoc        | http://127.0.0.1:8001/redoc             |
| Django Admin | http://127.0.0.1:8000/admin/            |
| Analytics    | http://127.0.0.1:8000/analytics/        |
| CSV Report   | http://127.0.0.1:8000/reports/sales.csv |
| PDF Report   | http://127.0.0.1:8000/reports/sales.pdf |

---

# 33. Troubleshooting

## Problem: `uvicorn` is not recognized

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Or use:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

---

## Problem: `401 Unauthorized`

Possible causes:

* JWT is missing
* JWT is expired
* Invalid JWT
* User is inactive

Solution:

```text
Login again
      ↓
Copy new JWT
      ↓
Authorize Swagger/Postman again
```

---

## Problem: `403 Insufficient permissions`

Check the user's role:

```sql
SELECT id, name, email, role
FROM users;
```

Change the role if required:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'user@example.com';
```

Then **login again** to generate a new JWT.

---

## Problem: MySQL connection error

Check:

```text
MySQL is running
Database exists
Username is correct
Password is correct
Port is correct
DATABASE_URL is correct
```

Default development URL:

```text
127.0.0.1:3306
```

Remember to URL-encode special characters in the database password.

---

## Problem: Django requires MySQL 8.4

This project uses MySQL 8.0.x.

Use:

```bash
pip install "Django==5.2.*"
```

Then verify:

```bash
python -m django --version
```

Run:

```bash
python manage.py check
```

---

## Problem: Stripe is not configured

Check `.env`:

```env
STRIPE_SECRET_KEY=sk_test_<YOUR_KEY>
```

Restart FastAPI after changing `.env`.

---

# 34. Security Guidelines

Do not commit sensitive information to GitHub.

Never commit:

```text
.env
Database passwords
JWT secret keys
Stripe secret keys
SMTP passwords
API keys
```

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
*.log
```

For production:

* Use HTTPS
* Use strong JWT secrets
* Use secure environment variables
* Restrict CORS
* Use Stripe live keys only in secure deployment configuration
* Rotate compromised secrets
* Restrict database permissions

---

# 35. Database Backup

Create a MySQL dump:

```bash
mysqldump -u root -p ecommerce > database\ecommerce.sql
```

Restore:

```bash
mysql -u root -p ecommerce < database\ecommerce.sql
```

The SQL dump can be included in the final project submission.

---



# 36. Current Project Scope

The current implementation is focused on the **backend**.

The backend consists of:

```text
FastAPI
    +
Django Admin
    +
MySQL
    +
Stripe
    +
JWT
    +
WebSocket
    +
Email Notifications
```

A frontend application can be developed separately and consume the FastAPI APIs.

---

# 38. Conclusion

The Smart E-Commerce backend provides a complete foundation for an online shopping system.

The project demonstrates:

* REST API development using FastAPI
* Database design using MySQL
* SQLAlchemy ORM
* Alembic database migrations
* JWT authentication
* Role-Based Access Control
* Product and category management
* Shopping cart functionality
* Order management
* Stripe payment integration
* Email notifications
* WebSocket notifications
* Django Admin
* Sales analytics
* CSV/PDF reporting
* Swagger/OpenAPI API documentation

The system is designed so that FastAPI handles customer-facing business APIs while Django Admin provides administrative management over the same MySQL database.
