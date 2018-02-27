from abc import ABCMeta, abstractmethod
class Protocol(metaclass=ABCMeta):
    @abstractmethod
    def GetRepositoryUri(self, user_name, repo_name): pass
class Https(Protocol):
    def GetRepositoryUri(self, user_name, repo_name):
        from database.Database import Database as Db
        pass_word = Db().Accounts['Accounts'].find_one(Username=user_name)['Password']
        return "https://{0}:{1}@github.com/{0}/{2}.git".format(user_name, pass_word, repo_name)
class Ssh(Protocol):
    def GetRepositoryUri(self, user_name, repo_name):
        from database.Database import Database as Db
        account = Db().Accounts['Accounts'].find_one(Username=user_name)
        sshHostName = Db().Accounts['SshConfigures'].find_one(AccountId=account['Id'])['HostName']
        return "git@{0}:{1}/{2}.git".format(sshHostName, user_name, repo_name)

