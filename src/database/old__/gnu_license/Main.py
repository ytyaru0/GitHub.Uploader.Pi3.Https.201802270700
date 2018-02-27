#!python3
#encoding:utf-8
import sys
import subprocess
import shlex
import os.path
import getpass
import dataset
import database.gnu_license.create.Main
import database.gnu_license.insert.main
class Main:
    def __init__(self, db_path):
        self.__db_path = db_path
        self.__path_this_dir = os.path.abspath(os.path.dirname(__file__))
    def Run(self):
        c = database.gnu_license.create.Main.Main(self.__db_path)
        c.Run()
        i = database.gnu_license.insert.main.GnuSite(self.__db_path)
        i.GetAll()

