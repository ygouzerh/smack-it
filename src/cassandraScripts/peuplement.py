
from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

session.execute("""INSERT INTO pays (nom_pays, emojis) VALUES ('France', ['1F600', '1F600','1F923','1F617','263A','1F61A','1F61F','1F92C','1F92C']);""")
session.execute("""INSERT INTO pays (nom_pays, emojis) VALUES ('Angleterre', ['1F600']);""")
session.execute("""INSERT INTO pays (nom_pays, emojis) VALUES ('Pakistan', ['1F600','1F621','1F621','1F62D','1F626','1F637','1F60C','1F609']);""")
