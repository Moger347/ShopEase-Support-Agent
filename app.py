import streamlit as st
import pandas as pd
import smtplib
import difflib
import re
from email.mime.text import MIMEText

# -------------------------------
# CONFIGURATION – CHANGE THESE
# -------------------------------
FAQ_FILE = "faq_data.csv"

# Use the Gmail you created for this project
SUPPORT_EMAIL = "shopeasecustomerhelp@gmail.com"         # your support Gmail
APP_PASSWORD = "aqvpuiwcfamkhyxn"                  # your Gmail app password


# -------------------------------
# LOAD FAQ DATA
# -------------------------------
@st.cache_data
def load_faq_data(path):
    df = pd.read_csv(path)
    # Make sure columns exist
    if not {"Question", "Answer"}.issubset(df.columns):
        raise ValueError("faq_data.csv must have 'Question' and 'Answer' columns")
    # Normalize once
    df["Question_lower"] = df["Question"].str.lower()
    return df

faq_df = load_faq_data(FAQ_FILE)


# -------------------------------
# EMAIL: SEND ESCALATION TO OWNER
# -------------------------------
def send_escalation_email(user_message, chat_history):
    """
    Sends an email to the support owner including the latest user message
    and the recent chat history.
    """
    subject = "🚨 Human Support Requested - ShopEase"

    history_lines = []
    for role, msg in chat_history[-10:]:  # last 10 turns
        who = "User" if role == "user" else "Bot"
        history_lines.append(f"{who}: {msg}")
    history_text = "\n".join(history_lines)

    body = f"""
A customer has requested a human support agent.

Latest customer message:
------------------------
{user_message}

Recent chat history:
------------------------
{history_text}

Please respond as soon as possible.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SUPPORT_EMAIL
    msg["To"] = SUPPORT_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SUPPORT_EMAIL, APP_PASSWORD)
            server.sendmail(SUPPORT_EMAIL, SUPPORT_EMAIL, msg.as_string())
        return True
    except Exception as e:
        # Show error in Streamlit, but don't crash
        st.error(f"❌ Could not send escalation email: {e}")
        return False


# -------------------------------
# FAQ MATCHING – MORE FLEXIBLE
# -------------------------------
def clean_text(text: str) -> str:
    """Lowercase and remove extra spaces/punctuation for better matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_best_faq_answer(user_input: str, df: pd.DataFrame, cutoff: float = 0.8):
    """
    Uses difflib to find the closest FAQ question to the user input.
    Works for different phrasings like 'forgot password', 'reset password', etc.
    """
    user_clean = clean_text(user_input)

    questions = df["Question_lower"].tolist()
    # difflib will return the closest question string if similarity > cutoff
    matches = difflib.get_close_matches(user_clean, questions, n=1, cutoff=cutoff)

    if matches:
        matched_q = matches[0]
        answer = df.loc[df["Question_lower"] == matched_q, "Answer"].values[0]
        return answer, matched_q
    else:
        return None, None


# -------------------------------
# STREAMLIT UI SETUP
# -------------------------------
st.set_page_config(page_title="ShopEase AI Support Assistant", layout="centered")

st.markdown(
    """
    <h1 style="text-align:center; color:#58A6FF;">
        🤖 ShopEase AI Support Assistant
    </h1>
    <p style="text-align:center;">
        Hi! I'm here to help with your ShopEase questions. How can I assist you? 👇
    </p>
    """,
    unsafe_allow_html=True,
)

# Chat history stored in session
if "chat" not in st.session_state:
    st.session_state.chat = []  # list of (role, message)


# -------------------------------
# USER INPUT
# -------------------------------
user_message = st.text_input("💬 Type your message:")

col1, col2 = st.columns([1, 1])

if col1.button("Send") and user_message.strip() != "":
    text_lower = user_message.lower()

    # Save user message first
    st.session_state.chat.append(("user", user_message))

    # 1️⃣ If user clearly asks for human support → escalate
    human_keywords = ["human", "agent", "real person", "support person"]
    if any(k in text_lower for k in human_keywords):
        email_ok = send_escalation_email(user_message, st.session_state.chat)
        if email_ok:
            bot_response = (
                "📩 I've notified a human support agent with your details. "
                "They will reach out to you shortly."
            )
        else:
            bot_response = (
                "⚠️ I tried to contact a human support agent but something went wrong. "
                "Please try again in a moment or use another support channel."
            )

    else:
        # 2️⃣ Try to answer from FAQ using fuzzy matching
        answer, matched_q = find_best_faq_answer(user_message, faq_df)

        if answer:
            bot_response = (
                f"✅ I found something related to your question:\n\n"
                f"**Q:** {matched_q}\n\n"
                f"**A:** {answer}\n\n"
                f"Anything else you’d like help with?"
            )
        else:
            # 3️⃣ Fallback when we truly don't know
            bot_response = (
                "🤔 I couldn't find an exact answer to that in our FAQ.\n\n"
                "You can try asking in a different way, or type **'I need a human agent'** "
                "if you’d like me to connect you to human support."
            )

    # Save bot response
    st.session_state.chat.append(("bot", bot_response))

# Reset Chat
if col2.button("🔄 Reset Chat"):
    st.session_state.chat = []
    st.success("Chat cleared!")


# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
st.markdown("<h3>💭 Chat</h3>", unsafe_allow_html=True)

for role, message in st.session_state.chat:
    if role == "user":
        st.markdown(
            f"""
            <div style='background:#0066FF; color:white; padding:10px; border-radius:10px;
                        margin:5px; width:fit-content;'>
                👤 {message}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:  # bot
        st.markdown(
            f"""
            <div style='background:#2ECC71; color:black; padding:10px; border-radius:10px;
                        margin:5px; width:fit-content;'>
                🤖 {message}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("---")
st.caption("© 2025 ShopEase - AI + Human Hybrid Support")
