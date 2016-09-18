from integration import Integration
from config import *
from time import sleep
from converter import db

vk = Integration()
playersPool = {}
interruptedGamesPlayersIds = []
levels = {}


def process():
    sleep(3)
    while True:
        for message in vk.get_unreadable_message()[1:]:
            body = message["body"]
            user_id = message["uid"]
            check_level(user_id, body)
            check_start(user_id, body)
            check_pause(user_id, body)
            check_resume(user_id, body)
            check_finish(user_id, body)
            check_to_get_cities(user_id, body)
            if body not in list(controlPhrases.values()):
                if check_is_city(user_id, body):
                    generate_new_word(user_id, body)

        sleep(2)


def check_start(user_id, body):
    if body == controlPhrases["phraseToInitGame"]:
        if user_id not in playersPool.keys():
            playersPool[user_id] = []
            levels[user_id] = 100
            vk.send_message(user_id, botPhrases["startPhrase"])
        else:
            vk.send_message(user_id, errorPhrases["illegalStartingGame"])


def check_pause(user_id, body):
    if body == controlPhrases["phraseToPauseGame"]:
        if user_id in playersPool.keys() and user_id not in interruptedGamesPlayersIds:
            interruptedGamesPlayersIds.append(user_id)
            vk.send_message(user_id, botPhrases["pausePhrase"])
        else:
            vk.send_message(user_id, errorPhrases["illegalPauseGame"])


def check_resume(user_id, body):
    if body == controlPhrases["phraseToResumeGame"]:
        if user_id in playersPool.keys() and user_id in interruptedGamesPlayersIds:
            interruptedGamesPlayersIds.remove(user_id)
            vk.send_message(user_id, botPhrases["resumePhrase"])
        else:
            vk.send_message(user_id, errorPhrases["illegalResumingGame"])


def check_finish(user_id, body):
    if body == controlPhrases["phraseToFinishGame"]:
        if user_id in interruptedGamesPlayersIds:
            interruptedGamesPlayersIds.remove(user_id)
        if user_id in playersPool.keys():
            playersPool.pop(user_id)
            vk.send_message(user_id, botPhrases["endPhrase"])
        else:
            vk.send_message(user_id, errorPhrases["illegalFinishingGame"])


def check_level(user_id, body):
    if body.startswith("level"):
        if len(body.split(" ")) == 2:
            level = body.split(" ")[1]
        else:
            return
        if level.isdigit() and 1 <= int(level) <= 1000:
            levels[user_id] = level
            vk.send_message(user_id, botPhrases["levelPhrase"] + level)
        else:
            vk.send_message(user_id, botPhrases["levelPhrase"] + str(levels[user_id]))
            vk.send_message(user_id, errorPhrases["illegalLevel"])


def check_to_get_cities(user_id, body):
    if body == controlPhrases["phraseToGetUsedCities"] and user_id in playersPool.keys():
        vk.send_message(user_id, playersPool[user_id])


def check_is_city(user_id, body):
    if body in playersPool[user_id]:
        vk.send_message(user_id, errorPhrases["illegalRepeatedCity"])
        return False
    tmp = body.lower()
    if user_id in playersPool.keys():
        for i in range(1, 1001):
            for j in db.smembers("en:{0}:{1}:{2}".format(i, tmp[0:1], tmp[-1:])):
                if j.decode('utf-8') == body:
                    playersPool[user_id].append(body)
                    return True
    else:
        vk.send_message(user_id, errorPhrases["illegalWordOutOfGame"])
    vk.send_message(user_id, errorPhrases["illegalCity"])
    return False


def generate_new_word(user_id, body):
    tmp = playersPool[user_id][-1].lower()
    for i in range(1, levels[user_id] + 1):
        for lastLetter in range(ord("a"), ord("z")):
            for j in db.smembers("en:{0}:{1}:{2}".format(i, tmp[-1:], chr(lastLetter))):
                if j.decode('utf-8') not in playersPool[user_id]:
                    playersPool[user_id].append(j.decode('utf-8'))
                    vk.send_message(user_id,j.decode('utf-8'))
                    return

process()
