# DuoTasker

DuoTasker is a Django-based web application designed for efficient task management, utilizing Django, Nginx, and Redis.

## Getting Started

Set up and run DuoTasker on your local machine or production environment using Docker.

### Prerequisites

- Docker Compose

### Installation and Usage

#### Using Docker Compose

1. **Set Up Environment Variables:**
   - Create a .env file with necessary configurations:
  
     
   ```env
    SECRET_KEY=your_secret_key
    DEBUG=False
    ALLOWED_HOSTS=your_domain.com or ip
    CSRF_TRUSTED_ORIGINS=http(s)://your_domain.com or ip
    TIME_ZONE=Your_Time_Zone
    SERVER_NAME=your_domain.com or ip
    ```
     

2. **Create a Docker Compose File:**
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

3. **Run with Docker Compose:**

```
docker compose up -d
```
   

### Accessing the Application

- **Localhost:** http://localhost:80
- **Production:** Replace localhost with your domain.

## Features

- Task management, responsive design, PWA capabilities.

## Configuring Nginx

- Modify nginx.conf for custom domain settings.


## Create Super User

```
docker-compose exec -it duotasker python manage.py createsuperuser

```


## Contributing

Contributions are welcome. Follow standard open-source contribution guidelines.

## License

Licensed under the MIT License.

## Acknowledgments

- Django Community and package maintainers.
