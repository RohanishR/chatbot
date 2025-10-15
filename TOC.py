import streamlit as st
import pandas as pd

# --- PDA Simulator Class ---
# This class encapsulates the logic of the Pushdown Automaton.
class PDASimulator:
    """
    The PDA engine. This part stays the same. It's a general machine
    that processes input based on a set of rules.
    
    Attributes:
        states (set): A set of all possible states.
        input_alphabet (set): A set of valid input symbols.
        stack_alphabet (set): A set of valid stack symbols.
        transitions (dict): The transition function of the PDA.
        start_state (str): The initial state.
        start_stack_symbol (str): The initial symbol on the stack.
        accept_states (set): A set of states that accept the input string.
    """
    def __init__(self, states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, accept_states):
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.accept_states = accept_states
        self.reset()

    def reset(self):
        """Resets the PDA to its initial configuration."""
        self.current_state = self.start_state
        self.stack = [self.start_stack_symbol]
        self.log = []

    def get_stack_visualization(self):
        """Returns a string representing the current stack for display."""
        if not self.stack:
            return "[] (Empty)"
        # Display with top on the left
        return f"[{' | '.join(self.stack)}]"

    def step(self, symbol):
        """Processes a single input symbol and updates the PDA's configuration."""
        if symbol not in self.input_alphabet:
            self.log.append({
                "Input": f"'{symbol}'",
                "Action": f"ERROR: Input not in alphabet.",
                "New State": self.current_state,
                "Stack": self.get_stack_visualization(),
                "Result": "Halted 🛑"
            })
            return False

        # Peek at the top of the stack without popping
        stack_top = self.stack[0] if self.stack else None
        key = (self.current_state, symbol, stack_top)

        if key in self.transitions:
            next_state, push_symbols = self.transitions[key]
            
            # Pop from stack
            popped_symbol = self.stack.pop(0)

            # Push new symbols to the stack
            if push_symbols:
                for item in reversed(push_symbols):
                    self.stack.insert(0, item)
            
            action_desc = f"Pop '{popped_symbol}'. Push '{''.join(push_symbols) if push_symbols else 'ε'}'. "
            self.log.append({
                "Input": f"'{symbol}'",
                "Action": action_desc,
                "New State": next_state,
                "Stack": self.get_stack_visualization(),
                "Result": "Success ✔️"
            })
            self.current_state = next_state
            return True
        else:
            self.log.append({
                "Input": f"'{symbol}'",
                "Action": f"No transition for ({self.current_state}, {symbol}, {stack_top})",
                "New State": self.current_state,
                "Stack": self.get_stack_visualization(),
                "Result": "Stuck ❌"
            })
            return False

    def run(self, sequence):
        """Runs the simulation on a full sequence of input symbols."""
        self.reset()
        
        # Initial state log
        self.log.append({
            "Input": "ε (start)",
            "Action": "Initial configuration",
            "New State": self.current_state,
            "Stack": self.get_stack_visualization(),
            "Result": "Start 🚀"
        })

        for symbol in sequence:
            if not self.step(symbol):
                return "Rejected" # Halt if stuck

        # Check for acceptance at the end
        if self.current_state in self.accept_states:
            return "Accepted"
        else:
            return "Rejected"

# --- PDA Configuration ---
# This PDA models a simplified pizza ordering process.
# O = Order, P = Pizza, T = Toppings
states = {'q_start', 'q_ordering', 'q_done'}
input_alphabet = {'order', 'pizza', 'toppings', 'done', 'pay'}
stack_alphabet = {'O', 'P', 'T', 'Z0'}
start_state = 'q_start'
start_stack_symbol = 'Z0'
accept_states = {'q_done'}

# Define the NEW, SIMPLE Transition Rules for ordering a pizza
transitions = {
    # (current_state, input, stack_top): (next_state, [push_symbols])
    # Start the order
    ('q_start', 'order', 'Z0'): ('q_ordering', ['O', 'Z0']),
    # Add a pizza to the order
    ('q_ordering', 'pizza', 'O'): ('q_ordering', ['P', 'O']),
    # Add toppings to the pizza
    ('q_ordering', 'toppings', 'P'): ('q_ordering', ['T', 'P']),
    # Done adding toppings, pop 'T' to go back to the pizza level
    ('q_ordering', 'done', 'T'): ('q_ordering', []),
    # Done with the pizza, pop 'P' to go back to the order level
    ('q_ordering', 'done', 'P'): ('q_ordering', []),
    # Pay for the order, pop 'O'
    ('q_ordering', 'pay', 'O'): ('q_done', []),
}


# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="PDA Simulator", page_icon="🍕")

st.title("🤖 Pushdown Automaton (PDA) Simulator")
st.markdown("A visual tool for understanding how a PDA processes a sequence of inputs, demonstrated with a pizza ordering bot.")

# --- UI Sections ---
info, viz = st.columns([1, 1])

with info:
    st.header("What is This PDA For?")
    st.markdown(
        """
        This Pushdown Automaton models a simple, logical conversation for ordering a pizza. 
        It accepts sequences that follow a specific grammar, like `order -> pizza -> toppings -> done -> done -> pay`.

        - **Stack:** The PDA uses a stack (a last-in, first-out data structure) as its memory to track context (e.g., are we adding toppings, or are we paying?).
        - **Transitions:** It follows a set of rules to decide what to do at each step.
        - **Goal:** To end in an **accept state** (`q_done`) after reading the entire input sequence.
        """
    )
    with st.expander("Explore the Transition Rules (The PDA's Brain)"):
        st.markdown(
            """
            The rules are defined as `(Current State, Input, Stack Top) ➞ (New State, Symbols to Push)`. 
            `ε` means nothing is pushed (it's a pop operation).
            1.  **(`q_start`, 'order', 'Z0') ➞ (`q_ordering`, ['O', 'Z0'])**: Start an order, placing 'O' (order context) on the stack.
            2.  **(`q_ordering`, 'pizza', 'O') ➞ (`q_ordering`, ['P', 'O'])**: Add a pizza, requiring a 'P' (pizza context).
            3.  **(`q_ordering`, 'toppings', 'P') ➞ (`q_ordering`, ['T', 'P'])**: Add toppings, requiring a 'T' (toppings context).
            4.  **(`q_ordering`, 'done', 'T') ➞ (`q_ordering`, [])**: Finish with toppings by popping 'T'.
            5.  **(`q_ordering`, 'done', 'P') ➞ (`q_ordering`, [])**: Finish with the pizza by popping 'P'.
            6.  **(`q_ordering`, 'pay', 'O') ➞ (`q_done`, [])**: Pay for the order by popping 'O' and moving to the final state.
            """
        )

with viz:
    st.header("State Diagram")
    # DOT language for Graphviz to render the PDA diagram
    graph_definition = """
    digraph PDA {
        rankdir=LR;
        node [shape=circle];
        " " [shape=none, width=0, height=0];
        q_done [shape=doublecircle];
        
        " " -> q_start;
        q_start -> q_ordering [label="order, Z0 / OZ0"];
        q_ordering -> q_ordering [label="pizza, O / PO\\ntoppings, P / TP\\ndone, T / ε\\ndone, P / ε"];
        q_ordering -> q_done [label="pay, O / ε"];
    }
    """
    st.graphviz_chart(graph_definition)


st.header("▶️ Run the Simulation")

# --- User Input and Examples ---
input_col, examples_col = st.columns([2, 1])

with input_col:
    user_input = st.text_input(
        "Enter a command sequence (separated by spaces):", 
        "order pizza toppings done done pay"
    )

with examples_col:
    st.markdown("##### Click to try an example:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Valid: Simple"):
            st.session_state.user_input = "order pizza toppings done done pay"
        if st.button("✅ Valid: Multi-Pizza"):
            st.session_state.user_input = "order pizza done pizza toppings done done pay"
    with col2:
        if st.button("❌ Invalid: Pay Early"):
            st.session_state.user_input = "order pizza toppings pay"
        if st.button("❌ Invalid: No Order"):
            st.session_state.user_input = "pizza toppings pay"

    # This check is to make the button clicks update the text_input
    if 'user_input' in st.session_state:
        user_input = st.session_state.user_input
        # Clear it so it doesn't persist on next run
        del st.session_state['user_input']


if user_input:
    pizza_bot = PDASimulator(states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, accept_states)
    sequence = user_input.strip().lower().split()
    result = pizza_bot.run(sequence)

    st.subheader("Results")
    
    # Display final status
    if result == "Accepted":
        st.success(f"✅ String '{user_input}' is Accepted!")
    else:
        st.error(f"❌ String '{user_input}' is Rejected!")

    st.markdown("### Step-by-Step Log")
    
    # Convert log to a pandas DataFrame for better display
    log_df = pd.DataFrame(pizza_bot.log)
    log_df.index = log_df.index.rename("Step")
    st.dataframe(log_df, use_container_width=True)

else:
    st.info("Enter a sequence above and see the PDA in action!")


