import threading
import time
class Locks:
    def __init__(self):
        self.lock_1 = threading.Lock()
        self.lock_2 = threading.Lock()
        self.count = 0
# Global lock for printing
print_lock = threading.Lock()


def thread_1_routine(locks):
    tid = threading.get_ident()
    with print_lock:
        print(f"Thread [{tid}]: wants lock 1")

    locks.lock_1.acquire()
    with print_lock:
        print(f"Thread [{tid}]: owns lock 1")

    time.sleep(0.1)  # Simulate some work

    with print_lock:
        print(f"Thread [{tid}]: wants lock 2")

    locks.lock_2.acquire()
    with print_lock:
        print(f"Thread [{tid}]: owns lock 2")
        locks.count += 1
        print(f"Thread [{tid}]: count updated to {locks.count}")

    locks.lock_2.release()
    with print_lock:
        print(f"Thread [{tid}]: unlocking lock 2")

    locks.lock_1.release()
    with print_lock:
        print(f"Thread [{tid}]: unlocking lock 1")
        print(f"Thread [{tid}]: finished")


def thread_2_routine(locks):
    tid = threading.get_ident()
    with print_lock:
        print(f"Thread [{tid}]: wants lock 2")

    locks.lock_2.acquire()
    with print_lock:
        print(f"Thread [{tid}]: owns lock 2")

    time.sleep(0.1)  # Simulate some work

    with print_lock:
        print(f"Thread [{tid}]: wants lock 1")

    locks.lock_1.acquire()
    with print_lock:
        print(f"Thread [{tid}]: owns lock 1")
        locks.count += 1
        print(f"Thread [{tid}]: count updated to {locks.count}")

    locks.lock_1.release()
    with print_lock:
        print(f"Thread [{tid}]: unlocking lock 1")

    locks.lock_2.release()
    with print_lock:
        print(f"Thread [{tid}]: unlocking lock 2")
        print(f"Thread [{tid}]: finished")


def main():
    locks = Locks()

    # Create and start threads
    thread_1 = threading.Thread(target=thread_1_routine, args=(locks,))
    print(f"Main: Created first thread [{thread_1.ident}]")
    thread_1.start()

    thread_2 = threading.Thread(target=thread_2_routine, args=(locks,))
    print(f"Main: Created second thread [{thread_2.ident}]")
    thread_2.start()

    # Wait for threads to finish
    thread_1.join()
    print(f"Main: Joined first thread [{thread_1.ident}]")

    thread_2.join()
    print(f"Main: Joined second thread [{thread_2.ident}]")

    # Final count evaluation
    if locks.count == 2:
        print(f"Main: OK. Total count is {locks.count}")
    else:
        print(f"Main: ERROR! Total count is {locks.count}")


if __name__ == "__main__":
    main()
