import requests
from fastapi import HTTPException

from app.core.config import settings

BASE_URL = settings.ART_API_BASE_URL


def get_artwork_details(external_id: int):
    """
    Fetches artwork details from Art Institute of Chicago API.
    Returns dictionary with title if found, else raises HTTPException.
    """
    url = f"{BASE_URL}/{external_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=f"Artwork with ID {external_id} not found in Art Institute API",
            )

        response.raise_for_status()
        data = response.json()

        # The API returns data wrapped in 'data'
        artwork_data = data.get("data")
        if not artwork_data:
            raise HTTPException(
                status_code=400,
                detail=f"Artwork with ID {external_id} not found in Art Institute API",
            )

        return {"id": artwork_data.get("id"), "title": artwork_data.get("title")}
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="External API unavailable")


def search_artworks(query: str = "", page: int = 1, limit: int = 50):
    """
    Searches artworks from Art Institute of Chicago API.
    """
    url = f"{BASE_URL}/search"
    params = {
        "page": page,
        "limit": limit,
        "fields": "id,title",  # Getting only needed fields
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        artworks = data.get("data", [])
        pagination = data.get("pagination", {})

        items = [
            {"external_id": art.get("id"), "title": art.get("title")}
            for art in artworks
        ]
        return {
            "items": items,
            "pagination": pagination,
        }
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="External API unavailable")
