import configparser
import os
import os.path
class Setting:
    def __init__(self):
#    def __init__(self, path_dir_root):
#        self.__path_dir_root = path_dir_root
        self.__path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.__config = configparser.ConfigParser()
        self.__path_config = os.path.join(self.__path_dir_root, 'res/config.ini')
        self.__config.read(self.__path_config)
        self.__LoadDbPath()
        self.__GithubUser()
        self.__GitRemote()
        
    @property
    def GitRemote(self): return self.__git_remote
    @property
    def DbPath(self): return self.__path_dir_db
    @property
    def GithubUsername(self): return self.__username

    def __GithubUser(self):
        if self.__IsUndefinedSectionAndKey('GitHub', 'User'): self.__username = None
        else: self.__username = self.__config['GitHub']['User']
        
    def __GitRemote(self):
        if self.__IsUndefinedSectionAndKey('Git', 'Remote'): self.__git_remote = 'HTTPS'
        else:
            if self.__config['Git']['Remote'] in {'SSH', 'HTTPS'}: self.__git_remote = self.__config['Git']['Remote']
            else: self.__git_remote = 'HTTPS'
        
    def __LoadDbPath(self):
        if self.__IsUndefinedSectionAndKey('Path', 'DB'): self.__path_dir_db = None
        else:
            self.__path_dir_db = self.__RelToAbs(self.__config['Path']['DB'])
            if not os.path.isdir(self.__path_dir_db):
                os.mkdir(self.__path_dir_db)
                #raise Exception('{0} のPath.DBに指定されたパス {1} は存在しないかディレクトリではありません。存在するディレクトリを指定してください。'.format(self.__path_config, self.__path_dir_db))
                print('{0} のPath.DBに指定されたパス {1} は存在しないため新規作成しました。'.format(self.__path_config, self.__path_dir_db))
            
    def __RelToAbs(self, path):
        if not os.path.isabs(path):
            # ./
            if path.startswith('./'):
                return os.path.join(self.__path_dir_root, path[2:])
            # ../../../
            abs_path = self.__base_path
            rel_path = path
            while rel_path.startswith('../'):
                rel_path = rel_path[3:]
                abs_path = os.path.dirname(abs_path)
            return os.path.join(abs_path, rel_path)
        return path

    def __IsUndefinedSectionAndKey(self, section, key):
        if section not in self.__config or key not in self.__config[section]: return True
        else: return False
        
