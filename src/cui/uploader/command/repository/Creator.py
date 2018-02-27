#!python3
#encoding:utf-8
import os.path
import subprocess
import shlex
import datetime
import time
import pytz
import requests
import json
#import setting.Setting
from setting.Config import Config
from database.Database import Database as Db

class Creator:
    def __init__(self, client, args):
#    def __init__(self, db, client, args):
#        self.__db = db
        self.__client = client
        self.__args = args
        self.__userRepo = Db().Repositories[self.__args.username]
        #self.__userRepo = self.__db.Repositories[self.__args.username]
        self.__repo_name = os.path.basename(self.__args.path_dir_pj)

    def Create(self):
        self.__LoadDb()
        self.__CreateLocalRepository()
        j = self.__client.Repositories.create(self.__repo_name, description=self.__args.description, homepage=self.__args.homepage)
        self.__InsertRemoteRepository(j)

    def __LoadDb(self):
        self.__account = Db().Accounts['Accounts'].find_one(Username=self.__args.username)
        #self.__account = self.__db.Accounts['Accounts'].find_one(Username=self.__args.username)
        if None is self.__account: raise Exception('未登録のアカウントです。登録してから再度実行してください。')
        self.__sshconfigures = Db().Accounts['SshConfigures'].find_one(AccountId=self.__account['Id'])
        #self.__sshconfigures = self.__db.Accounts['SshConfigures'].find_one(AccountId=self.__account['Id'])

    def __CreateLocalRepository(self):
        subprocess.call(shlex.split("git init"))
        print("git init")
        subprocess.call(shlex.split("git config --local user.name '{0}'".format(self.__args.username)))
        print("git config --local user.name '{0}'".format(self.__args.username))
        subprocess.call(shlex.split("git config --local user.email '{0}'".format(self.__account['MailAddress'])))
        print("git config --local user.email '{0}'".format(self.__account['MailAddress']))
        
        # HTTPS, SSL どちらかによってリポジトリ文字列を変える
        repo_str = Config().GitRemote.GetRepositoryUri(self.__args.username, self.__repo_name)
        #repo_str = self.__RemoteRepositoryName()
        """
        なぜかできない。LinuxMint17.3ではできたが、RaspberryPi3のRaspbianではできなかった。
        SSH通信ができない。ので、HTTPS通信に変更する。SSHよりセキュリティが弱い。
        subprocess.call(shlex.split("git remote add origin git@{0}:{1}/{2}.git".format(self.__sshconfigures['HostName'], self.__args.username, self.__repo_name)))
        print("git remote add origin git@{0}:{1}/{2}.git".format(self.__sshconfigures['HostName'], self.__args.username, self.__repo_name))
        """
        # https://{user}:{pass}@github.com/{user}/{repo}.git
#        subprocess.call(shlex.split("git remote add origin https://{0}:{1}@github.com/{0}/{2}.git".format(self.__args.username, self.__account['Password'], self.__repo_name)))
#        print("git remote add origin https://{0}:{1}@github.com/{0}/{2}.git".format(self.__args.username, self.__account['Password'], self.__repo_name))
        subprocess.call(shlex.split("git remote add origin {0}".format(repo_str)))
        print("git remote add origin {0}".format(repo_str))
    def __InsertRemoteRepository(self, j):
        self.__userRepo.begin()
        repo = self.__userRepo['Repositories'].find_one(Name=j['name'])
        # Repositoriesテーブルに挿入する
        if None is repo:
            self.__userRepo['Repositories'].insert(self.__CreateRecordRepositories(j))
            repo = self.__userRepo['Repositories'].find_one(Name=j['name'])
        # 何らかの原因でローカルDBに既存の場合はそのレコードを更新する
        else:
            self.__userRepo['Repositories'].update(self.__CreateRecordRepositories(j), ['Name'])

        # Countsテーブルに挿入する
        cnt = self.__userRepo['Counts'].count(RepositoryId=repo['Id'])
        if 0 == cnt:
            self.__userRepo['Counts'].insert(self.__CreateRecordCounts(self.__userRepo['Repositories'].find_one(Name=j['name'])['Id'], j))
        # 何らかの原因でローカルDBに既存の場合はそのレコードを更新する
        else:
            self.__userRepo['Counts'].update(self.__CreateRecordCounts(repo['Id'], j), ['RepositoryId'])
        self.__userRepo.commit()

    def __CreateRecordRepositories(self, j):
        return dict(
            IdOnGitHub=j['id'],
            Name=j['name'],
            Description=j['description'],
            Homepage=j['homepage'],
            CreatedAt=j['created_at'],
            PushedAt=j['pushed_at'],
            UpdatedAt=j['updated_at'],
            CheckedAt="{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc))
        )

    def __CreateRecordCounts(self, repo_id, j):
        return dict(
            RepositoryId=repo_id,
            Forks=j['forks_count'],
            Stargazers=j['stargazers_count'],
            Watchers=j['watchers_count'],
            Issues=j['open_issues_count']
        )

    """
    def __RemoteRepositoryName(self):
        # HTTPS, SSL どちらかによってリポジトリ文字列を変える
        #（Uploader.pyですでに実行しているのに2度目の実行をしてる。文字列比較ダサい。もっとスマートに実装できないか）
        #self.__setting = setting.Setting.Setting()
        if 'HTTPS' == Config().GitRemote:
            return "https://{0}:{1}@github.com/{0}/{2}.git".format(self.__args.username, self.__account['Password'], self.__repo_name)
        elif 'SSH' == Config().GitRemote:
            return "git@{0}:{1}/{2}.git".format(self.__sshconfigures['HostName'], self.__args.username, self.__repo_name)
        else:
            raise Exception('config.iniの[Git]Remoteは HTTPS か SSL のみ有効です。: {0}'.format(self.__setting.GitRemote))
    """

