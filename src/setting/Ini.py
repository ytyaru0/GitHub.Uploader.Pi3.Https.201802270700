import configparser
import pathlib
from _python.designpattern.Singleton import Singleton
class Ini(metaclass=Singleton):

    #def __init__(self): self.__config = None
    @property
    def Parser(self): return self.__config
        
    def __init__(self):
        self.__LoadIni()

    def __LoadIni(self):
        path_dir_root = pathlib.Path(__file__).parent.parent.parent
        #path_dir_root = pathlib.PurePath('../../../').relative_to(__file__)
        path_file_config = path_dir_root / 'res' / 'config.ini'
        
        self.__config = configparser.ConfigParser()
        if path_file_config.is_file():
            self.__config.read(path_file_config)
            #self.__Validate()
        if not path_file_config.is_file():
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

