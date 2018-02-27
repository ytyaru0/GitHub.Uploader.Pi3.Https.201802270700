#!python3
#encoding:utf-8
import os.path
import configparser
import shlex
import subprocess
import dataset
from web.service.github.api.v3.authentication.BasicAuthentication import BasicAuthentication
from web.service.github.api.v3.authentication.TwoFactorAuthentication import TwoFactorAuthentication
from web.service.github.api.v3.authentication.OAuthAuthentication import OAuthAuthentication
import web.service.github.api.v3.Client
"""
import database.language.Main
import database.api.Main
import database.gnu_license.create.Main
import database.gnu_license.Main
import database.license.Main
import database.account.Main
import database.repo.insert.command.repositories.Inserter
"""
import web.log.Log
import setting.Setting
import glob

from database.init.DbInitializer import DbInitializer
from database.init.AccountsDbInitializer import AccountsDbInitializer as Accounts
from database.init.ApisDbInitializer import ApisDbInitializer as Apis
from database.init.GnuLicensesDbInitializer import GnuLicensesDbInitializer as GnuLicenses
from database.init.LanguagesDbInitializer import LanguagesDbInitializer as Languages
from database.init.LicensesDbInitializer import LicensesDbInitializer as Licenses
from database.init.OtherRepositoriesDbInitializer import OtherRepositoriesDbInitializer as OtherRepositories
from database.init.RepositoriesDbInitializer import RepositoriesDbInitializer as Repositories
from database.init.ContributionsDbInitializer import ContributionsDbInitializer as Contributions

class DatabaseMeta(type):
    def __new__(cls, name, bases, attrs):
        #attrs['Initializers'] = {} # 3.6以降でないと順序保持されない。DB依存関係があるので順序必要
        from collections import OrderedDict
        attrs['_{0}__Initializers'.format(name)] = OrderedDict() # Database.__Initializers 実装
        for initer in [Apis(), Accounts(), Languages(), GnuLicenses(), Licenses(), OtherRepositories(), Repositories(), Contributions()]:
            attrs['_{0}__Initializers'.format(name)][initer.DbId] = initer # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer()
            #attrs['_{0}__Initializers'.format(name)][initer.DbId] = initer # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer()
            #attrs[initer.DbId] = property(lambda : initer) # Database.Accounts = property(lambda : database.init.AccountsDbInitializer.AccountsDbInitializer())
        return type.__new__(cls, name, bases, attrs)
        """
        for initer in [Apis(), Accounts(), Languages(), GnuLicenses(), Licenses(), OtherRepositories(), Repositories()]
            initer.CreateDb()
            initer.ConnectDb()
            #initer.Db.query('PRAGMA foreign_keys = false')
            initer.CreateTable()
            initer.InsertInitData()
            #initer.Db.query('PRAGMA foreign_keys = true')
            attrs[initer.DbId] = property(lambda : initer)
            #self[initer.DbId] = initer # プロパティにしたいが方法不明。これは属性値になってしまう
            #self.__dbs[initer.DbId] = initer # Db, DbFilePathなどが得られる
            # https://www.python-izm.com/advanced/property/
            #property(get_url, set_url, del_url, 'url Property')
            #property(lambda self x: x+1)
        return type.__new__(cls, name, bases, attrs)
        """
    def __init__(cls, name, bases, attrs):
        #attrs['BusinessLogics'.format(name)] = {}
        for initer in attrs['_{0}__Initializers'.format(name)]:
            # DB初期化処理
            initer.CreateDb()
            initer.ConnectDb()
            #initer.Db.query('PRAGMA foreign_keys = false')
            initer.CreateTable()
            initer.InsertInitData()
            #initer.Db.query('PRAGMA foreign_keys = true')
            attrs[initer.DbId] = property(lambda cls: initer.Db) # Database.Accounts = property(lambda : database.biz.Accounts.Accounts())

            # ビジネスロジック参照用プロパティ実装
            #import importlib
            #module = importlib.import_module('database.biz.{0}.{0}'.format(initer.DbId))
            #bizClass = getattr(module, initer.DbId)
            #bizIns = bizClass(initer.Db) # dataset.connect()を渡す
            #attrs[initer.DbId] = property(lambda cls: bizIns) # Database.Accounts = property(lambda : database.biz.Accounts.Accounts())
            #attrs['_{0}__BusinessLogics'.format(name)][initer.DbId] = module[initer.DbId]() # Database.BusinessLogics['Accounts'] = database.biz.Accounts.Accounts.Accounts()
            attrs['_{0}__Initializers'.format(name)][initer.DbId] = property(lambda cls: initer)

    # Singleton:
    # from database.Database import Database as Db
    # ins = Db()
    # Db().Accounts # property
    # Db().Accounts.GetAccounts() # BusinessLogic
    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
            #cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
        """
        path, namespace, module_name, class_name, method_name = self.__GetIds_ActionByPy(action)
        if os.path.isdir(path):
            # モジュール読込
            import importlib
            module = importlib.import_module(namespace_insert_py + module_name)
            # クラスのインスタンス生成
            cls = module[module_name](self.DbFilePath)
            # メソッドの取得と実行
            method = getattr(cls, method_name)
            method()
        """
    """
    def __GetClient(self, username=None):
        if None is username: account = self.__dbs['account']['Accounts'].find().next()
        else:                account = self.__dbs['account']['Accounts'].find_one(Username=username)
        twofactor = self.__dbs['account']['TwoFactors'].find_one(AccountId=account['Id'])
        authentications = []
        if None is not twofactor:
            authentications.append(TwoFactorAuthentication(account['Username'], account['Password'], twofactor['Secret']))
        else:
            authentications.append(BasicAuthentication(account['Username'], account['Password']))
        return web.service.github.api.v3.Client.Client(self, authentications)
    """
