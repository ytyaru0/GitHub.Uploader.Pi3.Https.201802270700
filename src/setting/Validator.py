import configparser
import os
import os.path
import pathlib
class Validator:

    def Valid(self, iniDict):
        self.__iniDict = iniDict
        self.__CreateConfigParser()



    def __Validate(self, target):
        self.__iniDict

        # Git Remote
        if not hasattr(target, 'GitRemote'):
            setattr(target, 'GitRemote', defIni['Git']['Remote'])
        else:
            if getattr(target, '_Setting__GitRemote') not in {'HTTPS', 'SSH'}:
                setattr(target, '_Setting__GitRemote', defIni['Git']['Remote'])
        # Path Db
        if not hasattr(target, '_Setting__PathDb'):
            path_db = defIni['Path']['Db']
        else:
            path_db = getattr(target, '_Setting__PathDb')
        setattr(target, '_Setting__PathDb', cls.__RelToAbs(path_db))
        os.makedirs(getattr(target, '_Setting__PathDb'), exist_ok=Tr





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

