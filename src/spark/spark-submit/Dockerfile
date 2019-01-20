FROM openjdk:8

# install jsk and spark
RUN wget http://mirrors.standaloneinstaller.com/apache/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
RUN tar -xvzf spark-2.4.0-bin-hadoop2.7.tgz
RUN rm spark-2.4.0-bin-hadoop2.7.tgz


COPY ./spark_submit.sh /spark-2.4.0-bin-hadoop2.7/spark_submit.sh

RUN chmod 700 /spark-2.4.0-bin-hadoop2.7/spark_submit.sh

WORKDIR /spark-2.4.0-bin-hadoop2.7


ENTRYPOINT ["./spark_submit.sh"]
