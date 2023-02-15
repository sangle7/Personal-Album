import os
import time
import logging

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from src.download import embed_by_file

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class NewImageHandler(LoggingEventHandler):
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')

    def on_created(self, event):
        if event.src_path.lower().endswith(self.IMAGE_EXTENSIONS):
            filename = os.path.basename(event.src_path)
            filepath = os.path.join('images', filename)
            logging.info(f'New image added: {filename} ({event.src_path})')
            embed_by_file(filepath)


if __name__ == "__main__":
    images_folder = os.path.join(os.getcwd(), "images")
    
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    event_handler = NewImageHandler()
    observer = Observer()

    observer.schedule(event_handler, images_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    with observer:
        observer.join()
