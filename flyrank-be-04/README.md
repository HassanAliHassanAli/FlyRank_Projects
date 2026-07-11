# FlyRank Backend AI Internship: Assignment BE-04
## Containerize your stack

### 📌 Overview
This repository demonstrates the migration from an in-memory data store to a real PostgreSQL database running in Docker. **A Postgres repository replaced the in-memory one, while the service and routes remained completely unchanged.**

### 💾 Persistence Proof
Data persistence was proven across app and container restarts by following these steps:
1. Started the entire stack using `docker compose up --build -d`.
2. Inserted a new user row via the `POST /users/` endpoint.
3. Restarted the containers using `docker compose restart`.
4. Fetched the data via the `GET /users/` endpoint. The inserted data was still there, proving that the Docker volume (`pgdata`) successfully persisted the database state.