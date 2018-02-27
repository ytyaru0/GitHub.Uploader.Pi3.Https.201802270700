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
"""
"""
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
#from database.DatabaseMeta import DatabaseMeta
#from database.init.DbInitializer import DbInitializer
#from database.init.ApisDbInitializer import ApisDbInitializer
#from database.init.GnuLicensesDbInitializer import GnuLicensesDbInitializer

class Database(metaclass=DatabaseMeta):
#class Database:
    def __init__(self):
#    def __init__(self, path_dir_root):
        self.__path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#        self.__setting = setting.Setting.Setting(path_dir_root)
#        self.__setting = setting.Setting.Setting(os.path.join(path_dir_root, "res/"))
        self.__setting = setting.Setting.Setting()
        self.__path_dir_this = os.path.abspath(os.path.dirname(__file__))
        self.__path_dir_db = self.__setting.DbPath
        """
        self.__files = {
            'lang': 'GitHub.Languages.sqlite3',
            'api': 'GitHub.Apis.sqlite3',
            'gnu_license': 'GNU.Licenses.sqlite3',
            'account': 'GitHub.Accounts.sqlite3',
            'license': 'GitHub.Licenses.sqlite3',
            'other_repo': 'GitHub.Repositories.__other__.sqlite3',
            'repo': 'GitHub.Repositories.{user}.sqlite3',
        }
        self.__dbs = {
            'lang': None,
            'api': None,
            'gnu_license': None,
            'account': None,
            'license': None,
            'other_repo': None,
            'repo': None,
            'repos': None,
        }
        """
        """
        self.__lang = None
        self.__api = None
        self.__gnu_license = None
        self.__account = None
        self.__license = None
        self.__other_repo = None
        self.__repo = None
        self.__repos = {}
        """
    """
    @property
    def Paths(self): return self.__files
    @property
    def Languages(self): return self.__dbs['language']
    @property
    def Apis(self): return self.__dbs['api']
    @property
    def GnuLicenses(self): return self.__dbs['gnu_license']
    @property
    def Accounts(self): return self.__dbs['account']
    @property
    def Licenses(self): return self.__dbs['license']
    @property
    def OtherRepositories(self):  return self.__dbs['other_repo']
    @property
    def Repositories(self): return self.__dbs['repos']
    """
    """
    @property
    def Paths(self):
        return self.__files
    @property
    def Languages(self):
        return self.__lang
    @property
    def Apis(self):
        return self.__api
    @property
    def GnuLicenses(self):
        return self.__gnu_license
    @property
    def Accounts(self):
        return self.__account
    @property
    def Licenses(self):
        return self.__license
    @property
    def OtherRepositories(self):
        return self.__other_repo
    @property
    def Repositories(self):
        return self.__repos
    """
    
    def Initialize(self):
        pass
        """
        for initer in self.__Initializers.values():
            initer.CreateDb()
            initer.ConnectDb()
            #initer.Db.query('PRAGMA foreign_keys = false')
            initer.CreateTable()
            initer.InsertInitData()
            #initer.Db.query('PRAGMA foreign_keys = true')
        """
        """
        from database.init.DbInitializer import DbInitializer
        from database.init.AccountsDbInitializer import AccountsDbInitializer as Accounts
        from database.init.ApisDbInitializer import ApisDbInitializer as Apis
        from database.init.GnuLicensesDbInitializer import GnuLicensesDbInitializer as GnuLicenses
        from database.init.LanguagesDbInitializer import LanguagesDbInitializer as Languages
        from database.init.LicensesDbInitializer import LicensesDbInitializer as Licenses
        from database.init.OtherRepositoriesDbInitializer import OtherRepositoriesDbInitializer as OtherRepositories
        from database.init.RepositoriesDbInitializer import RepositoriesDbInitializer as Repositories

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
        pass
        """
        """
        for initer in [ApisDbInitializer(), GnuLicensesDbInitializer()]
            initer.CreateDb()
            initer.ConnectDb()
            initer.CreateTable()
            initer.InsertInitData()
            self[initer.DbId] = initer # プロパティにしたいが方法不明。これは属性値になってしまう
            #self.__dbs[initer.DbId] = initer # Db, DbFilePathなどが得られる
            # https://www.python-izm.com/advanced/property/
            #property(get_url, set_url, del_url, 'url Property')
            #property(lambda self x: x+1)
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
    # 1. 全DBのファイルパス作成
    # 2. マスターDBファイルがないなら
    # 2-1. マスターDBファイル作成
    # 2-2. マスターDBデータ挿入
    # 3. アカウントDBがないなら
    # 3-1. アカウントDBファイル作成
    def Initialize(self):
        for key in self.__files.keys():
            self.__files[key] = os.path.join(self.__path_dir_db, self.__files[key])
        self.__OpenDb()

    def __OpenDb(self):
        # マスターDB生成（ファイル、テーブル、データ挿入）
        if None is self.__dbs['lang']:
            if not os.path.isfile(self.__files['lang']):
                m = database.language.Main.Main(self.__files['lang'])
                m.Run()
            self.__dbs['lang'] = dataset.connect('sqlite:///' + self.__files['lang'])
        if None is self.__dbs['api']:
            if not os.path.isfile(self.__files['api']):
                m = database.api.Main.Main(self.__files['api'])
                m.Run()
            self.__dbs['api'] = dataset.connect('sqlite:///' + self.__files['api'])
        if None is self.__dbs['gnu_license']:
            if not os.path.isfile(self.__files['gnu_license']):
                m = database.gnu_license.Main.Main(self.__files['gnu_license'])
                m.Run()
            self.__dbs['gnu_license'] = dataset.connect('sqlite:///' + self.__files['gnu_license'])

        # アカウントDB生成（ファイル、テーブル作成。データ挿入はCUIにて行う）
        if None is self.__dbs['account']:
            if not os.path.isfile(self.__files['account']):
                m = database.account.Main.Main(self.__files['account'])
                m.Create()
            self.__dbs['account'] = dataset.connect('sqlite:///' + self.__files['account'])

        # DB作成にTokenが必要なもの
        if 0 < self.__dbs['account']['Accounts'].count():
            # ライセンスDB生成（ファイル、テーブル作成。データ挿入）
            self.__CreateLicenseDb()

            # 自分アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）
            for account in self.__dbs['account']['Accounts'].find():
                #self.__OpenRepo(account['Username'])
                self.__CreateRepositoryDb(account['Username'])
            # 他者アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）

    # ライセンスDB作成
    def __CreateLicenseDb(self):
        if not(os.path.isfile(self.__files['license'])):
            web.log.Log.Log().Logger.debug(self.__files['license'])
            client = self.__GetClient()
            l = database.license.Main.Main(self, client)
            l.Create()
            self.__dbs['license'] = dataset.connect('sqlite:///' + self.__files['license'])
            l.Insert()
        if not 'license' in self.__dbs.keys():
            self.__dbs['license'] = dataset.connect('sqlite:///' + self.__files['license'])

    # 各ユーザのリポジトリDB作成
    def __CreateRepositoryDb(self, username):
        if None is self.__dbs['repos']: self.__dbs['repos'] = {}
        dbname = 'repo'
        path_db = self.__files[dbname].replace('{user}', username)
        if not os.path.isfile(path_db):
            # 空ファイル作成
            with open(path_db, 'w') as f: pass
            # DB接続
            self.__dbs['repos'][username] = dataset.connect('sqlite:///' + path_db)
            self.__dbs['repos'][username].query('PRAGMA foreign_keys = false')
            # テーブル作成（CreateTable文）
            for path_sql in self.__GetCreateTableSqlFilePaths(dbname):
                self.__ExecuteSqlFile(dbname, path_sql)
            # 初期値の挿入（Insert文）
            cilent = self.__GetClient(username) # 指定アカウントを用いる
            inserter = database.repo.insert.command.repositories.Inserter.Inserter(self, username, client)
            inserter.Insert()
            self.__dbs['repos'][username].query('PRAGMA foreign_keys = true')
        if not username in self.__dbs['repos'].keys():
            self.__dbs['repos'][username] = dataset.connect('sqlite:///' + path_db)

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
        
    # パス取得（テーブル作成用SQLファイル）
    def __GetCreateTableSqlFilePaths(self, dbname):
        path = os.path.join(self.__path_dir_this, dbname, 'sql', 'create')
        for path_sql in glob.glob(os.path.join(path + '*.sql')): yield path_sql

    # パス取得（初期値挿入用TSVファイル）
    def __GetInsertTsvFilePaths(self, dbname):
        path = os.path.join(self.__path_dir_this, dbname, 'tsv')
        for path_tsv in glob.glob(os.path.join(path + '*.tsv')): yield path_tsv
        return self.__dbs[dbname]

    # SQLファイル発行
    def __ExecuteSqlFile(self, dbname, sql_path):
        with open(sql_path, 'r') as f:
            sql = f.read()
            self.__dbs[dbname].query(sql)
    """






    """
    def __OpenDb(self):
        # 基本DB作成（順序あり）
        for name in ['language','api','gnu_license','account']:
            if None is self.__dbs[name]:
                self.__CreateDb(name)
        # DB作成にTokenが必要なもの（他DB依存）
        if 0 < self.__dbs['account']['Accounts'].count():
            self.__CreateLicenseDb()
            # 自分アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）
            for account in self.__dbs['account']['Accounts'].find():
                self.__CreateRepositoryDb(account['Username'])
            #for account in self.__account['Accounts'].find():
                #self.__OpenRepo(account['Username'])
            # 他者アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）

    # DBファイル生成
    def __CreateDb(self, dbname):
        if not os.path.isfile(self.__files[dbname]):
            # 空ファイル作成
            with open(self.__dbs[dbname], 'w') as f: pass
            # DB接続
            self.__dbs[dbname] = dataset.connect('sqlite:///' + self.__files[dbname])
            self.__dbs[dbname].query('PRAGMA foreign_keys = false')
            # テーブル作成（CreateTable文）
            for path_sql in self.__GetCreateTableSqlFilePaths(dbname):
                self.__ExecuteSqlFile(dbname, path_sql)
            # 初期値の挿入（Insert文）
            for path_tsv in self.__GetInsertTsvFilePaths(dbname):
                table_name = os.path.splitext(table_name)[0]
                loader = database.TsvLoader.TsvLoader()
                loader.ToSqlite3(path_tsv, self.__files[dbname], table_name)
            self.__dbs[dbname].query('PRAGMA foreign_keys = true')
        if not dbname in self.__dbs.keys():
            self.__dbs[dbname] = dataset.connect('sqlite:///' + self.__files[dbname])

    # パス取得（テーブル作成用SQLファイル）
    def __GetCreateTableSqlFilePaths(self, dbname):
        path = os.path.join(self.__path_dir_this, dbname, 'sql', 'create')
        for path_sql in glob.glob(os.path.join(path + '*.sql')): yield path_sql

    # パス取得（初期値挿入用TSVファイル）
    def __GetInsertTsvFilePaths(self, dbname):
        path = os.path.join(self.__path_dir_this, dbname, 'tsv')
        for path_tsv in glob.glob(os.path.join(path + '*.tsv')): yield path_tsv
        return self.__dbs[dbname]

    # SQLファイル発行
    def __ExecuteSqlFile(self, dbname, sql_path):
        with open(sql_path, 'r') as f:
            sql = f.read()
            self.__dbs[dbname].query(sql)

    # ライセンスDB作成（AccountDBに依存。WebAPIからデータ取得するため）
    def __CreateLicenseDb(self):
        dbname = 'license'
        if not os.path.isfile(self.__files[dbname]):
            # 空ファイル作成
            with open(self.__dbs[dbname], 'w') as f: pass
            # DB接続
            self.__dbs[dbname] = dataset.connect('sqlite:///' + self.__files[dbname])
            self.__dbs[dbname].query('PRAGMA foreign_keys = false')
            # テーブル作成（CreateTable文）
            for path_sql in self.__GetCreateTableSqlFilePaths(dbname):
                self.__ExecuteSqlFile(dbname, path_sql)
            # 初期値の挿入（Insert文）
            cilent = self.__GetClient() # AccessToken持ってる適当なアカウントを用いる
            import database.license.insert.Main
            inserter = database.license.insert.Main.Main(self.__dbs[dbname], client)
            inserter.Initialize()
            self.__dbs[dbname] = dataset.connect('sqlite:///' + self.__files[dbname])
            self.__dbs[dbname].query('PRAGMA foreign_keys = true')
        if not dbname in self.__dbs.keys():
            self.__dbs[dbname] = dataset.connect('sqlite:///' + self.__files[dbname])

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
        
    # 各ユーザのリポジトリDB作成
    def __CreateRepositoryDb(self, username):
        if None is self.__dbs['repos']: self.__dbs['repos'] = {}
        dbname = 'repo'
        path_db = self.__files[dbname].replace('{user}', username)
        if not os.path.isfile(path_db):
            # 空ファイル作成
            with open(path_db, 'w') as f: pass
            # DB接続
            self.__dbs['repos'][username] = dataset.connect('sqlite:///' + path_db)
            self.__dbs[dbname].query('PRAGMA foreign_keys = false')
            # テーブル作成（CreateTable文）
            for path_sql in self.__GetCreateTableSqlFilePaths(dbname):
                self.__ExecuteSqlFile(dbname, path_sql)
            # 初期値の挿入（Insert文）
            cilent = self.__GetClient(username) # 指定アカウントを用いる
            inserter = database.repo.insert.command.repositories.Inserter.Inserter(self, username, client)
            inserter.Insert()
            self.__dbs[dbname].query('PRAGMA foreign_keys = true')
        if not username in self.__dbs['repos'].keys():
            self.__dbs['repos'][username] = dataset.connect('sqlite:///' + path_db)
    """
    """
    def __OpenDb(self):
        # マスターDB生成（ファイル、テーブル、データ挿入）
        if None is self.__lang:
            if not os.path.isfile(self.__files['lang']):
                m = database.language.Main.Main(self.__files['lang'])
                m.Run()
            self.__lang = dataset.connect('sqlite:///' + self.__files['lang'])
        if None is self.__api:
            if not os.path.isfile(self.__files['api']):
                m = database.api.Main.Main(self.__files['api'])
                m.Run()
            self.__api = dataset.connect('sqlite:///' + self.__files['api'])
        if None is self.__gnu_license:
            if not os.path.isfile(self.__files['gnu_license']):
                m = database.gnu_license.Main.Main(self.__files['gnu_license'])
                m.Run()
            self.__gnu_license = dataset.connect('sqlite:///' + self.__files['gnu_license'])

        # アカウントDB生成（ファイル、テーブル作成。データ挿入はCUIにて行う）
        if None is self.__account:
            if not os.path.isfile(self.__files['account']):
                m = database.account.Main.Main(self.__files['account'])
                m.Create()
            self.__account = dataset.connect('sqlite:///' + self.__files['account'])

        # DB作成にTokenが必要なもの
        if 0 < self.__account['Accounts'].count():
            # ライセンスDB生成（ファイル、テーブル作成。データ挿入）
            if not(os.path.isfile(self.__files['license'])):
                web.log.Log.Log().Logger.debug(self.__files['license'])
                account = self.__account['Accounts'].find().next()
                twofactor = self.__account['TwoFactors'].find_one(AccountId=account['Id'])
                authentications = []
                if None is not twofactor:
                    authentications.append(TwoFactorAuthentication(account['Username'], account['Password'], twofactor['Secret']))
                else:
                    authentications.append(BasicAuthentication(account['Username'], account['Password']))
                client = web.service.github.api.v3.Client.Client(self, authentications)
                l = database.license.Main.Main(self, client)
                l.Create()
                self.__license = dataset.connect('sqlite:///' + self.__files['license'])
                l.Insert()
            self.__license = dataset.connect('sqlite:///' + self.__files['license'])
            # 自分アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）
            for account in self.__account['Accounts'].find():
                self.__OpenRepo(account['Username'])
            # 他者アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）

    def __OpenRepo(self, username):
        is_create = False
        path = self.__files['repo'].replace('{user}', username)
        if not(os.path.isfile(path)):
            # DBテーブル作成
            path_sh = os.path.join(self.__path_dir_this, 'repo/create/Create.sh')
            subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(path_sh, path)))
            self.__repos[username] = dataset.connect('sqlite:///' + path)
            # ダミー引数を渡す
            account = self.__account['Accounts'].find_one(Username=username)
            twofactor = self.__account['TwoFactors'].find_one(AccountId=account['Id'])
            authentications = []
            if None is not twofactor:
                authentications.append(TwoFactorAuthentication(account['Username'], account['Password'], twofactor['Secret']))
            else:
                authentications.append(BasicAuthentication(account['Username'], account['Password']))
            client = web.service.github.api.v3.Client.Client(self, authentications)
            inserter = database.repo.insert.command.repositories.Inserter.Inserter(self, username, client)
            inserter.Insert()
        if not(username in self.__repos.keys()):
            self.__repos[username] = dataset.connect('sqlite:///' + path)

    """

