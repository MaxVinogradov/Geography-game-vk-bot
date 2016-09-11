import json
import redis


countries = json.loads(open('cities/cities_en.json', 'r').read())
# print(countries["Russia"][0])
r = redis.StrictRedis(host='localhost', port=6379, db=0)
for x in range(ord('A'), ord('Z')):
    print(chr(x))