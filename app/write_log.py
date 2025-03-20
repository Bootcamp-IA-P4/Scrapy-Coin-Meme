
from datetime import datetime

def write_log(text):
    with open("/app/log.txt", "a") as log:
        log.write(f"[{datetime.now()}] {text}\n")