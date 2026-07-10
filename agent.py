from langchain_core.messages import HumanMessage
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from tools import get_booked_tickets,decision_history,get_movies,book_movie_tickets,book_human_approval,get_movies_from_title,get_seats_by_show,get_shows_by_movie_and_theatre,get_theatres_for_movie,select_movie,select_seats,select_show,select_theatre
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
memory = InMemorySaver()
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
                    11. Ask the user to choose seats.
                    12. After the user chooses,
                        call select_seats().
                    13. Summarize the booking.
                    14. Before starting booking ask user to approve payment using book_human_apprval()
                    15. Only after explicit confirmation call book_movie_tickets().
                    16. Retrieve all the tickets when asked to
                    
                    Never skip any step.
                    
                    Never answer from memory.
                    
                    Always use tools.""",
    checkpointer=memory
)

print("Welcome to ticket booking agent!\nType quit to exit the chat")
messages = []
while True:
    user_prompt = input("You : ")
    print(f"Decision History : {decision_history}")
    if user_prompt.lower()=="quit":
        print(f"Bot : Bye, have a great time 😊")
        break

    # messages.append(HumanMessage(user_prompt))
    agent_resp = booking_agent.invoke(
        {
            "messages":{
                "role": "user",
                "content": user_prompt
            }
        }
        ,
        config={
            "configurable": {
                "thread_id": "user1"
            }
        }
    )
    # messages.append(agent_resp["messages"][-1])
    print(agent_resp["messages"])
    print(f"Bot : {agent_resp["messages"][-1].content}")
