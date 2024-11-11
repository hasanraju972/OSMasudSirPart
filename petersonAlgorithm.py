import tkinter as tk
from tkinter import ttk
import time
flag = [False, False]  # Flags for process 0 and process 1
turn = 0               # Variable to indicate whose turn it is

def peterson_algorithm_0(process_label, status_label):
    global flag, turn

    # Entering the critical section
    status_label.config(text="Process 0: Entering", foreground="blue")
    flag[0] = True
    turn = 1
    while flag[1] and turn == 1:
        status_label.config(text="Process 0: Waiting", foreground="orange")
        process_label.config(background="orange")
        root.update()
        time.sleep(1)  # Simulate waiting

    # Critical section
    status_label.config(text="Process 0: In Critical Section", foreground="green")
    process_label.config(background="green")
    root.update()
    time.sleep(2)  # Simulate time in critical section

    # Exiting the critical section
    status_label.config(text="Process 0: Exiting", foreground="purple")
    process_label.config(background="purple")
    root.update()
    time.sleep(1)

    flag[0] = False
    status_label.config(text="Process 0: Non-Critical Section", foreground="black")
    process_label.config(background="white")
    root.update()

# Peterson's Algorithm for process 1
def peterson_algorithm_1(process_label, status_label):
    global flag, turn

    # Entering the critical section
    status_label.config(text="Process 1: Entering", foreground="blue")
    flag[1] = True
    turn = 0
    while flag[0] and turn == 0:
        status_label.config(text="Process 1: Waiting", foreground="orange")
        process_label.config(background="orange")
        root.update()
        time.sleep(1)  # Simulate waiting

    # Critical section
    status_label.config(text="Process 1: In Critical Section", foreground="green")
    process_label.config(background="green")
    root.update()
    time.sleep(2)  # Simulate time in critical section

    # Exiting the critical section
    status_label.config(text="Process 1: Exiting", foreground="purple")
    process_label.config(background="purple")
    root.update()
    time.sleep(1)

    flag[1] = False
    status_label.config(text="Process 1: Non-Critical Section", foreground="black")
    process_label.config(background="white")
    root.update()

# Run the Peterson's Algorithm for both processes
def run_simulation():
    # Reset the process labels to their initial state
    process_label_0.config(background="white")
    process_label_1.config(background="white")
    status_label_0.config(text="Process 0: Non-Critical Section", foreground="black")
    status_label_1.config(text="Process 1: Non-Critical Section", foreground="black")
    root.update()

    # Start the simulation
    peterson_algorithm_0(process_label_0, status_label_0)
    peterson_algorithm_1(process_label_1, status_label_1)

# GUI setup and logic
root = tk.Tk()
root.title("Peterson Algorithm Simulation")

# Process 0 frame
frame_0 = ttk.Frame(root)
frame_0.pack(padx=10, pady=10)

process_label_0 = tk.Label(frame_0, text="Process 0", background="white", width=20, height=5)
process_label_0.pack(pady=10)

status_label_0 = ttk.Label(frame_0, text="Process 0: Non-Critical Section", foreground="black")
status_label_0.pack(pady=5)

# Process 1 frame
frame_1 = ttk.Frame(root)
frame_1.pack(padx=10, pady=10)

process_label_1 = tk.Label(frame_1, text="Process 1", background="white", width=20, height=5)
process_label_1.pack(pady=10)

status_label_1 = ttk.Label(frame_1, text="Process 1: Non-Critical Section", foreground="black")
status_label_1.pack(pady=5)

# Start button
start_button = ttk.Button(root, text="Start Simulation", command=run_simulation)
start_button.pack(pady=20)

# Run the GUI event loop
root.mainloop()
