# Flitesmith

**A parody of LangChain's LangSmith, for Flite AI.**

---

## Overview

Flitesmith is a playful, experimental platform inspired by [LangChain's LangSmith](https://smith.langchain.com/), but designed for use with Flite AI. It provides a streamlit frontend for for managing interacting with a chatbot, and viewing the RAG snippets AI responses used as context. This project is not affiliated with LangChain or Flite AI.

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

2. **Set up environment variables:**
   - `MONGODB_URI` (your MongoDB connection string)
   - `PERSONAL_ANTHROPIC` (your Anthropic API key)
   - `HUGGINGFACE_HUB_TOKEN` (for SentenceTransformer)
   - (Optional) other .env variables as needed

3. **Start Redis and MongoDB locally, or connect to remote instances.**

4. **Expose your backend with ngrok:**
   ```bash
   ngrok http 8000
   ```
   Use the generated ngrok HTTPS link to connect your frontend or external services.

5. **Run the server:**
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
```json
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
```json
{
  "response": "<string: assistant's reply>",
  "retrieved_docs": [
    {"text": "<string: document snippet>",
      "...": "..." // any other fields, optional}
  ],
  "messages": [
    {"role": "user" | "assistant", "content": "<string>"}
  ],
  "session_id": "<string: UUID>"
}
```

---

## Notes
- This project is a parody and not intended for production use.
- Requires a running backend accessible via ngrok for external connections.
- Expects strict input/output formats as shown above.
- For more details, see `ground_truth.py`.

---

## License
MIT (parody/fair use) 
