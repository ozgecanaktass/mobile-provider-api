# API project for a Mobile Provider 

This project is developed as a midterm assignment for the SE4458 - Software Architecture course.  
It simulates the backend billing system of a mobile network operator.

- Users can register, authenticate, and interact with billing operations like adding usage, calculating monthly bills, viewing detailed usage, and paying bills. The API enforces JWT-based authentication on protected endpoints and is hosted on [Render](https://render.com) with a PostgreSQL database.
- Versioning, paging, and JWT-based authentication implemented as per course requirements.

---

## Live Deployment

- **Base URL:** [https://mobile-provider-api-vfpp.onrender.com](https://mobile-provider-api-vfpp.onrender.com)
- **Swagger UI:** [https://mobile-provider-api-vfpp.onrender.com/apidocs](https://mobile-provider-api-vfpp.onrender.com/apidocs)

---

## Tech Stack

- Python 3.11
- Flask (REST API Framework)
- Flask-JWT-Extended (Auth)
- Flask-SQLAlchemy (ORM)
- PostgreSQL (Cloud DB on Render)
- Gunicorn (Production WSGI Server)
- Render.com (Deployment)

---

## Folder Structure

```
.
├── app/
│   ├── dtos/                      # Request/response schemas (DTOs)
│   ├── models/                    # SQLAlchemy models
│   │   ├── bill.py
│   │   ├── subscriber.py
│   │   └── usage_model.py
│   ├── routes/                    # Flask route definitions (API endpoints)
│   │   ├── auth.py
│   │   ├── billing.py
│   │   ├── calculate_bill.py
│   │   └── usage.py
│   ├── services/                  # Business logic layer
│   │   ├── auth_service.py
│   │   ├── bill_service.py
│   │   ├── billing_service.py
│   │   └── usage_service.py
│   └── extensions.py              # Flask extension bindings (DB, JWT, etc.)
├── instance                
├── venv/                          
├── .env                          
├── main.py                        # App entry point
├── requirements.txt               # Dependencies
```

---

## Authentication

- JWT-based authentication is implemented using `Flask-JWT-Extended`.
- Protected endpoints like `/calculate-bill`, `/bill/details`, and `/usage` require a valid Bearer token.
- Token-based authorization is also supported in Swagger UI.

---

## 📬 API Endpoints Overview

| Method | Endpoint                   | Auth | Description                                             |
|--------|----------------------------|------|---------------------------------------------------------|
| POST   | `/api/v1/usage`            | ✅   | Add usage (phone → **minutes**, internet → **MB**)     |
| POST   | `/api/v1/calculate-bill`   | ✅   | Calculate bill based on total usage for month/year      |
| GET    | `/api/v1/bill`             | ❌   | Get bill total and payment status                       |
| GET    | `/api/v1/bill/details`     | ✅   | View bill breakdown (in **minutes** and **MB**)         |
| POST   | `/api/v1/pay-bill`         | ❌   | Mark a bill as paid (handles remaining balance logic)   |

---

## Billing Rules

- **Phone usage**: First 1000 minutes/month are free. Each extra 1000 mins → `$10`
- **Internet usage**: Up to 20GB (20480MB) → `$50`, then $10 for every 10GB (10240MB)

---

## Assumptions

- Phone usage is stored and billed in **minutes**
- Internet usage is stored and billed in **megabytes (MB)**  
  → **1GB = 1024MB**
- Remaining balance after payment is saved and can be re-paid later
- No real credit card integration — payments are simulated

---

## Issues Faced

- During rebase, VSCode removed some files unintentionally. The issue was resolved by manually restoring the files from previous versions.
- Setting up JWT-protected endpoints in Swagger required proper configuration for the Bearer token input.
- When switching from SQLite to PostgreSQL on Render, the DATABASE_URL had to be manually set and tested for connectivity issues.
- PostgreSQL connection failed due to missing `psycopg2` package. Fixed by installing `psycopg2-binary`.

---

## How to Test (via Swagger)

#### Open Swagger
- URL: [https://mobile-provider-api-vfpp.onrender.com/apidocs](https://mobile-provider-api-vfpp.onrender.com/apidocs)

---

#### Step 1: Register a New Subscriber
- Use the `/api/v1/auth/register` endpoint
- Example request body:
```json
{
  "subscriber_no": "36",
  "username": "ozge",
  "password": "test123"
}
```

---
#### Step 2: Login and Get JWT Token
- Use `/api/v1/auth/login` with your credentials
- Copy the returned `access_token`

---


## Local Setup

```bash
# clone the repo
git clone https://github.com/ozgecanaktass/mobile-provider-api.git
cd mobile-provider-api

# setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# create .env file and add:
# JWT_SECRET_KEY=super-secret-jwt-key
# DATABASE_URL=postgresql: postgresql://username:password@host:port/dbname


# run app
python main.py
```

---

## Hosted Version on Render

- This API is live and deployed on [https://mobile-provider-api-vfpp.onrender.com](https://mobile-provider-api-vfpp.onrender.com).
- The backend is automatically started by Render using the following command:

```bash
gunicorn main:app
```
- Render automatically installs all dependencies listed in requirements.txt, including gunicorn, Flask, and database drivers.
- A PostgreSQL database is also hosted via Render and connected using the DATABASE_URL environment variable.
- Swagger UI is accessible at: ➤ /apidocs

---

## Data Model (ER)

> ![image](https://github.com/user-attachments/assets/f171c470-a25d-4c58-ba1c-0d956355513a)

---

## 🎥 Demo Video

> https://drive.google.com/drive/folders/1TQag1qZOeIb8xrwzanTGRshjlWI1PP1_?usp=drive_link

---


👨‍💻 Developed by **Özgecan Aktaş - 21070001019** for SE4458 Midterm Project - Spring 2025

---

Instructor: *[Barış Ceyhan]*
