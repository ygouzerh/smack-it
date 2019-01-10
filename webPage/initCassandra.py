# -*- coding: utf-8 -*-

from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect()

session.execute("""DROP KEYSPACE "emoji";""")
#création du keyspace
session.execute("""CREATE KEYSPACE "emoji" WITH replication = {'class' : 'SimpleStrategy', 'replication_factor' : 1};""")
session.execute("""USE emoji;""")
#création table
session.execute("""CREATE TABLE PAYS(id text PRIMARY KEY, nom_pays text,lat double,long double,emojis text);""")
session.execute("INSERT INTO pays (id,nom_Pays,lat,long,emojis) VALUES ('1','France',47.0781336,2.3282634,'1F600');")
session.execute("INSERT INTO pays (id,nom_Pays,lat,long,emojis) VALUES ('2','Maroc',30.9355913,-6.9676089,'1F600');")
session.execute("INSERT INTO pays (id,nom_Pays,lat,long,emojis) VALUES ('3','Canada',56.7050486,-111.4404514,'1F600');")
session.execute("INSERT INTO pays (id,nom_Pays,lat,long,emojis) VALUES ('4','USA',36.2449313,-113.7316141,'1F600');")
