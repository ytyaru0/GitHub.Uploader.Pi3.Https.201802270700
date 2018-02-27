import configparser
import os
import os.path
import pathlib
class IniToDict:

    def Get(self):
        self.__CreateConfigParser()
        self.__dict = IniToDict()
        self.__Validate()
        return self.__dict

    def __GetDefault(self):
        return {
            'Path': {'Db': './res/db/'},
            'Git': {'Remote': 'HTTPS'},
            'Github': {'User': 'ytyaru'},
        }
        
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
        #path_file_this = pathlib.PurePath(__file__)
        #path_dir_root = pathlib.PurePath('../../../')
        cls.path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        cls.path_dir_config = os.path.join(cls.path_dir_root, 'res/')
        cls.path_config = os.path.join(cls.path_dir_config, 'config.ini')
        if os.path.isfile(cls.path_config):
        config = configparser.ConfigParser()
        if os.path.isfile(cls.path_config):
            cls.config.read(cls.path_config)
        """

    def __IniToDict(self):
        for section in self.__config:
            for key in self.__config[section]:
                s = section[0].upper() + section[1:].lower()
                k = key[0].upper() + key[1:].lower() 
                self.__dict[s+k] = self.__config[section][key]


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

