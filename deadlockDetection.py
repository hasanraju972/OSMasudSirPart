import tkinter as tk
from tkinter import messagebox

# Function to simulate deadlock detection
def detect_deadlock():
    n = int(entry_processes.get())  # Number of processes
    m = int(entry_resources.get())  # Number of resources

    allocation = []
    request = []
    available = []

    try:
        # Get Allocation Matrix
        for i in range(n):
            row = list(map(int, entries_allocation[i].get().split()))
            allocation.append(row)

        # Get Request Matrix
        for i in range(n):
            row = list(map(int, entries_request[i].get().split()))
            request.append(row)

        # Get Available Resources
        available = list(map(int, entry_available.get().split()))

        # Deadlock detection logic
        finish = [0] * n
        work = available[:]
        safe = False

        while True:
            safe = False
            for i in range(n):
                if finish[i] == 0:
                    can_allocate = True
                    for j in range(m):
                        if request[i][j] > work[j]:
                            can_allocate = False
                            break
                    if can_allocate:
                        for j in range(m):
                            work[j] += allocation[i][j]
                        finish[i] = 1
                        safe = True

            if not safe:
                break

        deadlocked_processes = [i for i in range(n) if finish[i] == 0]

        if len(deadlocked_processes) == 0:
            messagebox.showinfo("Result", "No Deadlock Detected.")
        else:
            messagebox.showwarning("Deadlock Detected", f"Deadlocked Processes: {', '.join(map(str, deadlocked_processes))}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid matrix data!")

# Create the GUI window
window = tk.Tk()
window.title("Deadlock Detection Simulator")

# Number of Processes and Resources
tk.Label(window, text="Number of Processes:").grid(row=0, column=0)
entry_processes = tk.Entry(window)
entry_processes.grid(row=0, column=1)

tk.Label(window, text="Number of Resources:").grid(row=1, column=0)
entry_resources = tk.Entry(window)
entry_resources.grid(row=1, column=1)

# Allocate space for Matrix input fields
tk.Label(window, text="Allocation Matrix (space-separated):").grid(row=2, column=0, columnspan=2)
entries_allocation = []

for i in range(5):  # Assuming max 5 processes
    entry = tk.Entry(window, width=30)
    entry.grid(row=3+i, column=0, columnspan=2)
    entries_allocation.append(entry)

tk.Label(window, text="Request Matrix (space-separated):").grid(row=8, column=0, columnspan=2)
entries_request = []

for i in range(5):  # Assuming max 5 processes
    entry = tk.Entry(window, width=30)
    entry.grid(row=9+i, column=0, columnspan=2)
    entries_request.append(entry)

# Available Resources
tk.Label(window, text="Available Resources (space-separated):").grid(row=14, column=0)
entry_available = tk.Entry(window)
entry_available.grid(row=14, column=1)

# Button to Trigger Deadlock Detection
tk.Button(window, text="Detect Deadlock", command=detect_deadlock).grid(row=15, column=0, columnspan=2)

# Start the GUI loop
window.mainloop()
