from datetime import time
from typing import List

from pydantic import BaseModel

class MovieModel(BaseModel):
    id:int
    title:str
    description:str
    language:str
    duration:float
    status:str

class ShowModel(BaseModel):
    id:int
    movie_id:int
    screen_id:int
    start_time:str
    end_time:str
    ticket_price:float
    available_seats:int

class ScreenModel(BaseModel):
    id:int
    theatre_id:int
    total_seats:int

class TheatreModel(BaseModel):
    id:int
    name:str
    city:str
    address:str
    phone:str

class BookingRequest(BaseModel):
    user_id: int
    show_id: int
    seat_ids: list[int]
    payment_method: str

class SeatsResponse(BaseModel):
    seat_id:int
    row_name:str
    seat_no: int
    seat_type: str
    is_booked: bool

class BookingResponse(BaseModel):
    message: str
    booking_id: int
    payment_id: int
    transaction_id: str
    payment_status: str
    total_amount: float
    booked_seats: List[int]

class TicketResponse(BaseModel):
    id: int
    show_id: int
    seat_id: int
    ticket_price: float
    row_name: str
    seat_no: int