from http.client import HTTPException

import requests

from database_models import TicketModel
from models import MovieModel, ShowModel, ScreenModel, TheatreModel, SeatsResponse, BookingRequest, BookingResponse, \
    TicketResponse

API_URL = "http://127.0.0.1:8000"

def get_theatres_by_movie_id(movie_id:int):
    try:
        resp = requests.get(f"{API_URL}/movie/theatres/{movie_id}")
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
        resp = requests.get(url=f"{API_URL}/movie/{title}")
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
        resp = requests.get(url=f"{API_URL}/theatre/{name}")
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
        resp = requests.get(f"{API_URL}/shows/{movie_id}/{theatre_id}")
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
        resp = requests.get(f"{API_URL}/seats/show/{show_id}")
        resp.raise_for_status()
        resp = resp.json()
        # seats = [SeatsResponse(**seat) for seat in resp]
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")

def book_tickets(req:BookingRequest):
    try:
        json = req.model_dump()
        resp = requests.post(f"{API_URL}/book",json=json)
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
        resp = requests.get(url=f"{API_URL}/tickets/{booking_id}")
        resp.raise_for_status()
        resp = resp.json()
        # return [TicketResponse(**ticket) for ticket in resp]
        return resp
    except requests.HTTPError:
        return []
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to api due to {e}")



