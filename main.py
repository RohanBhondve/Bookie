import datetime
from datetime import timedelta,datetime,time

from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database_models import MovieModel, ShowModel, ScreenModel, TheatreModel, Base, SeatModel, TicketModel, \
    PaymentModel, BookingModel
from database import session, engine
from uuid import uuid4

from models import BookingRequest

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_session():
    db = session()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/health")
def greet():
    return "hello"

@app.get("/movies/{movie_id}/theatres")
def get_theatres_by_movie_id(movie_id:int,db:Session = Depends(get_session)):
    theatres = (
        db.query(TheatreModel)
        .join(ScreenModel, TheatreModel.id == ScreenModel.theatre_id)
        .join(ShowModel, ScreenModel.id == ShowModel.screen_id)
        .filter(ShowModel.movie_id == movie_id)
        .distinct()
        .all()
    )
    if not theatres:
        HTTPException(status_code=404,detail="No theatres found")
    return theatres

@app.get("/movies")
def get_all_movies(db:Session = Depends(get_session)):
    movies = db.query(MovieModel).all()
    if not movies:
        raise HTTPException(status_code=404,detail="No movies available")
    return movies

@app.get("/movies/search/{title}")
def get_movie(title:str,db:Session = Depends(get_session)):
    db_movie = db.query(MovieModel).filter(MovieModel.title.ilike(f"%{title}%")).all()
    if db_movie is None:
        raise HTTPException(status_code=404,detail="Movie not found")
    return db_movie

@app.get("/theatres/name/{name}")
def get_theatre(name:str,db:Session = Depends(get_session)):
    db_theatres = db.query(TheatreModel).filter(TheatreModel.name == name.capitalize()).first()
    if db_theatres is None:
        raise HTTPException(status_code=404,detail="No theatres found")
    return db_theatres

@app.get("/movies/{movie_id}/theatres/{theatre_id}/shows")
def get_shows_for_movie_with_theatre(
    movie_id: int,
    theatre_id: int,
    db: Session = Depends(get_session)
):
    shows = (
        db.query(ShowModel)
        .join(ScreenModel, ScreenModel.id == ShowModel.screen_id)
        .filter(
            ShowModel.movie_id == movie_id,
            ScreenModel.theatre_id == theatre_id
        )
        .all()
    )

    if not shows:
        raise HTTPException(
            status_code=404,
            detail="No shows found"
        )

    return shows

@app.get("/shows/{show_id}/seats")
def get_seats_for_show(show_id: int, db: Session = Depends(get_session)):

    show = (
        db.query(ShowModel)
        .filter(ShowModel.id == show_id)
        .first()
    )

    if show is None:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    seats = (
        db.query(
            SeatModel,
            TicketModel.id
        )
        .outerjoin(
            TicketModel,
            (SeatModel.id == TicketModel.seat_id) &
            (TicketModel.show_id == show_id)
        )
        .join(
            ShowModel,
            ShowModel.screen_id == SeatModel.screen_id
        )
        .filter(ShowModel.id == show_id)
        .all()
    )

    response = []

    for seat, ticket_id in seats:
        response.append({
            "seat_id": seat.id,
            "row_name": seat.row_name,
            "seat_no": seat.seat_no,
            "seat_type": seat.seat_type,
            "is_booked": ticket_id is not None
        })

    return response

@app.get("/theatres/city/{city}")
def get_theatres_by_city(city:str,db:Session = Depends(get_session)):

    theatres = (
        db.query(TheatreModel)
        .filter(TheatreModel.city==city)
        .all()
    )

    if not theatres:
        raise HTTPException(status_code=404,detail="No theatres found")
    return theatres

@app.get("/theatres/{theater_id}/movies")
def get_movies_by_theater(theater_id:int, db:Session = Depends(get_session)):
    movies = (
        db.query(MovieModel)
        .join(ShowModel, MovieModel.id == ShowModel.movie_id)
        .join(ScreenModel, ShowModel.screen_id == ScreenModel.id)
        .filter(ScreenModel.theatre_id == theater_id)
        .distinct()
        .all()
    )

    if not movies:
        return "No movies found"
    return movies

@app.get("/time/{target_time}/shows")
def get_shows_by_time(target_time: time, window_minutes: int = 60, db: Session = Depends(get_session)):
    target = datetime.combine(datetime.today(), target_time)
    start = (target - timedelta(minutes=window_minutes)).time()
    end = (target + timedelta(minutes=window_minutes)).time()

    shows = (
        db.query(ShowModel,MovieModel,TheatreModel)
        .join(MovieModel, ShowModel.movie_id == MovieModel.id)
        .join(ScreenModel, ShowModel.screen_id == ScreenModel.id)
        .join(TheatreModel, ScreenModel.theatre_id == TheatreModel.id)
        .filter(
            ShowModel.start_time >= start,
            ShowModel.start_time <= end
        )
        .all()
    )
    if not shows:
        return "No shows found"
    return [dict(show._mapping) for show in shows]

@app.get("/movies/search/language/{language}")
def get_movies_by_language(language:str, db:Session = Depends(get_session)):
    movies = (
        db.query(MovieModel)
        .filter(MovieModel.language==language)
        .all()
    )

    if not movies:
        return "No movies found"
    return movies

@app.get("/movies/search/genre/{genre}")
def get_movies_by_genre(genre:str, db:Session = Depends(get_session)):
    movies = (
        db.query(MovieModel)
        .filter(MovieModel.description.ilike(f"%{genre}%"))
        .all()
    )

    if not movies:
        return "No movies found"
    return movies

@app.post("/bookings")
def book_seats(
    request:BookingRequest,
    db: Session = Depends(get_session)
):

    # -----------------------------
    # Check if show exists
    # -----------------------------
    show = (
        db.query(ShowModel)
        .filter(ShowModel.id == request.show_id)
        .first()
    )

    if show is None:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    # -----------------------------
    # Check if seats belong to screen
    # -----------------------------
    seats = (
        db.query(SeatModel)
        .filter(
            SeatModel.id.in_(request.seat_ids),
            SeatModel.screen_id == show.screen_id
        )
        .all()
    )

    if len(seats) != len(request.seat_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more selected seats are invalid."
        )

    # -----------------------------
    # Check if seats are already booked
    # -----------------------------
    booked = (
        db.query(TicketModel)
        .filter(
            TicketModel.show_id == request.show_id,
            TicketModel.seat_id.in_(request.seat_ids)
        )
        .first()
    )

    if booked:
        raise HTTPException(
            status_code=400,
            detail="One or more seats are already booked."
        )

    # -----------------------------
    # Calculate total amount
    # -----------------------------
    total_amount = len(request.seat_ids) * show.ticket_price

    # -----------------------------
    # Create Booking
    # -----------------------------
    booking = BookingModel(
        user_id=request.user_id,
        show_id=request.show_id,
        total_amt=total_amount,
        status="CONFIRMED"
    )

    db.add(booking)
    db.flush()

    # -----------------------------
    # Create Tickets
    # -----------------------------
    for seat_id in request.seat_ids:

        ticket = TicketModel(
            booking_id=booking.id,
            show_id=request.show_id,
            seat_id=seat_id,
            ticket_price=show.ticket_price
        )

        db.add(ticket)

    # -----------------------------
    # Create Payment
    # -----------------------------
    payment = PaymentModel(
        booking_id=booking.id,
        payment_method=request.payment_method,
        payment_status="SUCCESS",
        transaction_id=str(uuid4()),
        amount=total_amount
    )

    db.add(payment)

    # -----------------------------
    # Update available seats
    # -----------------------------
    show.available_seats -= len(request.seat_ids)

    db.commit()

    db.refresh(booking)
    db.refresh(payment)

    return {
        "message": "Booking Successful",
        "booking_id": booking.id,
        "payment_id": payment.id,
        "transaction_id": payment.transaction_id,
        "payment_status": payment.payment_status,
        "total_amount": total_amount,
        "booked_seats": request.seat_ids
    }

@app.get("/bookings/{booking_id}/tickets")
def get_tickets(booking_id:int,db:Session = Depends(get_session)):
    tickets = (
        db.query(TicketModel.id,TicketModel.show_id,TicketModel.seat_id,TicketModel.ticket_price,SeatModel.row_name,SeatModel.seat_no)
        .join(SeatModel,SeatModel.id == TicketModel.seat_id)
        .filter(TicketModel.booking_id==booking_id)
        .all()
    )
    if not tickets:
        raise HTTPException(status_code=404,detail="No tickets found")
    return [dict(row._mapping) for row in tickets]



