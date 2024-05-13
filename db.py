import sqlite3
import pymysql

class DBHelper:
    # Interface to get database records

    def __init__(self):
        self.host = "192.168.1.4"
        self.user = "oliver"
        self.password = "Tyranno02"
        self.db = "FinansDB"
        print("instansierer DBHelper")

    def __connect__(self):
        #print('Er i connect')
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.
                                   DictCursor)
        #self.con = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.db)
        #self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        print('Er i Fetch')
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def fetchone(self,sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchone()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()

    def executemany(self,sql,l):
        self.__connect__()
        self.cur.executemany(sql,l)
        self.con.commit()
        self.__disconnect__()