from http.client import HTTPException

import requests

from database_models import TicketModel
from models import MovieModel, ShowModel, ScreenModel, TheatreModel, SeatsResponse, BookingRequest, BookingResponse, \
    TicketResponse
from datetime import time,datetime

API_URL = "http://127.0.0.1:8000"

def get_theatres_by_movie_id(movie_id:int):
    try:
        resp = requests.get(f"{API_URL}/movies/{movie_id}/theatres")
        resp.raise_for_status()
        resp = resp.json()
        # theatres = [TheatreModel(**t) for t in resp]
        return resp
    except requests.HTTPError as e:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_all_movies():
    try:
        resp = requests.get(f"{API_URL}/movies")
        resp.raise_for_status()
        resp = resp.json()
        # movies = [MovieModel(**movie) for movie in resp]
        return resp
    except HTTPException as e:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_movies_by_title(title:str):
    try:
        resp = requests.get(url=f"{API_URL}/movies/search/{title}")
        resp.raise_for_status()
        resp = resp.json()
        # print(resp)
        # return [MovieModel(**movie) for movie in resp]
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_theatre_by_name(name:str):
    try:
        resp = requests.get(url=f"{API_URL}/theatres/name/{name}")
        resp.raise_for_status()
        resp = resp.json()
        # return TheatreModel(**resp)
        return resp
    except requests.HTTPError:
        return None
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_shows_for_movie_with_theatre(movie_id:int,theatre_id:int):
    try:
        resp = requests.get(f"{API_URL}/movies/{movie_id}/theatres/{theatre_id}/shows")
        resp.raise_for_status()
        resp = resp.json()
        # shows = [ShowModel(**show) for show in resp]
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_seats_for_show(show_id:int):
    try:
        resp = requests.get(f"{API_URL}/shows/{show_id}/seats")
        resp.raise_for_status()
        resp = resp.json()
        # seats = [SeatsResponse(**seat) for seat in resp]
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")


def get_theaters_by_city(city:str):
    try:
        resp = requests.get(f"{API_URL}/theatres/city/{city}")
        resp.raise_for_status()
        resp = resp.json()
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_movies_by_theater(theater_id:int):
    try:
        resp = requests.get(f"{API_URL}/theatres/{theater_id}/movies")
        resp.raise_for_status()
        resp = resp.json()
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_shows_by_time(target_time:str):
    try:
        t = datetime.strptime(target_time,"%H:%M").time()
        resp = requests.get(f"{API_URL}/time/{t}/shows")
        resp.raise_for_status()
        resp = resp.json()
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_movies_by_language(language:str):
    try:
        resp = requests.get(f"{API_URL}/movies/search/language/{language}")
        resp.raise_for_status()
        resp = resp.json()
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_movies_by_genre(genre:str):
    try:
        resp = requests.get(f"{API_URL}/movies/search/genre/{genre}")
        resp.raise_for_status()
        resp = resp.json()
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def book_tickets(req:BookingRequest):
    try:
        json = req.model_dump()
        resp = requests.post(f"{API_URL}/bookings",json=json)
        resp.raise_for_status()
        resp = resp.json()
        # return BookingResponse(**resp)
        return resp
    except requests.HTTPError:
        return None
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def get_tickets(booking_id:int):
    try:
        resp = requests.get(url=f"{API_URL}/bookings/{booking_id}/tickets")
        resp.raise_for_status()
        resp = resp.json()
        # return [TicketResponse(**ticket) for ticket in resp]
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")



