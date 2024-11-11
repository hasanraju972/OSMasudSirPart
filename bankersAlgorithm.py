import tkinter as tk
from tkinter import messagebox
class BankersAlgorithm:
    def __init__(self, n, r, allocation, maximum, available):
        self.n = n  # Number of processes
        self.r = r  # Number of resource types
        self.allocation = allocation  # Allocation matrix
        self.maximum = maximum  # Max matrix
        self.available = available  # Available resources
        self.need = [[0] * r for _ in range(n)]  # Need matrix
        self.calculate_need()

    def calculate_need(self):
        for i in range(self.n):
            for j in range(self.r):
                self.need[i][j] = self.maximum[i][j] - self.allocation[i][j]

    def is_safe(self):
        finish = [False] * self.n
        safe_sequence = []
        work = self.available[:]

        while len(safe_sequence) < self.n:
            allocated = False
            for i in range(self.n):
                if not finish[i]:
                    if all(self.need[i][j] <= work[j] for j in range(self.r)):
                        for j in range(self.r):
                            work[j] += self.allocation[i][j]
                        safe_sequence.append(i)
                        finish[i] = True
                        allocated = True
            if not allocated:
                break

        if len(safe_sequence) == self.n:
            return True, safe_sequence
        else:
            return False, []

class BankersAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm - Deadlock Avoidance")

        # Labels for input fields
        tk.Label(root, text="Number of Processes:").grid(row=0, column=0)
        tk.Label(root, text="Number of Resources:").grid(row=1, column=0)

        # Input fields for processes and resources
        self.n_entry = tk.Entry(root)
        self.r_entry = tk.Entry(root)
        self.n_entry.grid(row=0, column=1)
        self.r_entry.grid(row=1, column=1)

        # Button to generate input matrices
        tk.Button(root, text="Generate Matrices", command=self.create_matrices).grid(row=2, columnspan=2)

    def create_matrices(self):
        try:
            n = int(self.n_entry.get())
            r = int(self.r_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for processes and resources.")
            return

        # Create matrices input fields
        self.allocation_entries = []
        self.max_entries = []
        self.available_entries = []

        # Labels for matrices
        tk.Label(self.root, text="Allocation Matrix").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Max Matrix").grid(row=3, column=r+1, padx=5, pady=5)
        tk.Label(self.root, text="Available Resources").grid(row=3, column=2*r+1, padx=5, pady=5)

        # Row labels for processes
        for i in range(n):
            tk.Label(self.root, text=f"P{i}").grid(row=4 + i, column=0, padx=5, pady=5)

        # Column labels for resources
        for j in range(r):
            tk.Label(self.root, text=f"R{j}").grid(row=3, column=j+1)
            tk.Label(self.root, text=f"R{j}").grid(row=3, column=j+1+r)
            tk.Label(self.root, text=f"R{j}").grid(row=4 + n, column=j+2*r+1)

        # Input fields for Allocation and Max matrices
        for i in range(n):
            row_alloc = []
            row_max = []
            for j in range(r):
                entry_alloc = tk.Entry(self.root, width=3)
                entry_alloc.grid(row=4 + i, column=j+1)
                row_alloc.append(entry_alloc)

                entry_max = tk.Entry(self.root, width=3)
                entry_max.grid(row=4 + i, column=j+1+r)
                row_max.append(entry_max)
            self.allocation_entries.append(row_alloc)
            self.max_entries.append(row_max)

        # Input fields for Available resources
        for j in range(r):
            entry_avail = tk.Entry(self.root, width=3)
            entry_avail.grid(row=4 + n, column=j + 2*r + 1)
            self.available_entries.append(entry_avail)

        # Button to calculate the safe sequence
        tk.Button(self.root, text="Calculate Safe Sequence", command=self.calculate_safe_sequence).grid(row=5 + n, columnspan=2)

    def calculate_safe_sequence(self):
        n = int(self.n_entry.get())
        r = int(self.r_entry.get())

        # Get Allocation Matrix
        allocation = []
        for i in range(n):
            row = []
            for j in range(r):
                try:
                    row.append(int(self.allocation_entries[i][j].get()))
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid allocation values.")
                    return
            allocation.append(row)

        # Get Max Matrix
        maximum = []
        for i in range(n):
            row = []
            for j in range(r):
                try:
                    row.append(int(self.max_entries[i][j].get()))
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid maximum values.")
                    return
            maximum.append(row)

        # Get Available Resources
        available = []
        for j in range(r):
            try:
                available.append(int(self.available_entries[j].get()))
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid available resources.")
                return

        # Run Banker's Algorithm
        banker = BankersAlgorithm(n, r, allocation, maximum, available)
        is_safe, safe_sequence = banker.is_safe()

        # Display Result
        if is_safe:
            messagebox.showinfo("Safe Sequence", f"The system is in a safe state.\nSafe Sequence: {', '.join('P'+str(i) for i in safe_sequence)}")
        else:
            messagebox.showerror("Unsafe State", "The system is in an unsafe state, deadlock may occur.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersAlgorithmGUI(root)
    root.mainloop()
