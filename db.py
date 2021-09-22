#!/usr/bin/env python3

import sqlite3
from connection import Connection
import time
import os

READ = os.getenv('READ', None) is not None
WRITE = os.getenv('WRITE', None) is not None

class Database:
  def __init__(self):
    self.serial_connection = Connection('/dev/ttyACM0')
    self.conn = sqlite3.connect('serial_archive.db', check_same_thread=False)
    self.cur = self.conn.cursor() 
    self.init_db()
    self.write_db(0.1)

  def create_table(self, table):
    try:
      self.cur.execute(table)
    except AttributeError:
      pass

  def init_db(self):
    data_table = """CREATE TABLE IF NOT EXISTS serial_data (
                    time      text,
                    id        integer, 
                    pres      real,
                    gas_res   real,
                    a_temp    real,
                    a_hum     real,
                    gd_temp   real,
                    gd_hum    real,
                    gps_lat   real,
                    gps_lon   real,
                    gps_angle real,
                    gps_speed real);"""
    self.create_table(data_table)

  def append_td(self, data: dict):
    sql = "INSERT INTO serial_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
    sql_data = [v for k,v in data.items()]
    self.cur.execute(sql, sql_data)
    self.conn.commit()

  def read_db(self, n):
    acc = []
    for row in self.cur.execute('SELECT * FROM serial_data'):
      acc.append(row)
    if n == 0:
      return acc
    else:
      return acc[len(acc)-n:len(acc)]

  def write_db(self, delay_minutes): 
    time.sleep(delay_minutes*60)
    x = self.serial_connection.read(False, True) 
    self.append_td(x)
    print("\n%s - data has been written to the database" % x['time'])


if __name__ == "__main__":
  db = Database()
  if WRITE:
    while (1):
      db.write_db(0.1) 
  if READ:
    # usage:
    # n -> returns last n elements
    # 0 -> returns whole database
    import sys  
    n = int(sys.argv[-1])
    print(db.read_db(n))