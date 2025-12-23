# Django Enterprise SaaS Boilerplate

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat&logo=django)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=flat&logo=docker)
![Celery](https://img.shields.io/badge/Celery-Async_Tasks-orange?style=flat&logo=celery)

A production-ready, containerized backend starter kit designed for scalable SaaS applications. Built with **Django REST Framework**, **Docker**, **PostgreSQL**, and **Redis** for asynchronous task processing.

This boilerplate implements industry best practices for security, scalability, and maintainability, allowing developers to focus on business logic rather than infrastructure setup.

---

## Key Features

-   **Fully Dockerized:** Orchestrated using `docker-compose` for web, db, worker, and broker services.
-   **Asynchronous Processing:** Integrated **Celery** & **Redis** for handling background tasks (emails, PDF generation, data processing) without blocking the main thread.
-   **Robust Authentication:** JWT Authentication (via `djangorestframework-simplejwt`) with custom user models.
-   **PostgreSQL Database:** Configured for production with persistent volumes.
-   **Payment Ready:** Pre-configured structure for **Stripe Webhooks** and subscription handling.
-   **API Documentation:** Auto-generated Swagger/OpenAPI documentation (via `drf-spectacular` or `drf-yasg`).
-   **Security:** Environment variable management via `.env` files (detached from source control).

---

## 🛠️ Tech Stack

-   **Backend Framework:** Django 5.x + Django REST Framework
-   **Database:** PostgreSQL 16
-   **Cache & Message Broker:** Redis
-   **Task Queue:** Celery
-   **Containerization:** Docker & Docker Compose
-   **Server:** Gunicorn (Production) / Django Dev Server (Development)
-   **Reverse Proxy:** Nginx (Optional configuration included)

---

## Getting Started

Follow these steps to get the application running locally in minutes.

### Prerequisites

-   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/REPO_NAME.git](https://github.com/YOUR_USERNAME/REPO_NAME.git)
    cd REPO_NAME
    ```

2.  **Create your Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
    *(Ensure you fill in your database credentials and secret keys in the .env file)*

3.  **Build and Run with Docker:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply Migrations:**
    Once the containers are running, open a new terminal:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a Superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

### Access the Application

-   **API Root:** `http://localhost:8000/api/`
-   **Admin Panel:** `http://localhost:8000/admin/`
-   **Swagger Docs:** `http://localhost:8000/api/schema/swagger-ui/` (If configured)

---

## 📂 Project Structure

```text
├── app/                  # Main Django App configuration
├── core/                 # Core business logic and shared utilities
├── users/                # Custom User model and Auth logic
├── docker/               # Dockerfiles and entrypoint scripts
├── manage.py
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (Gitignored)
```

## Running Tests
To run the automated test suite inside the container:

```Bash
docker-compose exec web python manage.py test
```

## Future Roadmap
- Integration of Prometheus/Grafana for monitoring.

- WebSocket support using Django Channels.

- CI/CD Pipeline configuration (GitHub Actions).

## License
This project is licensed under the MIT License.
