
from cassandra.cluster import Cluster
from sentimentAnalysis import calcSentimentScore

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

rows = session.execute("""SELECT * FROM pays""");
for row in rows:
    print("Pays : {} . Emojis :".format(row.nom_pays), end="")
    for emoji in row.emojis:
        print(chr(int(emoji,16)), end="")
    print()
    print("Sentiment score : ", calcSentimentScore(row.emojis))
