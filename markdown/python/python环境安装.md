1. 下载3.6版本的anaconda，这样这个环境中默认的python就是3.6的

    https://www.anaconda.com/download/#macos

2. 根据提示完成安装，这时命令行中`conda --version` 无法执行，

   **for anaconda 2 :**

   ```
   export PATH=~/anaconda2/bin:$PATH
   ```

   **for anaconda 3 :**

    ```
    export PATH=~/anaconda3/bin:$PATH
    ```

   然后通过`conda --version` 确认

3. `export PATH=~/anaconda3/bin:$PATH` **有效时间为这次终端结束**，因此应该通过`sudo nano ~/.bashrc`(bash) 或者 `sudo nano ~/.zshrc`(zsh)修改配置文件，将命令复制保存在文件中，最后通过` source .bashrc`加载新的配置信息，使得配置立即生效。

4. 在pycharm设置中搜索 interpreter，添加解释器，选择conda 环境，如果想让新项目默认使用该解释器，勾选**make available to all projects**