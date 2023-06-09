# -*- coding:utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
mysql client

  - save data to mysql

@author guoweikuang
"""
import pymysql
from .config import Config
from .logger import logger
from .bloom_filter import is_repeat


class Client(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Client, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MysqlClient(Client):
    def __init__(self, pool_num=5):
        self.pool_num = pool_num
        self.config = Config()

        # self.conn = pymysql.connect(
        #     host=self.config.host,
        #     user=self.config.username,
        #     password=self.config.password,
        #     port=self.config.port,
        #     db=self.config.db,
        #     charset=self.config.charset
        # )
        # self.cur = self.conn.cursor()

    def client(self):
        return None
        # self.conn = pymysql.connect(
        #     host=self.config.host,
        #     user=self.config.username,
        #     password=self.config.password,
        #     port=self.config.port,
        #     db=self.config.db,
        #     charset=self.config.charset
        # )
        # self.cur = self.conn.cursor()
        # return self.cur

    def save_data_to_mysql(self, *args, **kwargs):
        """save data to mysql

        :param args:
        :param kwargs:
        :return:
        """
        title, pub_time, comment_num, like_num, url = args
        try:
            sql = "INSERT INTO content(title, pub_time, comment_num, like_num, url) VALUES(%s, %s, %s, %s, %s);"
            if is_repeat(url):
                return
            self.cur.execute(sql, (title.strip(), str(pub_time), str(comment_num), str(like_num), url))
            self.conn.commit()

        except Exception as e:
            logger.error('mysql error: %s', e)
            self.conn.rollback()

    def close_mysql(self):
        return
        #self.conn.close()
        # self.cur.close()


def get_mysql_client():
    client = MysqlClient()
    return client


def get_text_from_mysql(table_name, start_time, end_time):
    """获取指定时间段数据

    :param database_name: 数据库名称
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return:
    """
    client = get_mysql_client()
    rows = []
    sql = "SELECT title, comment_num, like_num, pub_time FROM %s WHERE pub_time BETWEEN '%s' AND '%s'"
    sql = sql % (table_name, start_time, end_time)
    try:
        client.cur.execute(sql)
        #client.cur.execute(sql, (database_name, start_time, end_time))
        rows = client.cur.fetchall()

    except Exception as e:
        logger.error("mysql select error: %s", e)
        client.close_mysql()

    return rows


def get_from_mysql(table_name, start_time, end_time):
    """获取指定时间段数据

    :param database_name: 数据库名称
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return:
    """
    client = get_mysql_client()
    rows = []
    sql = "SELECT title, pub_time, comment_num, like_num, url FROM %s WHERE pub_time BETWEEN '%s' AND '%s'"
    sql = sql % (table_name, start_time, end_time)
    try:
        client.cur.execute(sql)
        #client.cur.execute(sql, (database_name, start_time, end_time))
        rows = client.cur.fetchall()

    except Exception as e:
        logger.error("mysql select error: %s", e)
        client.close_mysql()

    return rows