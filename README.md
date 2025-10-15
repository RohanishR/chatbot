# Al-Chatbot-Logic-Verifier-using-TOC
🤖 PDA Chatbot Logic Verifier
An interactive web application that uses a Pushdown Automaton (PDA) to verify the logical consistency of a chatbot's conversation flow. This project serves as a practical demonstration of how formal language theory can be applied to build more robust and predictable conversational AI.

📋 Table of Contents
About The Project

Key Features

Getting Started

Prerequisites

Installation & Running

How It Works

The PDA Model

The Pizza Bot Logic

Built With

License

📖 About The Project
Chatbots, especially task-oriented ones, must guide users through a specific sequence of steps. If a user tries to perform an action out of order (e.g., providing payment details before selecting an item), the conversation becomes illogical and fails.

This project tackles that problem by using a Pushdown Automaton—a computational model that is perfect for recognizing context-sensitive grammars. We model the "correct" conversation as a formal language and use the PDA to check if a user's sequence of commands belongs to that language.

The Pizza Bot 🍕 example demonstrates this by enforcing the logical steps of ordering a pizza: you must start an order before adding a pizza, and you can only pay once the order is complete.

✨ Key Features
Interactive Simulation: Enter a sequence of commands and see the PDA process it in real-time.

State Diagram Visualization: A clear diagram shows the possible states and transitions of the PDA.

Step-by-Step Logging: A detailed table logs each step of the simulation, showing the input, the state change, and the stack's contents.

Pre-loaded Examples: One-click buttons to test both valid (✅ Accepted) and invalid (❌ Rejected) conversation flows.

Clear Pass/Fail Verdict: The application gives a definitive "Accepted" or "Rejected" result for any given input sequence.

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
You need to have Python 3.8 or newer installed on your system.

Python 3.8+

pip (Python package installer)

Installation & Running
Clone the repository:

git clone [https://github.com/your-username/pda-chatbot-verifier.git](https://github.com/your-username/pda-chatbot-verifier.git)
cd pda-chatbot-verifier

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:

pip install -r requirements.txt

(If you don't have a requirements.txt file, create one with the content streamlit and pandas)

Run the Streamlit application:

streamlit run pda_app.py

Your web browser should automatically open a new tab with the running application.

🔧 How It Works
The PDA Model
A Pushdown Automaton (PDA) is essentially a Finite Automaton (FA) with an added component: a stack. This stack provides a memory that allows the PDA to handle more complex, context-sensitive languages.

States: Represent the current stage of the conversation (e.g., q_start, q_ordering).

Input Alphabet: The set of valid commands the user can issue (e.g., order, pizza).

Stack: Acts as a memory. We push symbols onto the stack to remember the context and pop them when that context is resolved.

Transition Function: The core logic. It's a set of rules that dictates: "Given the current state, the user's input, and the symbol on top of the stack, what should the new state be, and what should I do with the stack?"

The Pizza Bot Logic
The logic of our Pizza Bot is defined by the following transition rules:

Current State

User Input

Stack Top

New State

Action on Stack

Description

q_start

order

Z0

q_ordering

Push O

Starts the order.

q_ordering

pizza

O

q_ordering

Push P

Adds a pizza to the order.

q_ordering

toppings

P

q_ordering

Push T

Adds toppings to the pizza.

q_ordering

done

T

q_ordering

Pop T

Finishes adding toppings.

q_ordering

done

P

q_ordering

Pop P

Finishes with the current pizza.

q_ordering

pay

O

q_done

Pop O

Completes the order to pay.

The conversation is Accepted only if it ends in a final state (q_done). If a user's command sequence leads to a situation not defined by these rules, the PDA gets "stuck" and the sequence is Rejected.

🛠️ Built With
Python - The core programming language.

Streamlit - For building the interactive web UI.

Pandas - For displaying the simulation log in a clean table.

Graphviz - To render the state diagram.

📄 License
Distributed under the MIT License. See LICENSE for more information.
