import configparser
import os
import os.path

# `Setting.{Section}{Key}`プロパティを実装する（読取専用）
class SettingMeta(type):
    def __new__(cls, name, bases, attrs):
        cls.path_dir_root = None
        cls.path_dir_config = None
        cls.path_config = None
        cls.config = None

        cls.__LoadIni(cls)
        cls.__AddVariable(cls, name, attrs)
        cls.__SetVarDefaultValue(cls, name, attrs)
        os.makedirs(attrs[cls.__GetVarName(cls, name, 'Path', 'Db')], exist_ok=True)
        return type.__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        """
        print('**********************************************')
        SettingMeta.__AddProperty(cls, name, attrs)
        #print('cls.__PathDb', cls.__PathDb)#AttributeError: type object 'Setting' has no attribute '_SettingMeta__PathDb'
        print(cls)
        print(type(cls))
        #print('cls.__PathDb', cls.__PathDb)#AttributeError: type object 'Setting' has no attribute '_SettingMeta__PathDb'
        #print('cls().__PathDb', cls().__PathDb)#AttributeError: 'Setting' object has no attribute '_SettingMeta__PathDb'
        print('cls._Setting__PathDb', cls._Setting__PathDb)
        print('cls.PathDb', cls.PathDb)
        print('cls().PathDb', cls().PathDb)
        print(attrs['_{0}__{1}'.format(name, 'PathDb')])
        print(cls().PathDb)
        print(dir(cls))
        print(dir(type(cls)))
        #print(SettingMeta.PathDb)#AttributeError: type object 'SettingMeta' has no attribute 'PathDb'
        """
        print('xxxxxxxxxxxxxxxxxxxxxxxx')
        print(cls, type(cls))
        print('xxxxxxxxxxxxxxxxxxxxxxxx')
        for section in SettingMeta.config:
            for key in SettingMeta.config[section]:
                varName = SettingMeta.__GetVarName(SettingMeta, name, section, key)
                propName = SettingMeta.__GetPropName(SettingMeta, section, key)
#                attrs[propName] = property(lambda cls: attrs[varName])
                #setattr(cls, propName, property(lambda cls: attrs[varName]))
                #setattr(cls, propName, property(lambda cls: cls._Setting__PathDb)) # OK!!!!!!
                #setattr(cls, propName, property(lambda cls: getattr(cls, SettingMeta.__GetVarName(SettingMeta, name, section, key))))
                #setattr(cls, propName, property(lambda cls: cls.__PathDb))
                #setattr(cls, propName, property(lambda cls: getattr(cls, varName)))
                print(varName, attrs[varName], hasattr(cls, varName))
        print('cls', cls)
        print('cls()', cls())
        print('cls.PathDb', cls.PathDb)
        print('cls().PathDb', cls().PathDb)
        print('cls._Setting__PathDb', cls._Setting__PathDb)
        print(dir(cls))
        print(dir(type(cls)))

    #path_dir_root = None
    #path_dir_config = None
    #path_config = None
    #config = None
    def __LoadIni(cls):
        configparser.ConfigParser()
        cls.path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        cls.path_dir_config = os.path.join(cls.path_dir_root, 'res/')
        cls.path_config = os.path.join(cls.path_dir_config, 'config.ini')
        cls.config = configparser.ConfigParser()
        if os.path.isfile(cls.path_config):
            cls.config.read(cls.path_config)
        else:
            os.makedirs(cls.path_dir_config, exist_ok=True)
            cls.config.read_dict(self.__GetDefaultIni())
            with open(cls.path_config, 'w', encoding='UTF-8') as f: cls.config.write(f)

    def __GetDefaultIni():
        return {
            'Path': {'Db': './res/db/'},
            'Git': {'Remote': 'HTTPS'},
            'Github': {'User': 'ytyaru'},
        }

    def __AddVariable(cls, name, attrs):
        for section in cls.config:
            for key in cls.config[section]:
                varName = cls.__GetVarName(cls, name, section, key)
                propName = cls.__GetPropName(cls, section, key)
                #attrs[varName] = None
                attrs[varName] = cls.__SetVarValue(cls, name, attrs, section, key)
                #attrs[propName] = property(lambda cls: attrs[varName])
                attrs[propName] = property(lambda cls: attrs[varName])
                #setattr(cls, propName, property(lambda cls: attrs[varName]))

    def __AddProperty(cls, name, attrs):
        print('xxxxxxxxxxxxxxxxxxxxxxxx')
        print(cls, type(cls))
        print('xxxxxxxxxxxxxxxxxxxxxxxx')
        for section in SettingMeta.config:
            for key in SettingMeta.config[section]:
                varName = SettingMeta.__GetVarName(SettingMeta, name, section, key)
                propName = SettingMeta.__GetPropName(SettingMeta, section, key)
#                attrs[propName] = property(lambda cls: attrs[varName])
                setattr(cls, propName, property(lambda cls: attrs[varName]))

    def __AddPropertyyyyyyyyyyyyyyyyyy(cls, name, attrs):
        for section in SettingMeta.config:
            for key in SettingMeta.config[section]:
                varName = SettingMeta.__GetVarName(SettingMeta, name, section, key)
                propName = SettingMeta.__GetPropName(SettingMeta, section, key)
#                attrs[propName] = property(lambda cls: attrs[varName])
                setattr(cls, propName, property(lambda cls: attrs[varName]))
                setattr(cls, propName, property(lambda cls: attrs[varName]))

    def __GetVarName(cls, name, section, key): return '_{0}__{1}'.format(name, cls.__GetPropName(cls, section, key))
    def __GetPropName(cls, section, key):
        secName = section[0].upper() + section[1:].lower()
        keyName = key[0].upper() + key[1:].lower()
        return secName + keyName
        #return '{0}{1}'.format(section, key)
        
    def __SetVarDefaultValue(cls, name, attrs):
        #cls.__path_dir_db = cls.__RelToAbs(config['Path']['Db'])
        #    if not os.path.isdir(self.__path_dir_db):
        #        os.makedirs(cls.__path_dir_db, exist_ok=True)
        cls.__SetVarValue(cls, name, attrs, 'Path', 'Db', cls.__RelToAbs(cls, cls.config['Path']['Db']))
        cls.__SetVarValue(cls, name, attrs, 'Git', 'Remote', 'HTTP')
        #cls.__SetVarValue(cls, name, attrs, 'Github', 'User')

    # セクションとキーが未定義ならデフォルト値をセットする
    def __SetVarValue(cls, name, attrs, section, key, defaultValue=None):
        varName = cls.__GetVarName(cls, name, section, key)
        if 'Path' == section and 'Db' == key:
            print('ddddddddddddddddddddddddddddddddddddddd')
            attrs[varName] = cls.__GetPathDbValue(cls)
            print(varName, attrs[varName])
        else:
            if varName not in attrs: attrs[varName] = defaultValue
            else: attrs[varName] = cls.config[section][key]
    #        if self.__IsUndefinedSectionAndKey(section, key): attrs[varName] = defaultValue
    #        else: attrs[varName] = config[section][key]

    def __GetPathDbValue(cls):
        path_dir_db = cls.__RelToAbs(cls, cls.config['Path']['Db'])
        if not os.path.isdir(path_dir_db):
            os.makedirs(path_dir_db, exist_ok=True)
        return path_dir_db

    def __RelToAbs(cls, path):
        if not os.path.isabs(path):
            # ./
            if path.startswith('./'):
                return os.path.join(cls.path_dir_root, path[2:])
            # ../../../
            abs_path = cls.base_path
            rel_path = path
            while rel_path.startswith('../'):
                rel_path = rel_path[3:]
                abs_path = os.path.dirname(abs_path)
            return os.path.join(abs_path, rel_path)
        return path





    """
    def __init__(self):
        self.__path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.__config = configparser.configParser()
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
    """
