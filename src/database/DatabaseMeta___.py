#!python3
#encoding:utf-8
"""
import os.path
import configparser
import shlex
import subprocess
import dataset
from web.service.github.api.v3.authentication.BasicAuthentication import BasicAuthentication
from web.service.github.api.v3.authentication.TwoFactorAuthentication import TwoFactorAuthentication
from web.service.github.api.v3.authentication.OAuthAuthentication import OAuthAuthentication
import web.service.github.api.v3.Client
import database.language.Main
import database.api.Main
import database.gnu_license.create.Main
import database.gnu_license.Main
import database.license.Main
import database.account.Main
import database.repo.insert.command.repositories.Inserter
import web.log.Log
import setting.Setting
import glob
"""
from database.init.DbInitializer import DbInitializer
from database.init.AccountsDbInitializer import AccountsDbInitializer as Accounts
from database.init.ApisDbInitializer import ApisDbInitializer as Apis
from database.init.GnuLicensesDbInitializer import GnuLicensesDbInitializer as GnuLicenses
from database.init.LanguagesDbInitializer import LanguagesDbInitializer as Languages
from database.init.LicensesDbInitializer import LicensesDbInitializer as Licenses
from database.init.OtherRepositoriesDbInitializer import OtherRepositoriesDbInitializer as OtherRepositories
from database.init.RepositoriesDbInitializer import RepositoriesDbInitializer as Repositories
from database.init.ContributionsDbInitializer import ContributionsDbInitializer as Contributions
from collections import OrderedDict

class DatabaseMeta(type):
    def __new__(cls, name, bases, attrs):

        # 単一DB
        attrs['_{0}__Initializers'.format(name)] = OrderedDict() # Database.__Initializers 実装
        for initer in [Apis(), Accounts(), Languages(), GnuLicenses(), Licenses(), OtherRepositories()]:
            print(type(initer), initer)
            attrs['_{0}__Initializers'.format(name)][initer.DbId] = initer # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer()
        return type.__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        # 単一DB
        print(attrs)
        for initer in attrs['_{0}__Initializers'.format(name)].values():
            initer.Initialize()
            attrs[initer.DbId] = property(lambda cls: initer.Db) # Database.Accounts =  = database.init.AccountsDbInitializer.AccountsDbInitializer().Db = dataset.connect('sqlite:///' + '.../')
            #attrs['_{0}__Initializers'.format(name)][initer.DbId] = property(lambda cls: initer) # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer().Db = dataset.connect('sqlite:///' + '.../')

        print(type(attrs['_{0}__Initializers'.format(name)]))
        
        if 0 == attrs['_{0}__Initializers'.format(name)]['Accounts'].Db['Accounts'].count(): raise Exception('登録ユーザがひとつもありません。UserRegister.pyで登録してから再実行してください。')
        #if 0 == attrs['Accounts'].count(): raise Exception('登録ユーザがひとつもありません。UserRegister.pyで登録してから再実行してください。')

        # ユーザ単位DB（AccountsDB生成後でないと作れない）
        attrs['_{0}__InitializersByMultiUsers'.format(name)] = OrderedDict()
        accountsDb = attrs['_{0}__Initializers'.format(name)]['Accounts'].Db
        for initer in [cls(accountsDb) for cls in [Repositories, Contributions]]:
            attrs['_{0}__InitializersByMultiUsers'.format(name)][initer.DbId] = initer # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer()
        for initer in attrs['_{0}__InitializersByMultiUsers'.format(name)].values():
            initer.Initialize()
            attrs[initer.DbId] = property(lambda cls: initer.Db) # Database.Accounts =  database.init.AccountsDbInitializer.AccountsDbInitializer().Db = dataset.connect('sqlite:///' + '.../')
            #attrs['_{0}__Initializers'.format(name)][initer.DbId] = property(lambda cls: initer) # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer().Db = dataset.connect('sqlite:///' + '.../')

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
