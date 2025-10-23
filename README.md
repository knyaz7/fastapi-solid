# FastAPI SOLID Template

This repository serves as a reference example of how to properly write applications, demonstrating best practices using modern technologies:

- **FastAPI** - modern web framework with automatic documentation
- **PostgreSQL** via **SQLAlchemy** - relational database with modern ORM
- **MongoDB** via **Beanie** - document-oriented database
- **Redis** - caching and session storage
- **Alembic** - database migrations

## 🚀 Quick Start

```bash
# Clone and install dependencies
git clone <repository-url>
cd fastapi-solid
uv sync

# Setup environment
cp postgres.env.example postgres.env
cp mongo.env.example mongo.env

# Start services
docker compose up --build -d

# Apply migrations
docker exec -it fastapi-solid uv run alembic upgrade head
```

API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/api/docs`.

## 🏗️ Domain Layer

The domain layer contains pure business logic and domain entities. Here we define the core models of the business domain and business rules.

### Domain Entities

```python
@dataclass(frozen=True)
class User:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True)
class Player:
    id: UUID
    color: str
    is_alive: bool
    created_at: datetime
```

### Business Rules

```python
def can_add_player(color: str) -> bool:
    return color != "imposter"
```

## 📋 Application Layer

The application layer contains use cases, interfaces, and DTOs. Here we implement application logic without being tied to specific technologies.

### Repository Pattern

Repository interfaces are defined at the application level and abstract data access:

```python
class UserRepository(ABC):
    @abstractmethod
    async def get_all(self, pagination: Pagination | None = None) -> list[User]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> User | None: ...

    @abstractmethod
    async def create(self, user_in: UserIn) -> User: ...

    @abstractmethod
    async def update(self, id: UUID, update_data: UserUpdate) -> User: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
```

### Unit of Work Pattern

Transaction management through context manager:

```python
class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> UnitOfWork: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
```

### Use Cases (Application Services)

At this level, we never depend on infrastructure - all repositories and other dependencies are abstractions:

```python
class UserService:
    def __init__(self, uow: UnitOfWork, users_repo: UserRepository):
        self.uow = uow
        self.users_repo = users_repo

    async def create(self, user_in: UserIn) -> UserOut:
        async with self.uow as unit_of_work:
            user = await self.users_repo.create(user_in)
            await unit_of_work.commit()
        return UserOut.model_validate(user, from_attributes=True)
```

### DTOs (Data Transfer Objects)

```python
class UserIn(BaseModel):
    name: str

class UserOut(UserIn):
    id: UUID
    created_at: datetime

class UserUpdate(UserIn):
    pass
```

### Exceptions

```python
class AppError(Exception):
    def __init__(self, error_type: ErrorType, message: str):
        self.error_type = error_type
        self.message = message

class NotFound(AppError):
    def __init__(self, message: str):
        super().__init__(ErrorType.NOT_FOUND, message)
```

## 🔧 Infrastructure Layer

The infrastructure layer contains implementations of interfaces from the application layer and integrations with external systems.

### Dependency Injection

Configuration of dependencies using `dependency-injector`:

```python
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["fastapi_solid.infrastructure.fastapi.endpoints.v1"]
    )

    redis = providers.Singleton(
        Redis.from_url,
        settings.redis_dsn,
    )

    key_value_cache = providers.Singleton(RedisCache, redis_client=redis)

    al_session = providers.ContextLocalSingleton(async_session_factory)
    be_session = providers.ContextLocalSingleton(client.start_session)

    alchemy_uow = providers.Factory(AlchemyUnitOfWork, session=al_session)
    beanie_uow = providers.Factory(
        BeanieUnitOfWork if settings.mongo_use_transactions else DummyBeanieUnitOfWork,
        session=be_session,
    )

    users_repo = providers.Factory(
        AlchemyUserRepo, session=al_session, cache=key_value_cache
    )
    users_service = providers.Factory(
        UserService, uow=alchemy_uow, users_repo=users_repo
    )

    player_repo = providers.Factory(BeaniePlayerRepo, session=be_session)
    player_service = providers.Factory(
        PlayerService, uow=beanie_uow, players_repo=player_repo
    )
```

### FastAPI

Creating endpoints with dependency injection. The `@cache` decorator provides HTTP response caching:

```python
from fastapi_cache.decorator import cache

@users_router.get("", response_model=list[UserOut])
@inject
async def get_users(
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
    pagination: Annotated[Pagination, Depends(get_pagination)],
):
    return await users_service.get_all(pagination)

@users_router.get("/{id}", response_model=UserOut)
@cache(10)  # HTTP response caching
@inject
async def get_user(
    id: UUID,
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
):
    return await users_service.get_by_id(id)
```

### SQLAlchemy

#### Base Repository

Base repository provides common CRUD operations to avoid code duplication:

```python
class AlchemyRepo[T: Base]:
    model: type[T]
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def _get_all(self, pagination: Pagination | None = None) -> Sequence[T]: ...
    async def _get_by_id(self, id: UUID) -> T | None: ...
    async def _create(self, values: Mapping[str, Any]) -> T: ...
    async def _update_by_id(self, id: UUID, values: Mapping[str, Any]) -> T: ...
    async def _delete(self, id: UUID) -> None: ...
```

#### Repository Implementation

```python
class AlchemyUserRepo(UserRepository, AlchemyRepo[UserOrm]):
    model = UserOrm

    async def get_all(self, pagination: Pagination | None = None) -> list[User]:
        users_orm = await self._get_all(pagination)
        return [to_dataclass(u, User) for u in users_orm]

    async def create(self, user_in: UserIn) -> User:
        created_user = await self._create(user_in.model_dump())
        return to_dataclass(created_user, User)
```

### Beanie (MongoDB)

#### Base Repository

Base repository provides common CRUD operations for MongoDB:

```python
class BeanieRepo[T: Document]:
    model: type[T]
    
    def __init__(self, session: AsyncClientSession):
        self._session = session
    
    async def _get_all(self, pagination: Pagination | None = None) -> Sequence[T]: ...
    async def _get_by_id(self, id: UUID) -> T | None: ...
    async def _create(self, values: dict[str, Any]) -> T: ...
    async def _update_by_id(self, id: UUID, values: dict[str, Any]) -> T: ...
    async def _delete(self, id: UUID) -> None: ...
```

#### Repository Implementation

```python
class BeaniePlayerRepo(PlayerRepository, BeanieRepo[PlayerOdm]):
    model = PlayerOdm

    async def get_all(self, pagination: Pagination | None = None) -> list[Player]:
        docs = await self._get_all(pagination)
        return [to_dataclass(d, Player) for d in docs]

    async def create(self, player_in: PlayerIn) -> Player:
        doc = await self._create(player_in.model_dump())
        return to_dataclass(doc, Player)
```

### Redis

Caching implementation:

```python
class RedisCache(KeyValueCache):
    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def get(self, key: str) -> CacheResponse:
        return await self._redis_client.get(key)

    async def set(self, key: str, value: str | bytes, ttl: int) -> None:
        await self._redis_client.set(key, value, ex=ttl)
```

### Unit of Work for SQLAlchemy

```python
class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> "UnitOfWork":
        await self._session.__aenter__()
        return self

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
```

### Alembic

Database migration management:

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Beanie Migrations

MongoDB migration management using custom commands:

```bash
# Create new migration
uv run mongo-migrate-create <migration_name>

# Apply all forward migrations
uv run mongo-migrate-af

# Apply one forward migration
uv run mongo-migrate-of

# Rollback one migration
uv run mongo-migrate-ob

# Rollback all migrations
uv run mongo-migrate-ab
```

Example migration file:

```python
from beanie import Document, iterative_migration

class OldPlayerOdm(Document):
    id: UUID = Field(default_factory=uuid4)
    clor: str  # typo in field name
    is_alive: bool
    created_at: datetime

class NewPlayerOdm(Document):
    id: UUID = Field(default_factory=uuid4)
    color: str  # fixed field name
    is_alive: bool
    created_at: datetime

class Forward:
    @iterative_migration()
    async def clor_to_color(
        self, input_document: OldPlayerOdm, output_document: NewPlayerOdm
    ):
        output_document.color = input_document.clor

class Backward:
    @iterative_migration()
    async def clor_to_color(
        self, input_document: NewPlayerOdm, output_document: OldPlayerOdm
    ):
        output_document.clor = input_document.color
```

## 📁 Project Structure

```
src/fastapi_solid/
├── domain/                    # Domain layer
│   ├── user/
│   │   └── model.py          # User domain entity
│   └── player/
│       ├── model.py          # Player domain entity
│       └── rules.py          # Business rules
├── application/               # Application layer
│   ├── exceptions/           # Application exceptions
│   ├── interfaces/           # Interfaces
│   │   ├── common/           # Common interfaces
│   │   │   ├── key_value_cache.py
│   │   │   ├── pagination.py
│   │   │   └── uow.py
│   │   ├── users/
│   │   │   └── repo.py       # User repository interface
│   │   └── players/
│   │       └── repo.py       # Player repository interface
│   ├── users/
│   │   ├── dto.py            # User DTOs
│   │   └── service.py        # User service
│   └── players/
│       ├── dto.py            # Player DTOs
│       └── service.py        # Player service
├── infrastructure/           # Infrastructure layer
│   ├── di/
│   │   └── container.py      # Dependency injection container
│   ├── fastapi/
│   │   ├── create_app.py     # Application factory
│   │   ├── dependencies/
│   │   │   └── pagination.py # Pagination dependencies
│   │   ├── endpoints/
│   │   │   └── v1/
│   │   │       ├── users.py   # User endpoints
│   │   │       └── players.py # Player endpoints
│   │   └── error_handler.py  # Error handler
│   ├── alembic/             # Database migrations
│   ├── redis/
│   │   └── cache.py          # Redis cache implementation
│   ├── sqlalchemy/           # SQLAlchemy implementation
│   │   ├── setup/
│   │   │   ├── base_model.py # Base model
│   │   │   ├── base_repo.py  # Base repository
│   │   │   └── engine.py     # Database engine
│   │   ├── uow.py            # Unit of Work for SQLAlchemy
│   │   └── user/
│   │       ├── repo.py       # User repository
│   │       └── table.py      # User ORM model
│   └── beanie/               # Beanie implementation
│       ├── setup/
│       │   ├── base_repo.py  # Base repository
│       │   └── client.py     # MongoDB client
│       ├── uow.py            # Unit of Work for Beanie
│       └── player/
│           ├── repo.py       # Player repository
│           └── model.py      # Player ODM model
└── utils/                    # Utilities
    ├── config/
    │   └── settings.py       # Application settings
    ├── converters/           # Data converters
    │   ├── alch_to_dc.py     # SQLAlchemy -> dataclass
    │   ├── beanie_to_dc.py   # Beanie -> dataclass
    │   └── json_to_dc.py    # JSON -> dataclass
    └── logging/
        ├── logger.py         # Logging setup
        └── lib_log_filter.py # Library log filter
```