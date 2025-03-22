import os

def test_log_file_exists():
    log_file = "./" + os.getenv("LOG_FILE", "log.txt")
    assert os.path.exists(log_file), f"El archivo {log_file} no existe"