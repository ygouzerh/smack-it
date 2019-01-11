
from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'France', '1F600', 30, toTimestamp(now()));""")
session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'France', '1F922', 7, toTimestamp(now()));""")
session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'France', '1F629', 3, toTimestamp(now()));""")
session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'France', '1F609', 9, toTimestamp(now()));""")
session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'France', '1F621', 7, toTimestamp(now()));""")
# session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'France', '1F621', 7, '2019-01-09 13:30:44.234');""")
session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'United States', '1F62D', 12, toTimestamp(now()));""")
session.execute("""INSERT INTO emoji_package (id, pays, id_emoji, nb_occurence, package_date) VALUES (uuid(), 'United States', '1F60A', 7, toTimestamp(now()));""")
