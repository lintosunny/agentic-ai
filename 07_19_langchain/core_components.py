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
openai_model = init_chat_model("openai:gpt-5.4-nano")
response = openai_model.invoke("In one line tell me what is Langchain")
print(response.content)


# 3. Messages
# Types: system message, human message (user message), ai message, tool message
from langchain_core.messages import SystemMessage, HumanMessage
message = [
    SystemMessage(content="You are a pirate and answer all the questions as a pirate"),
    HumanMessage(content="In one line tell me what is Langchain")
]
response = openai_model.invoke(message)
print(response.content)

# we can provide example as user and ai messages like few shot prompting to get better ai output
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
messages = [
    SystemMessage("You are helpful assistant"),
    HumanMessage("Can you help me?"),
    AIMessage("I'd be happy to help you with that question!"),
    HumanMessage("Great! What is 2+2?")
]
response = openai_model.invoke(messages)
print(response.content)

# we can also give this as a dictionary
messages = [
    {"role": "system", "content": "You are a poetry expert"},
    {"role": "user", "content": "Write a haiku about spring"},
    {"role": "assistant", "content": "Cherry blossoms bloom..."}
]


# 4. Streaming
# powers real-time chat UI, provides better UX. First check model support this or not.
# these chunks aren't a lesser type, they sum into exactly what invoke() would have returned.
import time
chunks = []
full_message = None 
for chunk in openai_model.stream("Write 2 sentence about AI"):
    chunks.append(chunk)
    print(chunk.text)
    full_message = chunk if full_message is None else full_message + chunk
    time.sleep(1)

print()
print("full message: ", full_message)


# 5. Batch
# collection of independent requests to a model can significantly improve performance and reduce cost, as the processing can be done in parallel
responses = openai_model.batch([
    "how are you?",
    "what is 2+2?",
    "what is ai?"
])
for response in responses:
    print(response)

# batch with streaming
for response in openai_model.batch_as_completed([
    "how are you?",
    "what is 2+2?",
    "what is ai?"
]):
    print(response)


# 6. Tools
def get_weather(location: str) -> str:
    """Returns weather of the loaction"""
    return f"Sunny in {location}"

model_with_tools = openai_model.bind_tools([get_weather])
response = model_with_tools.invoke("What is the weather in Delhi?")
print(response.content)
print(response.tool_calls)


# 7. Structured Output
from pydantic import BaseModel, Field
class Email(BaseModel):
    subject: str = Field(description="The subject of the mail")
    body: str = Field(description="The body of the mail")

model_with_structure = openai_model.with_structured_output(Email)
response = model_with_structure.invoke("Write a mail to my manager for sick leave")
print(response)