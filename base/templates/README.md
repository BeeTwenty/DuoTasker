# DuoTasker

DuoTasker is a Django-based web application designed for efficient task management. It leverages Django's robust framework capabilities, along with Nginx for web serving and Redis for enhanced performance.

## Getting Started

These instructions will guide you through setting up and running DuoTasker on your local machine or production environment.

### Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose

### Installation

1. **Clone the Repository:**
```
git clone https://github.com/BeeTwenty/DuoTasker.git
cd DuoTasker
```

2. **Set Up Environment Variables:**
- Copy the `.env.example` file to a new file named `.env`.
- Edit the `.env` file to include your specific settings:
  ```
  SECRET_KEY=your_secret_key
  DEBUG=False
  ALLOWED_HOSTS=your_domain.com
  CSRF_TRUSTED_ORIGINS=your_domain.com
  TIME_ZONE=Your_Time_Zone
  SERVER_NAME=your_domain.com
  ```
- Ensure `SECRET_KEY` is strong and unique.
- Set `DEBUG` to `False` in a production environment.

3. **Build and Run with Docker Compose:**
```
docker-compose up --build -d
```

### Usage

Once the application is running, access it via:
- **Localhost:** [http://localhost:8887](http://localhost:8887) (or the port you configured)
- **Production:** `http://your_domain.com` (replace with your actual domain)

### Features

- Task management functionalities.
- Responsive design for various devices.
- Progressive Web App (PWA) capabilities.

### Configuring Nginx

- The `nginx.conf` file is pre-configured for basic usage.
- For custom domain settings, modify the `server_name` directive in `nginx.conf`.

### Static Files

- Static files are managed by Django and served by Nginx.
- Run `docker-compose exec duotasker python manage.py collectstatic` to collect static files.

### Create Super User

- Run `docker-compose exec duotasker python manage.py createsuperuser` and fill inn the fields.

## Contributing

Contributions to DuoTasker are welcome. Please follow the standard procedures for contributing to open-source projects.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Django Community
- Contributors and maintainers of the used packages.
