#!python3
#encoding:utf-8
import sys
import subprocess
import shlex
import os.path
import getpass
import dataset
import database.TsvLoader

class Main:
    def __init__(self, db_path):
        self.__db_path = db_path
        self.__path_this_dir = os.path.abspath(os.path.dirname(__file__))

    def Run(self):
        self.__ConnectDb()
        # Create文
        for filename in ['Apis']:
            path = os.path.join(self.__path_this_dir, 'sql/create/{0}.sh'.format(filename))
            self.__ExecuteSqlFile(path)
        # Insert文
        self.__Insert()
#        self.__Check() # Check.shで正常に文字列結合できずパスを作成できない。

    # DBファイル生成＆接続
    def __ConnectDb(self):
        if not os.path.isfile(self.__db_path):
            with open(self.__db_path, 'w') as f: pass
        self.__db = dataset.connect('sqlite:///' + self.__db_path)

    # SQLファイル内文発行
    def __ExecuteSqlFile(self, sql_path):
        with open(sql_path, 'r') as f:
            sql = f.read()
            self.__db.query(sql)

    # 初期値の挿入
    def __Insert(self):
        tables = ['Apis']
        for table in tables:
#            path_tsv = os.path.join(self.__path_this_dir, "res/tsv/{0}.tsv".format(table))
            path_tsv = os.path.join(self.__path_this_dir, "tsv/meta_{0}.tsv".format(table))
            loader = database.TsvLoader.TsvLoader()
            loader.ToSqlite3(path_tsv, self.__db_path, table)

    # 確認用SQL発行
    def __Check(self):
        path = os.path.join(self.__path_this_dir, 'sql/check/check.sql')
        self.__ExecuteSqlFile(path)

    """
    def Run(self):
        self.__Create()
        self.__Insert()
#        self.__Check() # Check.shで正常に文字列結合できずパスを作成できない。

    def __Create(self):
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(os.path.join(self.__path_this_dir, "CreateTable.sh"), self.__db_path)))

    def __Insert(self):
        tables = ['Apis']
        for table in tables:
            path_tsv = os.path.join(self.__path_this_dir, "res/tsv/{0}.tsv".format(table))
            loader = database.TsvLoader.TsvLoader()
            loader.ToSqlite3(path_tsv, self.__db_path, table)

    def __Check(self):
        # sqlite3: Error: too many options:
#        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(os.path.join(self.__path_this_dir, "Check.sh"), self.__db_path)))
#        cmd = "sqlite3 \"{0}\" < \"{1}\"".format(self.__db_path, os.path.join(self.__path_this_dir, "res/sql/check/check.sql"))
#        cmd = "sqlite3 {0} < {1}".format(self.__db_path, os.path.join(self.__path_this_dir, "res/sql/check/check.sql"))
#        cmd = 'sqlite3 "{0}" "{1}"'.format(self.__db_path, os.path.join(self.__path_this_dir, "res/sql/check/check.sql"))
#        cmd = 'sqlite3 {0} < {1}'.format(self.__db_path, os.path.join(self.__path_this_dir, "res/sql/check/check.sql"))
#        cmd = 'sqlite3 {0} < \"{1}\"'.format(self.__db_path, os.path.join(self.__path_this_dir, "res/sql/check/check.sql"))
#        print(cmd)
#        subprocess.call(shlex.split(cmd))
        pass
    """

