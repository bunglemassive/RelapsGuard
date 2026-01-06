import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="RelapsGuard",
    page_icon="🛡️",
    layout="centered"
)

# Initialise Groq client securely using Streamlit secrets
@st.cache_resource
def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except FileNotFoundError:
        st.error("GROQ_API_KEY not found in Streamlit secrets. Please add it in the app settings.")
        st.stop()
    except KeyError:
        st.error("GROQ_API_KEY missing from secrets.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# App header
st.title("🛡️ RelapsGuard")
st.markdown("Your nervous system monitoring and relapse prevention assistant powered by Groq.")

# Initialise session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are RelapsGuard, a compassionate and knowledgeable assistant specialising in nervous system regulation, stress management, and relapse prevention. Use physiological insights, empathy, and practical strategies in your responses."}
    ]

# Display previous messages
for message in st.session_state.messages[1:]:  # Skip system prompt
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How are you feeling today, or what would you like support with?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=800
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # Add assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Sidebar information
with st.sidebar:
    st.header("About RelapsGuard")
    st.info("This app provides real-time support for nervous system awareness and relapse prevention using advanced AI.")
    st.caption("Powered by Llama 3.1 8B Instant via Groq")
    st.caption("Model: llama-3.1-8b-instant")
