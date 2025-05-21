import streamlit as st
import time
from utils import generate_sequence

# Set page config
st.set_page_config(
    page_title="Memory Game Trainer",
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

    /* Styles for the "pop-up" */
    .popup-container {
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
        background-color: #1a1a2e; /* Darker background for pop-up */
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
        text-align: center;
        max-width: 400px;
        color: #f1f1f1;
        font-size: 1.1rem;
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

    .popup-content .stButton>button {
        width: auto; /* Override full width for pop-up button */
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state defaults
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
if "user_input_widget" not in st.session_state:
    st.session_state.user_input_widget = ""
if "game_started" not in st.session_state:
    st.session_state.game_started = False
# NEW: For Game Over Pop-up
if "show_game_over_popup" not in st.session_state:
    st.session_state.show_game_over_popup = False
if "final_score" not in st.session_state:
    st.session_state.final_score = 0


# --- Callback Functions for Button Actions ---

# Function to handle game logic after submission
def handle_submit():
    # Get the raw user input
    user_raw_input = st.session_state.user_input_widget.strip()
    
    # Get the correct sequence (always a list of strings), ensuring consistency
    correct_sequence = [str(item).lower() for item in st.session_state.sequence] 
    
    entered_sequence = []
    if st.session_state.sequence_type == "Numbers":
        entered_sequence = list(user_raw_input) 
    else: # For Words
        entered_sequence = user_raw_input.lower().replace(",", " ").split() 

    # Compare the entered sequence with the correct sequence
    if entered_sequence == correct_sequence:
        st.session_state.score += 10 * st.session_state.level 
        st.session_state.level += 1 
        st.session_state.feedback = "Correct! Leveling up..." 
    else:
        # INCORRECT ANSWER: Show pop-up instead of immediate reset
        st.session_state.feedback = f"Incorrect. Correct sequence was: {' '.join(correct_sequence)}" 
        st.session_state.final_score = st.session_state.score # Store current score before eventual reset
        st.session_state.show_game_over_popup = True # Trigger the pop-up
        # Do NOT reset score/level here; it happens in start_new_game_after_popup

    st.session_state.input_phase = False # End input phase 
    st.session_state.user_input_widget = "" # Clear the input field 
    time.sleep(1.2) # A brief pause for feedback to be seen before next rerun 

# Callback to start the game
def start_game_callback():
    st.session_state.game_started = True
    # Reset other game state variables to ensure a fresh start
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.sequence = [] # Will be generated in main loop
    st.session_state.input_phase = False
    st.session_state.sequence_shown = False
    st.session_state.feedback = ""
    st.session_state.display_step = 0
    st.session_state.user_input_widget = ""
    st.session_state.show_game_over_popup = False # Ensure pop-up is hidden when starting
    # st.rerun() # Not strictly necessary as the main loop will run immediately after

# NEW: Callback for the "Start Again" button in the pop-up
def start_new_game_after_popup():
    reset_game_callback() # Use existing reset logic
    start_game_callback() # Start a new game immediately

# Reset state function - Now used as an on_click callback
def reset_game_callback():
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.sequence = []
    st.session_state.input_phase = False
    st.session_state.sequence_shown = False
    st.session_state.feedback = ""
    st.session_state.display_step = 0
    st.session_state.user_input_widget = "" # Clear the input widget content
    st.session_state.game_started = False # Set game_started to False on full reset
    st.session_state.show_game_over_popup = False # Ensure pop-up is hidden on reset

# Display sequence based on display_step
def display_sequence(seq):
    step = st.session_state.display_step

    if step < 3:
        return f"Memorize in {3 - step}..."
    elif step == 3:
        return '   '.join(seq)
    else:
        return None

def main():
    st.title("🧠 Memory Game Trainer")

    # Instructions
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
    seq_type = st.sidebar.radio("Choose sequence type:", ("Numbers", "Words"), key="seq_type_radio")
    st.session_state.sequence_type = seq_type

    st.sidebar.markdown("---")
    st.sidebar.markdown("Made by Aryaman Jain")
    st.sidebar.markdown("[Source Code](https://github.com/aryaman-jain03/MemoryGameTrainer)")

    # Scoreboard
    st.markdown(f"<div class='scoreboard'>Level: {st.session_state.level} | Score: {st.session_state.score}</div>", unsafe_allow_html=True)

    # --- Game Over Pop-up (Conditionally rendered) ---
    if st.session_state.show_game_over_popup:
        # Use st.container to create a div for the pop-up
        with st.container():
            st.markdown(
                f"""
                <div class="popup-container">
                    <div class="popup-content">
                        <h3>Game Over!</h3>
                        <p>Incorrect Answer.</p>
                        <p>Your Final Score: **{st.session_state.final_score}**</p>
                        <div class="stButton">
                            <button onclick="window.parent.document.querySelector('[data-testid=stSidebar]').style.display='none'; window.parent.document.querySelector('[data-testid=stExpanderSimple]').click();" style="width: auto;">Start A New Game</button>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # The actual button to trigger the game restart (hidden from direct view,
            # but called by the HTML button's JS)
            st.button("Start A New Game Trigger", on_click=start_new_game_after_popup, key="popup_start_again_btn")
            # Hide this button visually, as the HTML button will trigger the callback
            st.markdown("<style>#popup_start_again_btn { display: none; }</style>", unsafe_allow_html=True)
            # IMPORTANT: Rerunning here to make sure the popup appears and then disappears when the button is clicked
            # st.rerun() # This causes a continuous rerun if the popup is visible, moved the start_new_game_after_popup to handle it.


    # --- Main Game Flow (Only if pop-up is not visible) ---
    if not st.session_state.show_game_over_popup:
        if not st.session_state.game_started:
            st.write("Welcome! Select your sequence type from the sidebar and click 'Start Game' to begin.")
            st.button("Start Game", on_click=start_game_callback)
        else:
            # Only proceed with game logic if game has started
            if not st.session_state.input_phase and not st.session_state.sequence_shown:
                st.session_state.sequence = generate_sequence(st.session_state.level, st.session_state.sequence_type)
                st.session_state.feedback = ""
                st.session_state.sequence_shown = True
                st.session_state.display_step = 0
                st.rerun() # Trigger a rerun to start the display sequence

            # If showing sequence, handle countdown and display step-by-step
            if st.session_state.sequence_shown:
                output = display_sequence(st.session_state.sequence)
                if output is not None:
                    if st.session_state.display_step < 3:
                        st.markdown(f"<h4>{output}</h4>", unsafe_allow_html=True)
                        time.sleep(1)
                        st.session_state.display_step += 1
                        st.rerun()
                    elif st.session_state.display_step == 3:
                        st.markdown(f"<div class='sequence-display'>{output}</div>", unsafe_allow_html=True)
                        # Calculate display time based on sequence length
                        display_time = len(st.session_state.sequence) * 0.8 + 1.5 # Min 1.5 sec, then 0.8 per item
                        time.sleep(display_time)
                        st.session_state.display_step += 1
                        st.rerun()
                else:
                    # Sequence display finished, switch to input phase
                    st.session_state.sequence_shown = False
                    st.session_state.input_phase = True
                    st.session_state.display_step = 0
                    st.session_state.user_input_widget = ""  # Clear previous input for new round (important before widget rendering)
                    st.rerun() # Trigger a rerun to show the input field

            # Input phase
            if st.session_state.input_phase:
                # Adjusted placeholder text for better clarity on number input
                placeholder_text = "Type your sequence here (no spaces for numbers)" if st.session_state.sequence_type == "Numbers" else "Type your sequence here (space-separated for words)"
                
                st.text_input(
                    "Enter the sequence :",
                    value=st.session_state.user_input_widget,
                    placeholder=placeholder_text,
                    key="user_input_widget", # This key binds the input to st.session_state.user_input_widget
                    max_chars=150,
                )

                # Use on_click callback for submit button
                st.button("Submit", on_click=handle_submit)
            
            # Feedback message (only display if game has started AND no popup)
            if st.session_state.feedback and not st.session_state.show_game_over_popup:
                st.markdown(f"**{st.session_state.feedback}**")

    # Restart button (always visible)
    st.button("Restart Game", on_click=reset_game_callback)

    st.markdown("<div class='footer'>Memory Game Trainer — Built with Streamlit</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()