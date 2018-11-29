from cassandra.cluster import Cluster
import sched, time

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

s = sched.scheduler(time.time, time.sleep)
def repeat(sc):
    print("----"+datetime.datetime.now().time()+"----")
    rows = session.execute("""SELECT * FROM pays""");
    for row in rows:
        print("Pays : {} . Emojis : {}".format(row.nom_pays, row.emojis))
    s.enter(60, 1, repeat, (sc,))

s.enter(60, 1, repeat, (s,))
s.run()
