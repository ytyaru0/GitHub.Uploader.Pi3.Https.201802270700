class CodeTemplate:
    def __init__(self, ClassName):
        self.__cls = f'class {ClassName}:\n'
        self.__init = '    def __init__(self):\n'
        self.__setAttr = "        self.__{PropertyName} = '{Value}'\n"
        self.__decorator = '    @property\n'
        self.__method = '    def {PropertyName}(self): return self.__{PropertyName}\n'
    def Get(self, NameAndValues):
        code = self.__cls + self.__init
        for p, v in NameAndValues.items():
            code += self.__setAttr.format(PropertyName=p, Value=v)
        code += '\n'
        for p in NameAndValues.keys():
            code += self.__decorator
            code += self.__method.format(PropertyName=p) + '\n'
        return code
