from langchain_core.messages import HumanMessage
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from tools import get_booked_tickets,booking_state,get_movies,book_movie_tickets,book_human_approval,get_movies_from_title,get_seats_by_show,get_shows_by_movie_and_theatre,get_theatres_for_movie,select_movie,select_seats,select_show,select_theatre
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
from rich import print

future_prompt = """
You are an AI movie ticket booking assistant.

Your objective is to help the user complete a booking by gathering the required booking information.

Maintain the following booking state:

- movie
- theatre
- show
- seats

Users may begin the conversation from any point.
For example:
- searching for a movie
- asking for nearby theatres
- asking for movies at a theatre
- asking for shows in a time range
- asking for recommendations

Always determine what information is already known and what is still missing.

Use tools to retrieve all booking information.
Never invent movies, theatres, shows, seat availability, or booking details.

Only call a selection tool after the user has uniquely identified an option.

After a selection is made, use the appropriate search tool to retrieve the next information needed.

Before booking, summarize the complete booking and ask for explicit confirmation.

Never call the booking tool without confirmation.
"""

llm = ChatMistralAI(model_name="mistral-small-2603",temperature=0)
# memory = InMemorySaver()
booking_agent = create_agent(
    model=llm,
    tools=[
        book_movie_tickets,
        get_movies,
        get_movies_from_title,
        get_seats_by_show,
        get_shows_by_movie_and_theatre,
        get_theatres_for_movie,
        select_movie,
        select_seats,
        select_show,
        select_theatre,
        get_booked_tickets
    ],
    middleware=[book_human_approval],
    system_prompt=f"""You are an AI movie ticket booking assistant.

                    You MUST use tools for every step of the booking process.
                    Never invent movies, theatres, shows, seats, or booking information.
                    While calling any of the tool that updates booking state make sure you pass right IDs to them 
                    
                    Booking workflow:
                    
                    1. Search movies.
                    2. If exactly one movie is found, ask the user to confirm.
                    3. When the user confirms (yes, okay, continue, book it, etc.),
                       immediately call select_movie().
                    4. After select_movie succeeds,
                       immediately call get_theatres_for_movie().
                    5. Ask the user to choose a theatre.
                    6. After the user chooses,
                       call select_theatre().
                    7. Then call get_shows_by_movie_and_theatre().
                    8. Ask the user to choose a show.
                    9. After the user chooses,
                       call select_show().
                    10. Then call get_seats_by_show().
                    11. Ask the user to choose seats. Use Row+Seat number format (like A3,B6) when asking user to select seats.
                    12. After the user chooses,
                        call select_seats().
                    13. Summarize the booking.
                    14. Before starting booking ask user to approve payment using book_human_apprval()
                    15. Only after explicit confirmation call book_movie_tickets().
                    16. After tickets are booked call store_booking_ids() to store the booking_ids for future reference
                    17. Retrieve all the tickets when asked to
                    
                    Never skip any step.
                    
                    Never answer from memory.
                    
                    Always use tools.""",
    # checkpointer=memory
)

prefs_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)

print("Welcome to ticket booking agent!\nType quit to exit the chat")
messages = []
user_pref = ""

def summarize_messages(messages,user_pref):
    # print(f"--------------------Length--------------------\n{len(messages)}")
    prefs_resp = prefs_llm.invoke([
        ("system", f"""You are summarizing an ongoing conversation between a user and an AI movie booking assistant.

                                Your task is to create a concise summary that preserves only information that will be useful for continuing the conversation later.

                                Include:
                                - User preferences (preferred theatres, seat types, movie genres, languages, formats like IMAX, etc.)
                                - User constraints (budget, accessibility needs, timing preferences, location preferences)
                                - User intent that is still relevant.
                                - Any assumptions or decisions that should be remembered.

                                Do NOT include:
                                - Greetings or small talk.
                                - Questions asked by the assistant.
                                - Temporary reasoning.
                                - Repeated information.
                                - Information already stored in the structured booking state (movie, theatre, show, seats, payment status, booking status).

                                Write the summary as short bullet points.

                                If there is nothing important to remember, return exactly:

                                "No persistent conversation context."
                    """),
        ("user", f"Conversation:{messages[0:-10]}")
    ])
    if user_pref != "No persistent conversation context.":
        user_pref = f"\n{prefs_resp.content}"

    # print(f"--------------------User Pref--------------------\n{user_pref}")

    messages = messages[-10:]
    # print(f"--------------------Messages--------------------\n{messages}")
    # print(f"--------------------Length--------------------\n{len(messages)}")
    return messages,user_pref

while True:
    user_prompt = input("You : ")
    # print(f"Decision History : {decision_history}")
    if user_prompt.lower()=="quit":
        print(f"Bot : Bye, have a great time 😊")
        break

    messages.append(HumanMessage(user_prompt))

    if len(messages) > 10:
        messages,user_pref = summarize_messages(messages,user_pref)

    agent_resp = booking_agent.invoke(
        {
            "messages":messages,
            "booking_state":booking_state,
            "user_preferences":user_pref
        }
    )
    messages = agent_resp["messages"]
    # print(messages)
    print(booking_state)
    print(f"Bot : {agent_resp["messages"][-1].content}")
