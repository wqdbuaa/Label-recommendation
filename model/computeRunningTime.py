#coding=utf-8

from functools import wraps
import time
import os

"""
计时函数
"""

def fun_timer(funtion):
    @wraps(funtion)
    def function_timer(*args,**kwargs):
        t0 = time.time()
        result = function(*args,**kwargs)
        t1 = time.time()
        return str(t1-t0)
    return function_timer()




