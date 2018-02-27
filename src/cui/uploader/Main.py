#!/usr/bin/python3
#!python3
#encoding:utf-8
import os.path
import subprocess
import cui.uploader.command.repository.Creator
import cui.uploader.command.repository.Commiter
import cui.uploader.command.repository.Deleter
import cui.uploader.command.repository.Editor
import cui.uploader.command.aggregate.Aggregate
import web.log.Log
from database.Database import Database as Db

class Main:
    def __init__(self, client, args):
#    def __init__(self, db, client, args):
#        self.__db = db
        self.__client = client
        self.__args = args
        self.__creator = cui.uploader.command.repository.Creator.Creator(self.__client, self.__args)
        self.__commiter = cui.uploader.command.repository.Commiter.Commiter(self.__client, self.__args)
        self.__deleter = cui.uploader.command.repository.Deleter.Deleter(self.__client, self.__args)
        self.__editor = cui.uploader.command.repository.Editor.Editor(self.__client, self.__args)
        self.__agg = cui.uploader.command.aggregate.Aggregate.Aggregate(self.__args)
        """
        self.__creator = cui.uploader.command.repository.Creator.Creator(self.__db, self.__client, self.__args)
        self.__commiter = cui.uploader.command.repository.Commiter.Commiter(self.__db, self.__client, self.__args)
        self.__deleter = cui.uploader.command.repository.Deleter.Deleter(self.__db, self.__client, self.__args)
        self.__editor = cui.uploader.command.repository.Editor.Editor(self.__db, self.__client, self.__args)
        self.__agg = cui.uploader.command.aggregate.Aggregate.Aggregate(self.__db, self.__args)
        """
        
        #self.__account = self.__db.Accounts['Accounts'].find_one(Username=self.__args.username)
        #self.__ssh_configures = self.__db.Accounts['SshConfigures'].find_one(AccountId=self.__account['Id'])
        self.__account = Db().Accounts['Accounts'].find_one(Username=self.__args.username)
        self.__ssh_configures = Db().Accounts['SshConfigures'].find_one(AccountId=self.__account['Id'])
#        print(self.__args.path_dir_pj)
        self.__repo_name = os.path.basename(self.__args.path_dir_pj)
        self.__repos = Db().Repositories[self.__args.username]['Repositories'].find_one(Name=self.__repo_name)
        #self.__repos = self.__db.Repositories[self.__args.username]['Repositories'].find_one(Name=self.__repo_name)

    def Run(self):
        if -1 != self.__Create():
            if None is self.__repos: self.__repos = Db().Repositories[self.__args.username]['Repositories'].find_one(Name=self.__repo_name)
            #if None is self.__repos: self.__repos = self.__db.Repositories[self.__args.username]['Repositories'].find_one(Name=self.__repo_name)
            self.__Commit()

    def __CreateInfo(self):
        web.log.Log.Log().Logger.info('ユーザ名: {0}'.format(self.__account['Username']))
        web.log.Log.Log().Logger.info('メアド: {0}'.format(self.__account['MailAddress']))
        web.log.Log.Log().Logger.info('SSH HOST: {0}'.format(self.__ssh_configures['HostName']))
        if None is self.__repos:
            web.log.Log.Log().Logger.info('リポジトリ名: {0}'.format(self.__repo_name))
            web.log.Log.Log().Logger.info('説明: {0}'.format(self.__args.description))
            web.log.Log.Log().Logger.info('URL: {0}'.format(self.__args.homepage))
        else:
            web.log.Log.Log().Logger.info('リポジトリ名: {0}'.format(self.__repos['Name']))
            web.log.Log.Log().Logger.info('説明: {0}'.format(self.__repos['Description']))
            web.log.Log.Log().Logger.info('URL: {0}'.format(self.__repos['Homepage']))
        web.log.Log.Log().Logger.info('リポジトリ情報は上記のとおりで間違いありませんか？[y/n]')
        """
        if None is self.__repos:
            web.log.Log.Log().Logger.info('ユーザ名: {0}'.format(self.__args.username))
            web.log.Log.Log().Logger.info('メアド: {0}'.format(self.__args.mailaddress))
            web.log.Log.Log().Logger.info('SSH HOST: {0}'.format(self.__args.ssh_host))
            web.log.Log.Log().Logger.info('リポジトリ名: {0}'.format(self.__repo_name))
            web.log.Log.Log().Logger.info('説明: {0}'.format(self.__args.description))
            web.log.Log.Log().Logger.info('URL: {0}'.format(self.__args.homepage))
        else:
            web.log.Log.Log().Logger.info('ユーザ名: {0}'.format(self.__account['Username']))
            web.log.Log.Log().Logger.info('メアド: {0}'.format(self.__account['MailAddress']))
            web.log.Log.Log().Logger.info('SSH HOST: {0}'.format(self.__ssh_configures['HostName']))
            web.log.Log.Log().Logger.info('リポジトリ名: {0}'.format(self.__repos['Name']))
            web.log.Log.Log().Logger.info('説明: {0}'.format(self.__repos['Description']))
            web.log.Log.Log().Logger.info('URL: {0}'.format(self.__repos['Homepage']))
        web.log.Log.Log().Logger.info('リポジトリ情報は上記のとおりで間違いありませんか？[y/n]')
        """

    def __Create(self):
        if os.path.exists(".git"):
            return 0
        answer = ''
        while '' == answer:
            self.__CreateInfo()
            answer = input()
            if 'y' == answer or 'Y' == answer:
                self.__creator.Create()
                return 0
            elif 'n' == answer or 'N' == answer:
                web.log.Log.Log().Logger.info('call.shを編集して再度やり直してください。')
                return -1
            else:
                answer = ''

    def __CommitInfo(self):
        web.log.Log.Log().Logger.info('リポジトリ名： {0}/{1}'.format(self.__account['Username'], self.__repos['Name']))
        web.log.Log.Log().Logger.info('説明: {0}'.format(self.__repos['Description']))
        web.log.Log.Log().Logger.info('URL: {0}'.format(self.__repos['Homepage']))
        web.log.Log.Log().Logger.info('----------------------------------------')
        self.__commiter.ShowCommitFiles()
        web.log.Log.Log().Logger.info('commit,pushするならメッセージを入力してください。Enterかnで終了します。')
        web.log.Log.Log().Logger.info('サブコマンド    n:終了 a:集計 e:編集 d:削除 i:Issue作成')
        
    """
    def __CommitInfo(self):
        web.log.Log.Log().Logger.info('リポジトリ名： {0}/{1}'.format(self.__authData.Username, self.__repo.Name))
        web.log.Log.Log().Logger.info('説明: {0}'.format(self.__repo.Description))
        web.log.Log.Log().Logger.info('URL: {0}'.format(self.__repo.Homepage))
        web.log.Log.Log().Logger.info('----------------------------------------')
        self.__commiter.ShowCommitFiles()
        web.log.Log.Log().Logger.info('commit,pushするならメッセージを入力してください。Enterかnで終了します。')
        web.log.Log.Log().Logger.info('サブコマンド    n:終了 a:集計 e:編集 d:削除 i:Issue作成')
    """
    
    def __Commit(self):
        # 起動引数-mが未設定だとNoneになる。そのときはcommitとIssueの同時登録はしない。
        if None is not self.__args.messages:
            self.__commiter.AddCommitPushIssue(self.__args.messages)
            self.__agg.Show()
        else:
            while (True):
                self.__CommitInfo()
                answer = input()
                if '' == answer or 'n' == answer or 'N' == answer:
                    web.log.Log.Log().Logger.info('終了します。')
                    break
                elif 'a' == answer or 'A' == answer:
                    self.__agg.Show()
                elif 'e' == answer or 'E' == answer:
                    self.__ConfirmEdit()
                elif 'd' == answer or 'D' == answer:
                    self.__ConfirmDelete()
                    break
                elif 'i' == answer or 'I' == answer:
                    web.log.Log.Log().Logger.info('(Issue作成する。(未実装))')
                else:
                    self.__commiter.AddCommitPush(answer)
                    self.__agg.Show()

    def __ConfirmDelete(self):
        web.log.Log.Log().Logger.info('.gitディレクトリ、対象リモートリポジトリ、対象DBレコードを削除します。')
#        web.log.Log.Log().Logger.info('リポジトリ名： {0}/{1}'.format(self.__authData.Username, self.__repo.Name))
        web.log.Log.Log().Logger.info('リポジトリ名： {0}/{1}'.format(self.__account['Username'], self.__repos['Name']))
        self.__deleter.ShowDeleteRecords()
        web.log.Log.Log().Logger.info('削除すると復元できません。本当に削除してよろしいですか？[y/n]')
        answer = input()
        if 'y' == answer or 'Y' == answer:
            self.__deleter.Delete()
            web.log.Log.Log().Logger.info('削除しました。')
            return True
        else:
            web.log.Log.Log().Logger.info('削除を中止しました。')
            return False

    def __ConfirmEdit(self):
        web.log.Log.Log().Logger.info('編集したくない項目は無記入のままEnterキー押下してください。')
        web.log.Log.Log().Logger.info('リポジトリ名を入力してください。')
        name = input()
        # 名前は必須項目。変更しないなら現在の名前をセットする
        if None is name or '' == name: name = self.__repos['Name']
        web.log.Log.Log().Logger.info('説明文を入力してください。')
        description = input()
        web.log.Log.Log().Logger.info('Homepageを入力してください。')
        homepage = input()
        
        if '' == description and '' == homepage and self.__repos['Name'] == name:
            web.log.Log.Log().Logger.info('編集する項目がないため中止します。')
        else:
            self.__editor.Edit(name, description, homepage)
            web.log.Log.Log().Logger.info('編集しました。')
