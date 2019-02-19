FROM centos
RUN mkdir -p /root/exporter/
WORKDIR /root/exporter
COPY ./localtime /etc
COPY ./trx-remittance.py .
RUN yum clean all
RUN yum -y update
RUN yum install -y epel-release
RUN yum install -y python
RUN yum install -y python-requests
RUN yum install -y python-pip
RUN pip install prometheus_client
RUN pip install mysql-connector-python --allow-external mysql-connector-python
RUN pip install pymysql
RUN pip install requests
RUN yum clean all
CMD python trx-remittance.py
