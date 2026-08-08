# 1. Agents
# pip install -qU langchain "langchain[openai]"
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5.4-nano",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)


# 2. Models
# models are the reasoning engine of agents
from langchain.chat_models import init_chat_model
openai_model = init_chat_model("openai:gpt-5-mini")
response = openai_model.invoke("In one line tell me what is Langchain")
print(response.content)


# 3. Messages
from langchain_core.messages import SystemMessage, HumanMessage
message = [
    SystemMessage(content="You are a pirate and answer all the questions as a pirate"),
    HumanMessage(content="In one line tell me what is Langchain")
]
response = openai_model.invoke(message)
print(response.content)