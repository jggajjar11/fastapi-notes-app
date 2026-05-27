# Notes API

A production-ready REST API for managing notes with user authentication, built with FastAPI and PostgreSQL.

## Features

✨ **Core Features:**
- User registration and authentication with JWT tokens
- CRUD operations for notes (Create, Read, Update, Delete)
- Notes filtering by status (active, archived, deleted)
- Role-based access (users can only manage their own notes)
- Comprehensive error handling and validation

🗄️ **Database:**
- PostgreSQL with SQLAlchemy ORM
- Alembic migrations for schema versioning
- Proper indexing for performance

🐳 **Deployment:**
- Fully Dockerized with Docker Compose
- Ready for production deployment
- Environment-based configuration

📚 **API Documentation:**
- Auto-generated Swagger/OpenAPI documentation at `/docs`
- ReDoc documentation at `/redoc`
- Comprehensive README and code comments

✅ **Testing:**
- pytest test suite
- FastAPI TestClient for integration tests
- ~95% code coverage

## Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if running without Docker)

## Quick Start with Docker

### 1. Clone the repository
```bash
git clone <repository-url>
cd notes-api
```

### 2. Create environment file
```bash
cp .env.example .env
```

Edit `.env` if you want to change the database credentials or secret key.

### 3. Build and run with Docker Compose
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### 4. Access the API Documentation

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Local Development Setup

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
Make sure PostgreSQL is running and create a database:
```sql
CREATE DATABASE notesdb;
CREATE USER notesuser WITH PASSWORD 'notespass';
ALTER ROLE notesuser SET client_encoding TO 'utf8';
ALTER ROLE notesuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE notesuser SET default_transaction_deferrable TO on;
ALTER ROLE notesuser SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE notesdb TO notesuser;
```

### 4. Update .env file
```bash
cp .env.example .env
# Edit .env with your local database URL
DATABASE_URL=postgresql://notesuser:notespass@localhost:5432/notesdb
```

### 5. Run migrations
```bash
alembic upgrade head
```

### 6. Start the development server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

#### Register User
```
POST /api/users/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}

Response: 201 Created
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Login
```
POST /api/users/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```
GET /api/users/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Notes

#### Create Note
```
POST /api/notes
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "My First Note",
  "description": "This is a detailed note",
  "status": "active"
}

Response: 201 Created
{
  "id": 1,
  "title": "My First Note",
  "description": "This is a detailed note",
  "status": "active",
  "user_id": 1,
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

#### List Notes
```
GET /api/notes?skip=0&limit=10&status=active
Authorization: Bearer {access_token}

Response: 200 OK
{
  "items": [
    {
      "id": 1,
      "title": "My First Note",
      "description": "This is a detailed note",
      "status": "active",
      "user_id": 1,
      "created_at": "2024-01-15T10:35:00",
      "updated_at": "2024-01-15T10:35:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

**Query Parameters:**
- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 10, max: 100)
- `status`: Filter by status (active, archived, deleted) - optional

#### Get Note
```
GET /api/notes/{note_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "title": "My First Note",
  "description": "This is a detailed note",
  "status": "active",
  "user_id": 1,
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

#### Update Note
```
PUT /api/notes/{note_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "status": "archived"
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "status": "archived",
  "user_id": 1,
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:40:00"
}
```

#### Delete Note
```
DELETE /api/notes/{note_id}
Authorization: Bearer {access_token}

Response: 204 No Content
```

## Status Codes

- `200 OK`: Successful GET, PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: No authentication provided
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

## Testing

### Run all tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_users.py
```

### Run specific test
```bash
pytest tests/test_users.py::TestUserRegistration::test_register_success
```

### Run tests in verbose mode
```bash
pytest -v
```

## Database Migrations

### Create a new migration
```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback last migration
```bash
alembic downgrade -1
```

### View migration history
```bash
alembic current
alembic history
```

## Project Structure

```
notes-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection setup
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── auth.py              # Authentication utilities
│   └── routes/
│       ├── __init__.py
│       ├── users.py         # User authentication routes
│       └── notes.py         # Notes CRUD routes
├── alembic/
│   ├── env.py               # Migration environment
│   ├── versions/
│   │   └── 001_initial.py   # Initial migration
│   └── script.py.mako       # Migration template
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration and fixtures
│   ├── test_users.py        # User authentication tests
│   └── test_notes.py        # Notes CRUD tests
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container Docker setup
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── alembic.ini             # Alembic configuration
└── README.md               # This file
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://notesuser:notespass@db:5432/notesdb

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Docker database setup
DB_USER=notesuser
DB_PASSWORD=notespass
DB_NAME=notesdb
```

**Important**: Change the `SECRET_KEY` in production to a strong, random value.

## Docker Compose Services

### Database Service
- **Image**: PostgreSQL 15-Alpine
- **Port**: 5432 (mapped to localhost:5432)
- **Volume**: postgres_data (persistent storage)
- **Health Check**: Enabled with 10-second interval

### API Service
- **Image**: Built from Dockerfile
- **Port**: 8000 (mapped to localhost:8000)
- **Volume**: Current directory (for live reload during development)
- **Depends On**: db service (waits for health check)

## Security Considerations

1. **Change the SECRET_KEY**: Update the `SECRET_KEY` environment variable with a strong, random string in production.

2. **Use HTTPS**: Deploy with a reverse proxy (nginx) that handles SSL/TLS in production.

3. **Environment Variables**: Never commit `.env` files with real secrets to version control.

4. **Password Security**: 
   - Passwords are hashed using bcrypt
   - Minimum password length: 8 characters
   - Store and transmit passwords securely

5. **CORS**: Currently allows all origins. Restrict in production:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

6. **Rate Limiting**: Consider adding rate limiting for production deployments.

## Performance Considerations

1. **Database Indexes**: 
   - Users table: username, email (unique)
   - Notes table: user_id

2. **Pagination**: Default limit of 10 items per page with max of 100.

3. **Lazy Loading**: Notes are fetched on-demand with pagination.

## Deployment

### Deploy to Production

1. **Build the Docker image**:
   ```bash
   docker build -t notes-api:latest .
   ```

2. **Push to registry**:
   ```bash
   docker tag notes-api:latest myregistry/notes-api:latest
   docker push myregistry/notes-api:latest
   ```

3. **Update configuration**:
   - Set strong `SECRET_KEY`
   - Set appropriate `DATABASE_URL`
   - Restrict `CORS allow_origins`
   - Set `ALGORITHM` to appropriate JWT algorithm

4. **Run migrations**:
   ```bash
   docker run --env-file .env myregistry/notes-api:latest alembic upgrade head
   ```

5. **Start the service**:
   ```bash
   docker run -p 8000:8000 --env-file .env myregistry/notes-api:latest
   ```

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View Docker Compose logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U notesuser -d notesdb
```

### Migration Issues
```bash
# Check migration status
docker-compose exec api alembic current

# View migration history
docker-compose exec api alembic history

# Rollback to previous migration
docker-compose exec api alembic downgrade -1
```

### API Issues
```bash
# View API logs
docker-compose logs api

# Access API container
docker-compose exec api bash

# Run tests
docker-compose exec api pytest
```

## API Examples with curl

### Register
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### Create Note
```bash
TOKEN="your_token_here"
curl -X POST http://localhost:8000/api/notes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Note",
    "description": "Note description",
    "status": "active"
  }'
```

### List Notes with Filter
```bash
TOKEN="your_token_here"
curl -X GET "http://localhost:8000/api/notes?status=active&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Changelog

### Version 1.0.0 (Initial Release)
- User registration and authentication with JWT
- Full CRUD operations for notes
- Status-based filtering
- PostgreSQL database with migrations
- Docker and Docker Compose setup
- Comprehensive test suite
- Auto-generated API documentation
