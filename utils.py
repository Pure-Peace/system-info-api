'''
@author: Pure-Peace
@name: 工具函数
@time: 2020年8月17日
@version: 0.1
'''
import datetime
import time

def log(text: str, *args) -> None:
    '''
    logger，打印日志用，与print用法一致，但会显示时间

    Parameters
    ----------
    text : str
        DESCRIPTION.
    *args : TYPE
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    '''
    print('[{}] {}'.format(getTime(1), text), *args)


def getTime(needFormat: int = 0, formatMS: bool = True) -> [int, str]:
    '''
    获取当前时间

    Parameters
    ----------
    needFormat : int, optional
        需要格式化为2020年8月17日 20:01:40这样的字符串？. The default is 0.
    formatMS : bool, optional
        需要精确到毫秒吗？. The default is True.

    Returns
    -------
    [int, str]
        DESCRIPTION.

    '''
    if needFormat != 0:
        return datetime.datetime.now().strftime(f'%Y-%m-%d %H:%M:%S{r".%f" if formatMS else ""}')
    return int(str(time.time()).split('.')[0])