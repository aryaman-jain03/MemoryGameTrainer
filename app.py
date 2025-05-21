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

    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #f1f1f1;
    }
    .stApp {
        background: transparent;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.4);
        max-width: 600px;
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
        background: rgba(255, 255, 255, 0.1);
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
        background: rgba(255, 255, 255, 0.15);
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

# Initialize session state variables
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
    st.session_state.sequence_type = "Numbers"  # default
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Display sequence with delay
def display_sequence(seq):
    st.session_state.sequence_shown = True
    placeholder = st.empty()
    # Show sequence as spaced string
    placeholder.markdown(f"<div class='sequence-display'>{'   '.join(seq)}</div>", unsafe_allow_html=True)
    # Show for 2 seconds per item
    time.sleep(len(seq) * 1.8)
    # Clear display
    placeholder.empty()
    st.session_state.sequence_shown = False
    st.session_state.input_phase = True

# Reset the game state
def reset_game():
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.sequence = []
    st.session_state.input_phase = False
    st.session_state.sequence_shown = False
    st.session_state.feedback = ""

def main():
    st.title("🧠 Memory Game Trainer")
    st.write("Train your memory by memorizing sequences! The sequence will get longer each level. Good luck! 🍀")

    # Sidebar for settings
    st.sidebar.header("Settings")
    seq_type = st.sidebar.radio("Choose sequence type:", ("Numbers", "Words"))
    st.session_state.sequence_type = seq_type

    st.sidebar.markdown("---")
    st.sidebar.markdown("Created with ❤️ by Your Assistant")
    st.sidebar.markdown("[Source code](https://github.com/)")  # Add your repo's link here

    # Show current score and level
    st.markdown(f"<div class='scoreboard'>Level: {st.session_state.level} | Score: {st.session_state.score}</div>", unsafe_allow_html=True)
    
    # Game logic
    if not st.session_state.input_phase and not st.session_state.sequence_shown:
        # Generate new sequence
        st.session_state.sequence = generate_sequence(st.session_state.level, st.session_state.sequence_type)
        st.session_state.feedback = ""
        display_sequence(st.session_state.sequence)
    
    # When in input phase: show input box for user to type the sequence
    if st.session_state.input_phase:
        user_input = st.text_input(
            "Enter the sequence separated by spaces:",
            placeholder="Type your sequence here",
            key="user_input",
            max_chars=150,
        )

        submit_btn = st.button("Submit")

        if submit_btn:
            # Normalize input: split by spaces or commas, make lowercase
            entered = user_input.strip().lower().replace(",", " ").split()
            original = [e.lower() for e in st.session_state.sequence]

            if entered == original:
                st.session_state.score += 10 * st.session_state.level
                st.session_state.level += 1
                st.session_state.input_phase = False
                st.session_state.feedback = "🎉 Correct! Get ready for the next sequence."
                # Automatically move to next level after short delay
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.session_state.feedback = f"❌ Incorrect. The correct sequence was: {' '.join(st.session_state.sequence)}"
                st.session_state.input_phase = False
                st.session_state.level = 1
                st.session_state.score = 0

    # Show feedback message
    if st.session_state.feedback:
        st.markdown(f"**{st.session_state.feedback}**")

    # Restart button
    if st.button("🔄 Restart Game"):
        reset_game()
        st.experimental_rerun()

    # Help/Instructions toggler
    with st.expander("How to Play 🕹️"):
        st.write(
            """
            1. A sequence of numbers or words will be shown briefly.
            2. Memorize the sequence.
            3. After it disappears, type the sequence exactly as shown, separated by spaces.
            4. Press Submit to check your answer.
            5. If correct, the game goes to the next round with a longer sequence.
            6. If incorrect, your score resets and you start over.
            7. Have fun training your brain! 🧠✨
            """
        )

    # Footer text
    st.markdown("<div class='footer'>Memory Game Trainer — Built with Streamlit</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
