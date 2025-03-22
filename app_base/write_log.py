import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__),  "./"+os.getenv("LOG_TXT", "log.txt"))

def write_log(text):
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] {text}\n")