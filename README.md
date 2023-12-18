<div align="center">
  
# DuoTasker

  
  ![GitHub Repo stars](https://img.shields.io/github/stars/beetwenty/duotasker?logo=github) ![Docker Pulls](https://img.shields.io/docker/pulls/beetwenty/duotasker?logo=docker) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/beetwenty/duotasker/main?logo=github)![LICENSE](https://img.shields.io/github/license/beetwenty/duotasker
)

DuoTasker is a Django-based web application designed for efficient task management, utilizing Django, Nginx, and Redis. It uses websockets to update task creations, deletion, and markings in realtime so all users have the newest changes at all time.

## Getting Started

Set up and run DuoTasker on your local machine or production environment using Docker.

### Prerequisites

 Docker Compose

### Installation and Usage

#### Using Docker Compose

 **Set Up Environment Variables:**
    Create a .env file with necessary configurations:
  
  </div>
  
  ```env
 # Django settings
SECRET_KEY=VERY_SECRET_KEY
DEBUG=True
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
TIME_ZONE=UTC

# Nginx settings
SERVER_NAME=localhost

# SuperUser settings
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=adminpassword

# Database
DB_NAME=duotakser
DB_USER=duotasker
DB_PASSWORD=duotasker
DB_HOST=db
DB_PORT=5432
  ```
     

   **Create a Docker Compose File:**
   
  ```yml
  services:
    duotasker:
      container_name: duotasker
      image: beetwenty/duotasker:latest
      volumes:
        - /path/to/static/:/app/staticfiles/
      depends_on:
        - redis
      networks:
        - app-network
  
    nginx:
      image: nginx:alpine
      container_name: duotasker-web
      ports:
        - "80:80"
        - "443:443"
      volumes:
        - /path/to/nginx.conf:/etc/nginx/nginx.conf
        - /path/to/static:/app/staticfiles/
      environment:
        - SERVER_NAME=${SERVER_NAME}
      depends_on:
        - duotasker
      networks:
        - app-network
  
    redis:
      image: "redis:alpine"
      container_name: duotasker-redis
      networks:
        - app-network
  
  volumes:
    static_volume:
  
  networks:
    app-network:
      driver: bridge
  
  ```

<div align="center">
  
 **Run with Docker Compose:**
 
</div>

```
docker compose up -d
```

   <div align="center">

### Accessing the Application

 **Localhost:** http://localhost:80
 **Production:** Replace localhost with your domain.

## Features

 Task management, responsive design, PWA capabilities.




## Create Super User



set variables in .env

</div>

<div align="center">

## Contributing

Contributions are welcome. Follow standard open-source contribution guidelines.

## License

Licensed under the MIT License.

</div>
