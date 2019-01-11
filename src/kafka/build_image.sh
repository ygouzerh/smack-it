

docker build . -t tweet-producer
docker tag tweet-producer machine424/tweet-producer

docker push machine424/tweet-producer
