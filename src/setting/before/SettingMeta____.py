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
        return type.__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        cls.__LoadIni()
        cls.__SetAttributes(cls, name, attrs)
        print('__init__', cls().PathDb)
        print('__init__', cls().GitRemote)
        print('__init__', cls().GithubUser)
        cls.__Validate(cls)
        #cls.__SetVarDefaultValue(cls, name, attrs)
        #cls.__AddProperty(cls, name, attrs)
        #os.makedirs(getattr(cls, cls.__GetVarName(name, 'Path', 'Db')), exist_ok=True)
        #os.makedirs(attrs[cls.__GetVarName(name, 'Path', 'Db')], exist_ok=True)
        print('__init__', cls().PathDb)
        print('__init__', cls().GitRemote)
        print('__init__', cls().GithubUser)
        #print(getattr(cls, 'PathDb'))
        #print(getattr(cls, 'GitRemote'))
        #print(getattr(cls, 'GithubUser'))

    @classmethod
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

    @classmethod
    def __GetDefaultIni(cls):
        return {
            'Path': {'Db': './res/db/'},
            'Git': {'Remote': 'HTTPS'},
            'Github': {'User': 'ytyaru'},
        }

    @classmethod
    def __SetAttributes(cls, target, name, attrs):
        for section in cls.config:
            for key in cls.config[section]:
                varName = cls.__GetVarName(name, section, key)
                propName = cls.__GetPropName(section, key)
                print('aaaaaaaaaaaaaaaaaaaaaaaaa', varName, propName)
                #setattr(target, varName, cls.__GetVarDefaultValue(target, name, attrs, section, key))

                """
                configparser: Section=大文字小文字区別する、Key=大文字小文字区別しない
                自作プロパティ名: `SectionKey`のようにSection名とKey名の区切り位置のみ大文字にしたい
                iniファイルも自作プロパティ名に合わせて書く。たとえば`Github`はOKだが、`GitHub`はNG。
                """
                """
                defIni = cls.__GetDefaultIni()
                s = cls.__FirstUpperCamelcase(section)
                k = cls.__FirstUpperCamelcase(key)
                defaultValue = defIni[s][k]
                """
                setattr(target, varName, cls.config[section][key])
                #setattr(target, varName, cls.__GetVarDefaultValue(target, varName))
                #setattr(target, varName, cls.__GetVarDefaultValue(target, varName))
                
                var = getattr(target, varName)
                setattr(target, propName, property(lambda target: var))
                #setattr(target, propName, property(lambda target: getattr(target, varName)))
                #setattr(target, propName, property(lambda target: attrs[varName])) # Db.Secretプロパティ定義
                #setattr(target, propName, property(lambda cls: attrs[varName]))
                print('__SetAttributes', propName, getattr(target(), propName))

        print('__SetAttributes', 'PathDb', target().PathDb)
        print('__SetAttributes', 'GitRemote', target().GitRemote)
        print('__SetAttributes', 'GithubUser', target().GithubUser)
        print('__SetAttributes_Setting__PathDb', target()._Setting__PathDb)
        print('__SetAttributes_Setting__GitRemote', target()._Setting__GitRemote)
        print('__SetAttributes_Setting__GithubUser', target()._Setting__GithubUser)
    """
    @classmethod
    def __AddVariable(cls, target, name, attrs):
        for section in cls.config:
            for key in cls.config[section]:
                varName = cls.__GetVarName(name, section, key)
                propName = cls.__GetPropName(section, key)
                setattr(target, varName, cls.__GetVarDefaultValue(target, name, attrs, section, key))
                setattr(target, propName, property(lambda cls: attrs[varName]))
    """
    """
    @classmethod
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
    """
    """
    @classmethod
    def __AddPropertyyyyyyyyyyyyyyyyyy(cls, name, attrs):
        for section in SettingMeta.config:
            for key in SettingMeta.config[section]:
                varName = SettingMeta.__GetVarName(SettingMeta, name, section, key)
                propName = SettingMeta.__GetPropName(SettingMeta, section, key)
#                attrs[propName] = property(lambda cls: attrs[varName])
                setattr(cls, propName, cls.__SetVarValue(target, name, attrs, section, key), )
                setattr(cls, propName, property(lambda cls: attrs[varName]))
    """

    @classmethod
    def __GetVarName(cls, name, section, key): return '_{0}__{1}'.format(name, cls.__GetPropName(section, key))
    @classmethod
    def __GetPropName(cls, section, key):
        return cls.__FirstUpperCamelcase(section) + cls.__FirstUpperCamelcase(key)
        """
        secName = section[0].upper() + section[1:].lower()
        keyName = key[0].upper() + key[1:].lower()
        return secName + keyName
        #return '{0}{1}'.format(section, key)
        """
    @classmethod
    def __FirstUpperCamelcase(cls, word):
        return word[0].upper() + word[1:].lower()

    """
    @classmethod
    def __GetVarDefaultValue(cls, section, key):
        #configparserと自作プロパティ名とで命名規則が異なる点に注意！
        #  configparser: Section=大文字小文字区別する、Key=大文字小文字区別しない
        #  自作プロパティ名: `SectionKey`のようにSection名とKey名の区切り位置のみ大文字にしたい
        #iniファイルも自作プロパティ名に合わせて書く。たとえば`Github`はOKだが、`GitHub`はNG。
        defIni = cls.__GetDefaultIni()
        s = cls.__FirstUpperCamelcase(section)
        k = cls.__FirstUpperCamelcase(key)
        return defIni[s][k]

    @classmethod
    def __SetVarValue(cls, target, section, key, value):
        varName = cls.__GetVarName(name, section, key)
        s = cls.__FirstUpperCamelcase(section)
        k = cls.__FirstUpperCamelcase(key)
        # デフォルト値をセットする
        if 'Git' == section and 'Remote' == key: defaultValue = 'HTTPS'
        else: defaultValue=None
        # デフォルト値を返す
#        if 'Path' == section and 'Db' == key: return cls.__GetPathDbValue()
        if 'Path' == section and 'Db' == key:
            print('******************************************')
            setattr(cls, varName, value)
            print(target, varName, cls.__RelToAbs(cls.config[section][key]))
            return cls.__RelToAbs(cls.config[section][key])
        else:
            if not hasattr(target, varName): return defaultValue
            else: return cls.config[section][key]
    """

    @classmethod
    def __Validate(cls, target):
        defIni = cls.__GetDefaultIni()
        #varName = cls.__GetVarName(name, section, key)
        # Git Remote
        if not hasattr(target, '_Setting__GitRemote'):
            setattr(target, '_Setting__GitRemote', defIni['Git']['Remote'])
        else:
            if getattr(target, '_Setting__GitRemote') not in {'HTTPS', 'SSH'}:
                setattr(target, '_Setting__GitRemote', defIni['Git']['Remote'])
        # Path Db
        if not hasattr(target, '_Setting__PathDb'):
            path_db = defIni['Path']['Db']
        else:
            path_db = getattr(target, '_Setting__PathDb')
        setattr(target, '_Setting__PathDb', cls.__RelToAbs(path_db))
        os.makedirs(getattr(target, '_Setting__PathDb'), exist_ok=True)
        
    """
    @classmethod
    def __GetVarDefaultValue(cls, target, varName, section, key):
        s = cls.__FirstUpperCamelcase(section)
        k = cls.__FirstUpperCamelcase(key)
        # デフォルト値をセットする
        if 'Git' == s and 'Remote' == k: return 'HTTPS'
        if 'Path' == s and 'Db' == k: return cls.__RelToAbs(cls.config[section][key])
        else: None
    """
    """
        # デフォルト値をセットする
        if '_Setting__GitRemote' == varName: return 'HTTPS'
        else: defaultValue=None
        # デフォルト値を返す
        if '_Setting__PathDb' == varName: return ''
            return cls.__RelToAbs(cls.config[section][key])
        else:
            if not hasattr(target, varName): return defaultValue
            else: return cls.config[section][key]
    """
    """
    @classmethod
    def __GetVarDefaultValue(cls, target, varName):
        # デフォルト値をセットする
        if '_Setting__GitRemote' == varName: defaultValue = 'HTTPS'
        else: defaultValue=None
        # デフォルト値を返す
        if '_Setting__PathDb' == varName:
            return cls.__RelToAbs(cls.config[section][key])
        else:
            if not hasattr(target, varName): return defaultValue
            else: return cls.config[section][key]
    """
    """
    @classmethod
    def __GetVarDefaultValue(cls, target, name, attrs, section, key):
        print(section, key)
        varName = cls.__GetVarName(name, section, key)
        # デフォルト値をセットする
        if 'Git' == section and 'Remote' == key: defaultValue = 'HTTPS'
        else: defaultValue=None
        # デフォルト値を返す
#        if 'Path' == section and 'Db' == key: return cls.__GetPathDbValue()
        if 'Path' == section and 'Db' == key:
            print('******************************************')
            print(target, varName, cls.__RelToAbs(cls.config[section][key]))
            return cls.__RelToAbs(cls.config[section][key])
        else:
            if not hasattr(target, varName): return defaultValue
            else: return cls.config[section][key]
    """
    """
    @classmethod
    def __SetVarDefaultValue(cls, target, name, attrs):
        #cls.__path_dir_db = cls.__RelToAbs(config['Path']['Db'])
        #    if not os.path.isdir(self.__path_dir_db):
        #        os.makedirs(cls.__path_dir_db, exist_ok=True)
        cls.__SetVarValue(target, name, attrs, 'Path', 'Db', cls.__RelToAbs(cls.config['Path']['Db']))
        cls.__SetVarValue(target, name, attrs, 'Git', 'Remote', 'HTTP')
        #cls.__SetVarValue(cls, name, attrs, 'Github', 'User')

    # セクションとキーが未定義ならデフォルト値をセットする
    @classmethod
    def __SetVarValue(cls, target, name, attrs, section, key, defaultValue=None):
        varName = cls.__GetVarName(name, section, key)
        if 'Path' == section and 'Db' == key:
            print('ddddddddddddddddddddddddddddddddddddddd')
            #attrs[varName] = cls.__GetPathDbValue()
            #print(varName, attrs[varName])
            setattr(target, varName, cls.__GetPathDbValue())
            print(varName, '=', getattr(target, varName))
        else:
            if varName not in attrs: attrs[varName] = defaultValue
            else: attrs[varName] = cls.config[section][key]
    #        if self.__IsUndefinedSectionAndKey(section, key): attrs[varName] = defaultValue
    #        else: attrs[varName] = config[section][key]
    """
    """
    @classmethod
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
    """

    """
    @classmethod
    def __GetPathDbValue(cls):
        path_dir_db = cls.__RelToAbs(cls.config['Path']['Db'])
        if not os.path.isdir(path_dir_db):
            os.makedirs(path_dir_db, exist_ok=True)
        return path_dir_db
    """

    @classmethod
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
