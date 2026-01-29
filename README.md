# Travel Planner API

This is a RESTful API for a Travel Planner application, built with FastAPI.

## Features

- Manage Travel Projects (Create, Read, Update, Delete)
- Manage Places to visit within projects
- Integration with Art Institute of Chicago API to validate places and fetch titles
- Max 10 places per project
- Prevent deleting projects with visited places

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Explore the API**:
   Open your browser and navigate to:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing

You can use the interactive Swagger UI to test endpoints.

### Example Workflow

1. **Create a Project**: POST `/projects/`
   ```json
   {
     "name": "Chicago Art Trip",
     "description": "Visiting museums",
     "start_date": "2023-10-27",
     "places": [{ "external_id": 129884 }, { "external_id": 24645 }]
   }
   ```
2. **List Projects**: GET `/projects/`
3. **Add Place**: POST `/projects/{id}/places`
   ```json
   { "external_id": 80607 }
   ```
4. **Mark as Visited**: PUT `/places/{place_id}`
   ```json
   { "visited": true, "notes": "Amazing painting!" }
   ```
