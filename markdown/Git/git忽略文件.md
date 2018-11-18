1. 在用户的home目录下，新建一个`.gitignore_global` 文件填写的方式与` gitignore`一模一样

2. 在用户的home目录下，打开已有的`.gitconfig`文件，在最后添加如下2行：

   ```
   [user]
           name = jizx
           email = 1822980003@qq.com
   [core]
   		excludesfile = /Users/jizhongxian/.gitignore_global
   ```
