from setting.Ini import Ini 
from _python.designpattern.Singleton import Singleton
import pathlib
class Config(metaclass=Singleton):
    """
    __instance = None
    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            cls.__instance.__Initialize()
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        return cls._instance
    """

    def __init__(self):
        self.__PathDb = None
        self.__GitRemote = None
        self.__GithubUser = None
        self.__Initialize()

    @property
    def PathDb(self): return self.__PathDb
    @property
    def GitRemote(self): return self.__GitRemote
    @property
    def GithubUser(self): return self.__GithubUser
        
    def __Initialize(self):
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        defIni = self.__GetDefault()
        self.__SetGitRemote(defIni)
        self.__SetPathDb(defIni)


    def __GetDefault(self):
        return {
            'Path': {'Db': './res/db/'},
            'Git': {'Remote': 'HTTPS'},
            'Github': {'User': 'ytyaru'},
        }
        
    def __Validate(self, iniDict):
        defIni = self.__GetDefault()
        self.__SetGitRemote(defIni)
        self.__SetPathDb(defIni)

    def __SetGitRemote(self, defIni):
        if Ini().Parser.has_option('Git', 'Remote'):
            git_remote = Ini().Parser['Git']['Remote']
        else:
            git_remote = defIni['Git']['Remote']

        from web.service.github.uri import Protocol
        #import setting.Protocol
        if git_remote in {'HTTPS', 'SSH'}:
            protocol_class = getattr(Protocol, '{}'.format(git_remote[0].upper() + git_remote[1:].lower()))
            #cls = getattr(Protocol, '{}'.format(git_remote[0].upper() + git_remote[1:].lower()))
            #self.__GitRemote = cls()
            #module = importlib.import_module('setting.Protocol')
        else:
            protocol_class = Protocol.Https
            #self.__GitRemote = Protocol.Https()
        self.__GitRemote = protocol_class()
        
    def __SetPathDb(self, defIni):
        if Ini().Parser.has_option('Path', 'Db'):
            path_db = Ini().Parser['Path']['Db']
        else:
            path_db = defIni['Path']['Db']

        if pathlib.PurePath(path_db).is_absolute():
            self.__PathDb = path_db
        else:
            path_dir_root = pathlib.PurePath(__file__).parent.parent.parent
            #path_dir_root = pathlib.PurePath('../../../').relative_to(__file__)
            #setattr(self.__dict, 'PathDb', str(pathlib.PurePath(path_dir_root, path_db)))
            self.__PathDb = pathlib.PurePath(path_dir_root, path_db)
            pathlib.Path(self.__PathDb).resolve().mkdir(parents=True, exist_ok=True)
        
    def __SetGithubUser(self, defIni):
        if Ini().Parser.has_option('Github', 'User'):
            self.__GithubUser = Ini().Parser['Github']['User']
        else:
            self.__GithubUser = defIni['Github']['User']
        
    """
    def __LoadIni(self):
        path_dir_root = pathlib.PurePath('../../../').relative_to(__file__)
        path_file_config = path_dir_root / 'res' / 'config.ini'
        
        self.__config = configparser.ConfigParser()
        if path_file_config.isfile():
            self.__config.read(cls.path_config)
            #self.__Validate()
        if not path_file_config.isfile():
            pathlib.PurePath('../').relative_to(path_file_config).mkdir(parents=True, exist_ok=True)
            self.__config.read_dict(self.__GetDefault())
            with path_file_config.open('w', encoding='UTF-8') as f: self.__config.write(f)
    def __GetDefault(self):
        return {
            'Path': {'Db': './res/db/'},
            'Git': {'Remote': 'HTTPS'},
            'Github': {'User': 'ytyaru'},
        }
    """
        
    """
    def __CreateConfigParser(self):
        path_dir_root = pathlib.PurePath('../../../').relative_to(__file__)
        path_file_config = path_dir_root / 'res' / 'config.ini'
        
        self.__config = configparser.ConfigParser()
        if path_file_config.isfile(): self.__config.read(cls.path_config)
        if not path_file_config.isfile():
            pathlib.PurePath('../').relative_to(path_file_config).mkdir(parents=True, exist_ok=True)
            self.__config.read_dict(self.__GetDefault())
            with path_file_config.open('w', encoding='UTF-8') as f: self.__config.write(f)
    """

    """
        #path_file_this = pathlib.PurePath(__file__)
        #path_dir_root = pathlib.PurePath('../../../')
        cls.path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        cls.path_dir_config = os.path.join(cls.path_dir_root, 'res/')
        cls.path_config = os.path.join(cls.path_dir_config, 'config.ini')
        if os.path.isfile(cls.path_config):
        config = configparser.ConfigParser()
        if os.path.isfile(cls.path_config):
            cls.config.read(cls.path_config)
    def __IniToDict(self):
        for section in Ini().Parser:
            for key in Ini().Parser[section]:
                s = section[0].upper() + section[1:].lower()
                k = key[0].upper() + key[1:].lower() 
                self.__dict[s+k] = Ini().Parser[section][key]

    """


    """
    def __Validate(self, iniDict):
        defIni = self.__GetDefault()
        # Git Remote
        if not hasattr(self.__dict, 'GitRemote'):
            setattr(self.__dict, 'GitRemote', defIni['Git']['Remote'])
        else:
            if getattr(self.__dict, 'GitRemote') not in {'HTTPS', 'SSH'}:
                setattr(self.__dict, 'GitRemote', defIni['Git']['Remote'])
        # Path Db
        if not hasattr(self.__dict, 'PathDb'):
            path_db = defIni['Path']['Db']
        else:
            path_db = getattr(self.__dict, 'PathDb')
        if pathlib.PurePath(path_db).is_absolute():
            setattr(self.__dict, 'PathDb', path_db)
        else:
            path_dir_root = pathlib.PurePath('../../../').relative_to(__file__)
            setattr(self.__dict, 'PathDb', str(pathlib.PurePath(path_dir_root, path_db)))
        pathlib.PurePath(setattr(self.__dict, 'PathDb')).mkdir(parents=True, exist_ok=True)
        #pathlib.PurePath('../').relative_to(path_file_config).mkdir(parents=True, exist_ok=True)
        #os.makedirs(getattr(self.__dict, '_Setting__PathDb'), exist_ok=Tr
    """

    """

    def __SetAttrs(self):

    def __Exchanges(self):

    @classmethod
    def __Initialize(cls):
        cls.__LoadIni()
        cls.__SetAttrs()

    @classmethod
    def __LoadIni(cls):
        
    @classmethod
    def __SetAttrs(cls):

    @classmethod
    def __Exchanges(cls):
    """

