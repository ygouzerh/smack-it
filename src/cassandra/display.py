#!/usr/bin/env python3

from cassandra.cluster import Cluster

address = 'cassandra-db'

cluster = Cluster([address])
session = cluster.connect()

session.execute("""USE emoji;""")


r = session.execute("""SELECT * FROM EMOJI_PACKAGE;""")

for row in r:
    print(row.pays, row.id_emoji, row.nb_occurence)
