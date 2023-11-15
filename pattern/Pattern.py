from abc import abstractmethod

class MetaPattern(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'subpatterns'):
            cls.subpatterns = []
        else:
            cls.subpatterns.append(cls)
        super(MetaPattern, cls).__init__(name, bases, attrs)

class Pattern(metaclass=MetaPattern):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def mode(self) -> str:
        """
        应当返回该模式的正则字符串。
        """
        pass 

    @abstractmethod
    def next_title(self, title: str) -> str:
        """
        应当返回该模式下，给定 title 时的下一个标题。
        """
        pass

class Pattern1(Pattern):
    def mode(self) -> str:
        return r'\d\.'
    def next_title(self, title: str) -> str:
        digit = title[:-1]
        return str(int(digit) + 1) + '.'
class Pattern2(Pattern):
    def __init__(self):
        self.chars = '一二三四五六七八九十'
    def mode(self) -> str:
        return r'[一二三四五六七八九十]、'
    def next_title(self, title: str) -> str:
        char = title[0]
        idx = (self.chars.find(char) + 1) % len(self.chars)
        return self.chars[idx] + '、'