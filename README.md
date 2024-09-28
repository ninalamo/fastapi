We’ll go through creating a complete FastAPI project with CRUD operations, including setting up the virtual environment, installing dependencies, and initializing the database.
gasasg
### Complete Setup for FastAPI CRUD API

#### 1. **Create Project Directory**

```bash
mkdir fastapi-crud-docker
cd fastapi-crud-docker
```

#### 2. **Set Up Virtual Environment**

Create a virtual environment named `venv`:

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 3. **Install Dependencies**

Install FastAPI, Uvicorn, and SQLAlchemy:

```bash
pip install fastapi uvicorn sqlalchemy
```

Add `python-dotenv` to handle environment variables (optional but recommended):

```bash
pip install python-dotenv
```

Create `requirements.txt`:

```bash
pip freeze > requirements.txt
```

#### 4. **Create Project Files**

**1. `app/main.py`**:
This file contains the FastAPI application and routes.

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from . import crud, models, database

app = FastAPI()

# Initialize database
database.init_db()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    done: bool = False

class ItemInDB(Item):
    id: int

# Create Item
@app.post("/items/", response_model=ItemInDB)
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = crud.create_item(db=db, item=item)
    return db_item

# Read Items
@app.get("/items/", response_model=List[ItemInDB])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items

# Read Item by ID
@app.get("/items/{item_id}", response_model=ItemInDB)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Update Item
@app.put("/items/{item_id}", response_model=ItemInDB)
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete Item
@app.delete("/items/{item_id}", response_model=ItemInDB)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

**2. `app/models.py`**:
Define the SQLAlchemy model for the items.

```python
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Boolean, default=False)
```

**3. `app/crud.py`**:
CRUD operations interact with the database.

```python
from sqlalchemy.orm import Session
from . import models
from .main import Item

def create_item(db: Session, item: Item):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: Item):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
```

**4. `app/database.py`**:
Database connection and session setup.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for simplicity

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
```

#### 5. **Run the Application Locally**

Make sure you are in your virtual environment and run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` in your browser to see the interactive API documentation provided by FastAPI.

#### 6. **Build and Run with Docker (Optional)**

**Create a `Dockerfile`:**

```Dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create a `docker-compose.yml`:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

**Build and run the Docker container:**

```bash
docker-compose up --build
```

Visit `http://localhost:8000/docs` to access the API.

### Summary

- **Project Structure**: Includes `main.py`, `models.py`, `crud.py`, and `database.py`.
- **Database Initialization**: `init_db` creates tables.
- **Running Locally**: Use Uvicorn to run the FastAPI app.
- **Docker Setup**: Optional but useful for containerizing the application.

Let me know if you encounter any issues or have further questions!

<hr/>

To modify the FastAPI CRUD API setup to use PostgreSQL instead of SQLite, you'll need to make adjustments to the `app/database.py`, update the project’s dependencies to include `psycopg2`, and ensure that your database credentials are securely managed.

### Steps to Use PostgreSQL with FastAPI

#### 1. **Install PostgreSQL and psycopg2**

Make sure PostgreSQL is installed on your system. You can download it from [here](https://www.postgresql.org/download/).

Next, install `psycopg2`, the PostgreSQL adapter for Python, along with other dependencies:

```bash
pip install psycopg2-binary
```

Update your `requirements.txt` to include `psycopg2-binary`:

```bash
pip freeze > requirements.txt
```

#### 2. **Update `app/database.py`**

Modify the `SQLALCHEMY_DATABASE_URL` to use PostgreSQL instead of SQLite. You'll also need to define environment variables for your database credentials.

Here’s the updated `app/database.py`:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database URL format for PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "yourpassword")
POSTGRES_DB = os.getenv("POSTGRES_DB", "yourdatabase")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create the engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
```

#### 3. **Set Environment Variables**

Create a `.env` file in the root of your project to store your PostgreSQL credentials:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=yourdatabase
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Make sure to add the `.env` file to your `.gitignore` to avoid committing sensitive credentials.

#### 4. **Run PostgreSQL Locally (Optional)**

If you're running PostgreSQL locally using Docker, you can define a service in `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: yourdatabase
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  web:
    build: .
    depends_on:
      - db
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: yourdatabase
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432

volumes:
  postgres_data:
```

#### 5. **Apply Database Migrations**

In a production setup, instead of using `Base.metadata.create_all()` directly, it's better to use a database migration tool like **Alembic** to handle schema changes.

First, install Alembic:

```bash
pip install alembic
```

Then, initialize Alembic in your project:

```bash
alembic init alembic
```

Next, configure Alembic to connect to your PostgreSQL database by editing `alembic.ini`:

```ini
sqlalchemy.url = postgresql://postgres:yourpassword@localhost:5432/yourdatabase
```

You can now create migrations with:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

#### 6. **Run the Application**

Start PostgreSQL, then run your FastAPI application:

```bash
uvicorn app.main:app --reload
```

You can now access the API at `http://127.0.0.1:8000/docs` and see that the application is now connected to PostgreSQL.

#### 7. **Dockerize with PostgreSQL**

Update your `Dockerfile` to ensure it works with PostgreSQL and Docker Compose.

Here’s an updated `Dockerfile` that includes PostgreSQL:

```Dockerfile
# Use a base image with Python 3.9
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

To run your application using Docker, make sure Docker is installed and then run:

```bash
docker-compose up --build
```

You can now access the API at `http://localhost:8000/docs`.

### Summary of Changes
- **Database**: PostgreSQL replaces SQLite using `psycopg2` as the driver.
- **Environment Variables**: Credentials and database configuration are managed through a `.env` file.
- **Docker**: You can run PostgreSQL and your FastAPI application with Docker Compose for easier setup and deployment.

This setup enables a full CRUD API connected to a PostgreSQL database and ready for use in local or Docker environments. Let me know if you need further details!