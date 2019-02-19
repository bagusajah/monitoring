#!/usr/bin/python

from prometheus_client import start_http_server, Gauge
from threading import Thread
import pymysql.cursors, time, sys, logging, time, requests

remit_total = Gauge('remit_daily_total', 'Total transaksi hari ini')
remit_sukses = Gauge('remit_daily_sukses', 'Total transaksi sukses hari ini')
remit_gagal = Gauge('remit_daily_gagal', 'Total transaksi gagal hari ini')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def my_connection(fungsi):
    global my_conn
    fungsi = fungsi

    try:
           my_conn = pymysql.connect(host='172.16.80.126', user='grafana', password='kjw#JHE382c', db='mw_remittance', cursorclass=pymysql.cursors.DictCursor)
           logger.info(time.ctime() + ' -> Functions ' + fungsi + ' success connect to database...')
    except:
         logger.error(time.ctime() + ' -> Failed connect to database...')
         sys.exit()

def	daily_remit_trx():
    total = sukses = gagal = 0
    fungsi = 'daily_remit'

    my_connection(fungsi)
    my_cur = my_conn.cursor()
    my_cur.execute("SELECT STATUS, COUNT(*) FROM MTCN_TRANSACTION_DETAILS WHERE(1=1) AND MTCN_TRANSACTION_DETAILS.TYPE=1 AND DATE(CREATED_DATE) = CURDATE() GROUP BY STATUS")

    rows = my_cur.fetchall()

    for data in rows:
        if data['STATUS'] == 0:
           sukses = data['COUNT(*)']
        if data['STATUS'] != 0:
           gagal = data['COUNT(*)']

    total = sukses + gagal
    remit_total.set(total)
    remit_sukses.set(sukses)
    remit_gagal.set(gagal)
    my_cur.close()

if __name__ == '__main__':

    start_http_server(9982)

    while True:
         try:
             daily_mon_remit_thread = Thread(target=daily_remit_trx)
             daily_mon_remit_thread.start()
             time.sleep(10)

         except KeyboardInterrupt:
             logger.info(time.ctime() + ' -> Trx exporter was stop...')
             sys.exit()
    conn.close()
