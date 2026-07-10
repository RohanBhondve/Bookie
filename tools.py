from api_service import get_shows_for_movie_with_theatre,get_theatres_by_movie_id,get_seats_for_show,get_theatre_by_name,get_movies_by_title,get_all_movies,get_tickets,book_tickets
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call

from models import BookingRequest

decision_history = {
    "user_id" : 1
}

@tool
def get_movies():
    """
    Purpose:
    Retrieve all movies currently available in the system.

    When to call:
    - When the user asks to see all available movies.
    - When the user asks for movie suggestions without specifying a title.
    - When the user wants to browse movies.

    Do not call:
    - If the user has already provided a movie title. Use get_movies_from_title() instead.

    Returns:
    A list of available movies with their details.
    """
    try:
        movies = get_all_movies()
        if not movies:
            return "No movies found"
        return movies
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."


@tool
def get_movies_from_title(title:str):
    """
    Purpose:
    Search for movies whose title matches or partially matches the given title.

    When to call:
    - When the user specifies a movie title or part of a movie title.
    - When you need to find the movie the user wants to watch.

    Do not call:
    - If the user only wants to browse all available movies. Use get_movies() instead.

    After calling:
    - If exactly one movie is returned, ask the user to confirm the movie before calling select_movie().
    - If multiple movies are returned, present the options and ask the user to choose one.
    - If no movies are found, inform the user and ask them to try another title.

    Returns:
    A list of matching movies.
    """
    try:
        movies = get_movies_by_title(title)
        if not movies:
            return "No movies found"
        return movies
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_movie(movie_id:int):
    """
    Purpose:
    Store the user's selected movie in the current booking state.

    When to call:
    - Only after the user has explicitly selected or confirmed a single movie.
    - Never call if multiple movie options still need clarification.

    Do not call:
    - Before the user has made a clear choice.
    - If no matching movie has been found.

    After calling:
    - Use get_theatres_for_movie() to retrieve the theatres where the selected movie is playing.
    - Present the available theatres to the user and ask them to choose one.

    Returns:
    Confirmation that the movie has been stored in the booking state.
    """
    decision_history["movie_id"] = movie_id
    return {
        "status": "success",
        "selected_movie": movie_id
    }

@tool
def get_theatres_for_movie():
    """
    Purpose:
    Retrieve all theatres that are showing the currently selected movie.

    Requirements:
    - A movie must already be selected using select_movie().

    When to call:
    - After the user has selected or confirmed a movie.
    - When the user wants to see where the selected movie is playing.

    Do not call:
    - If no movie has been selected yet.

    After calling:
    - If one or more theatres are returned, present them to the user and ask them to choose one.
    - If no theatres are found, inform the user that the selected movie is not currently playing.

    Returns:
    A list of theatres showing the selected movie.
    """
    try:
        theatres = get_theatres_by_movie_id(decision_history["movie_id"])
        if not theatres:
            return "No theatres found"
        return  theatres
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_theatre(theatre_id:int):
    """
        Purpose:
        Store the user's selected theatre in the current booking state.

        Requirements:
        - A movie must already be selected.
        - The user must have explicitly selected or confirmed a single theatre from the presented options.

        When to call:
        - After the user has chosen one theatre.
        - Only when there is no ambiguity about the selected theatre.

        Do not call:
        - Before a movie has been selected.
        - If multiple theatre options still need clarification.

        After calling:
        - Use get_shows_by_movie_and_theatre() to retrieve the available shows for the selected movie at the selected theatre.
        - Present the available shows to the user and ask them to choose one.

        Returns:
        Confirmation that the theatre has been stored in the booking state.
        """
    decision_history["theatre_id"] = theatre_id
    return {
        "status": "success",
        "selected_theater": theatre_id
    }

@tool
def get_shows_by_movie_and_theatre():
    """
    Purpose:
    Retrieve all available shows for the currently selected movie at the currently selected theatre.

    Requirements:
    - A movie must already be selected.
    - A theatre must already be selected.

    When to call:
    - After the user has selected a theatre.
    - When the user wants to view available show timings for the selected movie and theatre.

    Do not call:
    - Before both a movie and theatre have been selected.

    After calling:
    - If one or more shows are returned, present the available show timings to the user and ask them to choose one.
    - If no shows are available, inform the user that there are no scheduled shows for the selected movie at the selected theatre.

    Returns:
    A list of available shows for the selected movie at the selected theatre.
    """
    try:
        shows = get_shows_for_movie_with_theatre(movie_id=decision_history["movie_id"],theatre_id=decision_history["theatre_id"])
        if not shows:
            return "No shows found"
        return shows
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_show(show_id:int):
    """
        Purpose:
        Store the user's selected show in the current booking state.

        Requirements:
        - A movie must already be selected.
        - A theatre must already be selected.
        - The user must have explicitly selected or confirmed a single show from the presented options.

        When to call:
        - After the user has chosen one show.
        - Only when there is no ambiguity about the selected show.

        Do not call:
        - Before a movie and theatre have been selected.
        - If multiple show options still need clarification.

        After calling:
        - Use get_seats_by_show() to retrieve the available seats for the selected show.
        - Present the available seats to the user and ask them to choose one or more seats.

        Returns:
        Confirmation that the show has been stored in the booking state.
        """
    decision_history["show_id"] = show_id
    return {
        "status": "success",
        "selected_show": show_id
    }

@tool
def get_seats_by_show():
    """
    Purpose:
    Retrieve all available seats for the currently selected show.

    Requirements:
    - A movie must already be selected.
    - A theatre must already be selected.
    - A show must already be selected.

    When to call:
    - After the user has selected a show.
    - When the user wants to view the available seats for the selected show.

    Do not call:
    - Before a show has been selected.

    After calling:
    - Present only the available seats to the user.
    - Ask the user to choose one or more seats.
    - After the user selects their seats, call select_seats() to store the selection.

    Returns:
    A list of available seats for the selected show.
    """
    try:
        seats = get_seats_for_show(decision_history["show_id"])
        if not seats:
            return "No seats found"
        return seats
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_seats(seat_ids:list[int]):
    """
        Purpose:
        Store the user's selected seat(s) in the current booking state.

        Requirements:
        - A movie must already be selected.
        - A theatre must already be selected.
        - A show must already be selected.
        - The user must have explicitly selected or confirmed one or more available seats.

        When to call:
        - After the user has chosen one or more seats.
        - Only when there is no ambiguity about the selected seats.

        Do not call:
        - Before a show has been selected.
        - If the user has not yet finalized their seat selection.

        After calling:
        - Summarize the complete booking, including the movie, theatre, show, and selected seats.
        - Ask the user for explicit confirmation before calling book_movie_tickets().

        Returns:
        Confirmation that the selected seats have been stored in the booking state.
        """
    decision_history["seat_ids"] = seat_ids
    return {
        "status": "success",
        "selected_seats": seat_ids
    }

@tool
def book_movie_tickets():
    """
    Purpose:
    Create a movie ticket booking using the current booking state.

    Requirements:
    - A movie must be selected.
    - A theatre must be selected.
    - A show must be selected.
    - One or more seats must be selected.
    - The booking summary must have been presented to the user.
    - The user must have explicitly confirmed that they want to proceed with the booking.

    When to call:
    - Only after all required booking information has been collected.
    - Only after the user has clearly confirmed the booking (for example: "yes", "confirm", "book it", or equivalent).

    Do not call:
    - If any booking information is missing.
    - If the user has not explicitly confirmed the booking.
    - If the user is still modifying their movie, theatre, show, or seat selection.

    Returns:
    The booking confirmation, including the booking details and any relevant confirmation information.
    """
    try:
        req: BookingRequest = BookingRequest(
            user_id=decision_history["user_id"],
            show_id=decision_history["show_id"],
            seat_ids=decision_history["seat_ids"],
            payment_method="UPI"
        )
        booking_resp = book_tickets(req)
        if booking_resp is None:
            return "Sorry, tickets couldn't be booked"
        decision_history["booking_id"] = booking_resp["booking_id"]
        return booking_resp
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@wrap_tool_call
def book_human_approval(request,handler):
    """
    Intercepts calls to the book_movie_tickets tool and requires explicit
    user approval before allowing the booking to proceed.

    If the user has not confirmed the booking, the tool execution is blocked
    and the agent asks the user for confirmation.

    If the user confirms, the middleware forwards the request to the tool by
    invoking the provided handler.
    """
    tool_name = request.tool_call["name"]
    if tool_name != "book":
        return handler(request)

    confirm = input("Do you allow agent to make payment?\nYes/No")
    if confirm.lower() == "no":
        return ToolMessage(
            content="Permission denied",
            tool_call_id = request.tool_call["id"]
        )
    return handler(request)

@tool
def get_booked_tickets():
    """
    Purpose:
    Retrieve all tickets associated with the current booking.

    Requirements:
    - A booking must have been successfully created.
    - A valid booking ID must be available in the booking state.

    When to call:
    - After a successful booking.
    - When the user asks to view, display, or retrieve their booked tickets.

    Do not call:
    - Before a booking has been completed.
    - If no booking ID is available.

    Returns:
    A list of tickets for the current booking, including the seat details,
    show information, and other relevant ticket information.
    """
    try:
        tickets = get_tickets(decision_history["booking_id"])
        if tickets is None:
            return "No tickets found"
        return tickets
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."