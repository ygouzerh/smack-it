
from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

session.execute("""INSERT INTO pays (nom_pays, emojis) VALUES ('France', ['emoContent1', 'emoTriste1']);""")
session.execute("""INSERT INTO pays (nom_pays, emojis) VALUES ('Angleterre', ['emoContent1', 'emoContent2', 'emoColere1']);""")
session.execute("""INSERT INTO pays (nom_pays, emojis) VALUES ('Pakistan', ['emoColere1', 'emoTriste1']);""")
