import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import os
from src.download import embed_by_file

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class NewImageHandler(LoggingEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith('.jpg') or event.src_path.lower().endswith(".jpeg") or event.src_path.lower().endswith('.png'):
            filename = os.path.basename(event.src_path)
            logging.info(f'New image added: {filename} ({event.src_path})')
            embed_by_file("images/"+filename)


if __name__ == "__main__":
    path = os.getcwd() + "/images"
    event_handler = NewImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
