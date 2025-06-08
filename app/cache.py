import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), decode_responses=True)

def cache_get(key: str):
    return r.get(key)

def cache_set(key: str, value, ex=300):
    r.set(key, json.dumps(value), ex)
