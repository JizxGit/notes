如果出现像下面的情况

```bash
git status -s
?? "\350\257\264\346\230\216.txt"
```



配置变量 core.quotepath 设置为false就可以解决中文文件名在这些Git命令输出中的显示问题。

```bash
git config --global core.quotepath false
git status -s
说明.txt
```

