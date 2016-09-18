import json
import redis
import config
from random import randint

db = redis.StrictRedis(host=config.redisHost, port=config.redisPort, db=0)


def add_data_to_db():
    countries = json.loads(open(config.citiesJson, 'r').read())
    db.flushall()
    for cityList in countries.values():
        for city in cityList:
            tmp = city.lower()
            db.sadd("en:{0}:{1}:{2}".format(randint(1, 1000), tmp[0:1], tmp[-1:]), city)
    return
