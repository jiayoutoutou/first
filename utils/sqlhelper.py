
class SqlHelper:
    def __init__(self):
        # 读取配置文件
        self.connect()
    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,arg):
        self.cursor.execute(sql, arg)
        ret = self.cursor.fetchall()
        return ret
    def get_one(self,sql,arg):
        self.cursor.execute(sql,arg)
        ret=self.cursor.fetchone()
        return ret
    def modify(self,sql,arg):
        self.cursor.execute(sql,arg)
        self.conn.commit()
        return self.cursor.lastrowid
    def multiple_modify(self,sql,arg):
        self.cursor.executemany(sql,arg)
        self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()

import pymysql
def get_list(sql,*arg):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,arg)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    return ret
def get_one(sql,*arg):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, arg)
    ret = cursor.fetchone()
    cursor.close()
    conn.close()
    return ret
def modify(sql,*arg):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,arg)
    new_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return new_id