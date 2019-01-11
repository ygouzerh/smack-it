from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from cassandra.cluster import Cluster
import random
from jinja2 import contextfilter

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

app = Flask(__name__)
#cassandra = CassandraCluster()
GoogleMaps(app)

address = 'localhost'
cluster = Cluster([address])
session = cluster.connect("emoji")
#app.config['CASSANDRA_NODES'] = ['cassandra-c1.terbiumlabs.com']  # can be a string or list of nodes


veryPositive = ["1F600","1F603","1F604","1F601","1F606","1F923","1F602","1F970","1F60D","1F929","1F618","1F60B","1F61B","1F61C","1F61D","1F911","1F917","1F60E","1F44D"]
positive = ["1F605","1F642","1F609","1F60A","1F607","1F617","263A","1F61A","1F619","1F92A","1F92D","1F60F","1F60C","1F924","1F48B","1F497","1F493","1F49E","1F495","2764"]

negative = ["1F612","1F637","1F912","1F915","1F922","1F92E","1F927","1F615","1F61F","1F641","2639","1F97A","1F626","1F628","1F631","1F616","1F61E"]
veryNegative = ["1F625","1F622","1F62D","1F623","1F629","1F62B","1F624","1F621","1F620","1F92C","1F480","1F4A9","1F494","1F44E"]

def convertToEmoji(strList):
    emoList = []
    for e in strList:
        emoList.append(chr(int(e,16)))
    return emoList


def calcSentimentScore(emojiDico):
    """Returns a score (from 0 to 100) representing the sentiment from the emojis"""
    score = 0
    nbEmoScored = 0
    for emoji, nbOcc in emojiDico.items():
        if emoji in veryPositive or emoji in convertToEmoji(veryPositive):
            score += 100*nbOcc
            nbEmoScored += nbOcc
        elif emoji in positive or emoji in convertToEmoji(positive):
            score += 75*nbOcc
            nbEmoScored += nbOcc
        elif emoji in negative or emoji in convertToEmoji(negative):
            score += 25*nbOcc
            nbEmoScored += nbOcc
        elif emoji in veryNegative or emoji in convertToEmoji(veryNegative):
            nbEmoScored += nbOcc
    if nbEmoScored == 0 :
        return 50
    score = score/nbEmoScored
    return round(score)

@app.route("/cassandraCall/<pays>")
def cassandraCall(pays):
    print(pays)
    rows = session.execute("SELECT * FROM emoji_package where pays = '"+pays+"' AND package_date > timeAgo(60) ALLOW FILTERING");
    emoji_dict = {}
    for row in rows:
        if row.id_emoji not in emoji_dict:
            emoji_dict[row.id_emoji] = row.nb_occurence
        else:
            emoji_dict[row.id_emoji] += row.nb_occurence
    score = calcSentimentScore(emoji_dict)
    print(score)
    emoji = '1f610'
    if score > 80 :
        emoji = "1F604"
    elif score > 70 :
        emoji = "1F603"
    elif score > 60 :
        emoji = "1F60A"
    elif score > 40 :
        emoji = '1F610'
    elif score > 30 :
        emoji = '1F623'
    elif score > 20 :
        emoji = '1F620'
    else :
        emoji = '1F621'

    return chr(int(emoji,16))


@app.route("/")
def mapview():
    return render_template('maaap.html', name="Allemagne")

if __name__ == '__main__':
    app.run(debug=True)
