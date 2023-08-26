import datetime
import hashlib
import threading

from fastapi import APIRouter, UploadFile, File
from starlette import status
from starlette.websockets import WebSocket

from src import redis_db, utils
from src.utils import unzip

router = APIRouter()


@router.post('/upload_archive/', status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile = File(...)) -> str:
    new_filename = hashlib.md5(file.file.read())\
                       .hexdigest() + str(int(datetime.datetime.now().timestamp())) + file.filename

    file.file.seek(0)

    with open(f'files/{new_filename}', 'wb') as f:
        while True:
            contents = file.file.read(2 ** 20)

            if not contents:
                break

            f.write(contents)

    unzip(f'files/{new_filename}', f'files/{new_filename}.unzipped/')

    thread = threading.Thread(target=utils.simulate_of_process, args=(new_filename,))
    thread.start()

    return new_filename


@router.websocket('/ws/get_percent/{archive_id}')
async def get_percent(websocket: WebSocket, archive_id: str):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        percent = redis_db.get_percent(archive_id)

        await websocket.send_text(percent)


@router.websocket('/ws/get_status/{archive_id}')
async def get_status(websocket: WebSocket, archive_id: str):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        status_ = redis_db.get_status(archive_id)

        await websocket.send_text(status_)
