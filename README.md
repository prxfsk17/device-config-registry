# Device Config Registry

A REST API that stores devices and their configurations. The domain is fictional (generic devices with parameters) and is used to practise backend development with a real database, migrations, tests, CI and deployment.

![CI](https://github.com/prxfsk17/device-config-registry/actions/workflows/ci.yml/badge.svg)

## Status

Work in progress. Implemented: device types, devices, versioned configurations and a diff between two versions.

## Tech stack

Python 3.12, FastAPI, SQLAlchemy 2, PostgreSQL 16, Alembic, pytest, Docker / Docker Compose, GitHub Actions

## Run with Docker

```bash
docker compose up --build
```

The API starts on http://localhost:8000, interactive docs are at http://localhost:8000/docs. Database migrations run automatically on start.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| POST, GET | `/device-types` | Create / list device types |
| GET | `/device-types/{id}` | Get one device type |
| POST, GET | `/devices` | Create / list devices |
| GET | `/devices/{id}` | Get one device |
| POST, GET | `/devices/{id}/configs` | Save a new configuration version / list versions |
| GET | `/devices/{id}/configs/latest` | Get the latest version |
| GET | `/devices/{id}/configs/{version}` | Get one version |
| GET | `/devices/{id}/configs/diff?from_version=1&to_version=2` | What was added, removed or changed between two versions |

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

Tests use FastAPI's test client with an in-memory SQLite database. The diff logic is a pure function (`app/diff.py`) with its own unit tests.

## Roadmap

- [x] Device types and devices, migrations, Docker, CI
- [x] Versioned configurations per device
- [x] Diff between two configuration versions
- [ ] Validation of parameters against rules of the device type
- [ ] Tests against PostgreSQL in CI
- [ ] Deployment on AWS EC2 with HTTPS
- [ ] Automatic deployment from GitHub Actions
