# Ampliación de Bases de Datos – Proyecto Final

Sistema full-stack que integra Django + DRF, Redis, MongoDB y Neo4j con despliegue dockerizado para cubrir los requisitos del proyecto final de la asignatura.

## Arquitectura

```
project/
├── app/
│   ├── config/                # settings, urls, asgi, channels
│   ├── core/                  # utilidades comunes (redis, otp, rate limiting)
│   ├── users/                 # autenticación con sesiones y OTP
│   ├── transcripts/           # CRUD completo sobre MongoDB con PyMongo
│   ├── realtime/              # canales WebSocket y contadores en Redis
│   ├── recommender/           # integración con Neo4j y endpoints de recomendación
│   ├── dashboards/            # dashboards y agregaciones con Chart.js
│   └── manage.py
├── scripts/                   # utilidades (seed, smoke tests)
├── docker/                    # Dockerfile y helpers
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── openapi.json
└── README.md
```

![Arquitectura](https://mermaid.ink/img/pako:eNp9kM1qwzAMhl9l5GvBIlFaVYUKs5hSpU5NlFSxI0YjlmptIGmNfy9tAbILle0x7177nF3oqRltVaGMfaiMMWWKAD2BUEa2wcTgeG1bTlYdbsFEk7uEa5d07JrWbY7l1irnOQ4_mWzRxtHHdYso1WeBMgA-5tSaa3UB4-4Bl1p8Vt7e0tbBVAOP3c0kryrjzfx5K_xH2Ptn7OYM1GCMur9aZ0G44gVtdm_kAE3vCg4ma8KRlWIMqRoNwsi9k5VPUf9hxKcJh8vBVnqh2cZpgH8RHecT7xkrgjujwWnZVBFwSUTJXk8X1idTn3FP_jzPxze8)

## Requisitos cubiertos

- **Django + DRF**: API principal, OpenAPI/Swagger en `/docs` (drf-spectacular).
- **Redis**: sesiones, rate limiting, OTP con TTL, contador global y notificaciones tiempo real (Channels + Redis pub/sub).
- **MongoDB + PyMongo**: CRUD total de transcripciones, filtros, agregaciones para dashboards y vistas Chart.js.
- **Neo4j**: modelos de usuarios/transcripciones/temas, recomendaciones por contenido, colaborativas e híbridas, consultas extra de usuarios similares y comunidades (GDS Louvain).
- **Dockerización**: servicios aislados (`web`, `redis`, `mongo`, `neo4j`), volúmenes persistentes, variables via `.env`.
- **Documentación**: README, `.env.example`, scripts de seed y `openapi.json` exportado.

## Puesta en marcha

```bash
cp .env.example .env
# Edita las variables si es necesario

docker compose up -d --build
```

La API quedará disponible en `http://localhost:8000`.

> 💡 **Windows/PowerShell**: para evitar conflictos con el alias integrado de `curl`, utiliza `curl.exe` (por ejemplo `curl.exe -X POST ...`) o `Invoke-RestMethod` con un diccionario de cabeceras (`-Headers @{"Content-Type"="application/json"}`).

Tras el primer arranque puedes seguir los logs con `docker compose logs -f web` para confirmar que el servicio está escuchando.

### Servicios en Docker Compose

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| web      | 8000   | Django + DRF + Channels servido con Daphne |
| redis    | 6379   | Cache, sesiones, OTP y pub/sub |
| mongo    | 27017  | Transcripciones (CRUD + agregaciones) |
| neo4j    | 7474/7687 | Motor de recomendaciones |

## Variables de entorno

Ver `.env.example`:

```
SECRET_KEY=changeme
DEBUG=1
ALLOWED_HOSTS=*
REDIS_URL=redis://redis:6379/0
MONGO_URI=mongodb://mongo:27017
MONGO_DB=abdb
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4jpass
```

## Casos de uso implementados

### Redis
- **Sesiones**: `SESSION_ENGINE` configurado para Redis.
- **OTP**: `POST /auth/otp/request` y `POST /auth/otp/verify`, TTL 120s y máximo 3 intentos en 10 minutos.
- **Cache**: `GET /cache/ping` realiza operación costosa y cachea resultados.
- **Tiempo real**: WebSocket `/ws/notifications/`, contador `/realtime/counter`, publicación en canal `events:transcriptions` al crear transcripciones.

### MongoDB
- Colección `transcriptions` manipulada con PyMongo.
- CRUD completo `/transcriptions/` con filtros por carpeta y temas.
- Agregaciones en `/dash/summary` para dashboards (gráfico de barras y donut en `/dash/`).

### Neo4j
- Endpoints `/reco/content/{user_id}`, `/reco/collab/{user_id}`, `/reco/hybrid/{user_id}`.
- Registro de escuchas `/reco/listen`.
- Consultas adicionales: `/reco/similar/{user_id}` (usuarios similares) y `/reco/communities` (Louvain sobre GDS).

### Documentación y pruebas
- OpenAPI exportado en `openapi.json`.
- Tests automatizados: OTP, caché, CRUD Mongo y recomendaciones.
- Scripts: `seed_mongo.py`, `seed_neo4j.py`, `smoke.sh`.

## Uso de la API (curl)

```bash
# Login
curl.exe -X POST http://localhost:8000/auth/login -d '{"username":"admin","password":"secret"}' -H "Content-Type: application/json"

# Solicitud OTP
curl.exe -X POST http://localhost:8000/auth/otp/request -d '{"user_id":1}' -H "Content-Type: application/json"

# Verificación OTP
curl.exe -X POST http://localhost:8000/auth/otp/verify -d '{"user_id":1,"code":"123456"}' -H "Content-Type: application/json"

# CRUD de transcripciones
curl.exe http://localhost:8000/transcriptions/

# WebSocket (notificaciones)
websocat ws://localhost:8000/ws/notifications/  # instala websocat o usa wscat

# Recomendaciones
curl.exe http://localhost:8000/reco/content/u1
curl.exe http://localhost:8000/reco/collab/u1
curl.exe http://localhost:8000/reco/hybrid/u1
```

## Scripts de semilla

```bash
# Requiere variables de entorno configuradas
# y dependencias instaladas (`pip install -r requirements.txt` si lo ejecutas desde tu máquina)
python scripts/seed_mongo.py
python scripts/seed_neo4j.py
```

## Tests

```bash
pip install -r requirements.txt
cd app
pytest
```

## Presentación técnica

1. **Redis**: sesiones de Django, OTP con TTL + rate limiting, caché y pub/sub para notificaciones.
2. **MongoDB**: almacenamiento documental de transcripciones con agregaciones para dashboards.
3. **Neo4j**: grafo de usuarios, transcripciones y temas con recomendaciones multi-enfoque y análisis de comunidades.
4. **Docker**: despliegue reproducible con servicios aislados y redes compartidas.

Este repositorio entrega todos los componentes solicitados para la asignatura, listos para demostración y defensa.
