#!python3
#encoding:utf-8
import sys
import os.path
import subprocess
import configparser
import argparse
import web.service.github.api.v3.AuthenticationsCreator
import web.service.github.api.v3.Client
#import database.Database
from database.Database import Database as Db
import cui.uploader.Main
import web.log.Log
import database.contributions.Main
import setting.Setting
import threading

class Main:
    def __init__(self):
        pass

    def Run(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-u', '--username')
        parser.add_argument('-d', '--description')
        parser.add_argument('-l', '--homepage', '--link', '--url')
        parser.add_argument('-m', '--messages', action='append')
        args = parser.parse_args()
#        print(args)
#        print('path_dir_pj: {0}'.format(args.path_dir_pj))
#        print('-u: {0}'.format(args.username))
#        print('-d: {0}'.format(args.description))
#        print('-l: {0}'.format(args.homepage))

        self.__setting = setting.Setting.Setting()
#        self.__setting = setting.Setting.Setting(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
#        self.__setting = setting.Setting.Setting(os.path.abspath(os.path.dirname(__file__)))
        path_dir_db = self.__setting.DbPath
        web.log.Log.Log().Logger.debug(path_dir_db)
        
        # os.path.basename()で空文字を返されないための対策
        # https://docs.python.jp/3/library/os.path.html#os.path.basename
        if args.path_dir_pj.endswith('/'):
            args.path_dir_pj = args.path_dir_pj[:-1]
        
        if None is args.username:
            print(self.__setting.GithubUsername)
            args.username = self.__setting.GithubUsername        
        #self.__db = database.Database.Database()
#        self.__db = database.Database.Database(os.path.abspath(os.path.dirname(__file__)))
        #self.__db.Initialize()
        
        if None is Db().Accounts['Accounts'].find_one(Username=args.username):
        #if None is self.__db.Accounts['Accounts'].find_one(Username=args.username):
            web.log.Log.Log().Logger.warning('指定したユーザ {0} はDBに存在しません。GitHubUserRegister.pyで登録してください。'.format(args.username))
            return
        
        # Contributionsバックアップ
        usernames = []
        #for a in self.__db.Accounts['Accounts'].find(): usernames.append(a['Username'])
        for a in Db().Accounts['Accounts'].find(): usernames.append(a['Username'])
        #th = ContributionsThread(path_dir_db, self.__db, usernames)
        th = ContributionsThread(path_dir_db, usernames)
        th.start()
        
        # アップローダ起動
#        creator = web.service.github.api.v3.AuthenticationsCreator.AuthenticationsCreator(self.__db, args.username)
        creator = web.service.github.api.v3.AuthenticationsCreator.AuthenticationsCreator(args.username)
        authentications = creator.Create()
#        client = web.service.github.api.v3.Client.Client(self.__db, authentications, args)
        client = web.service.github.api.v3.Client.Client(authentications, args)
#        main = cui.uploader.Main.Main(self.__db, client, args)
        main = cui.uploader.Main.Main(client, args)
        main.Run()

class ContributionsThread(threading.Thread):
#    def __init__(self, path_dir_db, db, usernames):
    def __init__(self, path_dir_db, usernames):
        threading.Thread.__init__(self)
        self.__path_dir_db = path_dir_db
        #self.__db = db
        self.__usernames = usernames 
    def run(self):
        m = database.contributions.Main.Main(self.__path_dir_db)
        for username in self.__usernames: m.Run(username)


if __name__ == '__main__':
    main = Main()
    main.Run()
