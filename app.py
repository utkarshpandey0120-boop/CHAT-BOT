import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="BAGESHWAR DHAM", page_icon="🙏", layout="centered")

# 2. API KEY (Yahan apni key paste karein)
API_KEY = "PASTE_YOUR_KEY_HERE" 

# 3. STYLING & BACKGROUND (Full App Design)
# Background image link: Aap Maharaj-ji ki photo ka link yahan badal sakte hain
BG_URL = "https://images.unsplash.com/photo-1620206343767-7da98185edd4?q=80&w=2000"

st.markdown(f"""
    <style>
    /* Background Image setup */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Chat Box styling */
    [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px;
        color: #1e1e1e !important;
    }}
    /* Text Color */
    h1, h3, p {{
        color: #FFD700 !important;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. APP HEADER
st.title("🙏 BAGESHWAR DHAM")
st.markdown("### बागेश्वर बालाजी की महिma - आपकी हर समस्या का समाधान")

# 5. AI ENGINE INITIALIZATION
if API_KEY == "PASTE_YOUR_KEY_HERE":
    st.error("❌ Error: Aapne API Key nahi daali hai. Code ki line number 10 mein apni key paste karein.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    
    # System Instruction: Isse AI Maharaj-ji ki tarah baat karega
    system_prompt = (
        "You are Bageshwar Dham Sarkar (Pandit Dhirendra Krishna Shastri). "
        "Start every answer with 'Sitaram'. Talk in Hinglish (Hindi + English). "
        "Provide spiritual solutions, motivate people to have faith in Balaji, "
        "and behave like a divine guide. Keep answers quick and effective."
    )
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Fastest model available
        system_instruction=system_prompt
    )

    # 6. CHAT MEMORY (Pichli baatein yaad rakhne ke liye)
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # Display Chat History
    for message in st.session_state.chat.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # 7. CHAT INPUT & RESPONSE
    if user_input := st.chat_input("अपनी समस्या यहाँ लिखें (Write your problem)..."):
        # Display User Question
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI Answer
        with st.chat_message("assistant"):
            with st.spinner("Balaji is guiding..."):
                try:
                    response = st.session_state.chat.send_message(user_input)
                    st.markdown(response.text)
                except Exception as api_err:
                    st.error(f"API Error: {api_err}")

except Exception as main_err:
    st.error(f"Main App Error: {main_err}")
