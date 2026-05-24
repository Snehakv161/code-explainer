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
        "deepseek-coder",
        "mistral"
    ]
)

# LANGUAGE SELECTION
language = st.sidebar.selectbox(
    "Programming Language",
    [
        "Python",
        "C",
        "C++",
        "Java",
        "JavaScript",
        "C#",
        "HTML",
        "CSS"
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

st.write("Paste code and get instant AI explanation.")

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
        st.session_state.clipboard_data = clipboard_code

# ---------------- CODE INPUT ----------------

default_code = st.session_state.get("clipboard_data", "")

code = st.text_area(
    "Paste your code here",
    value=default_code,
    height=300
)

# ---------------- DISPLAY OLD CHAT ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "user":
            st.code(msg["content"], language=language.lower())

        else:
            st.write(msg["content"])

# ---------------- MAIN BUTTON ----------------

if st.button("🚀 Explain Code"):

    if code.strip() == "":
        st.warning("Please paste some code.")
        st.stop()

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": code
    })

    with st.chat_message("user"):
        st.code(code, language=language.lower())

    # AI PROMPT
    prompt = f"""
    You are an expert coding teacher.

    TASK:
    {mode}

    PROGRAMMING LANGUAGE:
    {language}

    EXPLANATION LEVEL:
    {level}

    INSTRUCTIONS:
    - Explain clearly
    - Use simple English
    - Explain line by line if needed
    - Make it beginner friendly

    CODE:
    {code}
    """

    # AI RESPONSE
    with st.chat_message("assistant"):

        stream = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
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