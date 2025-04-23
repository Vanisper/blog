需求是把原有仓库的 git-commit-msg 中 emoji 标识的位置统一迁移至 msg 的开头。

以 `<type>(?<scope>): <?emoji> <subject> <?ticket>` 为例

这样做的原因是，emoji 标识在中间的时候，由于各 commit 的 `<type>(?<scope>)` 部分的长短可能不一，导致在 git-web 中看到的 commit 记录由于 emoji 的存在会显得乱乱的。

如果统一移到最开始，在视图上 emoji 处于一条线上，会好看很多。

> BTW，这是一个无聊的需求，但是点滴的积累可能就是从这些无聊的需求中获得的。

说一下可选方案，一个是 git 工具官方的命令 `git filter-branch` - <https://git-scm.com/docs/git-filter-branch/zh_HANS-CN> 。

这个方案官方都不太推荐，所以就没做更多的了解了。在 AI 的帮助下，计划使用 `git-filter-repo` - <https://github.com/newren/git-filter-repo> 。

---

>
> 重写提交信息相关的参考文章：
> - https://www.burtonini.com/blog/2018/03/06/rewriting-git-commit-messages/
>
> python 对 emoji 的正则匹配相关参考：
> - https://www.kaggle.com/code/eliasdabbas/how-to-create-a-python-regex-to-extract-emoji/notebook
> - https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1
> - https://gist.github.com/Saluev/604c9c3a3d6032770e15a0da143f73bd
>
> 一些关于字符编码的工具站：
> - https://www.compart.com/en/unicode/U+1F300
> - https://www.codetable.net/
>

### **1. 安装 git-filter-repo：**
``` bash
pip install git-filter-repo
```

### **2. 运行 filter-repo：**
``` bash
git filter-repo --commit-callback 'rw-commit-msg.py' --force
```
>
> `rw-commit-msg.py` 代码内容可以看[这里](./rw-commit-msg.py)。
>
> 其中关于 emoji 的正则匹配可以看[这个笔记](../正则匹配commit-msg)。
>
> 需要注意的是，上面的笔记是 JavaScript 的实现，正则中的一些 Unicode 的写法在 python 中是不生效的，见[此处](./rw-commit-msg.py#L17-L19)。
>

### **3. 强制推送：**
```bash
# git filter-repo 在执行的时候会删除当前本地仓库的 origin 绑定，此处需要重新绑定上
git remote add origin <远程仓库URL>
git push origin --force --all
git push origin --force --tags
```

### **4. 在另外一侧以前拉取过的本地仓库：**
要么删了重新 git clone，要么如下操作：
``` bash
# 获取远程仓库的最新数据
git fetch origin

# 强制将本地的 main 分支重置为远程的 main 分支，丢弃本地的更改
git reset --hard origin/main
```