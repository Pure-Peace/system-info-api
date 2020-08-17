# system-info-api
python的系统信息web api。包括restful和socketio，方便绘制可视化图表

Python system information web api. Including restful and socketio, convenient to draw visual charts


# 说明
此项目包含基于flask的restful api以及socketio，分为两种方式提供服务。

0. 系统信息：背景线程将会每间隔数秒更新系统信息（cpu、内存、硬盘、负载等），并在本地进行缓存，缓存形式包括json文件以及内存（变量）。
1. 主动推送：每当背景线程更新系统信息，socketio将会广播这些系统信息数据。
2. 被动获取：你可以通过访问web api来主动获取已经缓存的系统信息，这些缓存信息会随着背景线程的运行而更新。

## systemInfo.py
systemInfo.py模块中包含所有可用的系统信息函数（所有api可以在此处找到，包含一些说明）
项目地址：https://github.com/Pure-Peace/system-info

## main.py
包含背景线程以及flask、socketio。

# 运行

## 虚拟环境
当前提供windows x64下已安装依赖的虚拟环境（python3.8）：
https://github.com/Pure-Peace/system-info-api/blob/master/venv_windows.zip

![sc](https://github.com/Pure-Peace/system-info-api/blob/master/sc.png)

将其解压到项目目录下，运行`run.bat`即可

## 非虚拟环境

请手动安装python3解释器，并使用命令安装依赖
```
pip install -r requirements.txt
```


然后运行
```
python main.py
```

#### 运行后，访问地址
```
http://localhost:5678
```

即启动成功
```
{
"message": "hello",
"status": 1
}
```

## [初次]运行后等待5-8秒，项目目录下将会出现缓存的json文件

例如
```
cpuInfo.json
memInfo.json
ioInfo.json
networkInfo.json
loadInfo.json
```
这些文件的内容将会不断更新。

您可以通过下列地址访问这些系统信息的缓存：
```
http://localhost:5678/cpu_constants
http://localhost:5678/cpu_info
http://localhost:5678/io_info
http://localhost:5678/mem_info
http://localhost:5678/network_info
http://localhost:5678/load_info
```

## 测试socketio

打开python服务端后，用浏览器打开`socketio.html`

![demo](https://github.com/Pure-Peace/system-info-api/blob/master/demo.png)

在网页建立一个socketio对象，连接到服务端
socketio：https://socket.io/#examples

以下是socketio的更新事件（event）：
```
update_cpu
update_io
update_mem
update_net
update_load
```

# Pure-Peace

