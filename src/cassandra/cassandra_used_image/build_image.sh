docker build . -t modified-cassandra
docker tag modified-cassandra machine424/modified-cassandra

docker push machine424/modified-cassandra
