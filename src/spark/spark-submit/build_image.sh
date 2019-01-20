
sudo docker build . -t spark-submit
sudo docker tag spark-submit machine424/spark-submit

sudo docker push machine424/spark-submit
