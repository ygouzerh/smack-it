

docker build . -t app-f
docker tag app-f machine424/app-f

docker push machine424/app-f
