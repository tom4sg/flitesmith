# Flitesmith

**A parody of LangChain's LangSmith for RAG Evaluation.**

---

## Overview

Flitesmith is an experimental platform inspired by [LangChain's LangSmith](https://smith.langchain.com/), but designed for use with Flite AI. It provides a streamlit frontend for for managing interacting with a chatbot, and viewing the RAG snippets AI responses used as context.

---

## Features
- Expects connection to a backend via an **ngrok** link (for secure tunneling)
- Strict API response format (see below)

---

## Requirements
- Python 3.8+
- `requirements.txt` dependencies:
  - streamlit
  - requests
  - uuid
- Ngrok (for exposing backend to the internet)

---

## Setup

1. **Clone the repo and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Expose your backend with ngrok:**
   ```bash
   ngrok http 8000
   ```
   Use the generated ngrok HTTPS link to connect your frontend or external services.

3. **Run the server:**
   ```bash
   python ground_truth.py
   # or
   uvicorn ground_truth:app --reload
   ```

---

## API

### `/chat` (POST)
- Expects a JSON body with the following fields:
  - `context`: List of messages (see below)
  - `text`: User's input
  - `max_new_tokens`: (optional) Max tokens to generate
  - `session_id`: (optional) Session identifier

#### Message Format
```python
class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
```

#### Example Request
```jsonc
{
  "context": [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi, how can I help you?"}
  ],
  "text": "What is Flite?",
  "session_id": "abc123"
}
```

#### Example Response
```jsonc
{
  "response": "<string: assistant's reply>",
  "retrieved_docs": [
    {"text": "<string: document snippet>",
      "...": "..." // any other fields, optional
    }
  ],
  "messages": [
    {"role": "user", "content": "<string>"}
    {"role": "assistant", "content": "<string>"}
  ],
  "session_id": "<string: UUID>"
}
```
