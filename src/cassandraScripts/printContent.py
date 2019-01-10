
from cassandra.cluster import Cluster
from sentimentAnalysis import calcSentimentScore

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

rows = session.execute("""SELECT * FROM emoji_package where package_date > timeAgo(60) ALLOW FILTERING""");
pays_dict = {}
for row in rows:
    if row.pays not in pays_dict :
        pays_dict[row.pays] = {}
    if row.id_emoji not in pays_dict[row.pays]:
        pays_dict[row.pays][row.id_emoji] = row.nb_occurence
    else:
        pays_dict[row.pays][row.id_emoji] += row.nb_occurence
for pays in pays_dict.keys():
    print("Pays : {} . Emojis :".format(pays), end="")
    for emoji in pays_dict[pays].keys():
        print(chr(int(emoji,16)), end="")
    print()
    print("Sentiment score : ", calcSentimentScore(pays_dict[pays]))
