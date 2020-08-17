'''
@author: Pure-Peace
@name: 系统信息
@time: 2020年8月17日
@version: 0.1
'''

import systemInfo
from utils import log, getTime

from gevent import monkey; monkey.patch_all()

import threading
import time
import json

from flask_socketio import SocketIO
from flask import Flask, jsonify, request
from flask_cors import CORS

# fix: windows cmd cannot display colors
from colorama import init
init(autoreset=True)


# initial(s)
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'asdqwezxc'
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config["JSON_AS_ASCII"] = False

# 跨域
CORS(app)

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*', async_mode='gevent')

class Cache:
    def __init__(self, name: str, limit: int = 30):
        '''
        缓存

        Parameters
        ----------
        name : str
            缓存名称，关系到文件保存.
        limit : int, optional
            缓存上限，最高存储多少条信息. The default is 30.

        Returns
        -------
        None.

        '''
        self.name = name
        self.limit = limit
        self.read()

    def add(self, item):
        '''
        添加数据到缓存中

        Parameters
        ----------
        item : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        if len(self.data) >= self.limit: del(self.data[0])
        self.data.append(item)
        self.save()

    def save(self):
        '''
        将缓存持久化，存储到name对应的json文件中

        Returns
        -------
        None.

        '''
        try:
            with open(f'{self.name}.json', 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4)
        except:
            pass

    def read(self):
        '''
        读取缓存（如果有）

        Returns
        -------
        None.

        '''
        try:
            with open(f'{self.name}.json', 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except:
            self.data = []


# apis -------------------------------

@app.route('/')
def root():
    return jsonify({'status': 1, 'message': 'hello'})

@app.route('/cpu_constants')
def cpuConstants():
    return jsonify(cpuData)

@app.route('/cpu_info')
def cpuInfo():
    return jsonify(cpuCache.data)

@app.route('/io_info')
def ioInfo():
    return jsonify(ioCache.data)

@app.route('/mem_info')
def memInfo():
    return jsonify(memCache.data)

@app.route('/network_info')
def networkInfo():
    return jsonify(networkCache.data)

@app.route('/load_info')
def loadInfo():
    return jsonify(loadCache.data)

# socketio -------------------------------

@socketio.on('disconnect')
def sioDisconnect():
    log('socketio连接断开：', request.remote_addr)

@socketio.on('connect')
def sioConnect():
    log('socketio连接建立：', request.remote_addr)

# 背景线程 -------------------------------

def cpuBackground(interval: int = 8) -> None:
    '''
    更新cpu信息并更新缓存，同时向前端socketio推送信息

    Parameters
    ----------
    interval : int, optional
        间隔多少时间更新一次cpu信息. The default is 8.

    Returns
    -------
    None
        DESCRIPTION.

    '''
    def task():
        data: dict = systemInfo.GetCpuInfo(constants = False) # 获取cpu信息
        cpuCache.add(data) # 更新缓存
        socketio.emit('update_cpu', data, broadcast=True) # 推送信息，事件名为update_cpu
    loopRun(task, interval) # 循环执行，每隔interval秒执行一次

def ioBackground(interval: int = 5) -> None:
    def task():
        data: dict = systemInfo.GetIoReadWrite()
        ioCache.add(data)
        socketio.emit('update_io', data, broadcast=True)
    loopRun(task, interval)

def memBackground(interval: int = 5) -> None:
    def task():
        data: dict = systemInfo.GetMemInfo()
        memCache.add(data)
        socketio.emit('update_mem', data, broadcast=True)
    loopRun(task, interval)

def networkBackground(interval: int = 5) -> None:
    def task():
        data: dict = systemInfo.GetNetWork()
        networkCache.add(data)
        socketio.emit('update_net', data, broadcast=True)
    loopRun(task, interval)

def loadBackground(interval: int = 5) -> None:
    def task():
        data: dict = systemInfo.GetLoadAverage()
        loadCache.add(data)
        socketio.emit('update_load', data, broadcast=True)
    loopRun(task, interval)

def loopRun(func, interval: int, *arg, **kwargs) -> None:
    '''
    循环执行

    Parameters
    ----------
    func : TYPE
        要执行的函数.
    interval : int
        间隔时间.
    *arg : TYPE
        位置参数.
    **kwargs : TYPE
        关键字参数.

    Returns
    -------
    None
        DESCRIPTION.

    '''
    while True:
        try:
            time.sleep(interval)
            func(*arg, **kwargs)
        except Exception as err:
            log('循环线程执行异常：', err)

# 线程列表
ts: list = [
      threading.Thread(target=cpuBackground),
      threading.Thread(target=ioBackground),
      threading.Thread(target=memBackground),
      threading.Thread(target=networkBackground),
      threading.Thread(target=loadBackground)
]

# 获取cpu常量信息
cpuData = systemInfo.cpuConstants.getDict

# 建立缓存
cpuCache = Cache('cpuInfo')
ioCache = Cache('ioInfo')
memCache = Cache('memInfo')
networkCache = Cache('networkInfo')
loadCache = Cache('loadInfo')
    
if __name__ == '__main__':
    # 开启所有线程
    for t in ts: t.start()
    
    log('应用已启动')
    # 启动app（危险：0.0.0.0将使得外网可直接访问）
    socketio.run(app, host = '0.0.0.0', port = 5678)
