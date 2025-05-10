import openai
import streamlit as st

openai.api_key = st.secrets.get("openai_api_key")
clue = st.secrets.get("clue")

# --- PAGE SETUP ---
st.set_page_config(page_title="SPELLETJES MASTER✨", page_icon="🌍", layout="wide")

# --- AUDIO PLAYBACK CONTROL ---
if 'audio_playing' not in st.session_state:
    st.session_state.audio_playing = True  # Start with audio playing by default

audio_url = "https://raw.githubusercontent.com/aapies/Verniek/main/06%20Uchida's%20Theme.mp3"

# Define the button label based on audio state
if st.session_state.audio_playing:
    button_label = 'Pause Theme Music'
else:
    button_label = 'Play Theme Music'

# Button to toggle play/pause
if st.button(button_label):
    st.session_state.audio_playing = not st.session_state.audio_playing

# Display the audio player and start the audio immediately (autoplay) when audio is playing
if st.session_state.audio_playing:
    st.markdown(f"""
        <audio id="audio_player" autoplay>
            <source src="{audio_url}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        <script>
            // Autoplay when the page loads
            document.getElementById('audio_player').play();
        </script>
    """, unsafe_allow_html=True)
else:
    # Pause the audio using JavaScript when paused
    st.markdown("""
        <script>
            document.getElementById('audio_player').pause();
        </script>
    """, unsafe_allow_html=True)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 10px;
        }
        .tagline {
            text-align: center;
            font-size: 20px;
            color: #555;
            margin-bottom: 20px;
        }
        .custom-box {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 15px;
            border-left: 5px solid #1f77b4;
            margin-bottom: 10px;
        }
        .user-msg { color: #1a5276; font-weight: bold; }
        .ai-msg { color: #117864; font-style: italic; }
        .caption { text-align: center; font-size: 16px; color: #444; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)


# --- LAYOUT ---
left, center, right = st.columns([1.2, 2.5, 1.2])

# --- LEFT COLUMN ---
with left:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/Football_%28soccer_ball%29.svg", use_container_width=True)
    st.markdown('<div class="caption">Football vibes ⚽</div>', unsafe_allow_html=True)

    st.image("https://upload.wikimedia.org/wikipedia/commons/5/57/Imagen_de_los_canales_conc%C3%A9ntricos_en_%C3%81msterdam.png", use_container_width=True)
    st.markdown('<div class="caption">Greetings from Amsterdam 🇳🇱</div>', unsafe_allow_html=True)

# --- CENTER COLUMN ---
with center:
    st.markdown('<div class="title-container">⚽ WELKOM MEIDEN ⚽</div>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">IT\'S A BOYS WORLD</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Antwoord mijn vragen goed, en vind geluk...</p>', unsafe_allow_html=True)


    # --- SESSION STATE ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"Spreek alleen in het nederlands. Je gaat 4 vragen stellen aan wat meiden. De vragen met antwoorden zijn:" 
"1. Wat is Bauke’s Japanse bijnaam? (biisuke)"
"2. Wie is Joel’s main met super smash melee. (Luigi)"
"3. Met welke zangroep heeft Bauke in 2004 een reclame opgenomen voor C&A? (CH!PZ)"
"4. Wat is Joel’s lievelingsstraat in Utrecht (Wittevrouwensingel)"
"Stel een vraag, en ga pas door naar de volgende vraag als er een goed antwoord wordt gegeven. Felicteer ze wanneer ze een vraag goed hebben, en trootst ze als ze het niet goed hebben. Noem ze meiden of gurls en dat soort termen. Geef nooit het antwoord zelf, ze moeten dit zelf raden. Je mag wel hele moeilijke hints geven. Als het ze niet lukt, kan je iets zeggen van, misschien weten jullie het niet, maar anderen wel... Wanneer ze alle 4 de vragen hebben beantwoord hebben, krijgen ze de volgende zin: 'Gefeliciteerd, jullie hebben alle vragen goed beantwoord! Hier is jullie volgende hint: {clue}'"}
        ]
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    # --- DISPLAY CHAT ---
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='custom-box user-msg'>👤 You: {msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='custom-box ai-msg'>🤖 AI: {msg['content']}</div>", unsafe_allow_html=True)

    # --- TEXT INPUT & SUBMIT ---
    st.session_state.input_text = st.text_area("✍️ Enter your message below:", st.session_state.input_text)

    if st.button("💬 Submit"):
        user_input = st.session_state.input_text.strip()
        if user_input:
            with st.spinner("⚙️ Generating response..."):
                try:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=st.session_state.messages
                    )
                    response_text = response.choices[0].message["content"].strip()
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    st.session_state.input_text = ""  # Clear input
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a message before submitting.")

    # --- CLEAR CHAT BUTTON ---
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": f"Spreek alleen in het nederlands. Je gaat 4 vragen stellen aan wat meiden. De vragen met antwoorden zijn:"
"1. Wat is Bauke’s Japanse bijnaam? (biisuke)"
"2. Wie is Joel’s main met super smash melee. (Luigi)"
"3. Met welke zangroep heeft Bauke in 2004 een reclame opgenomen voor C&A? (CH!PZ)"
"4. Wat is Joel’s lievelingsstraat in Utrecht (Wittevrouwensingel)"
"Stel een vraag, en ga pas door naar de volgende vraag als er een goed antwoord wordt gegeven. Felicteer ze wanneer ze een vraag goed hebben, en trootst ze als ze het niet goed hebben. Noem ze meiden of gurls en dat soort termen. Geef nooit het antwoord zelf, ze moeten dit zelf raden. Je mag wel hele moeilijke hints geven. Als het ze niet lukt, kan je iets zeggen van, misschien weten jullie het niet, maar anderen wel... Wanneer ze alle 4 de vragen hebben beantwoord hebben, krijgen ze de volgende zin: 'Gefeliciteerd, jullie hebben alle vragen goed beantwoord! Hier is jullie volgende hint: {clue}'"}
        ]
        st.session_state.input_text = ""
        st.rerun()

# --- RIGHT COLUMN ---
with right:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c5/Ludo_Pieces.JPG", use_container_width=True)
    st.markdown('<div class="caption">Board game strategies ♟️</div>', unsafe_allow_html=True)

    st.image("https://upload.wikimedia.org/wikipedia/commons/b/be/Marilyn_Monroe_Niagara.png", use_container_width=True)
    st.markdown('<div class="caption">Blond is a lifestyle 💇‍♀️</div>', unsafe_allow_html=True)









