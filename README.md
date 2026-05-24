# Docker-PythonAPI-MySQL
complete, working sample Docker project that runs a Python API (FastAPI) connected to a MySQL database, using Docker Compose

**1. Project Purpose**
Run a Python FastAPI app and a MySQL database together using Docker.

Use Docker Compose to manage both services easily.

**2. Folder Structure**

app/ → Python API code + Dockerfile

db/ → SQL file to initialize MySQL

docker-compose.yml → Defines and runs both containers

**3. Python API (FastAPI)**
main.py:

Creates FastAPI app

Connects to MySQL using hostname mysql

/ endpoint → returns a message

/users endpoint → returns users from database

requirements.txt → lists Python dependencies

Dockerfile → builds the API image:

Uses Python 3.11

Installs dependencies

Runs Uvicorn on port 8000

**4. MySQL Database**
init.sql:

Creates database mydb

Creates users table

Inserts sample users (Alice, Bob, Charlie)

MySQL container automatically runs this file on first startup.

**5. Docker Compose**
Defines two services:

a) api
Builds from app/

Exposes port 8000

Depends on MySQL

Shares the same internal network

b) mysql
Uses official MySQL image

Loads init.sql automatically

Stores data in a persistent volume

Exposes port 3306

**6. Networking**
Docker Compose creates a private network.

API connects to MySQL using hostname: mysql

No IP address needed.

**7. Data Persistence**
MySQL data stored in a Docker volume:

Data survives container restarts

Safe and persistent

**8. Running the Project**
Code
docker compose up --build
Then visit:

http://localhost:8000

http://localhost:8000/users
