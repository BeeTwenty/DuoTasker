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
  DEBUG=False
  ALLOWED_HOSTS=localhost,127.0.0.1
  CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
TIME_ZONE=UTC

# SuperUser settings
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=adminpassword

# Database
DB_NAME=duotasker
DB_USER=duotasker
DB_PASSWORD=duotasker
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
  ```
     

   **Create a Docker Compose File:**
   
  ```yml
  services:
  postgres:
    image: postgres:18
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-duotasker}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-duotasker}
      POSTGRES_DB: ${DB_NAME:-duotasker}
    volumes:
      - postgres_data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-duotasker} -d ${DB_NAME:-duotasker}"]

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis_data:/data

  duotasker:
    build:
      context: .
    image: beetwenty/duotasker:latest
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      REDIS_HOST: redis
      REDIS_PORT: 6379
    volumes:
      - static_data:/app/staticfiles
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  nginx:
    image: nginx:stable-alpine
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - static_data:/app/staticfiles:ro
    depends_on:
      duotasker:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
  static_data:
  
  ```

<div align="center">
  
 **Run with Docker Compose:**
 
</div>

```
cp .env.example .env
docker compose up -d --build
```

   <div align="center">

### Accessing the Application

 **Localhost:** http://localhost:80
 **Production:** Replace localhost with your domain.

## Features

 Task management, responsive design, PWA capabilities.

## Smart Categories

Categories can use multilingual aliases in the `keywords` field. For shopping lists, that means a category can learn item names such as `milk, melk, lait` instead of only full task phrases.

The smart categorizer is built into the app and works in two stages:
- a fast rules layer for exact aliases, phrase matches, and token overlap
- a built-in statistical classifier for ambiguous items and learned behavior

It supports:
- exact item matching
- phrase and token matching
- accent folding such as `brod` matching `brød`
- multilingual aliases stored per category
- learned classification from previously categorized items

How it works:
- Every category builds training examples from its name, its keyword aliases, and all already-categorized task titles.
- Input text is normalized across languages using case folding, accent folding, and Nordic-character simplification.
- The built-in classifier extracts both word tokens and character trigrams, which makes it more robust for short shopping items and multilingual spelling differences.
- When a user manually assigns an item to a category, that item title becomes part of future learning for that category.

In practice, this means:
- `milk`, `melk`, and `lait` can all point at the same category if listed as aliases.
- `brød` can still match a bakery category even if the saved alias is `brod`.
- If many dairy items like `yoghurt`, `kefir`, and `milk` have been categorized under Dairy before, new dairy-like items are more likely to land there even without an exact alias.




## Create Super User



set variables in .env

</div>

<div align="center">

## Contributing

Contributions are welcome. Follow standard open-source contribution guidelines.

## License

Licensed under the MIT License.

</div>
