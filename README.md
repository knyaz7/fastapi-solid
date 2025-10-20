# FastAPI SOLID Template

A production-ready FastAPI application template built with SOLID principles, Domain-Driven Design (DDD), and Clean Architecture patterns. Demonstrates best practices for scalable, maintainable Python web applications.

## 🏗️ Architecture Overview

**Clean Architecture** with clear separation of concerns:
- **Domain Layer**: Pure business logic and entities
- **Application Layer**: Use cases, services, and interfaces  
- **Infrastructure Layer**: External dependencies (database, web framework, caching)

## 🚀 Features

### Core Architecture
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Domain-Driven Design (DDD)**: Rich domain models with clear boundaries
- **Dependency Injection**: Using `dependency-injector` for loose coupling
- **Unit of Work Pattern**: Transaction management with automatic rollback
- **Repository Pattern**: Data access abstraction
- **Error Handling**: Centralized exception handling with custom error types
- **Pagination**: Built-in pagination support for API endpoints

### Technology Stack
- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **SQLAlchemy 2.0**: Async ORM with type hints and modern syntax
- **PostgreSQL**: Production-ready relational database
- **Redis**: Caching and session storage
- **Alembic**: Database migrations
- **Pydantic**: Data validation and serialization
- **Rich**: Beautiful logging with colored output

### Advanced Features
- **Async/Await**: Full async support throughout the application
- **Caching**: Redis-based caching with `fastapi-cache2` and custom cache abstraction
- **Logging**: Structured logging with Rich console output and filtering
- **Database Migrations**: Automated schema management with Alembic
- **Docker Support**: Production-ready containerization with health checks
- **Type Safety**: Full type hints with mypy compatibility
- **Code Quality**: Ruff for linting and formatting
- **API Versioning**: Structured API versioning with `/api/v1` prefix
- **Data Conversion**: JSON to dataclass converters for serialization

## 📁 Project Structure

```
src/fastapi_solid/
├── domain/                    # Domain layer (business logic)
│   └── user/
│       └── model.py          # Domain entities
├── application/               # Application layer (use cases)
│   ├── exceptions/           # Custom exception hierarchy
│   │   ├── app_error.py      # Base application exceptions
│   │   └── error_types.py    # Error type definitions
│   ├── interfaces/           # Abstract interfaces
│   │   ├── common/
│   │   │   ├── key_value_cache.py # Cache interface
│   │   │   ├── pagination.py      # Pagination interface
│   │   │   └── uow.py             # Unit of Work interface
│   │   └── users/
│   │       └── repo.py       # Repository interface
│   └── users/
│       ├── dto.py            # Data Transfer Objects
│       └── service.py        # Application services
├── infrastructure/           # Infrastructure layer
│   ├── di/
│   │   └── container.py      # Dependency injection container
│   ├── fastapi/
│   │   ├── create_app.py     # FastAPI application factory
│   │   ├── dependencies/
│   │   │   └── pagination.py # Pagination dependencies
│   │   ├── endpoints/
│   │   │   ├── __init__.py   # API router configuration
│   │   │   └── v1/
│   │   │       └── users.py  # Versioned API endpoints
│   │   └── error_handler.py  # Global error handling
│   ├── migrator/             # Database migrations
│   ├── redis/
│   │   └── cache.py          # Redis cache implementation
│   └── sqlalchemy/           # Database implementation
│       ├── setup/
│       │   ├── base_model.py # SQLAlchemy base model
│       │   ├── base_repo.py  # Generic repository
│       │   └── engine.py     # Database engine
│       ├── uow.py            # Unit of Work implementation
│       └── user/
│           ├── repo.py       # User repository implementation
│           └── table.py      # User ORM model
└── utils/                    # Shared utilities
    ├── config/
    │   └── settings.py       # Configuration management
    ├── converters/
    │   ├── alch_to_dc.py     # ORM to dataclass converter
    │   └── json_to_dc.py     # JSON to dataclass converter
    └── logging/
        ├── logger.py         # Logging setup
        └── lib_log_filter.py # Library log filtering
```

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.13+
- Docker and Docker Compose
- UV package manager (recommended)

### Quick Start

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd fastapi-solid
   uv sync
   ```

2. **Set up environment:**
   ```bash
   cp db.env.example db.env
   cp env.example .env
   # Edit .env and db.env with your credentials
   ```

3. **Start services:**
   ```bash
   docker compose up --build -d
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the application:**
   ```bash
   # Development
   uv run fastapi-solid
   
   # Or using Docker (production-ready)
   docker compose up --build -d
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/api/docs`.


## 🚦 API Endpoints

### Users (`/api/v1/users`)
- `GET /api/v1/users` - Get all users with pagination support
- `GET /api/v1/users/random` - Get a random user (demonstrates custom caching)
- `GET /api/v1/users/{id}` - Get user by ID (cached for 10 seconds)
- `POST /api/v1/users` - Create a new user
- `DELETE /api/v1/users/{id}` - Delete a user

### Pagination
All list endpoints support pagination with query parameters:
- `limit` (1-100, default: 10) - Number of items per page
- `offset` (≥0, default: 0) - Number of items to skip

### Error Handling
- **Automatic validation** with Pydantic
- **Type safety** with UUID and datetime handling
- **Centralized error handling** with custom exception hierarchy
- **HTTP status mapping** for different error types
- **OpenAPI documentation** generation

## 🔄 Transaction Management

The application uses the **Unit of Work pattern** for transaction management:

```python
async with self.uow as unit_of_work:
    user = await self.users_repo.create(user_in)
    await unit_of_work.commit()  # Explicit commit
    # Automatic rollback on exception
```

## 🐳 Docker & Production Setup

### Production-Ready Dockerfile
- **Multi-stage build** with optimized layers
- **Security best practices** with non-root user execution
- **Minimal attack surface** with slim Python image
- **UV package manager** for fast dependency installation
- **Frozen dependencies** for reproducible builds

### Docker Compose with Health Checks
- **Service health monitoring** for all components
- **Dependency management** with proper startup order
- **Volume persistence** for database and Redis data
- **Network isolation** between services

### Configuration Management
- **Environment-based settings** with Pydantic
- **Configurable API port** via environment variables
- **Optimized logging** with colored terminal output
- **Development vs Production** configurations

## 🧪 Development

### Code Quality
- **Ruff** for linting and formatting
- **Type hints** throughout the codebase
- **Consistent code style** with automatic formatting

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Testing
The template is ready for testing with:
- **Pytest** for unit and integration tests
- **Test containers** for database testing
- **Mocking** with dependency injection
- **Async test support**

## 📚 Learning Resources

This template demonstrates:
- **Clean Architecture** principles
- **Domain-Driven Design** patterns
- **SOLID principles** in practice
- **Modern Python** async/await patterns
- **FastAPI** best practices with API versioning
- **SQLAlchemy 2.0** modern syntax
- **Dependency injection** patterns
- **Transaction management** strategies
- **Error handling** with custom exception hierarchy
- **Caching strategies** with Redis and custom abstractions
- **Pagination** implementation for scalable APIs
- **Data serialization** with Pydantic and custom converters
- **Production deployment** with Docker and health checks
- **Container security** best practices

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Add tests for new features
3. Update documentation as needed
4. Ensure all checks pass before submitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.