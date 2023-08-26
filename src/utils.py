import time
import zipfile

from src import redis_db


def unzip(path: str, directory_to: str):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(directory_to)


def simulate_of_process(archive_id):
    redis_db.set_status(archive_id, False)

    percent = 0

    while percent <= 100:
        redis_db.set_percent(archive_id, percent)
        percent += 16
        time.sleep(8)

    redis_db.set_status(archive_id, True)
