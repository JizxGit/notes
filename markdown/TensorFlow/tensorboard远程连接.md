想要在本机的浏览器查看远程服务器的tensorboard

在本机的命令行里输入如下：

```
ssh -L 16006:127.0.0.1:6006 zxji@192.168.140.158
zxji@192.168.140.158's password:
```

就会登录远程的服务器，然后在本机启动服务器的tensorboard，可指定端口，与上面的命令要一致“6006”

```
[zxji@localhost logs]$ tensorboard --port=6006 --logdir="./"
```

最后就可以在本机的浏览器输入

```
http://localhost:16006
```

> 注意16006、6006 这些端口