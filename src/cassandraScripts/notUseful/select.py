from cassandra.cluster import Cluster
import sched, time
from sentimentAnalysis import calcSentimentScore

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

s = sched.scheduler(time.time, time.sleep)
def repeat(sc):
    print("----"+datetime.datetime.now().time()+"----")
    rows = session.execute("""SELECT * FROM pays""");
    for row in rows:
        print("Pays : {} . Emojis :".format(row.nom_pays), end="")
        for emoji in row.emojis:
            print(chr(int(emoji,16)), end="")
        print()
        print("Sentiment score : ", calcSentimentScore(row.emojis))    # session.execute("""TRUNCATE pays"""); #Deleting selected tweets.
    s.enter(60, 1, repeat, (sc,))

s.enter(60, 1, repeat, (s,))
s.run()
