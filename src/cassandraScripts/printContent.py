
from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

rows = session.execute("""SELECT * FROM pays""");
for row in rows:
    print("Pays : {} . Emojis : {}".format(row.nom_pays, row.emojis))
