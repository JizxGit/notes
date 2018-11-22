### pickle

The [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) module 实现了二进制协议，用于serializing 和 de-serializing  Python object structure 并保存到磁盘中，并在需要的时候读取出来，任何对象（lambda除外）都可以执行序列化操作。

Pickle模块中最常用的函数为：

#### 保存为文件

1. `dump(obj, file, [,protocol])`

   功能：将obj对象序列化存入已经打开的file中。

   - obj: 想要序列化的obj对象。
   - file: file对象
   - protocol: 序列化使用的协议。如果该项省略，则默认为0。如果为负值或HIGHEST_PROTOCOL，则使用最高的协议版本。

   ```python
   with open('data.pickle', 'wb') as file:
       # 使用 highest protocol Pickle the 'data' dictionary 
       pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
   ```

2. `load(file)`

    功能：将file中的对象反序列化读出。

    ```python
    with open('data.pickle', 'rb') as file:
        # protocol版本会自动检测，不要指定
        data = pickle.load(file)
    ```

> 因为pickle是使用二进制保存文件，因此open的读写模式，要使用‘b’

#### 保存为string

1. `dumps(obj [, protocol])`

    功能：将obj对象**序列化为`string`形式**，而不是存入文件中。

    - obj：想要序列化的obj对象。

    - protocol：如果该项省略，则默认为0。如果为负值或HIGHEST_PROTOCOL，则使用最高的协议版本。

2. `loads(string)`

    函数的功能：从string中读出序列化前的obj对象。

    - string：pickle序列化后的字符串对象

    ```python
    import pickle
    # dumps
    li = [11,22,33]
    r = pickle.dumps(li)
    print(r)
    #(lp0
    # I11
    # aI22
    # aI33
    # a.

    # loads
    result = pickle.loads(r)
    print(result)
    # [11, 22, 33]
    ```


### tqdm(TODO)

tqdm(list)，会自动获取list的长度，显示对应的进度



### os

#### 创建目录

`os.mkdir` 与`os.makedirs`的差别在于 **`os.makedirs` 会递归地去建立目录**，也就是说连同中继的目录也会一起建立，就类似于 Linux 中的 `mkdir -p`．

```
>>> import os
>>> os.mkdir('foo/bar')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 2] No such file or directory: 'foo/bar'
>>> os.makedirs('foo/bar')
```

使用 `os.mkdir `时，如果你给定的 path 参数是个多层的 path，如果某个中继的目录不存在(比如说上例中的 foo), Python 将会报错．

但如果使用 `os.makedirs` 则 Python 会连同中间的目录一起建立．但有一点值得注意，当 path 末端的目录已经存在的话，os.makedirs 也是会引发例外．