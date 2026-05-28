import streamlit as st
import ollama
import pyperclip

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="💻",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3, p, label {
    color: white;
}

textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-size: 16px;
}

.stDownloadButton button {
    background-color: #16a34a;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙ AI Settings")

# MODEL SELECTION
model_name = st.sidebar.selectbox(
    "Choose AI Model",
    [
        "codellama",
        "deepseek-coder:latest",
        "mistral"
    ]
)

# EXPLANATION LEVEL
level = st.sidebar.selectbox(
    "Explanation Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# MODE
mode = st.sidebar.selectbox(
    "Mode",
    [
        "Explain Code",
        "Find Errors",
        "Optimize Code",
        "Add Comments"
    ]
)

# CLEAR CHAT
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []

# ---------------- TITLE ----------------

st.title("💻 AI Code Explainer")

st.write("Ask coding doubts or paste code for AI explanation.")

# ---------------- SESSION MEMORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "response" not in st.session_state:
    st.session_state.response = ""

# ---------------- CLIPBOARD DETECTION ----------------

clipboard_code = pyperclip.paste()

if clipboard_code:

    st.info("📋 Code detected in clipboard!")

    if st.button("Paste Clipboard Code"):

        st.session_state.messages.append({
            "role": "user",
            "content": clipboard_code
        })

# ---------------- DISPLAY OLD CHAT ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "user":
            st.code(msg["content"])

        else:
            st.write(msg["content"])

# ---------------- CHAT INPUT ----------------

user_input = st.chat_input("Ask coding doubts or paste code...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.code(user_input)

# ---------------- AI RESPONSE ----------------

if st.session_state.messages:

    last_message = st.session_state.messages[-1]

    if last_message["role"] == "user":

        with st.chat_message("assistant"):

            try:

                stream = ollama.chat(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""
You are an expert AI coding assistant.

MODE:
{mode}

EXPLANATION LEVEL:
{level}

YOUR TASKS:
1. Detect programming language automatically.
2. Explain code clearly.
3. Detect errors if present.
4. Suggest improvements.
5. Suggest optimization if possible.
6. Continue conversation naturally.
7. Help beginners understand coding.
8. Mention syntax errors clearly.
"""
                        }
                    ] + st.session_state.messages,
                    stream=True
                )

                response = st.write_stream(
                    chunk["message"]["content"]
                    for chunk in stream
                )

                st.session_state.response = response

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                st.error(f"Error: {e}")

# ---------------- COPY BUTTON ----------------

if st.session_state.response != "":

    if st.button("📋 Copy Explanation"):

        pyperclip.copy(st.session_state.response)

        st.success("Explanation copied!")

# ---------------- DOWNLOAD BUTTON ----------------

if st.session_state.response != "":

    st.download_button(
        label="⬇ Download Explanation",
        data=st.session_state.response,
        file_name="explanation.txt",
        mime="text/plain"
    )
