import urllib.error
import urllib.request
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}"

@tool  # Adding this to show how to add a tool using decorator
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Fransico?"}]}
)
print("=====RESULT=====")
print(result)
print("=====MESSAGE=====")
print(result["messages"][-1].content_blocks)