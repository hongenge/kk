## KK

用python开发的快捷输入开源小工具。

用途：不经常用到的命令，和一些不容易记住的长命令，和一些代码片段，和长文本内容，都可以自定义短语来进行快速输入。

#### 运行：

```
pythonw ok.py
```

备注：如果用`python ok.py`会弹出`cmd`窗口。建议用`pythonw ok.py`运行



#### 使用：

按两`Ctrl+Alt`键，会弹出快捷输入框，输入自定义的短语。选择需要的短语就会自动复制到剪贴板上面。

![](https://gitee.com/zzwhe/kk/raw/master/log.png)

#### 命令操作：

```
#命令帮助
python edit.py -h

#查看所有命令列表
python edit.py --list

#添加命令
python edit.py --add
备注：title快捷短语，lable显示的标签，note:代码片段

#编辑
python edit.py --edit 1
备注：1为ID，可以通过list查看列表ID

#删除
python edit.py --delete 1
```

备注：

`data.db`为数据库文件，默认添加了我用到的一些常用命令和代码片段。如果不需要可以删除`data.db`用`python edit.py --create_ok`命令创建新的空数据库。

python开发环境:python3.7

用到的python库

```
PyQt5,keyboard,sqlite3,argparse
```

