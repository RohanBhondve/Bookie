from api_service import get_shows_for_movie_with_theatre, get_theatres_by_movie_id, get_seats_for_show, \
    get_theatre_by_name, get_movies_by_title, get_all_movies, get_tickets, book_tickets, get_shows_by_time, \
    get_movies_by_theater,get_theaters_by_city,get_movies_by_theater,get_shows_by_time,get_movies_by_language,get_movies_by_genre
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call

from models import BookingRequest

booking_state = {
    "user_id" : 1,
    "movie_id": None,
    "theatre_id":None,
    "show_id":None,
    "seat_ids":None,
    "booking_ids":[]
}

@tool
def get_movies():
    """
    Retrieve all movies currently available for booking.

    Use this tool when the user wants to browse or discover movies without
    specifying a particular title. This includes requests for all available
    movies, movie recommendations, or when the user asks what movies are
    currently showing.

    Do not use this tool if the user has already mentioned a specific movie
    title. In that case, use get_movies_from_title() to search for matching
    movies.

    Returns:
        A list of all available movies along with their details.
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
    Search for movies whose title matches or partially matches the user's input.

    Use this tool when the user mentions a specific movie title, even if the
    title is incomplete or only partially matches the actual movie name. This
    tool helps identify the movie the user intends to watch.

    Do not use this tool when the user wants to browse all available movies or
    asks for general movie suggestions. In those cases, use get_movies().

    After calling:
    - If no matching movies are found, inform the user and ask them to try a different title.
    - If multiple movies are found, present the matching options and ask the user to choose one.
    - If exactly one movie is found, present its details and ask the user to confirm that it is the intended movie.
    - Only call select_movie() after the user explicitly confirms their choice.

    Returns:
        A list of movies matching the provided title.
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
    Store the user's confirmed movie selection in the current booking state.

    Use this tool only after the user has explicitly confirmed or selected a
    single movie. This tool records the selected movie so it can be used by
    subsequent tool calls and the booking process.

    Do not use this tool if:
    - The user has not yet confirmed their movie choice.
    - Multiple movie options are still awaiting clarification.
    - No matching movie has been identified.

    After calling:
    - Review the current booking state and the conversation context to determine
      what information is still required.
    - Continue the booking process by determining what information is still required and using the appropriate tool.
        Do not assume a fixed booking sequence.
    - Use the appropriate retrieval tool to obtain the next piece of information.
    - Do not assume a fixed booking sequence.

    Returns:
        Confirmation that the selected movie has been stored in the booking state.
    """
    booking_state["movie_id"] = movie_id
    return {
        "status": "success",
        "selected_movie": movie_id
    }

@tool
def get_theatres_for_movie(movie_id:int):
    """
    Retrieve all theatres showing the movie currently stored in the booking state.

    Use this tool when the user wants to know where the selected movie is
    playing or when theatre information is required to continue the booking
    process.

    Requirements:
    - A movie must already be stored in the booking state using select_movie().

    Do not use this tool if:
    - No movie has been selected yet.
    - The user is looking for theatres in a particular city without first
      selecting a movie. Use the appropriate city-based theatre search tool instead.

    After calling:
    - If one or more theatres are found, present them to the user and ask them
      to choose one.
    - If no theatres are found, inform the user that the selected movie is not
      currently playing in any theatre.

    Returns:
        A list of theatres showing the selected movie.
    """
    try:
        theatres = get_theatres_by_movie_id(movie_id)
        if not theatres:
            return "No theatres found"
        return  theatres
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_theatre(theatre_id:int):
    """
        Store the user's confirmed theatre selection in the current booking state.

    Use this tool only after the user has explicitly selected or confirmed a
    single theatre. This tool records the selected theatre so it can be used
    by subsequent tool calls and the booking process.

    Requirements:
    - The selected theatre must be unambiguous.

    Do not use this tool if:
    - The user has not yet confirmed their theatre choice.
    - Multiple theatre options are still awaiting clarification.
    - No valid theatre has been identified.

    After calling:
    - Review the current booking state and the conversation context to
      determine what information is still required.
    - Continue the booking process by determining what information is still required and using the appropriate tool.
        Do not assume a fixed booking sequence.
    - Use the appropriate retrieval tool to obtain the next missing piece of
      information. Do not assume a fixed booking sequence.

    Returns:
        Confirmation that the selected theatre has been stored in the booking state.
        """
    booking_state["theatre_id"] = theatre_id
    return {
        "status": "success",
        "selected_theater": theatre_id
    }

@tool
def get_shows_by_movie_and_theatre(movie_id:int,theater_id:int):
    """
    Retrieve all available shows for the movie and theatre currently stored in
    the booking state.

    Use this tool when both a movie and a theatre have already been selected
    and the user wants to view the available show timings for that combination.

    Requirements:
    - A movie must already be stored in the booking state.
    - A theatre must already be stored in the booking state.

    Do not use this tool if:
    - Either the movie or theatre has not yet been selected.
    - The user is searching for shows based on other criteria (such as time).
      Use the find_show_by_time tool for those scenarios.

    After calling:
    - If one or more shows are found, present the available show timings and
      ask the user to choose one.
    - If no shows are found, inform the user that there are no scheduled shows
      for the selected movie at the selected theatre.

    Returns:
        A list of available shows for the selected movie and theatre.
    """
    try:
        shows = get_shows_for_movie_with_theatre(movie_id=movie_id, theatre_id=theater_id)
        if not shows:
            return "No shows found"
        return shows
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_show(show_id:int):
    """
        Store the user's confirmed show selection in the current booking state.

    Use this tool only after the user has explicitly selected or confirmed a
    single show. This tool records the selected show so it can be used during
    the booking process.

    Requirements:
    - The selected show must be unambiguous.

    Do not use this tool if:
    - The user has not yet confirmed their show choice.
    - Multiple show options are still awaiting clarification.
    - No valid show has been identified.

    After calling:
    - Review the current booking state and the conversation context to
      determine what information is still required.
    - Continue the booking process by determining what information is still required and using the appropriate tool.
        Do not assume a fixed booking sequence.
    - Use the appropriate retrieval tool to obtain the next missing piece of
      information. Do not assume a fixed booking sequence.

    Returns:
        Confirmation that the selected show has been stored in the booking state.
        """
    booking_state["show_id"] = show_id
    return {
        "status": "success",
        "selected_show": show_id
    }

@tool
def get_seats_by_show(show_id:int):
    """
    Retrieve all available seats for the show currently stored in the booking state.

    Use this tool when the user wants to view or choose seats for the selected
    show.

    Requirements:
    - A show must already be stored in the booking state using select_show().

    Do not use this tool if:
    - No show has been selected yet.

    After calling:
    - Present only the available seats to the user.
    - Ask the user to choose one or more seats.
    - After the user explicitly confirms their seat selection, call
      select_seats() to store the selected seats in the booking state.

    Returns:
        A list of available seats for the selected show.
    """
    try:
        seats = get_seats_for_show(show_id)
        if not seats:
            return "No seats found"
        return seats
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def select_seats(seat_ids:list[int]):
    """
        Store the user's confirmed seat selection in the current booking state.

    Use this tool only after the user has explicitly selected or confirmed one
    or more available seats. All selected seat IDs should be provided in a
    single call.

    Requirements:
    - A show must already be stored in the booking state.
    - The selected seats must be available and unambiguous.

    Do not use this tool if:
    - No show has been selected yet.
    - The user has not finalized their seat selection.
    - There is any ambiguity about which seats the user wants.

    After calling:
    - Summarize the complete booking details, including the movie, theatre,
      show, and selected seats.
    - Ask the user for explicit confirmation before calling
      book_movie_tickets().

    Returns:
        Confirmation that the selected seats have been stored in the booking state.
        """
    booking_state["seat_ids"] = seat_ids
    return {
        "status": "success",
        "selected_seats": seat_ids
    }

@tool
def show_theatres_by_city(city:str):
    """
    Retrieve all theatres located in the specified city.

    Use this tool when the user wants to browse theatres in a particular city
    without specifying a movie. This tool helps the user discover available
    theatres before selecting one.

    Do not use this tool if:
    - The user is asking where a previously selected movie is playing. Use
      get_theatres_for_movie() instead.

    After calling:
    - If one or more theatres are found, present them to the user and ask them
      to choose one.
    - If the user explicitly selects or confirms a theatre, call
      select_theatre() to store it in the booking state.
    - If no theatres are found, inform the user that no theatres are available
      in the specified city.

    Returns:
        A list of theatres in the specified city.
    """
    try:
        theatres = get_theaters_by_city(city)
        if not theatres:
            return "No theatres found"
        return theatres
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def show_movies_by_theatre(theatre_id:int):
    """
    Retrieve all movies currently playing at the specified theatre.

    Use this tool when the user wants to know what movies are playing at a
    particular theatre or when movie information is required after a theatre
    has been identified.

    Requirements:
    - A valid theatre must be identified or stored in the booking state.

    Do not use this tool if:
    - The user wants to browse all available movies. Use get_movies() instead.
    - The user is searching for a movie by its title. Use get_movies_from_title() instead.

    After calling:
    - If exactly one movie is returned, present its details and ask the user
      to confirm it before calling select_movie().
    - If multiple movies are returned, present the available options and ask
      the user to choose one.
    - If no movies are found, inform the user that no movies are currently
      playing at the selected theatre.

    Returns:
        A list of movies currently playing at the specified theatre.
    """
    try:
        movies = get_movies_by_theater(theatre_id)
        if not movies:
            return "No movies found"
        return movies
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def find_shows_by_time(time:str):
    """
     Retrieve all shows scheduled around the specified time. The time must be
    provided in 24-hour format (HH:MM).

    Use this tool when the user wants to find shows based on a preferred time
    without specifying a movie or theatre.

    Do not use this tool if:
    - The user has already selected both a movie and a theatre. Use
      get_shows_by_movie_and_theatre() instead.

    After calling:
    - If one or more shows are found, present the available show options,
      including their movie and theatre details, and ask the user to choose one.
    - If the user explicitly selects or confirms a show, call the following
      tools in order to update the booking state:
        1. select_movie()
        2. select_theatre()
        3. select_show()
    - If no shows are found, inform the user that no shows are available around
      the specified time.

    Returns:
        A list of matching shows along with their associated movie and theatre
        details."""
    try:
        shows = get_shows_by_time(time)
        if not shows:
            return "No shows found"
        return shows
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def get_movies_from_language(language:str):
    """
    Retrieve all movies available in the specified language.

    Use this tool when the user wants to browse or search for movies based on
    a preferred language, such as Hindi, English, Marathi, or Tamil.

    Do not use this tool if:
    - The user wants to browse all available movies. Use get_movies() instead.
    - The user specifies a movie title. Use get_movies_from_title() instead.

    After calling:
    - If exactly one movie is returned, present its details and ask the user
      to confirm it before calling select_movie().
    - If multiple movies are returned, present the matching movies and ask the
      user to choose one.
    - If no movies are found, inform the user that no movies are available in
      the specified language.

    Returns:
        A list of movies available in the specified language.
    """
    try:
        movies = get_movies_by_language(language)
        if not movies:
            return "No movies found"
        return movies
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def get_movies_from_genre(genre:str):
    """
    Retrieve all movies matching the specified genre.

    Use this tool when the user wants to browse or search for movies based on
    a preferred genre, such as Action, Comedy, Drama, Horror, or Romance.

    Do not use this tool if:
    - The user wants to browse all available movies. Use get_movies() instead.
    - The user specifies a movie title. Use get_movies_from_title() instead.

    After calling:
    - If exactly one movie is returned, present its details and ask the user
      to confirm it before calling select_movie().
    - If multiple movies are returned, present the matching movies and ask the
      user to choose one.
    - If no movies are found, inform the user that no movies are available in
      the specified genre.

    Returns:
        A list of movies matching the specified genre.
    """
    try:
        movies = get_movies_by_genre(genre)
        if not movies:
            return "No movies found"
        return movies
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@tool
def book_movie_tickets():
    """
    Create a movie ticket booking using the current booking state.

    Use this tool only after the booking state is complete and the user has
    explicitly confirmed that they want to proceed with the booking.

    Requirements:
    - The booking state must contain a selected movie.
    - The booking state must contain a selected theatre.
    - The booking state must contain a selected show.
    - The booking state must contain one or more selected seats.
    - A complete booking summary must have been presented to the user.
    - The user must have explicitly confirmed the booking.

    Do not use this tool if:
    - Any required booking information is missing from the booking state.
    - The user has not explicitly confirmed the booking.
    - The user is still modifying their movie, theatre, show, or seat selection.

    Returns:
        A booking confirmation containing the booking details and confirmation
        information.
    """
    try:
        req: BookingRequest = BookingRequest(
            user_id=booking_state["user_id"],
            show_id=booking_state["show_id"],
            seat_ids=booking_state["seat_ids"],
            payment_method="UPI"
        )
        booking_resp = book_tickets(req)
        if booking_resp is None:
            return "Sorry, tickets couldn't be booked"
        booking_state["booking_ids"] = booking_state["booking_ids"].append(booking_resp["booking_id"])
        return booking_resp
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."

@wrap_tool_call
def book_human_approval(request,handler):
    """
    Middleware that intercepts calls to the book_movie_tickets() tool and
    enforces explicit user confirmation before a booking is created.

    This middleware acts as a safety check to ensure that bookings are never
    completed without the user's final approval.

    Behavior:
    - Intercepts every invocation of book_movie_tickets().
    - If the user has not explicitly confirmed the booking, blocks the tool
      execution and instructs the agent to request confirmation.
    - If the user explicitly confirms the booking, forwards the request to
      book_movie_tickets() by invoking the provided handler.

    Returns:
        The result of book_movie_tickets() after approval, or a response
        requesting the user's confirmation if approval has not been granted.
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
def store_booking_ids(booking_id:int):
    """
        Store the booking ID of a successfully completed booking in the current
    booking state.

    Use this tool immediately after book_movie_tickets() successfully creates
    a booking. This tool maintains a history of all bookings made during the
    current conversation, allowing the agent to reference or retrieve previous
    bookings later if needed.

    Requirements:
    - The booking must have been successfully created.
    - A valid booking ID must be available.

    Do not use this tool if:
    - The booking was unsuccessful.
    - No booking ID has been returned.
    - book_movie_tickets() has not yet been executed successfully.

    Returns:
        Confirmation that the booking ID has been added to the booking history.
        """
    booking_state["booking_ids"].append(booking_id)
    return {
        "status": "success",
        "booking_ids": booking_state["booking_ids"]
    }

@tool
def get_booked_tickets(booking_id:int):
    """
    Retrieve all tickets associated with the specified booking ID.

    Use this tool when the user wants to view, display, or retrieve tickets
    for a previously completed booking.

    Requirements:
    - The booking must have been successfully created.
    - A valid booking ID must be available.

    Do not use this tool if:
    - No booking has been completed.
    - No valid booking ID is available.
    - The user has multiple bookings but has not specified or confirmed which
      booking they want to view.

    After calling:
    - Present the ticket details, including the movie, theatre, show time,
      seats, booking ID, and transaction ID.

    Returns:
        The ticket details for the specified booking.
    """
    try:
        tickets = get_tickets(booking_id)
        if tickets is None:
            return "No tickets found"
        return tickets
    except Exception:
        return "Sorry, I couldn't reach the booking service right now."
