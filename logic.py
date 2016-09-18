from integration import Integration
from config import *
from time import sleep

vk = Integration()
playersPool = {}
interruptedGamesPlayersIds = []

while True:
    for massage in vk.get_unreadable_message()[1:]:
        body = massage["body"]
        userId = massage["uid"]
        if body == controlPhrases["phraseToInitGame"]:
            if userId not in playersPool:
                playersPool[userId] = []
                vk.send_message(userId, botPhrases["startPhrase"])
            else:
                vk.send_message(userId, errorPhrases["illegalStartingGame"])

        elif body == controlPhrases["phraseToPauseGame"]:
            if userId in playersPool and userId not in interruptedGamesPlayersIds:
                interruptedGamesPlayersIds.append(userId)
                vk.send_message(userId, botPhrases["pausePhrase"])
            else:
                vk.send_message(userId, errorPhrases["illegalPauseGame"])

        elif body == controlPhrases["phraseToResumeGame"]:
            if userId in playersPool and userId in interruptedGamesPlayersIds:
                interruptedGamesPlayersIds.remove(userId)
                vk.send_message(userId, botPhrases["resumePhrase"])
            else:
                vk.send_message(userId, errorPhrases["illegalResumingGame"])

        elif body == controlPhrases["phraseToFinishGame"]:
            if userId in interruptedGamesPlayersIds:
                interruptedGamesPlayersIds.remove(userId)
            if userId in playersPool:
                playersPool.pop(userId)
                vk.send_message(userId, botPhrases["endPhrase"])                
            else:
                vk.send_message(userId, errorPhrases["illegalFinishingGame"])
    sleep(3)
