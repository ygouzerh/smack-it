#!/usr/bin/env python3

from cassandra.cluster import Cluster

address = 'cassandra-db'

cluster = Cluster([address])
session = cluster.connect()

session.execute("""DROP KEYSPACE IF EXISTS "emoji";""")
#création du keyspace
session.execute("""CREATE KEYSPACE "emoji" WITH replication = {'class' : 'SimpleStrategy', 'replication_factor' : 2};""")
session.execute("""USE emoji;""")
#création table
session.execute("""CREATE TABLE EMOJI_PACKAGE(id UUID PRIMARY KEY, pays text, id_emoji text, nb_occurence int, package_date timestamp);""")

r = session.execute("""SELECT * FROM EMOJI_PACKAGE;""")

for row in r:
    prints(row.pays, row.id_emoji, row.nb_occurence)


session.shutdown()
cluster.shutdown()
