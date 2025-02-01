import multiprocessing
import time

def cpu_intensive_task():
    while True:
        pass  # Infinite loop to keep the CPU busy

if __name__ == "__main__":
    processes = []
    for _ in range(5):
        p = multiprocessing.Process(target=cpu_intensive_task)
        p.start()
        processes.append(p)
    
    # Keep the main process running while the child processes are busy
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
