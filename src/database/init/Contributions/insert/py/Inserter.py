#!python3
#encoding: utf-8
import requests
from bs4 import BeautifulSoup
import dataset
import datetime
import os.path
from database.Database import Database as Db

class Inserter(object):
    def __init__(self, db):
        self.__db = db # db = {'user1': dataset.connect('sqlite:///' + '.../GitHub.Contributions.{user}.sqlite3'), ...} 呼出元: DbInitializer.__ActionByPy() 作成元: ContributionsDbInitializer
    """
    ContributionDBの生成と更新を実行する。
    DBが存在しなければDBファイルとテーブルを作成する。
    DBが存在すればレコードを更新する。
    @param {string} usernameは対象ユーザ名。
    """
    def Insert(self):
        for username in db.keys():
            self.__Insert(self.__GetContributionsSince(self.__GetContributionsSVG(username), self.__GetLastDateFromDB()))
    """
    指定した日付と同じかそれより未来のみを対象としたContributionsを取得する。
    @param {dict} 
    """
    def __Insert(self, contributions):
        if None is contributions:
            return
        self.__db.begin()
        # 指定した日付と同日なら更新する
        self.__db['Contributions'].update(contributions[0], 'Date')
        # 指定した日付以降なら挿入する
        for c in contributions[1:]:
            self.__db['Contributions'].insert(c)
        self.__db.commit()
    """
    指定した日付と同じかそれより未来のみを対象としたContributionsを取得する。
    @param {soup.find} svgはHTML内のSVG要素。
    @param {string} sinceは日付。yyyy-MM-dd書式。Noneや空文字ならすべての日付を対象とする。
    @return {dict} 指定した日付とそれ以降におけるSVGのContributions。
    """
    def __GetContributionsSince(self, svg, since):
        if None is svg:
            return None
        contributions = []
        for rect in svg.find_all('rect'):
            date = rect.get('data-date')
            if not since or (since and since <= date):
                contributions.append({"Date": date, "Count": rect.get('data-count')})
        return contributions
    """
    GitHub個人ページからSVG要素を取得し返す。
    @param {string} usernameは対象ユーザ名。
    @return {soup.find} HTML内のSVG要素。
    """
    def __GetContributionsSVG(self, username):
        last_date = self.__GetLastDateFromDB()
        if None is last_date or None is not last_date and last_date < "{0:%Y-%m-%d}".format(datetime.datetime.now()):
            print('************************{0}'.format(username))
            url = 'https://github.com/{username}'.format(username=username)
            file_name = '{username}_contributions'.format(username=username)
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser') # html.parser, lxml
            return soup.find("svg", attrs={"class": "js-calendar-graph-svg"})
        else:
            return None
    """
    DBから最終日を取得する。
    @return {soup.find} HTML内のSVG要素。
    """
    def __GetLastDateFromDB(self):
        if None is self.__db:
            return None
        sql = 'select MAX("Date") LastDate from Contributions;'
        return self.__db.query(sql).next()['LastDate']
