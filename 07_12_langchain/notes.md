# LangChain Notes

## Learning Flow

```text
LangChain → LangGraph → Deep Agents
```

We'll cover the topics in this order.

**Version:**

```bash
langchain==1.3.13
```


# What is an Agent?

```text
Agent = Model + Harness
```

**Harness:**  
A harness is the execution framework around the model that manages tools, memory, prompts, and the agent's decision-making process. It enables the model to perform tasks beyond simple text generation.


# `create_agent`

`create_agent` is a **minimal, highly configurable harness** for building AI agents in LangChain.


# LangChain vs LangGraph vs Deep Agents vs LangSmith

| Component | Purpose |
|-----------|---------|
| **LangChain** | Build AI applications and simple agents with models, tools, and prompts. |
| **LangGraph** | Build stateful, multi-step, and controllable agent workflows. |
| **Deep Agents** | Higher-level framework for creating autonomous agents with planning, memory, and tool usage. |
| **LangSmith** | Debug, trace, evaluate, and monitor your LangChain/LangGraph applications. |


# Tools

Tools allow the model to interact with external systems by calling functions that we define.

They can:
- Call APIs
- Query databases
- Read or write files
- Execute custom Python functions
- Depend on runtime context
- Interact with the agent's memory


# Memory

Memory enables an agent to maintain state across interactions.

It allows the agent to:
- Remember previous conversations
- Retain important context
- Use past information in future responses
- Provide more personalized and coherent interactions