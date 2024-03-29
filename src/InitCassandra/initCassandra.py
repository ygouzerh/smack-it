from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect()

session.execute("""DROP KEYSPACE "emoji";""")
#création du keyspace
session.execute("""CREATE KEYSPACE "emoji" WITH replication = {'class' : 'SimpleStrategy', 'replication_factor' : 1};""")
session.execute("""USE emoji;""")
#création table
session.execute("""CREATE TABLE PAYS(nom_pays text PRIMARY KEY, emojis list<text>);""");
