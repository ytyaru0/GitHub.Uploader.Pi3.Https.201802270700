#!python3
#encoding: utf-8
import requests
from bs4 import BeautifulSoup
import dataset
import datetime
import os.path
from database.Database import Database as Db

class Creater(object):
    def __init__(self, db):
        self.__db = db # db = {'user1': dataset.connect('sqlite:///' + '.../GitHub.Contributions.{user}.sqlite3'), ...} 呼出元: DbInitializer.__ActionByPy() 作成元: ContributionsDbInitializer
    """
    ContributionsDBのテーブルを生成する。（全ユーザ分）
    """
    def Creater(self):
        for username in db.keys(): self.__Create(username)

    def __Create(self, username):
        sql = """
create table "Contributions"(
    "Id"                integer primary key,
    "Date"              text not null,
    "Count"             integer not null check(0 <= "Count")
);
"""
        self.__db[username].query(sql)

