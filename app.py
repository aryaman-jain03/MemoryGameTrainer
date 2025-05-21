import streamlit as st
import time
from utils import generate_sequence

# Set page config
st.set_page_config(
    page_title="🧠 Memory Game Trainer",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
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

    .stButton>button:hover {
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
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state variables if not present
if "sequence" not in st.session_state:
    st.session_state.sequence = []
if "level" not in st.session_state:
    st.session_state.level = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "input_phase" not in st.session_state:
    st.session_state.input_phase = False
if "sequence_shown" not in st.session_state:
    st.session_state.sequence_shown = False
if "sequence_type" not in st.session_state:
    st.session_state.sequence_type = "Numbers"
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "display_step" not in st.session_state:
    st.session_state.display_step = 0
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Reset game state
def reset_game():
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.sequence = []
    st.session_state.input_phase = False
    st.session_state.sequence_shown = False
    st.session_state.feedback = ""
    st.session_state.display_step = 0
    st.session_state.user_input = ""

# Async display sequence with rerun, showing countdown and sequence progressively
def display_sequence(seq):
    # Step 0-2: countdown 3..2..1
    if st.session_state.display_step < 3:
        st.markdown(f"<h4>Memorize in {3 - st.session_state.display_step}...</h4>", unsafe_allow_html=True)
        time.sleep(1)
        st.session_state.display_step += 1
        st.experimental_rerun()

    # Step 3: show the sequence for a duration based on length
    elif st.session_state.display_step == 3:
        st.markdown(f"<div class='sequence-display'>{'   '.join(seq)}</div>", unsafe_allow_html=True)
        time.sleep(len(seq) * 1.5)
        st.session_state.display_step += 1
        st.experimental_rerun()

    # Step 4: done showing sequence, switch to input phase
    else:
        st.session_state.display_step = 0
        st.session_state.sequence_shown = False
        st.session_state.input_phase = True
        st.session_state.user_input = ""  # clear input box for new level

def main():
    st.title("🧠 Memory Game Trainer")

    # Instructions
    with st.expander("📘 How to Play", expanded=True):
        st.markdown("""
        1️⃣ A sequence of **numbers** or **words** will appear after a short countdown.  
        2️⃣ **Memorize** the sequence quickly!  
        3️⃣ After it disappears, **enter it exactly** in the text box below.  
        4️⃣ Press **Submit** to check your answer.  
        5️⃣ Correct? 🎉 Your score increases and the game gets harder.  
        6️⃣ Wrong? ❌ Game resets. Try again and beat your best! 🧠✨
        """)

    st.sidebar.header("Settings")
    seq_type = st.sidebar.radio("Choose sequence type:", ("Numbers", "Words"))
    st.session_state.sequence_type = seq_type

    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ by Your Assistant")
    st.sidebar.markdown("[Source Code](https://github.com/your-repo)")

    # Scoreboard
    st.markdown(
        f"<div class='scoreboard'>Level: {st.session_state.level} | Score: {st.session_state.score}</div>", 
        unsafe_allow_html=True
    )

    # Game loop: generate and display sequence if not in input phase or sequence shown
    if not st.session_state.input_phase and not st.session_state.sequence_shown:
        st.session_state.sequence = generate_sequence(st.session_state.level, st.session_state.sequence_type)
        st.session_state.feedback = ""
        st.session_state.sequence_shown = True
        display_sequence(st.session_state.sequence)

    # Show input box only when input phase is active
    if st.session_state.input_phase:
        user_input = st.text_input(
            "Enter the sequence (space-separated):",
            placeholder="Type your sequence here...",
            key="user_input",
            value=st.session_state.user_input,
            max_chars=150,
        )
        st.session_state.user_input = user_input  # sync session state input

        if st.button("✅ Submit"):
            entered = user_input.strip().lower().replace(",", " ").split()
            correct = [e.lower() for e in st.session_state.sequence]

            if entered == correct:
                st.session_state.score += 10 * st.session_state.level
                st.session_state.level += 1
                st.session_state.input_phase = False
                st.session_state.feedback = "🎉 Correct! Leveling up..."
                time.sleep(1.2)
                st.experimental_rerun()
            else:
                st.session_state.feedback = f"❌ Incorrect. Correct sequence was: {' '.join(correct)}"
                st.session_state.input_phase = False
                st.session_state.level = 1
                st.session_state.score = 0
                time.sleep(1.5)
                st.experimental_rerun()

    else:
        st.write("⏳ Please wait, sequence is being shown...")

    # Show feedback message if any
    if st.session_state.feedback:
        st.markdown(f"**{st.session_state.feedback}**")

    # Restart game button
    if st.button("🔄 Restart Game"):
        reset_game()
        st.experimental_rerun()

    st.markdown("<div class='footer'>Memory Game Trainer — Built with Streamlit</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
