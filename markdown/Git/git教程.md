

![](./git常用命令流程图.png)

## Git本地基本

### 配置全局信息

当安装完 Git 应该做的**第一件事**就是设置你的用户名称与邮件地址。 这样做很重要，因为每一个 Git 的提交都会使用这些信息，并且它会写入到你的每一次提交中，不可更改

```bash
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```

> 注意：`git config`命令的`--global`参数，用了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址。在那个项目目录下运行没有`--global`选项的命令来配置。

其他有用的配置

```bash
git config --global core.editor "notepad"  #commit时的默认编辑器
```



### 查看配置信息

如果想要检查你的配置，可以使用 git config --list 命令来列出所有 Git 当时能找到的配置。

```bash
git config--list

user.name=JohnDoe
user.email=johndoe@example.com
color.status=auto
color.branch=auto
color.interactive=auto
color.diff=auto
...
```

你可能会看到重复的变量名，因为 Git 会从不同的文件中读取同一个配置（例如：/etc/gitconfig 与~/.gitconfig）。 这种情况下，Git 会使用它找到的每一个变量的最后一个配置。

你可以通过输入 `git config <key>`： 来检查 Git 的某一项配置

```
$ git config user.name
Jizx
```

### 创建仓库

#### 在现有目录中初始化仓库

通过`git init`命令把这个目录(可以是非空目录)变成Git可以管理的仓库。

如果你是在一个已经存在文件的文件夹（而不是空文件夹）中初始化 Git 仓库来进行版本控制的话，你应该开始跟踪这些文件并提交。 你可通过 `git add `命令来实现对指定文件的跟踪，然后执行` git commit` 提交

 

#### 克隆现有的仓库

克隆仓库的命令格式是 `git clone [url] 本地仓库名字 `。可以不定义本地仓库名字，默认适应原仓库名字。比如，要克隆 Git 的可链接库 libgit2，可以用下面的命令：

`$ git clonehttps://github.com/libgit2/libgit2  mylibgit2`

这会在当前目录下创建一个名为 “mylibgit2”的目录，并在这个目录下初始化一个 .git 文件夹，从远程仓库拉取下所有数据放入 .git 文件夹，然后从中读取最新版本的文件的拷贝。



### 提交文件

**第一步，**用命令git add告诉Git，把文件添加到暂存区：

`git add readme.txt`

add一个文件之后，如果又对文件进行了修改，需要重新add，不然commit只会保存最后一次git add的文件内容。

 

**第二步，**用命令git commit告诉Git，把文件提交到仓库：

`git commit -m "wrote a readmefile"`

或者git commit，将会打开默认的文本编辑器（vim）进行文字输入。若实在不习惯 Vim，也可以设置为其它编辑器：

`git config --global core.editor "notepad"`

其中 notepad 可以替换为更好用的 wordpad、notepad++ 等（不过它们在命令行里无法直接访问，得先设置 PATH 变量）。

为什么Git添加文件需要add，commit一共两步呢？因为commit可以一次提交很多文件，所以你可以多次add不同的文件，比如：

```bash
git addfile1.txt
git addfile2.txt file3.txt
git commit-m "add 3 files."
```



**快速提交：**

Git 提供了一个跳过使用暂存区域的方式，只要在提交的时候，`git commit -a` 选项，Git 就会自动把所有已经跟踪过的文件暂存起来一并提交，**从而跳过 git add 步骤**。



### 重新提交

有时候我们提交完了才发现漏掉了几个文件没有添加，或者提交信息写错了。 此时，可以运行带有`--amend` 选项的提交命令尝试重新提交，命令执行后将暂存区中的文件提交，因此分为以下2种情况：

1. 修改提交信息：

   `git commit --amend`

2. 添加忘记/漏add的文件，同时修改提交信息：
   ```bash
   $ git commit -m 'initial commit'  # 错误的提交
   $ git add forgotten_file
   $ git commit –amend
   ```

### 查看文件状态

要查看哪些文件处于什么状态，可以用 `git status` 命令。

使用 `git status -s` 命令或 `git status --short `命令，你将得到一种更为紧凑的格式输出。

```
$ git status -s
 M README
MM Rakefile
A  lib/git.rb
M  lib/simplegit.rb
?? LICENSE.txt
```

- ?? 标记：新添加的未跟踪文件
- A 标记：新添加到暂存区中的文件
- M 标记：修改过的文件
  - 出现在**右边的 M**表示该文件被修改了但是还没放入暂存区
  - 出现在**左边的 M**表示该文件被修改了并放入了暂存区。

例如，上面的状态报告显示： README 文件在工作区被修改了但是还没有将修改后的文件放入暂存区，lib/simplegit.rb 文件被修改了并将修改后的文件放入了暂存区。 而 **Rakefile 在工作区被修改并提交到暂存区后又在工作区中被修改了**，所以在暂存区和工作区都有该文件被修改了的记录。

![文件状态周期](./文件状态周期.png)

Untracked未跟踪的文件意味着 Git 在之前的快照（提交）中没有这些文件（比如新建的文件）；Git 不会自动将之纳入跟踪范围，除非你明明白白地告诉它“我需要跟踪该文件”。被追踪后处于3种状态：未修改-已修改-已暂存。将暂存的文件commit后就保存在git数据库中，文件就回到未修改状态了。
接下来介绍如何对修改的文件进行版本控制。

### 查看文件修改内容

![查看文件变化内容](./查看文件变化内容.png)

查看**尚未暂存的文件**更新了哪些部分，输入` git diff`
此命令比较的是工作目录中当前文件和暂存区域快照之间的差异， 也就是修改之后还没有暂存起来的变化内容。

查看**暂存区里将要添加到下次提交**里的内容，可以用 `git diff --cached`命令。
也就是查看暂存区里与已保存的文件的区别（Git 1.6.1 及更高版本还允许使用 git diff --staged，效果是相同的，但更好记些。）

### 忽略文件（不追踪文件）

在Git工作区的根目录下创建一个特殊的.gitignore文件，（window下直接新建不了，最好用命令行创建）使用命令` cat .gitignore`或者` touch .gitignore`，然后把要忽略的文件名或者目录填进去，Git就会自动忽略这些文件、文件夹。最后一步就是把``.gitignore`也提交到Git，就完成了！

> 注意：`.gitignore`文件只能作用于 Untracked Files，也就是那些从来没有被 Git 记录过的文件（自添加以后，从未 add 及 commit 过的文件）。如果要忽略被提交了的文件，请看【删除文件、取消追踪、恢复误删】这节内容



#### gitignore编写规则

1.     所有空行或者以 # 开头的行都会被 Git 忽略。


2.     可以使用标准的 glob 模式匹配。
3.     匹配模式可以以（/）开头防止递归。
4.     以（/）结尾 指定目录，忽略该目录下全部内容。
5.     要忽略指定模式以外的文件或目录，可以在模式前加上惊叹号（!）取反。

所谓的 **glob 模式**是指shell 所使用的简化了的正则表达式。

- 星号`*`匹配零个或多个任意字符；[abc] 匹配任何一个列在方括号中的字符
- 问号`?`只匹配一个任意字符；
- 如果在方括号中使用短划线分隔两个字符，表示所有在这两个字符范围内的都可以匹配（比如 [0-9] 表示匹配所有 0 到 9 的数字）。
- 使用两个星号`**` 表示匹配**任意中间目录**，比如`a/**/z` 可以匹配 `a/z, a/b/z 或 a/b/c/z`等。

```bash
# 忽略任何 以 .a 结尾文件
*.a
# 但不忽略 lib.a 这个例外
!lib.a

# 只忽略当前文件夹下的 TODO ，不忽略子文件夹下的 subdir/TODO
/TODO

# 忽略全部在 build/ 文件夹下的文件
build/

# 只忽略doc文件夹下的.txt,子目录下的doc/server/arch.txt 不受影响，
doc/*.txt 

# 忽略所有doc文件夹下的 .pdf 文件
doc/**/*.pdf
```

GitHub 在 [github/gitignore](https://github.com/github/gitignore)仓库 提供了一个官方推荐的 .gitignore 文件列表，包括各种流行的操作系统、环境、开发语言。

#### 强制添加

有些时候，你想添加一个文件到Git，但发现添加不了，原因是这个文件被.gitignore忽略了：

```bash
$ git add App.class

The following paths are ignored by one of your .gitignore files:
    App.class
Use -f if you really want to add them.
```

如果你确实想添加该文件，可以用`-f`强制添加到Git：
`git add -f App.class`
当然也可以在.gitignore里使用`!`排除这个文件。

#### 忽略已经添加到git的文件

如果你已经将文件提交到到git中，那么git不会处理你后来添加的gitignore规则。这种情况就需要通过下面的命令先取消追踪文件：

```bash
git rm --cached filename
```



#### 测试规则

或者你发现，可能是`.gitignore`写得有问题，需要找出来到底哪个规则写错了，可以用`git check-ignore`命令检查：

```bash
$ git check-ignore -v App.class
.gitignore:3:*.class    App.class
```

Git会告诉我们：.gitignore的第3行规则忽略了该文件，于是我们就可以知道应该修订哪个规则。



#### 全局忽略

可以为你的电脑上每个仓库创建一份全局的忽略文件，这样就不必每个仓库都单独创建一个gitignore文件。

1. 在home目录创建`~/.gitignore_global`文件
2. 在命令行中执行`git config --global core.excludesfile ~/.gitignore_global`

The Octocat 提供了一个推荐列表 方便添加到全局忽略文件中 [a Gist containing some good rules](https://gist.github.com/octocat/9257657) 

#### 本地忽略

` .gitignore` 这个文件本身会提交到版本库中去，用来保存的是公共的需要排除的文件。

如果你不想创建一份与他人共享的`.gitignore`，比如由你的编辑器产生的附属文件，而别人不会产生的情况。可以订制一份本地的忽略规则，这份规则不会提交到git中。

打开仓库中的`.git/info/exclude` 文件，在这里添加忽略规则即可，这里设置的则是你自己本地需要排除的文件。 他不会影响到其他人。也不会提交到版本库中去。



### 撤销修改、提交

#### 取消本地修改

场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时， 使用命令`git checkout –– filename`。`git checkout`其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原”。

#### 取消add

场景2：当你不但改乱了工作区某个**已经追踪的文件**的内容，还添加到了暂存区时(`git add`)，想丢弃修改，分两步：

1. 第一步用命令`git reset HEAD fileName`（取消add到暂存区），就回到了场景1（即文件未暂存到暂存区中，仍为被修改过的状态）
2. 第二步按场景1操作。

如果是新文件（未提交到git中），那么应该使用`git rm --cached <file>` 来取消add操作。

![](./撤销修改.png)

#### 版本回退

场景3：当你不但添加到了暂存区时(`git add`)，还提交了(`git commit`)，那就得进行版本回退了

在Git中，用`HEAD`表示当前版本，上一个版本就是`HEAD^`，上上一个版本就是`HEAD^^`，当然往上100个版本写100个^比较容易数不过来，所以写成`HEAD~100`。

上面的方法仅适合近期恢复，如果忘记应该回退到哪个版本或者要回退到比较久之前的版本，应该通过`git log` 查看commit id，即可回退到你需要的时间点

```bash
$ git log
commit c0ce54b1ce75f69259d7f615bf280ff7a07e3eac (HEAD -> master, origin/master, origin/HEAD)
Author: jizx <1822980003@qq.com>
Date:   Sun Nov 18 23:16:49 2018 +0800

    git命令行中文乱码解决方法

commit 0c0bfca1e3208d83a89366c5be76982d24e03dee
Author: jizx <1822980003@qq.com>
Date:   Sun Nov 18 20:52:07 2018 +0800

    过滤上根目录的DS_Store
```

其中commit 后面的一串字符串就是commit id

```bash
$ git reset --hard HEAD^     # 回退到上一个版本
$ git reset --hard commit_id # 通过git log 获取的commit id
```


第二天早上就后悔了，想恢复到新版本怎么办？找不到新版本的commit id怎么办？在Git中，总是有后悔药可以吃的，Git提供了一个命令`git reflog`用来记录你的每一次命令，这样就可以找到你全部提交过的commit id。



### 删除文件、取消追踪、恢复误删

- 同时删除库中的文件与工作目录的文件：

  使用命令`git rm fileName`删掉，并且`git commit –m “someLog”`

- 仅删除库中的文件（取消追踪/恢复未追踪状态）：

  换句话说，你想让文件保留在磁盘，但是并不想让 Git 继续跟踪,可以输入命令：`git rm –cached filename/dir `

- 另一种情况是**在文件夹里误删了**，因为版本库里还有呢，所以可以很轻松地把误删的文件恢复到最新版本：`git checkout -- test.txt`

### 文件重命名

要在 Git 中对文件改名，可以这么做：

 `git mv README.md NewName.md`

其实，运行 `git mv` 就相当于运行了下面三条命令：

```bash
mv README.md NewName.md
git rm README.md
git add NewName.md
```

如此分开操作，Git 也会意识到这是一次改名，所以不管何种方式结果都一样。两者唯一的区别是，`git mv` 是一条命令而另一种方式需要三条命令，直接用 `git mv `轻便得多。 不过有时候用其他工具批处理改名的话，要记得在提交前删除老的文件名，再添加新的文件名。



### 版本历史

#### git log

`git log`   显示从最近到最远的提交日志

`git log -p -2`  一个常用的选项是 -p，用来显示每次提交的内容差异。你也可以加上 -2 来仅显示最近两次提交 
`git log --decorate`  命令查看各个分支当前所指的对象。

`git log --pretty=oneline`
另外一个常用的选项是`--pretty`。 这个选项可以**指定使用不同于默认格式的方式展示**提交历史。 这个选项有一些内建的子选项供你使用。 比如用`oneline` 将每个提交放在一行显示，查看的提交数很大时非常有用。 另外还有` short，full 和 fuller`可以用（不过不怎么实用）。

`git log --pretty=format:"%h - %an, %ar : %s"` 最有意思的是format，可以定制要显示的记录格式

| **选项**  | 说明                         |
| :-----: | -------------------------- |
| **%H**  | 提交对象（commit）的完整哈希字串        |
| **%h**  | 提交对象的简短哈希字串                |
| **%T**  | 树对象（tree）的完整哈希字串           |
| **%t**  | 树对象的简短哈希字串                 |
| **%P**  | 父对象（parent）的完整哈希字串         |
| **%p**  | 父对象的简短哈希字串                 |
| **%an** | 作者（author）的名字              |
| **%ae** | 作者的电子邮件地址                  |
| **%ad** | 作者修订日期（可以用 --date= 选项定制格式） |
| **%ar** | 作者修订日期，按多久以前的方式显示          |
| **%cn** | 提交者(committer)的名字          |
| **%ce** | 提交者的电子邮件地址                 |
| **%cd** | 提交日期                       |
| **%cr** | 提交日期，按多久以前的方式显示            |
| **%s**  | 提交说明                       |

> **作者**指的是实际作出修改的人，**提交者**指的是最后将此工作成果提交到仓库的人



图像化展示提交记录

`$ git log --graph`

`$ git log --graph --pretty=oneline --abbrev-commit` 简洁视图版本

当 oneline 或 format 与另一个 log 选项 --graph 结合使用时尤其有用。 这个选项添加了一些ASCII字符串来形象地展示你的分支、合并历史。

 **git log** 的常用选项，可以一起使用                                     

| **选项**              | **说明**                                   |
| ------------------- | ---------------------------------------- |
| **-p**              | 按补丁格式显示每个更新之间的差异。                        |
| **--stat**          | 显示每次更新的文件修改统计信息。                         |
| **--shortstat**     | 只显示 --stat 中最后的行数修改添加移除统计。               |
| **--name-only**     | 仅在提交信息后显示已修改的文件清单。                       |
| **--name-status**   | 显示新增、修改、删除的文件清单。                         |
| **--abbrev-commit** | 仅显示 SHA-1 的前几个字符，而非所有的 40 个字符。           |
| **--relative-date** | 使用较短的相对时间显示（比如，“2 weeks ago”）。           |
| **--graph**         | 显示 ASCII 图形表示的分支合并历史。                    |
| **--pretty**        | 使用其他格式显示历史提交信息。可用的选项包括 oneline，short，full，fuller 和 format（后跟指定格式）。 |



限制`git log`输出的选项

| **选项**                    | **说明**            |
| ------------------------- | ----------------- |
| **-(n)**                  | 仅显示最近的 n 条提交      |
| **--since**, **--after**  | 仅显示指定时间之后的提交。     |
| **--until**, **--before** | 仅显示指定时间之前的提交。     |
| **--author**              | 仅显示指定作者相关的提交。     |
| **--committer**           | 仅显示指定提交者相关的提交。    |
| **--grep**                | 仅显示含指定关键字的提交      |
| **-S**                    | 仅显示添加或移除了某个关键字的提交 |



例子：
`git log --pretty="%h - %s" --author=gitster --since="2008-10-01" --before="2008-11-01" `



#### git relog

`$ git reflog`  //查看全部命令记录，以及HEAD指针



### git help 命令提示

```
git help command # 可以显示某条command的使用方法
```



## Git远程



### 从远程仓库克隆到本地

在某个目录下，打开命令行，运行以下命令，就可以把远程的仓库克隆到当前目录


```bash
# 通用命令
$ git clone username@host:/path/to/repository
```

```bash
# 如果远程服务器是github
$ git clone git@github.com:你的GitHub用户名/你的某一个仓库名.git
# .git可以不用写
```
默认远程仓库别名为 origin，如果要自定义，可以在克隆时运行命令：
`git clone -o jizx git@github.com:你的GitHub用户名/你的某一个仓库名.git`，那么你默认的远程分支名字将会是 `jizx/master`
注意：克隆后本地只有master分支，如果想要把别的分支如dev克隆下来，需要使用:`git checkout -b dev origin/dev`
也就是说，当你的小伙伴从远程库clone时，默认情况下，你的小伙伴只能看到本地的master分支。现在，你的小伙伴要在dev分支上开发，就必须创建远程origin的dev分支到本地，于是他用这个命令创建本地dev分支：`git checkout -b dev origin/dev`
git clone 命令会自动设置本地 master 分支跟踪克隆的远程仓库的 master 分支（或不管是什么名字的默认分支）

### 本地关联到远程仓库

#### 空文件夹

新建一个文件夹，进入文件夹后使用git init命令，然后再使用`git remote add `命令关联一个远程仓库，再使用`git pull` 命令就可以把管理仓库的所有文件复制到本文件夹中，同样可以修改文件并完成push。

```bash
# 通用命令
$ git remote add remoteName  git@server-name:path/仓库名.git

# github服务器命令
$ git remote add remoteName  git@github.com:你的用户名/你的某一个仓库名.git
```

或者在一个文件夹下直接使用`git clone`命令，会把远程仓库整个复制到这个文件夹下，然后进入这个文件夹就可以修改文件并完成push。 这时默认远程的url别名为origin

#### 非空仓库(TODO非空文件怎么关联)



### 查看远程库信息

用`git remote`可以查看到默认的远程库：`origin`

用`git remote -v`显示更详细的信息：

```bash
$ git remote-v
origin  git@github.com:jizxgit/learngit.git (fetch)
origin  git@github.com:jizxgit/learngit.git (push)
```

### remote 详细用法

`git help remote` 即可显示详细命令用法

```bash
git remote [-v | --verbose]
git remote add [-t <branch>] [-m <master>] [-f] [--[no-]tags] [--mirror=<fetch|push>] <name> <url>
git remote rename  <old>  <new>
git remote remove  <name>
git remote rm  <name>
git remote set-head <name> (-a | --auto | -d | --delete | <branch>)
git remote set-branches [--add] <name> <branch>…
git remote get-url [--push] [--all] <name>
git remote set-url [--push] <name> <newurl> [<oldurl>]
git remote set-url --add [--push] <name> <newurl>
git remote set-url --delete [--push] <name> <url>
git remote [-v | --verbose] show [-n] <name>…
git remote prune [-n | --dry-run] <name>…
git remote [-v | --verbose] update [-p | --prune] [(<group> | <remote>)…]
```



### 本地推送到远程仓库

第一次更新时： `git push -u origin master`

origin：远程服务器url别名  master：本地仓库的一个分支

加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令

以后更新时： `git push origin master`

如果要推送本地其他分支，比如dev，就改成：
`git push origin dev`

以上其实做了一定的简化，完整的命令是：

```bash
$ git push origin 本地分支：远程分支
```

如果并不想让远程仓库上的分支叫做 serverfix，可以运行 `git push origin serverfix:awesomebranch`来将本地的 serverfix 分支推送到远程仓库上的 awesomebranch 分支。

但是，并不是一定要把本地分支往远程推送，那么，哪些分支需要推送，哪些不需要呢？

- master分支是主分支，因此要时刻与远程同步；
- dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；
- bug分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；
- feature分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。

#### 冲突、推送失败

当你和其他人在同一时间克隆，他们先推送到上游然后你再推送到上游，你的推送就会毫无疑问地被拒绝。 你必须先将他们的工作拉取pull下来并将其合并进你的工作后才能推送。



相当于是从远程获取最新版本并merge到本地

### 从远程仓库获取数据

`$ git fetch [remote-name]`

这个命令会访问远程仓库，从中拉取所有你**还没有的数据**。 执行完成后，你将会拥有那个远程仓库中所有分支的引用，可以随时合并或查看，它并**不会自动合并或修改你当前的工作**。

`$ git pull [remote-name]`

如果你有一个分支设置为**跟踪一个远程分支**，可以使用 git pull 命令来自动的抓取然后合并远程分支到当前分支。git clone 命令会自动设置本地 master 分支跟踪克隆的远程仓库的 master 分支（或不管是什么名字的默认分支）。 运行 git pull 通常会从最初克隆的服务器上抓取数据并**自动尝试合并到当前所在的分支**。

如果git pull失败，一般是因为没有指定本地dev分支与远程origin/dev分支的链接，根据提示，设置dev和origin/dev的链接：

```bash
$ git branch --set-upstream dev origin/dev

Branch dev set up to track remote branch dev from origin.
```

### 删除远程分支

假设你已经通过远程分支做完所有的工作了，也就是说你和你的协作者已经完成了一个特性并且将其合并到了远程仓库的 master 分支（或任何其他稳定代码分支）。 可以运行带有` --delete` 选项的 `git push` 命令来删除一个远程分支。 如果想要从服务器上删除 serverfix 分支，运行下面的命令：

```bash
$ git push origin --delete serverfix

To https://github.com/schacon/simplegit
  - [deleted]         serverfix
```

基本上这个命令做的只是从服务器上移除这个指针。 Git 服务器通常会保留数据一段时间直到垃圾回收运行，所以如果不小心删除掉了，通常是很容易恢复的。

## Git 本地高级操作

### 分支操作

#### 创建、切换分支

创建并切换到新的分支dev

`$ git branch dev`

`$ git checkout dev`

等价于`$ git checkout -b dev`  

​       

复制远程分支到本地

`$ git checkout -b dev origin/dev`

dev是本地新建的分支名字，origin/dev是远程分支

 

查看所有分支，以及当前所在分支，*表示当前分支

`$ git branch`  

切换分支

`$ git checkout dev`

切换出去前，要保存好编辑过的文件，用`add commit`，或者保存现场

 

#### 保存现场

`$ git stash`

当在一个分支的开发工作未完成，却又要切换到另外一个分支进行开发的时候，并不是不想提交，而是工作只进行到一半，还没法提交，预计完成还需1天时间。除了commit原分支的代码改动的方法外，我觉得保存现场是一个更加便捷的选择，暂时冻结开发现场，等待其他分支完成后继续回来完成。

查看现场

`git stash list`

恢复现场

`git stash apply，`默认恢复最新的现场，但是恢复后，stash内容并不删除，你需要用`git stash drop`来删除

`git stash pop，`恢复的同时把stash内容也删了



可以多次stash，恢复的时候，先用`git stash list`查看，然后恢复指定的stash，用命令：`$ git stash apply stash@{0}`

删除合并后的分支

`$ git branch -d dev` 

 丢弃一个没有被合并过的分支

` $ git branch -D dev`强行删除。

### 分支详解

当使用` git commit` 进行提交操作时，Git 会先计算每一个子目录的校验和，然后在 Git 仓库中这些校验和被保存为树对象。随后，Git 便会创建一个提交对象（98ca9），它除了包含上面提到的那些信息外，还包含指向这个树对象（92ec2）的指针。如此一来，Git 就可以在需要的时候重现此次保存的快照。

现在，Git 仓库中有五个对象：一个提交对象（包含着指向前述树对象的指针和所有提交信息） 、一个树对象（记录着目录结构和 blob 对象索引）以及三个 blob 对象（保存着文件快照）。

![commit 操作解释](./commit操作解释.png)





## Git bash 快捷键（window）

### 全屏

`ATL+ENTER`

### 字体变化

`CTRL+PLUS/MINUS/ZERO`

### 右键

`ALT+SPACE`