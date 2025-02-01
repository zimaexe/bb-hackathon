# Digital fair portal for [Revúca](https://revuca.sk) city

## Set up development environment

```bash
cp .env.example .env
source .env
```

## Services

### Backend

```bash
poetry shell
poetry install --no-root
docker compose up -d
alembic upgrade head
fastapi dev backend/main.py
```

### Frontend

```bash
cd frontend
yarn install
yarn dev
```

## Availiablity

Frontend will be availiable on `localhost:3000`
Backend will be availiable on `localhost:8000`
