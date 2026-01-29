# Travel Planner API

This is a robust RESTful API for a Travel Planner application, built with a modern Python stack and following domain-driven design principles.

## 🚀 Technologies Used

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework.
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server for Python.
- **Database**: [SQLite](https://sqlite.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) ORM.
- **Configuration Management**: [Pydantic Settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/) for typed environment variables.
- **Rate Limiting**: [SlowAPI](https://github.com/laurentS/slowapi) for DDoS protection.
- **Containerization**: [Docker](https://www.docker.com/).
- **Validation**: [Pydantic](https://docs.pydantic.dev/) for data schemas.
- **External Integration**: [Art Institute of Chicago API](https://api.artic.edu/docs/) for artwork validation.

## ✨ Key Features

- **Project Management**: CRUD operations for travel projects.
- **Place Management**: Add and manage places (artworks) within projects.
- **Validation Business Logic**:
  - Maximum 10 places per project.
  - Transactions for atomic project/place creation.
  - Prevention of project deletion if any place is marked as "visited".
- **Centralized Error Handling**: Global exception handlers to prevent sensitive data leaks.
- **Centralized Logging**: Structured logging for database operations and API errors.
- **Rate Limiting**: Protects your endpoints from abuse.

## 🛠️ Setup & Local Running

### 1. Configure Environment

Create a `.env` file in the root directory (you can use the existing template):

```env
PROJECT_NAME="Travel Planner API"
DATABASE_URL="sqlite:///./travel_planner.db"
DEFAULT_RATE_LIMIT="60/minute"
```

### 2. Local Installation

1. Register and activate your virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🐳 Docker Support

If you have Docker installed, you can run the app without local Python installation:

1. **Build the image**:

   ```bash
   docker build -t travel-planner-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env travel-planner-api
   ```

## 📖 API Documentation

Once the server is running, explore the interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📁 Project Structure

```bash
app/
├── core/            # Configuration, database, and logging setup
├── external/        # External API clients (Art Institute)
├── places/          # Places domain (Router, Service, Repository, Schemas)
├── projects/        # Projects domain (Router, Service, Repository, Schemas)
└── main.py          # FastAPI application entry point
```
