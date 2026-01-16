Graphical Based Reasoning project:

This project explores a simple graph-based reasoning system inspired by thinking about neurons as graphical units 
working together in the brain as one network.

Each position in a numerical sequence is assigned a node in a graph. Known values are fixed anchors, while unknown 
values represented as blanks, are assigned symbolic nodes. Reasoning emerges through local propogation of nodes 
through their neighbors and a final symbolic linear interpolar inference step.

The goal is not preformance, but to explore graphical-based reasoning.

How to Run:
    1. clone the repo: git clone https://github.com/Nervaahk/graph-reasoning-network.git
       move to directory: cd graph-reasoning-network
       2. Create the Virtual Env:
       python -m venv venv
       (Linux) source venv/bin/activate
       (Windows) venv\Scripts\activate.bat
       pip install -r requirements.txt
       3. Run the Network:
       python graphicalnetwork.py

    Example input and output:
    input: 1, 2, 3, 4, _, 6, 7
    output: 1, 2, 3, 4, 5, 6, 7

_Important Note on Authorship:
AI tools were used extensively during this project to assist with implementation and coding. The architecture,
reasoning approach, and project direction were designed conceptualy by me however.
This project is intended as a learning and exploration exercise.

Why this project exists:
I had one question: If neurons form structured networks in the brain, can they be represented mathematically, more
specfically graphically? If so, what kind of computation and reasoning can arrive from such as structure?

Status:
Early experimentation prototpye
