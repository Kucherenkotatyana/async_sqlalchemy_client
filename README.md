# Getting started

### 1. Please create the .env file and fill it with your credentials.
Use this command to copy .env.example:
```
cp .env.example .env
```

### 2. Build and run Docker containers:
```
docker compose build
```
```
docker compose up -d
```

### 3. Apply the migration inside the Docker container:
Enter the app container using the following command:
```
docker compose exec app alembic upgrade head
```

### 4. Run main.py file to interact with the program.
```
docker compose exec app python main.py
```

# Check code quality

### Run unit tests
```
pytest tests
```

### Run ruff to check if code formatting matches common best practices
```
ruff check
```

### Run mypy to check if there are any type mismatch errors in the code
```
mypy .
```
