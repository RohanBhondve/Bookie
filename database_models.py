from sqlalchemy import Column, Integer, String, Float, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BookingModel(Base):
    __tablename__ = "bookings"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    show_id = Column(Integer,ForeignKey("shows.id"))
    total_amt = Column(Float)
    status = Column(String(100))

class MovieModel(Base):
    __tablename__ = "movies"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    title = Column(String(100))
    description = Column(String(300))
    duration = Column(Float)
    language = Column(String(100))
    status = Column(String(100))

class PaymentModel(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    payment_method = Column(String(50))
    payment_status = Column(String(50))
    transaction_id = Column(String(100))
    amount = Column(Float)

class ScreenModel(Base):
    __tablename__ = "screens"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    theatre_id = Column(Integer,ForeignKey("theatres.id"))
    total_seats = Column(Integer)

class SeatModel(Base):
    __tablename__ = "seats"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    screen_id = Column(Integer,ForeignKey("screens.id"))
    seat_no = Column(Integer)
    row_name = Column(String(100))
    seat_type = Column(String(100))

class ShowModel(Base):
    __tablename__ = "shows"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    movie_id = Column(Integer,ForeignKey("movies.id"))
    screen_id = Column(Integer,ForeignKey("screens.id"))
    start_time = Column(Time)
    end_time = Column(Time)
    ticket_price = Column(Float)
    available_seats = Column(Integer)

class TheatreModel(Base):
    __tablename__ = "theatres"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String(100))
    city = Column(String(100))
    address = Column(String(300))
    phone = Column(String(100))

class TicketModel(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    show_id = Column(Integer,ForeignKey("shows.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    ticket_price = Column(Float)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(10))
