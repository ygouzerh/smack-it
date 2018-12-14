
veryPositive = ["1F600","1F603","1F604","1F601","1F606","1F923","1F602","1F970","1F60D","1F929","1F618","1F60B","1F61B","1F61C","1F61D","1F911","1F917","1F60E","1F44D"]
positive = ["1F605","1F642","1F609","1F60A","1F607","1F617","263A","1F61A","1F619","1F92A","1F92D","1F60F","1F60C","1F924","1F48B","1F497","1F493","1F49E","1F495","2764"]

negative = ["1F612","1F637","1F912","1F915","1F922","1F92E","1F927","1F615","1F61F","1F641","2639","1F97A","1F626","1F628","1F631","1F616","1F61E"]
veryNegative = ["1F625","1F622","1F62D","1F623","1F629","1F62B","1F624","1F621","1F620","1F92C","1F480","1F4A9","1F494","1F44E"]

def calcSentimentScore(emojiList):
    """Returns a score (from 0 to 100) representing the sentiment from the emojis"""
    score = 0
    nbEmoScored = 0
    for emoji in emojiList:
        if emoji in veryPositive:
            score += 100
            nbEmoScored += 1
        elif emoji in positive:
            score += 75
            nbEmoScored += 1
        elif emoji in negative:
            score += 25
            nbEmoScored += 1
        elif emoji in veryNegative:
            nbEmoScored += 1
    score = score/nbEmoScored
    return round(score)
