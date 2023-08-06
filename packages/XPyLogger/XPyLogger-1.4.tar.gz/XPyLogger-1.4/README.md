# XLogger
> By 这里是小邓

## 介绍
XPyLogger 是提供了一个开箱即用的日志库，较好的解决了Python 自带 logging 库使用繁琐，函数玄学的问题，支持 rich 库彩色输出。
> 项目原名 XLogger，后因重名，故改名为 XPyLogger

## 依赖
1. Python (3.9+)
2. Rich

## 编译步骤
### GIT
1. 克隆 XPyLogger
2. 放入程序文件夹
3. 安装`rich`：
```bash
pip install rich
```
4. `from XPyLogger import *`
### PIP
```bash
pip install XPyLogger
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

### XPyLogger.init(file_enable = True,file_name = int(time.time()),dir_name = "logs")
自定义初始化log对象
- file_enable：是否启用文件记录
- file_name：日志文件名(不含.log)
- dir_name：日志文件夹名

## Demo
```python
import XPyLogger as log
log.init(file_enable = False)
log.log("This is a information!",log.INFO)
log.log("This is a warning!",log.WARN)
log.log("This is a error!",log.ERR)
close()
```

## Change Log
更高的自定义性（待测试）
