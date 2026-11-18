from RAG_ChatBot import ChatBot
import streamlit as st


@st.cache_resource
def get_chatbot():
    """Build the chatbot once — cached across reruns so documents are not
    re-embedded and re-uploaded on every chat message."""
    return ChatBot()


# Build the chatbot — show a friendly message instead of a raw crash when
# API keys are missing or invalid
try:
    bot = get_chatbot()
except Exception as e:
    st.error(f"Failed to start the chatbot: {e}")
    st.info(
        "Check that your `.env` file contains valid `OPENAI_API_KEY` and "
        "`PINECONE_API_KEY` values, and that OpenAI/Pinecone are reachable. "
        "See the README for setup instructions."
    )
    st.stop()

st.title("Toronto Travel Assistant Bot")
st.caption("A retrieval-augmented chatbot that answers questions about traveling to Toronto.")


# Function for generating the LLM response
def generate_response(query):
    return bot.rag_chain.invoke(query)


# Store LLM-generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm TravelBot. How can I assist you with your travel plans today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if user_input := st.chat_input("Ask me about Toronto..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

# Generate a new response if the last message is from the user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = generate_response(st.session_state.messages[-1]["content"])
            except Exception as e:
                response = f"Sorry, something went wrong: {e}"
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
