# Docker-PythonAPI-MySQL
complete, working sample Docker project that runs a Python API (FastAPI) connected to a MySQL database, using Docker Compose

**1. Project Structure — What Each Part Represents**
Code
myproject/
│
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── db/
│   └── init.sql
│
└── docker-compose.yml
This structure separates your application layer, database layer, and orchestration layer.

**2. The Python API (FastAPI)**
'app/main.py'
This file defines your web API.

What happens inside:
a) FastAPI app creation
python
'app = FastAPI()'
This creates the ASGI application object. Uvicorn will run this object as the web server.

b) Database connection function
python
def get_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="rootpassword",
        database="mydb"
    )
Key detail:
host="mysql" works because Docker Compose creates an internal DNS entry for the MySQL container.
Inside the network, the MySQL container is reachable simply as:

Code
mysql
No IPs needed.

c) API endpoints
python
@app.get("/")
def root():
    return {"message": "Python API + MySQL via Docker!"}
This is a simple health check endpoint.

python
@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users;")
    rows = cursor.fetchall()
    return {"users": rows}
This endpoint:

Connects to MySQL

Runs a SQL query

Returns the results as JSON

This is a real working API endpoint backed by a real database.

3. Python Dockerfile — How the API Container Is Built




app/Dockerfile
dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
What each step does:
FROM python:3.11-slim  
Lightweight Python base image.

WORKDIR /app  
All commands run inside /app.

COPY requirements.txt .  
Copies only the dependency file first → enables Docker caching.

RUN pip install …  
Installs dependencies inside the image.

COPY . .  
Copies your application code.

EXPOSE 8000  
Documents that the app listens on port 8000.

CMD ["uvicorn", ...]  
Starts the FastAPI server.

This container becomes your web service.

4. MySQL Initialization Script
db/init.sql




This script is automatically executed by MySQL on first startup.

sql
CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO users (name) VALUES ("Alice"), ("Bob"), ("Charlie");
This ensures:

The database exists

The users table exists

Sample data is inserted

This is how you bootstrap a database in Docker.

5. Docker Compose — The Orchestrator
docker-compose.yml


This file defines how all containers run together.

🔹 Service 1: API
yaml
api:
  build: ./app
  container_name: python_api
  ports:
    - "8000:8000"
  depends_on:
    - mysql
  networks:
    - backend
What this means:
build: ./app → Build the API image from the Dockerfile in app/

ports: "8000:8000" → Expose API to your host machine

depends_on: mysql → Start MySQL before the API

networks: backend → API joins the internal network

🔹 Service 2: MySQL
yaml
mysql:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: rootpassword
    MYSQL_DATABASE: mydb
  volumes:
    - mysql_data:/var/lib/mysql
    - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
  ports:
    - "3306:3306"
  networks:
    - backend
Key behaviors:
a) MySQL image
Uses the official MySQL 8.0 image.

b) Environment variables
These configure MySQL on startup.

c) Volumes
Two important mounts:

mysql_data:/var/lib/mysql  
Persistent storage for database files
→ Your data survives container restarts.

init.sql:/docker-entrypoint-initdb.d/  
MySQL automatically runs any .sql file in this folder on first startup.

d) Ports
3306:3306 exposes MySQL to your host (optional but useful for tools like MySQL Workbench).

e) Network
Both services share the same internal network → they can talk to each other.

🔗 6. How the Containers Communicate
Inside the Docker network:

API container hostname: python_api

MySQL container hostname: mysql

So the API connects to MySQL using:

Code
host="mysql"
Docker Compose automatically provides:

DNS resolution

Internal networking

Isolated environment

This is why you don’t need IP addresses.

7. How Data Persistence Works




The volume:

yaml
volumes:
  mysql_data:
Maps to:

Code
/var/lib/mysql
This is where MySQL stores:

Tables

Indexes

Binary logs

Metadata

Even if you delete the MySQL container:

Code
docker rm -f mysql
Your data remains in the volume.

8. Running the Entire Stack
Code
docker compose up --build
What happens:

MySQL container starts

MySQL initializes database + tables

API container builds

API connects to MySQL

You can access:

API root:
http://localhost:8000

Users endpoint:
http://localhost:8000/users
