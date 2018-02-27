import yaml
import pathlib
from _python.designpattern.Singleton import Singleton
class Yaml(metaclass=YamlMeta):
#class Yaml(metaclass=Singleton):
    def __init__(self):
        self.__Load()
        self.__SetValues()

    @property
    def Yaml(self): return self.__yaml

    def __Load(self):
        path = pathlib.Path('../res/config.yaml').resolve()
        with path.open() as f:
            self.__yaml = yaml.load(f)
            #self.Yaml = yaml.load(f)
            print(self.__yaml)

    def __SetValues(self):
        self.Yaml['Path']['Db']
        self.__SetPathDb()
        self.__SetGitRemote()

    def __SetPathDb(self):
        if '' == self.__yaml['Path']['Db']: self.__yaml['Path']['Db'] = './res/db/'
        if not pathlib.PurePath(self.__yaml['Path']['Db']).is_absolute():
            path_dir_root = pathlib.PurePath(__file__).parent.parent.parent
            self.__yaml['Path']['Db'] = pathlib.Path(path_dir_root, path_db)
            self.__yaml['Path']['Db'].mkdir(parents=True, exist_ok=True)
            print(self.Yaml['Path']['Db'])

    def __SetGitRemote(self):
        class_name = self.__yaml['Git']['Remote'][0].upper() + self.__yaml['Git']['Remote'][1:].lower()
        protocol_class = getattr(Protocol, class_name)
        self.__yaml['Git']['Remote'] = protocol_class()
        """
        if Ini().Parser.has_option('Git', 'Remote'):
            git_remote = Ini().Parser['Git']['Remote']
        else:
            git_remote = defIni['Git']['Remote']

        from web.service.github.uri import Protocol
        #import setting.Protocol
        if git_remote in {'HTTPS', 'SSH'}:
            class_name = self.Yaml['Git']['Remote'][0].upper() + self.Yaml['Git']['Remote'][1:].lower()
            protocol_class = getattr(Protocol, class_name)
        else:
            protocol_class = Protocol.Https
        self.__GitRemote = protocol_class()
        """
    #def __SetDefaultValue(self):
    #def __Validate(self):
