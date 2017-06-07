from config import DEBUG
from functools import wraps
import psutil
import socket
import numpy as np
from typing import *
import threading


def print_hex(b):
    print(":".join("{:02X}".format(bt) for bt in b))


def printResult(func):
    if DEBUG is not None and DEBUG:

        @wraps(func)
        def callf(*args, **kwargs):
            result = func(*args, **kwargs)
            print(func.__name__ + ": ", end='')
            print_hex(result)
            return result

        return callf

    else:
        return func


def get_net_interfaces():
    net_interfaces = []
    info = psutil.net_if_addrs()

    for k, v in info.items():
        name = k
        address = None
        netmask = None
        for i in v:
            if i.family == socket.AF_INET:
                address = i.address
                netmask = i.netmask

        if address is not None and netmask is not None:
            net_interfaces.append((name, address, netmask))

    return net_interfaces


def get_ppp_interfaces():
    net_interfaces = []
    info = psutil.net_if_addrs()

    for k, v in info.items():
        name = k  # type: str
        ptp = None
        if not name.startswith('ppp'):
            continue
        ptp = v[0].ptp

        net_interfaces.append((name, ptp))

    return net_interfaces


class RingBuffer():
    "A 1D ring buffer using numpy arrays"

    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) % self.data.size
        return self.data[idx]


class RepeatTimer(threading.Thread):
    def __init__(self, callback: Callable, interval: float, args: List = (), kwargs: Dict = {}):
        super().__init__()
        self._callback = callback
        self._interval = interval
        self._args = args
        self._kwargs = kwargs
        self._timer = None  # type: threading.Timer
        self.stop_event = threading.Event()
        self.stop_event.set()

    def run(self):
        while self.stop_event.is_set():
            timer = threading.Timer(self._interval, self._callback, args=self._args, kwargs=self._kwargs)
            timer.start()
            timer.join()

    def stop(self):
        self.stop_event.clear()


if __name__ == "__main__":
    a = get_ppp_interfaces()
    for i in a:
        print(i)
