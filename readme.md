# [![Typing SVG](https://readme-typing-svg.demolab.com?font=Oswald&pause=1000&color=F5C518&width=435&lines=Bookie%F0%9F%AB%B0%F0%9F%8F%BB-+Chat+%E2%80%A2+Book+%E2%80%A2+Watch)](https://git.io/typing-svg)
> **An AI-powered movie ticket booking agent that lets users book movie tickets through natural language conversations.**

Bookie is an AI agent that aims to simplify the movie ticket booking experience. Instead of navigating through multiple pages on ticket booking websites, users can simply chat with the agent, provide the required details, approve the booking, and let the agent handle the rest.

---

# 💡 Inspiration

The idea for Bookie came to me while thinking about booking tickets for **Spider-Man: Brand New Day**.

Booking tickets for highly anticipated movie releases usually involves repeatedly checking ticketing websites, selecting theatres, browsing show timings, choosing seats, and completing the payment before the desired seats are taken.

That made me wonder:

> **Why should I manually perform all these repetitive steps when an AI agent could do them for me?**

I wanted an experience where I could simply say:

> *"Book two tickets for Spider-Man tomorrow evening."*

The agent would then ask only for the missing information, present the available options, get my approval, and complete the booking.

That idea eventually became **Bookie**.

---

# 🏗️ Why I Built My Own Backend

One of the biggest challenges while building Bookie was that popular movie ticket booking platforms do not provide public APIs for searching shows, checking seat availability, or booking tickets.

To build and experiment with an autonomous booking agent, I first needed a backend that the agent could interact with.

Instead of relying on closed third-party services, I built my own movie ticket booking system using **FastAPI**, **SQLAlchemy**, and **MySQL**. The backend exposes APIs for retrieving movies, theatres, shows, available seats, and booking tickets.

> **Bookie does not currently book tickets on BookMyShow or any other commercial ticket booking platform.**

Instead, it interacts with a custom-built backend that simulates a real-world movie ticket booking system. This gives me complete control over the booking workflow and allows me to experiment with agent orchestration, tool calling, state management, and human approval.

---

# ✨ Current Features (Version 1)

Version 1 implements a guided conversational booking workflow.

The agent can currently:

- 🎬 Display available movies
- 🏢 Show theatres playing the selected movie
- 🕒 Display available shows for the selected theatre
- 💺 Show real-time seat availability
- 🎟️ Book movie tickets
- ✅ Ask for user approval before confirming the booking
- 🧠 Maintain booking state throughout the conversation

---

# 🎯 Current Booking Flow

The current version follows a simple guided workflow:

1. Select a movie
2. View available theatres
3. Select a theatre
4. View available shows
5. Select a show
6. View available seats
7. Select seats
8. Confirm booking approval
9. Book the tickets

---

# 🚀 Future Vision

Version 1 intentionally starts from the movie selection step.

The long-term goal is to make Bookie significantly more flexible by allowing users to begin the booking process from **any point** in the conversation.

For example, users should be able to say things like:

- "Show nearby theatres."
- "What movies are playing around 8 PM?"
- "Book me something for tonight."
- "I want the last row."
- "What can I watch near me this evening?"

Instead of following a fixed sequence, the agent will intelligently determine the missing information and ask only the questions necessary to complete the booking.

Ultimately, Bookie should behave like a real booking assistant rather than a form with conversational input.

---

# 🛠️ Tech Stack

### AI & Agent Framework

- LangChain
- Tool Calling
- Human Approval Middleware

### Backend

- FastAPI
- Pydantic
- SQLAlchemy
- Requests

### Database

- MySQL

### Language

- Python

---

# 🌐 Backend API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/movies` | Retrieve all available movies |
| `GET` | `/movie/{title}` | Retrieve details of a specific movie |
| `GET` | `/movie/theatres/{movie_id}` | List theatres showing a particular movie |
| `GET` | `/theatre/{name}` | Retrieve theatre details |
| `GET` | `/shows/{movie_id}/{theatre_id}` | Retrieve available shows for a movie in a theatre |
| `GET` | `/seats/show/{show_id}` | Retrieve seat availability for a show |
| `POST` | `/book` | Book selected seats |
| `GET` | `/tickets/{booking_id}` | Retrieve booked tickets |

---

# 📌 Current Status

This repository contains **Version 1** of Bookie.

The primary focus of this version is building a reliable conversational booking workflow with a custom backend and an AI agent capable of guiding users through the ticket booking process.

Future versions will introduce more flexible conversations, smarter reasoning, richer recommendations, and eventually support integration with real-world ticket booking services if suitable APIs become available.

---

# ⭐ Support

If you found this project interesting, consider giving it a ⭐ on GitHub.

It really motivates me to continue building AI agents and open-source projects.

