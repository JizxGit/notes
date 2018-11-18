#————————————————————元类法——————————————————————
class Singleton(type):
    # __new__方法它主要用于我们需要对类的结构进行改变的时候我们才要重写这个方法。

    def __init__(self, *args, **kwargs):
        print("__init__")
        self.__instance = None
        super().__init__(*args, **kwargs)

    # Foo()会调用元类中的call方法 【1】
    def __call__(self, *args, **kwargs):
        print("__call__")
		# self指的是Foo类
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance


class Foo(object, metaclass=Singleton):
    def __init__(self):
        print("instance_init")

    # foo()会调用Foo类中的call方法 【2】
    def __call__(self):
        print("instance_call")
# 在代码执行到这里的时候，元类中的__new__方法和__init__方法其实已经被执行了，
# 而不是在Foo实例化的时候执行。且仅会执行一次。

foo1 = Foo() # 进入元类的call方法【1】
foo1() # 进入Foo的call方法【2】
foo2 = Foo()
print(foo1 is foo2)

#————————————————————new法——————————————————————
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


s1 = Singleton()
s2 = Singleton()

print s1 is s2

