import redis
from utils.config import settings

_redis = None

def get_redis():
    global _redis
    if _redis is None:
        # decode_responses=True -> str in/out
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis
