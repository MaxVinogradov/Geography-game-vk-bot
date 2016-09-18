# pass to .json file
citiesJson = "cities/cities_en.json"

# Redis db config
redisHost = "localhost"
redisPort = 6379

# app_id for vk_api
appID = 00000
# file, where auth data is saved
authFile = '.auth_data'

# bot phrases
botPhrases = {
    "startPhrase": "Hi! Game has been started by you.",
    "pausePhrase": "Hi! Game has been paused by you.",
    "resumePhrase": "Hi! Game has been resumed by you.",
    "endPhrase": "Game has been ended by you. Bye!",
    "levelPhrase": "Your current level is "
}

# control phrases
controlPhrases = {
    "phraseToInitGame": "start",
    "phraseToPauseGame": "pause",
    "phraseToResumeGame": "resume",
    "phraseToFinishGame": "finish",
    "phraseToGetUsedCities": "cities"
}

# error phrases
errorPhrases = {
    "illegalStartingGame": "Error: game already started!",
    "illegalPauseGame": "Error: you can not pause the game without starting it or game has already paused!",
    "illegalResumingGame": "Error: you can not resume the game because you hadn't paused game before!",
    "illegalFinishingGame": "Error: you can not finish the game without starting it!",
    "illegalLevel": "Error: level is not correct! It must be digit between 1 and 1000. Try again!",
    "illegalWordOutOfGame": "Error: game hasn't started yet.",
    "illegalCity": "Error: it is not city.",
    "illegalRepeatedCity": "Error: we have already used this word in our game."
}
