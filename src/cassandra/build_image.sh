

# docker build . -t create-table-cassandra
# docker tag create-table-cassandra machine424/create-table-cassandra
#
# docker push machine424/create-table-cassandra


docker build . -t dispay-table-cassandra
docker tag dispay-table-cassandra machine424/dispay-table-cassandra

docker push machine424/dispay-table-cassandra
