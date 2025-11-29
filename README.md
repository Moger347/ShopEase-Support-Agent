# 🛍️ ShopEase AI Support Assistant

A smart AI-powered customer support chatbot built using Python, Streamlit, and ML-based fuzzy search.  
It answers FAQs and can escalate unresolved queries to a human support agent via email.

---

## 🚀 Features

- 💬 Real-time conversational chatbot  
- 🔍 Intelligent FAQ matching (supports similar question wording)  
- 📩 Auto-email escalation to support team  
- 🧠 Memory of chat history  
- 🎨 Clean UI with reset option  
- ☁️ Deployable on Streamlit Cloud  

---

## 🛠️ Tech Stack

This project is built using a combination of modern tools and technologies to deliver an efficient and scalable AI-powered customer support agent.

- 🐍 **Python** – Core programming language  
- 🎨 **Streamlit** – Interactive frontend for chatbot UI  
- 📂 **Pandas** – Handling and processing FAQ dataset  
- 🧠 **difflib** – Fuzzy matching algorithm for intelligent response search  
- ✉️ **SMTP with Gmail App Password** – Escalates unanswered queries via email  
- 🔐 **TOML** – Secure credential storage (Streamlit Secrets)  
- ☁️ **Streamlit Cloud** – Hosting and deployment platform  

---


## 🔗 APIs & Services Used

This project integrates several external services and internal API mechanisms to enable chatbot functionality, email escalation, and secure deployment.


### ✉️ Gmail SMTP Service

- Used to send escalation emails when the chatbot cannot answer a customer query.
- Implemented via the built-in Python `smtplib` library.
- Authenticated using a **Gmail App Password** (not the normal email password).
- Ensures safe automated communication between the bot and the human support team.

**SMTP Configuration Used:**

| Key | Value |
|-----|-------|
| SMTP Server | `smtp.gmail.com` |
| Port | `465` (SSL) |
| Authentication | Gmail App Password |

---

### 🔐 Streamlit Secrets Manager API

- Used to securely store and access sensitive information like email credentials.
- Prevents credentials from being pushed to GitHub.
- Automatically injected during deployment by Streamlit Cloud.

**Sample Secret File Format (`.streamlit/secrets.toml`):**

```toml
SUPPORT_EMAIL="your-email@gmail.com"
APP_PASSWORD="your-app-password"


---




## 💡 Example Queries

Here are some sample questions users can ask the bot:

- How do I reset my password?
- How to recover account access?
- How do I apply a discount code?
- How do I track my order?
- What payment methods do you accept?
- Can I cancel my order?
- I need a human agent.

---

## 🏗️ System Architecture

- The architecture diagram represents how the AI Support Assistant processes user queries and escalates unanswered tickets to email
- check screenshot folder for the architecture diagram

---

## 🚀 Live Demo:  
🔗 https://shopease-support-agent-qethwc7xxdpnhjdycrcdcz.streamlit.app/

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shopease-support-agent-qethwc7xxdpnhjdycrcdcz.streamlit.app/)

---





