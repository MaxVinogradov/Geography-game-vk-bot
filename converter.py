import json
import redis
import config
from random import randint


def add_data_to():
    countries = json.loads(open(config.citiesJson, 'r').read())
    r = redis.StrictRedis(host=config.redisHost, port=config.redisPort, db=0)
    r.flushall()
    for cityList in countries.values():
        for city in cityList:
            tmp = city.lower()
            r.sadd("en:{0}:{1}:{2}".format(randint(1, 1000), tmp[0:1], tmp[-1:]), city)
    return

