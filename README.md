# VetAPI — Veterinary Clinic Management API

A RESTful backend API for managing veterinary clinic operations, built with **Python, FastAPI, SQLAlchemy, and PostgreSQL**. VetAPI provides endpoints for managing pets, owners, veterinary visits, and user accounts, with JWT-based authentication and role-based access control.

The application uses UUIDs for entity identifiers, Pydantic schemas for request validation and response serialization, and Alembic for database schema migrations.

## Features

- **Pet Management:** Create, retrieve, update, search, filter, sort, and soft-delete pet records.
- **Owner Management:** Register pet owners and retrieve owner information.
- **Visit Management:** Create, retrieve, update, and delete veterinary visit records.
- **Relationship Management:** Associate pets with owners and visits with pets.
- **JWT Authentication:** Authenticate users and issue access tokens.
- **Role-Based Access Control:** Restrict operations according to Admin, Vet, and Receptionist roles.
- **Password Hashing:** Hash passwords using Passlib and bcrypt.
- **Advanced Pet Queries:** Filter by species, breed, owner name, age range, and search term, with pagination and sorting.
- **Database ORM:** Use SQLAlchemy to manage database models and queries.
- **Database Migrations:** Manage schema changes with Alembic.
- **Request Logging:** Record HTTP methods, paths, response statuses, and request processing times.
- **Error Handling:** Provide consistent JSON responses for HTTP errors, validation errors, and unexpected server errors.
- **Interactive API Documentation:** Explore and test endpoints through FastAPI's Swagger UI.
- **Docker Support:** Build and run the API using the included Dockerfile.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| SQLAlchemy | ORM and database operations |
| PostgreSQL | Relational database |
| Psycopg2 | PostgreSQL database driver |
| Pydantic | Request validation and response schemas |
| Pydantic Settings | Environment-based configuration |
| Alembic | Database schema migrations |
| Python-JOSE | JWT creation and validation |
| Passlib | Password hashing and verification |
| Bcrypt | Password-hashing algorithm |
| Docker | Containerization |

## Architecture

```text
                   Client
                     |
                     v
                  FastAPI
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Pet API    Owner API   Visit API
          |          |          |
          +----------+----------+
                     |
                     v
                SQLAlchemy
                     |
                     v
                 PostgreSQL

              Authentication
                     |
                     v
              JWT Access Tokens
                     |
                     v
           Role-Based Authorization

              Alembic Migrations
                     |
                     v
             Database Schema
```

## Project Structure

```text
VetAPI/
├── alembic/
│   ├── versions/
│   │   ├── 3e57ab06de47_add_users_table.py
│   │   └── 56dabfa4db0a_initial_schema.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── .dockerignore
├── .env.example
├── .gitignore
├── .python-version
├── Dockerfile
├── OwnerModels.py
├── PetModels.py
├── UserModels.py
├── VisitModels.py
├── alembic.ini
├── config.py
├── crud.py
├── database.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── schemas.py
└── security.py
```

## Database Models

### Pet

Stores pet details, including:

- UUID identifier
- Name, species, breed, and age
- Associated owner ID
- Creation and update timestamps
- Soft-deletion status and deletion timestamp

### Owner

Stores owner information, including:

- UUID identifier
- Name, phone number, and email
- Creation and update timestamps

The owner's email is configured as a unique field.

### Visit

Stores veterinary visit records, including:

- UUID identifier
- Associated pet ID
- Visit date
- Reason for the visit
- Clinical notes
- Creation and update timestamps

A pet can have multiple visits. The SQLAlchemy relationship and foreign-key configuration support cascading behavior for associated visit records when a pet is physically deleted. The API's pet deletion endpoint, however, performs a **soft delete** by setting `is_deleted` and `deleted_at`.

### User

Stores authentication and authorization information, including:

- UUID identifier
- Name and unique email
- Hashed password
- Role
- Creation and update timestamps

The supported roles are `ADMIN`, `VET`, and `RECEPTIONIST`.

## API Endpoints

The following endpoints are defined in `main.py`.

### Home

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Check whether the API is running |

### Pets

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/pets` | Create a pet |
| `GET` | `/pets` | List pets with filtering, sorting, search, and pagination |
| `GET` | `/pets/{pet_id}` | Retrieve a pet by UUID |
| `PUT` | `/pets/{pet_id}` | Update pet information |
| `DELETE` | `/pets/{pet_id}` | Soft-delete a pet |
| `POST` | `/pets/{pet_id}/visits` | Create a visit for a pet |
| `GET` | `/pets/{pet_id}/visits` | Retrieve visits for a pet |

### Owners

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/owners` | Create an owner |
| `GET` | `/owners` | Retrieve all owners |
| `GET` | `/owners/{owner_id}/pets` | Retrieve pets associated with an owner |

### Visits

| Method | Endpoint | Description |
|---|---|---|
| `PUT` | `/visits/{visit_id}` | Update a visit |
| `DELETE` | `/visits/{visit_id}` | Delete a visit |

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a user; requires Admin authorization |
| `POST` | `/auth/login` | Authenticate a user and obtain a JWT access token |
| `GET` | `/auth/user-context` | Retrieve the authenticated user's information |

## Authorization

VetAPI uses JWT bearer tokens to authenticate users and enforce role-based access.

| Operation | Required role |
|---|---|
| Create a pet | Receptionist or Admin |
| Update a pet | Vet or Admin |
| Delete a pet | Admin |
| Create a visit | Receptionist or Admin |
| Update a visit | Receptionist or Admin |
| Delete a visit | Receptionist or Admin |
| Register a user | Admin |
| Log in | Valid credentials |
| Retrieve authenticated user context | Authenticated user |

Some read endpoints, including pet listings and owner retrieval, are not protected by authentication in the current implementation.

### Authentication Flow

1. An authorized administrator registers a user through `POST /auth/register`.
2. The user logs in through `POST /auth/login` using form-encoded credentials.
3. The API verifies the password against the stored hash.
4. The API returns a JWT access token.
5. The client sends the token in the `Authorization` header for protected endpoints.

Example header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The token expiration is configurable through `ACCESS_TOKEN_EXPIRE_MINUTES`.

## Getting Started

### Prerequisites

- Python 3.14 or a compatible Python version supported by the project dependencies.
- PostgreSQL database.
- Git.
- Optional: Docker for containerized execution.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/VetAPI.git
cd VetAPI
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository URL if necessary.

### 2. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Using `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Alternatively, install the project from its `pyproject.toml` using `uv`:

```bash
pip install uv
uv pip install --system .
```

When using the `uv` command above, ensure the installation environment is the one you intend to use.

### 4. Configure Environment Variables

Create a `.env` file in the project root. You can use `.env.example` as a reference.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/vetapi
JWT_SECRET_KEY=replace_with_a_secure_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Replace the database URL with your actual PostgreSQL connection string.

**Important:**

- Use a strong, randomly generated JWT secret.
- Keep `.env` out of version control.
- Never commit production database credentials or signing secrets.
- Ensure the database exists and is reachable before starting the application.

### 5. Apply Database Migrations

The repository includes Alembic configuration and migration scripts.

Run:

```bash
alembic upgrade head
```

This applies the available migrations to your configured database.

The current application also calls `Base.metadata.create_all()` during startup. For existing deployments, use Alembic to manage schema changes and verify the migration state before starting the API.

### 6. Start the API

Run from the project root:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Interactive API Documentation

FastAPI automatically generates API documentation.

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

Use Swagger UI to inspect request schemas, send API requests, authenticate with a bearer token, and review responses.

## Example Requests

### Create an Owner

**`POST /owners`**

```json
{
  "name": "Alex Morgan",
  "phone": "9876543210",
  "email": "alex@example.com"
}
```

This endpoint requires Receptionist or Admin authorization. The returned owner record includes its generated UUID.

### Create a Pet

**`POST /pets`**

```json
{
  "name": "Bella",
  "species": "Dog",
  "breed": "Labrador",
  "age": 3,
  "owner_id": "REPLACE_WITH_OWNER_UUID"
}
```

Replace the owner ID with a valid UUID from an existing owner record.

This endpoint requires Receptionist or Admin authorization.

### Filter Pets

**`GET /pets`**

Example query:

```text
/pets?species=Dog&min_age=1&max_age=8&page=1&limit=10&sort_by=name&sort_order=asc
```

Supported query parameters include:

- `species`
- `breed`
- `owner_name`
- `min_age`
- `max_age`
- `search`
- `page`
- `limit`
- `sort_by`
- `sort_order`

### Create a Visit

**`POST /pets/{pet_id}/visits`**

```json
{
  "visit_date": "2026-10-22T10:30:00",
  "reason": "Routine checkup",
  "notes": "General examination"
}
```

Replace `{pet_id}` with the UUID of an existing pet. This endpoint requires Receptionist or Admin authorization.

### Log In

**`POST /auth/login`**

This endpoint uses `application/x-www-form-urlencoded` credentials, as required by `OAuth2PasswordRequestForm`.

Fields:

```text
username=alex@example.com
password=your_password
```

Although the form field is named `username`, the application uses its value as the user's email address.

Example response:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "token_type": "bearer"
}
```

Use the returned token to call protected endpoints.

## Database Migrations

Alembic manages database schema changes.

Common commands:

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "describe schema change"

# Apply pending migrations
alembic upgrade head

# View the current migration revision
alembic current

# View migration history
alembic history
```

Always inspect autogenerated migration files before applying them, and back up important databases before schema changes.

## Docker

A `Dockerfile` is included for containerized execution.

Build the image:

```bash
docker build -t vetapi .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 vetapi
```

Ensure `DATABASE_URL` points to a database reachable from inside the container. A PostgreSQL server running on the host may require a different hostname than `localhost` from the container's perspective.

After starting the container, open:

`http://127.0.0.1:8000/docs`

## Error Handling and Logging

The application includes:

- Request logging with HTTP method, path, status code, and processing time.
- Structured JSON responses for HTTP exceptions.
- JSON responses for validation failures.
- Logging of unhandled server exceptions.
- Standard HTTP status codes for missing resources, invalid credentials, and insufficient permissions.

## Security Considerations

- Passwords are hashed before being stored.
- JWTs are used to authenticate protected requests.
- Role dependencies restrict selected operations to authorized users.
- Environment variables keep database credentials and JWT secrets outside source code.

**Before production deployment:** remove any debugging statements that print submitted passwords, use a strong secret, review which read endpoints should require authentication, configure CORS with explicit trusted origins, and validate authorization for all sensitive data operations.

## Future Improvements

Potential extensions include:

- Add automated tests for endpoints and authorization rules.
- Introduce service and router modules to separate concerns as the application grows.
- Add stronger validation for pet and visit fields.
- Add database transaction and error-handling improvements.
- Add response pagination metadata.
- Introduce audit logging for changes to clinical records.
- Add deployment automation and monitoring.
- Expand access controls and data isolation for production use.

## License

No license has been specified in the repository. Add a `LICENSE` file if you intend to distribute the project under a particular open-source license.

---

**Built with Python, FastAPI, SQLAlchemy, PostgreSQL, and Alembic.**
