import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

# Buffer settings
BUFFER_SIZE = 5
buffer = []
in_index = 0
out_index = 0

# Synchronization variables
empty = BUFFER_SIZE
full = 0
buffer_lock = threading.Lock()


# GUI setup
class ProducerConsumerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Producer-Consumer Problem")

        self.buffer_frame = tk.Frame(master)
        self.buffer_frame.pack(pady=10)

        self.buffer_labels = []
        for i in range(BUFFER_SIZE):
            label = tk.Label(self.buffer_frame, text="Empty", width=10, borderwidth=2, relief="groove")
            label.grid(row=0, column=i, padx=5)
            self.buffer_labels.append(label)

        self.start_button = tk.Button(master, text="Start", command=self.start_threads)
        self.start_button.pack(pady=5)

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack()

    def start_threads(self):
        self.status_label.config(text="Starting producer and consumer...")
        self.start_button.config(state=tk.DISABLED)

        producer_thread = threading.Thread(target=self.producer)
        consumer_thread = threading.Thread(target=self.consumer)

        producer_thread.start()
        consumer_thread.start()

    def producer(self):
        global empty, full, in_index

        for _ in range(10):  # Produce 10 items
            time.sleep(random.uniform(0.5, 1.5))  # Simulate production time

            item = random.randint(1, 100)  # Produce a random item

            # Wait for an empty slot
            with buffer_lock:
                while empty == 0:
                    pass  # Busy wait
                buffer.append(item)
                in_index = (in_index + 1) % BUFFER_SIZE
                self.update_buffer()  # Update GUI buffer display
                full += 1
                empty -= 1

            self.status_label.config(text=f"Produced: {item}")

    def consumer(self):
        global empty, full, out_index

        for _ in range(10):  # Consume 10 items
            time.sleep(random.uniform(0.5, 1.5))  # Simulate consumption time

            # Wait for a full slot
            with buffer_lock:
                while full == 0:
                    pass  # Busy wait
                item = buffer.pop(0)
                out_index = (out_index + 1) % BUFFER_SIZE
                self.update_buffer()  # Update GUI buffer display
                full -= 1
                empty += 1

            self.status_label.config(text=f"Consumed: {item}")

    def update_buffer(self):
        for i in range(BUFFER_SIZE):
            if i < len(buffer):
                self.buffer_labels[i].config(text=str(buffer[i]))
            else:
                self.buffer_labels[i].config(text="Empty")


# Create the main window
root = tk.Tk()
app = ProducerConsumerGUI(root)
root.mainloop()
