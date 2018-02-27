#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.init.DbInitializer import DbInitializer
import os.path
from setting.Config import Config
#import setting.Setting
import dataset

# ユーザ単位DB（※AccountsDBの初期化後であること（DatabaseMetaの呼出順に注意））
# DbInitializerとの違いは、ユーザ単位のDBをdictで持つこと。
# * DbFileName = {f'{user}': f'GitHub.{DbId}.{user}.sqlite3', ... }
# * DbFilePath = {f'{user}': os.path.join(setting.DbPath, DbFileName[f'{user}']), ... }
# * Db         = {f'{user}': dataset.connect('sqlite:///' + self.__filepaths[f'{user}']), ...}
class DbInitializerByMultiUsers(DbInitializer):
    def __init__(self, accountsDb):
#    def __init__(self):
        super().__init__()
        self.__accountsDb = accountsDb
        self.__filenames = {}
        self.__CreateFilenames()
        self.__filepaths = {}
        self.__CreateFilepath()
        self.__dbs = {}
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', self.__accountsDb['Accounts'].count(), self.DbFilePath)

    def Initialize(self):
        self._CreateDb()
        self._ConnectDb()
        for username in self.__GetUsernames(): self.Db[username].query('PRAGMA foreign_keys = false')
        #self.__CreateTable()
        #self.__InsertInitData()
        #print(type(super().__name__))
        #print(dir(super())
        #print(type(super(DbInitializer, self)))
        #super(DbInitializer, self).__CreateTable()
        #super(DbInitializer, self).__InsertInitData()
        #super().super().__CreateTable()
        #super().super().__InsertInitData()
        #super().__CreateTable()
        #super().__InsertInitData()
        self._CreateTable()
        self._InsertInitData()
        for username in self.__GetUsernames(): self.Db[username].query('PRAGMA foreign_keys = true')

    def _CreateDb(self):
        for username in self.DbFileName:
            if not os.path.isfile(self.__filepaths[username]):
                with open(self.__filepaths, 'w') as f: pass

    def _ConnectDb(self):
        for username in self.DbFileName:
            self.__dbs[username] = dataset.connect('sqlite:///' + self.__filepaths[username])

    @property
    def DbFileName(self): return self.__filenames
    @property
    def DbFilePath(self): return self.__filepaths
    @property
    def Db(self): return self.__dbs

    def __CreateFilepath(self):
        #import setting.Setting
        #setting = setting.Setting.Setting()
        for username in self.__GetUsernames():
            self.__filepaths[username] = os.path.join(Config()['Path']['Db'], self.__filenames[username])
            #self.__filepaths[username] = os.path.join(Config().PathDb, self.__filenames[username])
            #self.__filepaths[username] = os.path.join(setting.DbPath, self.__filenames[username])

    def __CreateFilenames(self):
        for username in self.__GetUsernames():
            self.__filenames[username] = 'GitHub.{0}.{1}.sqlite3'.format(self.DbId, username)

    def __GetUsernames(self):
        #from database.Database import Database as Db # ImportError: cannot import name 'Database'
        #for username in Db().Accounts['Accounts'].find()['Username']: yield username
        #for username in self.__accountsDb['Accounts'].find()['Username']: yield username
        for account in self.__accountsDb['Accounts'].find(): yield account['Username']

