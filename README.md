<div align="center">
  
# DuoTasker

  
  ![GitHub Repo stars](https://img.shields.io/github/stars/beetwenty/duotasker?logo=github) ![Docker Pulls](https://img.shields.io/docker/pulls/beetwenty/duotasker?logo=docker) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/beetwenty/duotasker/main?logo=github)![LICENSE](https://img.shields.io/github/license/beetwenty/duotasker
)

DuoTasker is a Django-based web application designed for efficient task management, utilizing Django, Nginx, and Redis.

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
      SECRET_KEY=your_secret_key
      DEBUG=False
      ALLOWED_HOSTS=your_domain.com or ip
      CSRF_TRUSTED_ORIGINS=http(s)://your_domain.com or ip
      TIME_ZONE=Your_Time_Zone
      SERVER_NAME=your_domain.com or ip
      DJANGO_SUPERUSER_USERNAME=admin
      DJANGO_SUPERUSER_EMAIL=admin@example.com
      DJANGO_SUPERUSER_PASSWORD=adminpassword
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

## Configuring Nginx

 Modify nginx.conf for custom domain settings.


## Create Super User

</div>

```
docker-compose exec -it duotasker python manage.py createsuperuser

```

<div align="center">

## Contributing

Contributions are welcome. Follow standard open-source contribution guidelines.

## License

Licensed under the MIT License.

</div>
