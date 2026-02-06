import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION (USING SECRETS) ---
# We use labels here; the actual values stay hidden in the dashboard
SENDER_EMAIL = st.secrets["sender_email"]
SENDER_PASSWORD = st.secrets["sender_password"]
RECEIVER_EMAIL = st.secrets["receiver_email"]

# --- 2. QUESTION BANK ---
QUESTIONS = {
    "🌱 Childhood": [
        "What is your earliest childhood memory?",
        "What was your favorite toy or game growing up?",
        "What is a smell that instantly takes you back to your childhood?",
        "What is a 'quiet' trait about yourself that you wish more people noticed or appreciated?",
    ],
    "💍 Our Love Story": [
        "What is a 'small' memory of us that carries a surprisingly large amount of weight for you?",
        "When did you realize you wanted us to get married?",
        "What is your favorite memory from our wedding day?",
        "What is one small thing I do that always makes you feel loved?",
        "How have I changed your perspective on the world or on yourself?",
    ],
    "🚀 Career & Ambition": [
        "What was the takeaway from your very first job?",
        "If you could start any business tomorrow with zero risk, what would it be?",
        "What is the proudest moment of your professional life so far?",
        "What is a belief you held firmly ten years ago that you have since let go of?"
    ],
    "🔮 Wisdom & Legacy": [
        "What is the best piece of advice you’ve ever received?",
        "If you could tell your 18-year-old self one thing, what would it be?",
        "What do you want people to remember most about you?",
        "What is a family tradition we don't have yet that you’d love to start with me?",
        "When you think about our future together, what is the 'mundane' thing you look forward to most?",
        "What part of your 'story' do you most want our (current or future) children to understand?",
        "If you could be remembered for just one act of kindness, what would it be?"
    ]
}

# --- 3. UI & THEME (The Fixed Heart Background) ---
st.set_page_config(page_title="Our Story Vault", page_icon="❤️")

st.markdown("""
    <style>
    /* 1. The Main Background with Visible Hearts */
    .stApp {
        background-color: #fff0f5;
        background-image:  box-shadow(inset 0 0 0 2000px rgba(255, 240, 245, 0.3)); /* Tint */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cpath fill='%23b91c1c' fill-opacity='0.15' d='M40 25 C 35 10, 15 15, 15 30 C 15 45, 40 65, 40 65 C 40 65, 65 45, 65 30 C 65 15, 45 10, 40 25 Z'/%3E%3C/svg%3E");
        background-repeat: repeat;
    }

    /* 2. Target the 'Your entry' label and input text to be RED */
    .stTextArea label p {
        color: #b91c1c !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }

    .stTextArea textarea {
        color: #b91c1c !important;
        font-family: 'Georgia', serif !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
    }

    /* 3. General Polish */
    h1 { color: #b91c1c !important; font-family: 'Georgia', serif; text-align: center; }
    h3 { color: #991b1b !important; text-align: center; font-style: italic; }

    .stButton>button { 
        background-color: #b91c1c !important; color: white !important; 
        border-radius: 25px !important; width: 100%; font-weight: bold;
    }

    /* Center the question text */
    [data-testid="stMarkdownContainer"] h3 {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP CONTENT ---
st.title("Our Story Vault")
st.subheader("For an everlasting Noomie-Moonoo love")
st.markdown("---")

col1, col2 = st.columns([1, 1.5])
with col1:
    category = st.selectbox("Choose a Theme:", list(QUESTIONS.keys()))
with col2:
    question = st.selectbox("Pick a Prompt:", QUESTIONS[category])

st.markdown(f"### 🖋️ {question}")

# This is where the red text magic happens
story_text = st.text_area("Your entry:", placeholder="What does Noomie's heart say...", height=300)

# --- 5. BACKEND (EMAIL LOGIC) ---
if st.button("🎁 Seal this Memory"):
    if not story_text.strip():
        st.error("Please write a little something first! ❤️")
    else:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            msg['Subject'] = f"Anniversary Story: {question}"
            msg.attach(MIMEText(f"Prompt: {question}\n\n{story_text}", 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()

            st.success("✅ Perfectly sent! Your story is safe in the vault.")
            st.balloons()
        except Exception as e:
            st.error(f"Something went wrong. Error: {e}")