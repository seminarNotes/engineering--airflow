FROM apache/airflow:2.8.0

USER root

RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y default-libmysqlclient-dev

CMD ["webserver"]
