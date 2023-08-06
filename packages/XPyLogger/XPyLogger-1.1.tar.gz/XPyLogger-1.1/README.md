# XPyLogger
> By 这里是小邓

## 介绍
XPyLog 是提供了一个开箱即用的日志库，较好的解决了Python 自带 logging 库使用繁琐，函数玄学的问题，支持 rich 库彩色输出。

## 依赖
1. Python (3.9+)
2. Rich

## 编译步骤
### GIT
1. 克隆 XLOGGER
2. 放入程序文件夹
3. 安装`rich`：
```bash
pip install rich
```
4. `from XPyLogger import *`
### PIP(推荐)
```bash
pip install XPyLogger
```

## Demo
```python
import XPyLogger as log
log.log("Hello world!")
log.close()
```

## 函数介绍
### XPyLogger.log(msg, level = INFO, sender = SENDER_MAIN)
输出一条日志
- msg：log信息
- level：日志等级
- sender：发送者

### XPyLogger.close()
关闭日志本地记录文件

### XPyLogger.INFO
日志等级-信息

### XPyLogger.WARN
日至等级-警告

### XPyLogger.ERR
日志等级-错误

