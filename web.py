import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.get("devices/lora/807B859020000001/lmt01")