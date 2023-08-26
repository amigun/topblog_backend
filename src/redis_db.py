import redis

r = redis.Redis(
    host='redis',
    port=6379
)


def set_percent(
        archive_id: str,
        percent: int
):
    return r.set(f'{archive_id}:percent', percent)


def set_status(
        archive_id: str,
        finished: bool
):
    return r.set(f'{archive_id}:finished', 'yes' if finished else 'no')


def get_percent(archive_id: str):
    return r.get(f'{archive_id}:percent')


def get_status(archive_id: str):
    return r.get(f'{archive_id}:finished')
