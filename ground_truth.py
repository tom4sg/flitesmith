import streamlit as st
import requests
import uuid

# Set up session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "api_url" not in st.session_state:
    st.session_state.api_url = ""

st.title("💬 Flite RAG Chat & QA Dashboard")
# Let user input ngrok URL
st.session_state.api_url = st.text_input(
    "Enter your backend URL (e.g. https://1234.ngrok-free.app)",
    value=st.session_state.api_url
)

# Stop everything if no URL is given
if not st.session_state.api_url:
    st.warning("Please enter your backend URL to begin.")
    st.stop()

API_URL = st.session_state.api_url

# --- Chat UI ---
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call backend
    resp = requests.post(
        f"{API_URL}/chat",
        json={
            "text": user_input,
            "session_id": st.session_state.session_id,
            "context": st.session_state.messages  # optional but helps cold start
        }
    )

    data = resp.json()

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": data["response"], "retrieved_docs": data["retrieved_docs"]})

# --- Display all messages ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg.get("content", ""))

    # Show RAG snippets if available (assistant only)
    if msg["role"] == "assistant":
        retrieved = msg.get("retrieved_docs", [])
        if retrieved:
            with st.expander("🔍 RAG Snippets"):
                for i, doc in enumerate(retrieved):
                    snippet_text = doc.get("text", "").replace("\n", "<br>")
                    st.markdown(f"**Snippet {i+1}:**<br>{snippet_text}", unsafe_allow_html=True)
                    # corr = st.text_area("✏️ Correction", key=f"corr_{idx}_{i}")
                    # if st.button("💾 Save Correction", key=f"save_{idx}_{i}"):
                    #     # You can insert to Mongo or another system here
                    #     st.success("Saved ✅")
        else:
            st.info("No RAG snippets were returned.")
