import streamlit as st
import time
from utils import generate_sequence  # Ensure utils.py exists and works

import base64
import base64

def play_sound(sound_file_path):
    """Plays a sound by embedding it in HTML using base64 encoding."""
    with open(sound_file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

def play_countdown_sound():
    with open("countdown.wav", "rb") as f:
        data = f.read()
    st.audio(data, format="audio/wav", start_time=0)


# Page config
st.set_page_config(
    page_title="Memory Game Trainer",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
html, body, .stApp {
    background-color: #0e1117 !important;
    color: #f1f1f1 !important;
    font-family: 'Poppins', sans-serif;
}
.stApp {
    padding: 2rem;
    border-radius: 15px;
    max-width: 700px;
    margin: auto;
}
h1 {
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.2rem;
    color: #ffe600;
    text-shadow: 1px 1px 6px #3b0091;
}
.sequence-display {
    font-size: 1.8rem;
    letter-spacing: 0.15rem;
    text-align: center;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    user-select: none;
    color: #ffd600;
    text-shadow: 1px 1px 5px #29006d;
}
.scoreboard {
    text-align: center;
    margin: 1rem 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffdb00;
    text-shadow: 0 0 8px #b67f00;
}
.footer {
    text-align: center;
    font-size: 0.85rem;
    margin-top: 2rem;
    color: #ddddddaa;
    user-select: none;
}
.stButton>button {
    background: linear-gradient(90deg, #ffbb33, #ff8800);
    border: none;
    color: #fff;
    font-weight: 700;
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    box-shadow: 0 3px 10px rgba(255,136,0,0.7);
    transition: background 0.3s ease;
    width: 100%;
}
            /* Keep the shape and colors even when button is disabled */
.stButton>button:disabled {
    background: linear-gradient(90deg, #ffbb33, #ff8800) !important;
    color: #fff !important;
    border-radius: 50px !important;
    box-shadow: 0 3px 10px rgba(255,136,0,0.7) !important;
    opacity: 0.7;  /* Slightly faded to indicate disabled, adjust if needed */
    cursor: not-allowed;
}

/* Optional: style button on focus and active */
.stButton>button:focus,
.stButton>button:active {
    outline: none;
    box-shadow: 0 0 12px #ffb800cc;
    background: linear-gradient(90deg, #ff8800, #ffbb33);
    cursor: pointer;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #ff8800, #ffbb33);
    cursor: pointer;
}
            .stButton>button:hover:not(:disabled) {
    background: linear-gradient(90deg, #ff8800, #ffbb33);
    cursor: pointer;
}

.stTextInput>div>input {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    border: none;
    color: #fff;
    font-weight: 600;
    padding: 0.7rem 1rem;
    font-size: 1.1rem;
    text-align: center;
    letter-spacing: 0.05rem;
    box-shadow: 0 0 8px #ffb800aa inset;
}
.stTextInput>div>input::placeholder {
    color: #ffe066cc;
    font-style: italic;
}
/* Pop-up */
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.popup-content {
    background-color: #1a1a2e;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    text-align: center;
    max-width: 400px;
    color: #f1f1f1;
    font-size: 1.1rem;
    position: relative;
}
.popup-content h3 {
    color: #ffe600;
    margin-bottom: 15px;
}
.popup-content p {
    margin-bottom: 20px;
    font-size: 1.2rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
defaults = {
    "sequence": [],
    "level": 1,
    "score": 0,
    "input_phase": False,
    "sequence_shown": False,
    "sequence_type": "Numbers",
    "feedback": "",
    "display_step": 0,
    "user_input_widget": "",
    "game_started": False,
    "show_game_over_popup": False,
    "final_score": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Game logic handlers ---
def handle_submit():
    user_raw_input = st.session_state.user_input_widget.strip()
    correct_sequence = [str(item).lower() for item in st.session_state.sequence] 

    if st.session_state.sequence_type == "Numbers":
        entered_sequence = list(user_raw_input) 
    else:
        entered_sequence = user_raw_input.lower().replace(",", " ").split() 

    if entered_sequence == correct_sequence:
        st.session_state.score += 10 * st.session_state.level 
        st.session_state.level += 1 
        st.session_state.feedback = "Correct! Leveling up..." 
        st.session_state.input_phase = False
        st.session_state.user_input_widget = ""
        play_sound("correct.wav")  # Play correct sound
    else:
        st.session_state.feedback = f"Incorrect. Correct sequence was: {' '.join(correct_sequence)}"
        st.session_state.final_score = st.session_state.score
        st.session_state.show_game_over_popup = True
        st.session_state.input_phase = False
        st.session_state.user_input_widget = ""
        play_sound("wrong.wav")  # Play wrong sound


    st.session_state.input_phase = False # End input phase 
    st.session_state.user_input_widget = "" # Clear the input field 
    time.sleep(1.2) # A brief pause for feedback to be seen before next rerun 
 
def start_game_callback():
    reset_game_callback()
    st.session_state.game_started = True

def retry_game_callback():
    reset_game_callback()
    st.session_state.game_started = True

def close_game_over_popup():
    reset_game_callback()

def reset_game_callback():
    for k, v in defaults.items():
        st.session_state[k] = v

def display_sequence(seq):
    step = st.session_state.display_step
    if step < 3:
        return f"Memorize in {3 - step}..."
    elif step == 3:
        return '   '.join(seq)
    else:
        return None

# --- Main App ---
def main():
    st.title("🧠 Memory Game Trainer")

    with st.expander("How to Play", expanded=True):
        st.markdown("""
        1 A sequence of **numbers** or **words** will appear after a short countdown.  
        2 **Memorize** the sequence quickly!  
        3 After it disappears, **enter it exactly** in the text box below.  
        4 Press **Submit** to check your answer.  
        5 Correct? Your score increases and the game gets harder.  
        6 Wrong? Game ends, see your score, and start again!
        """)

    st.sidebar.header("Settings")
    st.session_state.sequence_type = st.sidebar.radio("Choose sequence type:", ("Numbers", "Words"), key="seq_type_radio")
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made by Aryaman Jain")
    st.sidebar.markdown("[Source Code](https://github.com/aryaman-jain03/MemoryGameTrainer)")

    st.markdown(f"<div class='scoreboard'>Level: {st.session_state.level} | Score: {st.session_state.score}</div>", unsafe_allow_html=True)

    # --- Game Over Inline Display ---
    if st.session_state.show_game_over_popup:
        st.markdown("## Game Over!")
        st.markdown("**Incorrect Answer.**")
        st.markdown(f"**Your Final Score:** `{st.session_state.final_score}`")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("↻ Retry", on_click=retry_game_callback)
        with col2:
            st.button("✖ Back to Menu", on_click=close_game_over_popup)
        return

     

    # --- Game not started ---
    if not st.session_state.game_started:
        st.write("Welcome! Select your sequence type from the sidebar and click 'Start Game' to begin.")
        st.button("Start Game", on_click=start_game_callback)
        return

    # --- Game in progress ---
    if not st.session_state.input_phase and not st.session_state.sequence_shown:
        st.session_state.sequence = generate_sequence(st.session_state.level, st.session_state.sequence_type)
        st.session_state.sequence_shown = True
        st.session_state.display_step = 0
        st.rerun()

    if st.session_state.sequence_shown:
        output = display_sequence(st.session_state.sequence)
        if output is not None:
            if st.session_state.display_step < 3:
                st.markdown(f"<h4>{output}</h4>", unsafe_allow_html=True)
                play_countdown_sound()
                st.session_state.display_step += 1
                st.rerun()
            elif st.session_state.display_step == 3:
                st.markdown(f"<div class='sequence-display'>{output}</div>", unsafe_allow_html=True)
                time.sleep(len(st.session_state.sequence) * 0.8 + 1.5)
                st.session_state.display_step += 1
                st.rerun()
        else:
            st.session_state.sequence_shown = False
            st.session_state.input_phase = True
            st.session_state.user_input_widget = ""
            st.rerun()

    if st.session_state.input_phase:
        placeholder_text = "Type your sequence here (no spaces for numbers)" if st.session_state.sequence_type == "Numbers" else "Type your sequence here (space-separated for words)"
        user_input = st.text_input(
            "Enter the sequence:",
            value=st.session_state.user_input_widget,
            placeholder=placeholder_text,
            key="temp_input_value",
            max_chars=150
        )

        def handle_submit_wrapper():
            st.session_state.user_input_widget = st.session_state.temp_input_value
            handle_submit()
            st.session_state.temp_input_value = ""  # Clear text input after submit


        st.button("Submit", on_click=handle_submit_wrapper)


    if st.session_state.feedback and not st.session_state.show_game_over_popup:
        st.markdown(f"**{st.session_state.feedback}**")

    st.button("Restart Game", on_click=reset_game_callback)
    st.markdown("<div class='footer'>Memory Game Trainer — Built with Streamlit</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()



