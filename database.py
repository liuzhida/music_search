'''
'''
import brukva
import redis
from tornado import gen

class AsyncRedis():

    @classmethod
    def client(cls):
        if not hasattr(cls, '_client'):
            cls._client = brukva.Client()
            cls._client.connect()
        return cls._client

class RamRedis():

    @classmethod
    def client(cls):
        if not hasattr(cls, '_client'):
            cls._client = redis.StrictRedis()
        return cls._client
