import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime


class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def log_change(self, event_type, src_path):
        # Günlük değişikliği yapılandırma
        change = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "file": src_path
        }
        try:
            # JSON formatında loglama
            with open(self.log_file, 'a') as file:
                file.write(json.dumps(change) + "\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def on_created(self, event):
        self.log_change("created", event.src_path)

    def on_deleted(self, event):
        self.log_change("deleted", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.log_change("modified", event.src_path)


def main():
    watch_directory = "/home/vboxuser/bsm/test"
    log_file = "/home/vboxuser/bsm/logs/changes.json"

    # Log dosyasının varlığını kontrol et
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            file.write("")

    # Watchdog observer başlat
    event_handler = DirectoryChangeHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=True)

    print(f"Watching directory: {watch_directory}")
    observer.start()
    try:
        while True:
            pass  # Observer'ı sürekli çalıştır
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
