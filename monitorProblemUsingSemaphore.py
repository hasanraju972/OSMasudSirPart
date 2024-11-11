import threading
import time
import random

read_count = 0  # Number of readers currently accessing the resource
shared_data = 0  # Shared data (resource)

# Semaphores
mutex = threading.Semaphore(1)        # Controls access to read_count (critical section)
rw_mutex = threading.Semaphore(1)     # Controls access to the resource for both readers and writers

# Reader function
def reader(reader_id):
    global read_count, shared_data

    for _ in range(3):  # Each reader will read 3 times
        # Entry section for readers (monitor-style protection)
        mutex.acquire()  # Ensure mutual exclusion for read_count modification
        read_count += 1
        if read_count == 1:
            rw_mutex.acquire()  # First reader blocks writers
        mutex.release()

        # Reading section (critical section)
        print(f"Reader {reader_id} is reading the shared data: {shared_data}")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate reading time

        # Exit section for readers (monitor-style protection)
        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            rw_mutex.release()  # Last reader allows writers
        mutex.release()

        time.sleep(random.uniform(0.5, 2))  # Simulate time between reads

# Writer function
def writer(writer_id):
    global shared_data

    for _ in range(2):  # Each writer will write 2 times
        rw_mutex.acquire()  # Ensure only one writer (or readers) can access the shared resource

        # Writing section (critical section)
        shared_data = random.randint(1, 100)  # Modify the shared data
        print(f"Writer {writer_id} wrote the value: {shared_data}")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate writing time

        rw_mutex.release()  # Release the lock, allowing readers or writers

        time.sleep(random.uniform(1, 3))  # Simulate time between writes

# Main function to start threads
if __name__ == "__main__":
    num_readers = 5
    num_writers = 2

    # Create reader and writer threads
    reader_threads = [threading.Thread(target=reader, args=(i + 1,)) for i in range(num_readers)]
    writer_threads = [threading.Thread(target=writer, args=(i + 1,)) for i in range(num_writers)]

    for t in reader_threads:
        t.start()

    for t in writer_threads:
        t.start()

    # Wait for all threads to complete
    for t in reader_threads:
        t.join()

    for t in writer_threads:
        t.join()

    print("All readers and writers have finished.")
