# AI Terms, Properly Explained

## Large Language Model (LLM)

Examples: Gemini, ChatGPT, Claude, etc.

A Large Language Model (LLM) does **not** have an "understanding module." It is an advanced pattern-recognition system trained to predict the most likely next token based on everything it has seen so far.

For example, if you type **"thank"**, it often continues with **"you"**—not because it understands gratitude, but because **"you"** is simply the most probable next token.

## Tokens

Tokens are the **building blocks** AI models process. They are not always whole words.

Think of them as puzzle pieces of text—the **currency of AI**.

**Examples:**
- `cat` → `cat` (1 token)
- `unbelievable` → `unbeliev` + `able` (multiple tokens)

AI models read, generate, and bill usage in **tokens**, not words.

## Vector (Embedding)

An **embedding** is a numerical representation of text that captures its meaning.

Think of it like a **GPS coordinate for meaning**. Words or sentences with similar meanings are placed closer together in a high-dimensional space.

**Example:**
- `dog` and `puppy` → close together
- `dog` and `airplane` → far apart

## Context Window

The **context window** is everything an AI model can "see" at one time.

This includes:
- Your current message
- Previous messages
- Uploaded documents
- System instructions

Every model has a maximum context size. Once that limit is reached, the **oldest content is dropped** to make room for new content.

## LLM Calls Are Stateless

An individual LLM API call is **stateless**.

This means the model **does not remember previous conversations** unless that information is sent again in the current request. Any memory must be provided externally (for example, by an application that stores conversation history).

## Parameters

Parameters are the model's learned internal values.

Think of them as **millions or billions of tiny knobs**. Individually they mean very little, but together they determine everything the model has learned during training.

The model's intelligence emerges from the combined values of all these parameters.

## AI Agent

An **AI agent** is a system that combines:
- **Brain (AI Model)**
- **Memory**
- **Tools**

It can perceive information, reason about it, use tools when needed, and take actions autonomously to achieve a goal.

> **AI Agent = Brain (AI Model) + Memory + Tools**

