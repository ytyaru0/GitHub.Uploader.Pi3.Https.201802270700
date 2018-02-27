#!python3
#encoding:utf-8
import os.path
import subprocess
import shlex
import time
import requests
import json
import datetime
from database.Database import Database as Db
import cui.sh.Client

class Commiter:
    def __init__(self, client, args):
#    def __init__(self, db, client, args):
#        self.__db = db
        self.__client = client
        self.__args = args
        self.__userRepo = Db().Repositories[self.__args.username]
        #self.__userRepo = self.__db.Repositories[self.__args.username]
        self.__repo_name = os.path.basename(self.__args.path_dir_pj)

    def ShowCommitFiles(self):
        cui.sh.Client.Client.Run("git add -n .", cwd=self.__args.path_dir_pj)
        #subprocess.call(shlex.split("git add -n ."), cwd=self.__args.path_dir_pj)

    def AddCommitPushIssue(self, commit_messages):
        if 1 == len(commit_messages):
            issue = self.__client.Issues.create(commit_messages[0])
        elif 2 <= len(commit_messages) and '' != commit_messages[1]:
            commit_messages.insert(1, '')
            issue = self.__client.Issues.create(commit_messages[0], body='\n'.join(commit_messages[2:]))
        else:
            issue = self.__client.Issues.create(commit_messages[0], body='\n'.join(commit_messages[2:]))
        
        # http://surumereflection.hatenadiary.jp/entry/2016/09/14/223838
        # git commit -m "fix #Issue番号 1行目" -m "2行目" -m "3行目" ...
        message_command = ''
        for i, line in enumerate(commit_messages):
            if 0 == i: message_command += ' -m "fix #' + str(issue['number']) + ' ' + line + '" '
            else: message_command += ' -m "' + line + '" '
        
        client = cui.sh.Client.Client({'cwd': self.__args.path_dir_pj})
        client.run("git add .")
        client.run("git commit {0}".format(message_command))
        client.run("git push origin master")

        """
        subprocess.call(shlex.split("git add .", cwd=self.__args.path_dir_pj))
        subprocess.call(shlex.split("git commit {0}".format(message_command), cwd=self.__args.path_dir_pj))
        subprocess.call(shlex.split("git push origin master", cwd=self.__args.path_dir_pj))
        """
        """
        subprocess.call(shlex.split("git add ."))
        subprocess.call(shlex.split('git commit ' + message_command))
        subprocess.call(shlex.split("git push origin master"))
        """
        time.sleep(3)
        self.__InsertLanguages(self.__client.Repositories.list_languages())

    def AddCommitPush(self, commit_message):
        #client = cui.sh.Client.Client({'cwd': self.__args.path_dir_pj})
        client = cui.sh.Client.Client(cwd=self.__args.path_dir_pj)
        client.run("git add .")
        client.run("git commit -m '{0}'".format(commit_message))
        client.run("git push origin master")
        time.sleep(3)
        self.__InsertLanguages(self.__client.Repositories.list_languages())

        """
        subprocess.call(shlex.split("git add ."), cwd=self.__args.path_dir_pj)
        print("git add .")
        subprocess.call(shlex.split("git commit -m '{0}'".format(commit_message)), cwd=self.__args.path_dir_pj)
        print("git commit -m '{0}'".format(commit_message))
        # 2018-02-15 追加 start
        # https://github.com/{0}/{1}.git
        #subprocess.call(shlex.split("git remote add origin git@github.com:{0}/{1}.git".format(self.__args.username, self.__repo_name)))
        # 2018-02-15 追加 end
        subprocess.call(shlex.split("git push origin master"), cwd=self.__args.path_dir_pj)
        print("git push origin master")
        time.sleep(3)
        print("ローカルDBに追加 start")
        self.__InsertLanguages(self.__client.Repositories.list_languages())
        print("ローカルDBに追加 end")
        """
    def __InsertLanguages(self, j):
        self.__userRepo.begin()
        repo_id = self.__userRepo['Repositories'].find_one(Name=os.path.basename(self.__args.path_dir_pj))['Id']
        self.__userRepo['Languages'].delete(RepositoryId=repo_id)
        for key in j.keys():
            self.__userRepo['Languages'].insert(dict(
                RepositoryId=repo_id,
                Language=key,
                Size=j[key]
            ))
        self.__userRepo.commit()

