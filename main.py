from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        print(f"Detected change in {event.src_path}. Restarting server...")
        self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

if __name__ == "__main__":
    path = "."  # Monitoruje bieżący katalog
    command = "python python_server/server.py"  # Zastąp 'your_flask_server.py' nazwą swojego serwera

    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"Starting server with hot reload at {path}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
