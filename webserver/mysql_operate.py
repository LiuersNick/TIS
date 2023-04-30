import pymysql
from mysql_config import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB


class MysqlDb():
    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db
        )
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def select_db(self, sql):
        self.conn.ping(reconnect=True)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def execute_db(self, sql):
        try:
            self.conn.ping(reconnect=True)
            self.cur.execute(sql)
            self.conn.commit()
            return 'Execute success!'
        except Exception as e:
            self.conn.rollback()
            return 'Execute failed, rolling back...'

# Import mysql_operate.py at first, then use mysql_operate.db.<Method>() to execute sql or select results.
db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB)

