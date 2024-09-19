To use PostgreSQL with Docker instead of SQLite in your SQLAlchemy setup, follow these steps:

### Step 1: Install PostgreSQL and Docker
First, ensure that you have Docker installed on your machine. Then, you can run PostgreSQL in a Docker container using a Docker image.

### Step 2: Pull the PostgreSQL Docker Image and Run a Container
You can pull a PostgreSQL Docker image and create a container with the following command:

```bash
docker pull postgres
```

Once the image is pulled, run the container:

```bash
docker run --name my_postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
```

- `myuser`: Replace with your preferred username.
- `mypassword`: Replace with your preferred password.
- `mydatabase`: Replace with the name of the database you want to create.
- The container will expose the PostgreSQL service on port `5432`.

### Step 3: Update Your Python Code for PostgreSQL

In your SQLAlchemy setup, modify the `SQLALCHEMY_DATABASE_URL` to connect to the PostgreSQL database running in the Docker container.

Install the necessary PostgreSQL driver for Python:

```bash
pip install psycopg2
```

Then, modify your `SQLALCHEMY_DATABASE_URL` to connect to PostgreSQL:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use the following URL format: 
# "postgresql://<username>:<password>@<host>:<port>/<database>"

# Update the connection string to connect to your Docker container
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Creates the database tables (if they don't already exist)
    Base.metadata.create_all(bind=engine)
```

### Step 4: Connect to the PostgreSQL Database

Now that your Docker container is running PostgreSQL, and your Python app is set up to connect to it via SQLAlchemy, you can proceed with defining your models and interacting with the PostgreSQL database.

### Example Docker Setup:

You can verify that the PostgreSQL container is running by checking Docker:

```bash
docker ps
```

The container should be listed as running, and you should be able to interact with it using SQLAlchemy from your Python code.

### Step 5: Optional - Docker Compose Setup

If you want to automate the setup, you can use **Docker Compose**. Here's a `docker-compose.yml` file that spins up a PostgreSQL container:

```yaml
version: '3'
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"
```

Run the following command to spin up the container using Docker Compose:

```bash
docker-compose up -d
```

This simplifies managing your Docker containers and ensures your PostgreSQL setup is reproducible across environments.
