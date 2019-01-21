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
session.execute(""" CREATE FUNCTION IF NOT EXISTS timeAgo(seconds int)
  CALLED ON NULL INPUT
  RETURNS timestamp
  LANGUAGE java AS '
    long now = System.currentTimeMillis();
    if (seconds == null)
      return new Date(now);
    return new Date(now - (seconds.intValue() * 1000));
  ';""")

session.shutdown()
cluster.shutdown()
