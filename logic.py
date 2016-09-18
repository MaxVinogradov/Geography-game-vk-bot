from integration import Integration
from config import *
from time import sleep
from converter import db

vk = Integration()
playersPool = {}
interruptedGamesPlayersIds = []
levels = {}


def process():
    while True:
        for message in vk.get_unreadable_message()[1:]:
            body = message["body"]
            user_id = message["uid"]
            check_level(user_id, body)
            check_start(user_id, body)
            check_pause(user_id, body)
            check_resume(user_id, body)
            check_finish(user_id, body)
    sleep(3)


def check_start(user_id, body):
    if body == controlPhrases["phraseToInitGame"]:
        if user_id not in playersPool.keys():
            playersPool[user_id] = []
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
        levels[user_id] = body.split(" ")[1]
        vk.send_message(user_id, botPhrases["levelPhrase"])

process()
