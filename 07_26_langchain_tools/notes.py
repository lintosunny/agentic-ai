# Tools are just glorified functions/API calls
# Whenever we use tool, atleast 2 times llm is used
# 1. To determine which tool to call, 2. To summarize the tool output

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()


model = init_chat_model("openai:gpt-5.4-nano")

@tool
def check_showtimes(movie_title: str) -> str:
    """Check available showtimes for a movie"""
    fake_showtimes = {
        "dune": "7.00 PM and 7.30 PM",
        "troy": "10.00 AM only",
        "swapped": "Sold out for tonight"
    }
    return fake_showtimes.get(movie_title.lower(), "no showtimes found for the title")

# Overwrite function name and description. reserve -> book seats and same for description
@tool('book seats', description='Book movie for a customer, whenever customer wantst to book/reserve')
def reserve(movie: str, seats: int) -> str:
    """Reserve seats"""
    return f"Reserved {seats} seat for {movie}"

tool = TavilySearch(
    max_results = 5,
    topic = "general"
)

@tool
def search_internet(topic: str) -> str:
    return TavilySearch()



# Args Schema
# While defining tool don't use config and runtime args. They are reserved by langchain
class SeatBookingInput(BaseModel):
    movie_title: str = Field(description="Exact name of movie")
    seat_count: int = Field(description="Number of seats to book", ge=1, le=10)
    preferred_row: Literal["front", "middle", "back"] = Field(description="preferred seat row", default="middle")

@tool(args_schema=SeatBookingInput)
def book_seats(movie_title: str, seats: int, preferred_row: str) -> str:
    """Book seats for a movie"""
    return f"Booked {seats} seats for {movie_title} in row {preferred_row}"

print(book_seats.args)
# output = {
# 'movie_title': {'description': 'Exact name of movie', 'title': 'Movie Title', 'type': 'string'}, 
# 'seat_count': {'description': 'Number of seats to book', 'maximum': 10, 'minimum': 1, 'title': 'Seat Count', 'type': 'integer'}, 
# 'preferred_row': {'default': 'middle', 'description': 'preferred seat row', 'enum': ['front', 'middle', 'back'], 'title': 'Preferred Row', 'type': 'string'}
# }



# Binding vs Executions
# Bind tools to the model → invoke with a question → model decides whether a tool is needed.
# If needed, tool_calls are populated as a request only; nothing executes yet.
# create_agent handles the actual tool execution.

model_with_tools = model.bind_tools([book_seats, check_showtimes])
response = model_with_tools.invoke("Is Troy showing tonight, can you book 2 seats?")

for tool_call in response.tool_calls:
    print("--->", tool_call['name'], tool_call['args'])



# Runtime in tools
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import HumanMessage

@tool
def get_last_movie_mentioned(runtime: ToolRuntime) -> str:
    """Gets last movie mentioned"""
    pass

print(get_last_movie_mentioned.args)
# output-> {'movie': {'title': 'Movie', 'type': 'string'}}


# Memmory
from langgraph.store.memory import InMemoryStore
from langchain_core.tools import tool
from langchain.tools import tool,ToolRuntime
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

from typing import Any


loyalty_store= InMemoryStore()


@tool
def save_favourite_genres(customer_id:str,genre:str,runtime:ToolRuntime) -> str:
  """Save a customer's facvourite movie genre for future visits"""
  runtime.store.put((customer_id,"preferences"),"favourite_genre",{"value":genre})
  return f"Got it -- I will remmeber you like {genre} movies"

@tool
def recall_favourite_genre(customer_id:str,runtime:ToolRuntime) -> str:
  """ Recall a customer's fav movie genre, if we have saved it before"""
  favourite_genre = runtime.store.get((customer_id,"preferences"),"favourite_genre")
  return favourite_genre.value["value"] if favourite_genre else "We don't have any saved preference for this user"


memory_agent = create_agent(
    model = model,
    tools=[save_favourite_genres,recall_favourite_genre],
    store=loyalty_store  # Attached to the agent, tools can access it using runtime
)

memory_agent.invoke({"messages": [("user", "Hi, I'm customer priya_01, I love sci-fi movies, please remember that.")]})
result = memory_agent.invoke({"messages": [("user", "What genre do I usually like? I'm priya_01.")]})
print(result['messages'][-1].content)
# output -> You usually like sci-fi. Would you like recommendations in that genre?

# runtime.executionInfo
# runtime.server_info --------> valid on Langchain server and is None for local development.
@tool
def log_booking_context(runtime:ToolRuntime) -> str:
  info = runtime.execution_info


# Skippping the Model's final Polishing
@tool(return_direct=True)
def get_exact_refund_policy() -> str:
    """Tell the refund policy."""
    return "Tickets are refundable up to 2 hours before showtime. No refunds after that."

direct_agent = create_agent(model="openai:gpt-5-mini", tools=[get_exact_refund_policy])
result = direct_agent.invoke({"messages": [("user", "What's your refund policy? Please explain in points")]})
print(result["messages"][-1].content)
# output -> Tickets are refundable up to 2 hours before showtime. No refunds after that.

# Dynamic Tool Loading & Calling
# Tools available to the agent is modified at runtime rather than defined all upfront
# state based tools, store based tools, 
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@tool
def standard_booking(movie_title: str) -> str:
    """Book a standard seat."""
    return f"Standard seat booked for {movie_title}."

@tool
def vip_lounge_booking(movie_title: str) -> str:
    """Book a VIP lounge seat with premium service. VIP members only."""
    return f"VIP lounge seat booked for {movie_title}."

@wrap_model_call
def gate_vip_tools(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Only expose vip_lounge_booking to VIP members."""
    is_vip = request.state.get("is_vip_member", False)
    if not is_vip:
        allowed = [t for t in request.tools if t.name != "vip_lounge_booking"]
        request = request.override(tools=allowed)
    return handler(request)

gated_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[standard_booking, vip_lounge_booking],
    middleware=[gate_vip_tools],
)

result_regular = gated_agent.invoke({"messages": [("user", "Book me a VIP lounge seat for Dune?")]})
print("Regular member result:", result_regular["messages"][-1].content)

result_vip = gated_agent.invoke(
    {"messages": [("user", "Book me a VIP lounge seat for Dune")], "is_vip_member": True}
)
print("VIP member result:", result_vip["messages"][-1].content)
print()
print("Same code, same query -- only the 'is_vip_member' flag differed. The model literally")
print("could not choose vip_lounge_booking in the first case -- it wasn't on its menu at all.")



# How can we give state as an input
from langchain.agents import create_agent, AgentState

class GatedState(AgentState):
    is_vip_member: bool 

gated_agent_with_middleware = create_agent(
    model="openai:gpt-5-mini",
    tools=[standard_booking, vip_lounge_booking],
    middleware=[gate_vip_tools],
    state_schema=GatedState
)

result_with_state_input = gated_agent_with_middleware.invoke(
    {"messages": [("user", "Book me a VIP lounge ticket for Dune")], "is_vip_member": False} 
)



# Headless tools
# will be running at users end. examples are clipboard, location, latency, payments, etc.


# InMomorySaver or Checkpointing
# one usecase agent will remember you
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": "Lintos messages"}}
aget_stateful = create_agent(
    model="openai:gpt-5-mini",
    system_prompt="you are a movie booking assistant",
    checkpointer=checkpointer
)

aget_stateful.invoke({"messages": [("user", "I am Linto")]}, config=config)
aget_stateful.invoke({"messages": [("user", "Who am I")]}, config=config)
# now it will remember my name
