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
        cls.__Test(cls, name)
        #cls.__Validate(cls)
        print('__init__', 'cls()._Setting__PathDb', cls()._Setting__PathDb)
        print('__init__', 'cls()._Setting__GitRemote', cls()._Setting__GitRemote)
        print('__init__', 'cls()._Setting__GithubUser', cls()._Setting__GithubUser)
        print('__init__', 'cls().PathDb', cls().PathDb)
        print('__init__', 'cls().GitRemote', cls().GitRemote)
        print('__init__', 'cls().GithubUser', cls().GithubUser)

    @classmethod
    def __Test(cls, target, name):
        for section in cls.config:
            for key in cls.config[section]:
                print('cls.config[{}][{}]={}'.format(section, key, cls.config[section][key]))
                varName = cls.__GetVarName(name, section, key)
                propName = cls.__GetPropName(section, key)
                print(varName, propName)
                setattr(target, varName, cls.config[section][key])
                #setattr(target, '_{0}__{1}'.format(name, section + key), cls.config[section][key])
                #setattr(target, '{0}'.format(section + key), property(lambda target: getattr(target, '_{0}__{1}'.format(name, section + key))))
                setattr(target, propName, property(lambda target: getattr(target, varName)))


                """
                setattr(target, '_{0}__{1}'.format(name, section + key), str(cls.config[section][key]))
                #setattr(target, '_{0}__{1}'.format(name, section + key), cls.config[section][key])
                #setattr(target, '{0}'.format(section + key), property(lambda target: getattr(target, '_{0}__{1}'.format(name, section + key))))
                setattr(target, key, property(lambda target: getattr(target, '_{0}__{1}'.format(name, section + key))))

                #setattr(target, '_{0}__{1}'.format(name, key), val) # Db.Secretプロパティ定義
                #setattr(target, key, property(lambda target: getattr(target, '_{0}__{1}'.format(name, key))))

                print(section, key, cls.config[section][key])
        print(dir(target))
                """
        #print('target().db******************', target().db)
        """
        for attr in ['Pathdb', 'Gitremote', 'Githubuser']:
        #for attr in ['PathDb', 'GitRemote', 'GithubUser']:
            print('_{0}__{1}'.format(name, attr), getattr(target, '_{0}__{1}'.format(name, attr)))
            print(attr, getattr(target, attr), getattr(target(), attr))
        """
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
                print('__SetAttributes', varName, propName)
                #setattr(target, varName, cls.__GetVarDefaultValue(target, name, attrs, section, key))

                setattr(target, varName, cls.config[section][key])
                #setattr(target, varName, cls.__GetVarDefaultValue(target, varName))
                #setattr(target, varName, cls.__GetVarDefaultValue(target, varName))
                print('__SetAttributes', varName, getattr(target(), varName))
                
                #var = getattr(target, varName)
                #setattr(target, propName, property(lambda target: var))
                #setattr(target, propName, property(lambda target: getattr(target, varName)))
                setattr(target, propName, property(lambda target: cls.config[section][key]))
                #setattr(target, propName, property(lambda target: attrs[varName])) # Db.Secretプロパティ定義
                #setattr(target, propName, property(lambda cls: attrs[varName]))
                print('__SetAttributes', propName, getattr(target(), propName))

                if hasattr(target, '_Setting__PathDb'): print('*', '_Setting__PathDb', target()._Setting__PathDb)
                if hasattr(target, '_Setting__GitRemote'): print('*', '_Setting__GitRemote', target()._Setting__GitRemote)
                if hasattr(target, '_Setting__GithubUser'): print('*', '_Setting__GithubUser', target()._Setting__GithubUser)
                if hasattr(target, 'PathDb'): print('*', 'PathDb', target().PathDb)
                if hasattr(target, 'GitRemote'): print('*', 'GitRemote', target().GitRemote)
                if hasattr(target, 'GithubUser'): print('*', 'GithubUser', target().GithubUser)

        print('__SetAttributes', 'PathDb', target().PathDb)
        print('__SetAttributes', 'GitRemote', target().GitRemote)
        print('__SetAttributes', 'GithubUser', target().GithubUser)
        print('__SetAttributes_Setting__PathDb', target()._Setting__PathDb)
        print('__SetAttributes_Setting__GitRemote', target()._Setting__GitRemote)
        print('__SetAttributes_Setting__GithubUser', target()._Setting__GithubUser)

    @classmethod
    def __GetVarName(cls, name, section, key): return '_{0}__{1}'.format(name, cls.__GetPropName(section, key))
    @classmethod
    def __GetPropName(cls, section, key):
        return cls.__FirstUpperCamelcase(section) + cls.__FirstUpperCamelcase(key)
    @classmethod
    def __FirstUpperCamelcase(cls, word):
        return word[0].upper() + word[1:].lower()

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

