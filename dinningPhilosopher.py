import threading
import time
import random
import tkinter as tk
import math


K = 5


chopsticks = [threading.Lock() for _ in range(K)]


philosopher_states = [0] * K


root = tk.Tk()
root.title("Dining Philosophers Problem")

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

positions = [(300 + 200 * round(math.cos(2 * math.pi * i / K), 2),
              300 + 200 * round(math.sin(2 * math.pi * i / K), 2)) for i in range(K)]

philosophers = [canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="lightblue") for x, y in positions]
chopstick_lines = []

for i in range(K):
    x1, y1 = positions[i]
    x2, y2 = positions[(i + 1) % K]
    line = canvas.create_line(x1, y1, x2, y2, width=4, fill="gray")
    chopstick_lines.append(line)

state_labels = [canvas.create_text(x, y - 50, text="Thinking", font=("Arial", 10)) for x, y in positions]

def update_philosopher_state(index, state):
    if state == 0:  # Thinking
        canvas.itemconfig(philosophers[index], fill="lightblue")
        canvas.itemconfig(state_labels[index], text="Thinking")
    elif state == 1:  # Hungry
        canvas.itemconfig(philosophers[index], fill="orange")
        canvas.itemconfig(state_labels[index], text="Hungry")
    else:  # Eating
        canvas.itemconfig(philosophers[index], fill="lightgreen")
        canvas.itemconfig(state_labels[index], text="Eating")


def update_chopstick_state(index, state):

    if state == 0:  # Available
        canvas.itemconfig(chopstick_lines[index], fill="gray")
    else:  # In use
        canvas.itemconfig(chopstick_lines[index], fill="red")


class Philosopher(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index  # Philosopher index (number)
        self.left_chopstick = chopsticks[index]  # Left chopstick (lock)
        self.right_chopstick = chopsticks[(index + 1) % K]  # Right chopstick (lock)

    def run(self):

        while True:
            self.think()  # Philosopher is thinking
            self.hungry()  # Philosopher gets hungry
            self.eat()    # Philosopher starts eating

    def think(self):
        update_philosopher_state(self.index, 0)  # Set state to "Thinking"
        print(f"Philosopher {self.index} is thinking.")
        time.sleep(random.uniform(2, 4))  # Think for 2-4 seconds

    def hungry(self):

        update_philosopher_state(self.index, 1)  # Set state to "Hungry"
        print(f"Philosopher {self.index} is hungry.")
        time.sleep(random.uniform(1, 2))  # Remain hungry for 1-2 seconds

    def eat(self):

        print(f"Philosopher {self.index} is trying to pick up the left chopstick.")
        with self.left_chopstick:  # Acquire the left chopstick (lock)
            update_chopstick_state(self.index, 1)  # Left chopstick is now in use (red)
            print(f"Philosopher {self.index} picked up the left chopstick.")
            time.sleep(1)

            print(f"Philosopher {self.index} is trying to pick up the right chopstick.")
            with self.right_chopstick:  # Acquire the right chopstick (lock)
                update_chopstick_state((self.index + 1) % K, 1)  # Right chopstick is now in use (red)
                print(f"Philosopher {self.index} picked up the right chopstick and starts eating.")
                update_philosopher_state(self.index, 2)  # Set state to "Eating"
                time.sleep(random.uniform(2, 4))  # Eating for 2-4 seconds
                print(f"Philosopher {self.index} finished eating and puts down chopsticks.")


                update_chopstick_state((self.index + 1) % K, 0)  # Right chopstick is now available (gray)


        update_chopstick_state(self.index, 0)  # Left chopstick is now available (gray)


def main():
    philosophers = [Philosopher(i) for i in range(K)]  # Create philosopher threads


    for philosopher in philosophers:
        philosopher.start()  # Start the philosopher's lifecycle (thinking, hungry, eating)

threading.Thread(target=main, daemon=True).start()
root.mainloop()  # Start the Tkinter event loop to display the GUI
