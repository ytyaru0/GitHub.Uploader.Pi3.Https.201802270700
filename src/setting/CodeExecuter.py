import IniToDict
import CodeTemplate
import importlib

class CodeExecuter:        
    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            super().__call__(*args, **kwargs)
            cls._instance = cls.__Execute()
            #cls._instance = super().__call__(*args, **kwargs)
            #cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance

    @classmethod
    def __Execute(self):
        class_name = 'Config'
        code = CodeTemplate(class_name).Get(IniToDict.Get())
        exec(code)
        cls = getattr(locals(), class_name)
        return cls
        #importlib.import_module('foo.some')
    """
    def Execute(self):
        class_name = 'Config'
        code = CodeTemplate(class_name).Get(IniToDict.Get())
        exec(code)
        cls = getattr(locals(), class_name)
        
        #importlib.import_module('foo.some')

    def __CreatePyFile(self):
    """
