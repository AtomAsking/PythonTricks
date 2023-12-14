# socket_select_http.py
"""
通过I/O多路复用模型中的select模式或者epoll模式实现http请求
"""

import socket

# selectors包的作用是根据不同的操作系统自动选择最佳的I/O多路复用模型
# 我们不要使用select包，而是要使用基于select包再次封装的selectors包
# DefaultSelector会自动帮我们根据代码运行的操作系统去选择使用poll或者epoll
# 在Windows下就是select，在Linux下就是epoll
# 而且DefaultSelector还为我们提供了注册机制
from selectors import EVENT_READ, EVENT_WRITE, DefaultSelector
from urllib.parse import urlparse

selector = DefaultSelector()  # 创建一个selector对象(选择器)


class Fetcher:
    def __init__(self):
        self.host = ""  # 域名
        self.path = ""  # 路径
        self.data = b""  # 存储返回的数据
        self.client = None  # socket对象

    def get_url(self, url):
        """
        通过socket请求html
        """
        url = urlparse(url)  # 解析url
        self.host = url.netloc  # 获取域名
        self.path = url.path  # 获取域名后的子路径
        self.data = b""  # 存储返回的数据
        if self.path == "":
            self.path = "/"  # 如果直接请求的域名则把子路径改成/

        # 创建socket对象<class 'socket.socket'>, socket.AF_INET表示ipv4, socket.SOCK_STREAM表示TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将socket设置为阻塞(true)或非阻塞(false), 默认为阻塞
        self.client.setblocking(False)  # 使用非阻塞
        try:
            # 连接
            self.client.connect((self.host, 80))  # 注意这里是非阻塞的,所以不会等待连接成功,而是会立刻返回并继续执行后续代码,所以会抛出BlockingIOError异常
        except BlockingIOError as e:
            pass  # 抛出BlockingIOError异常是合理的，虽然抛出了异常，但是与host的建立连接请求已经发出去了。

        # 将socket注册到selector中，监听socket是否是可写的状态
        # 参数1: socket的文件描述符
        # 参数2: 事件，有EVENT_WRITE和EVENT_READ
        # 参数3: 回调函数，即当socket的状态变为可写的时候，就会调用此回调函数
        selector.register(self.client.fileno(), EVENT_WRITE, self.connected)  # 使用事件监听, 等待连接成功, 然后再执行后面的代码
        # 注意这后面不能再写代码了，如果写了代码就是阻塞式IO了，所以我们才要使用事件监听，采用回调的方式来处理

    def connected(self, key):
        """连接成功的回调函数，当socket的状态变为可写的时候，就会调用此回调函数，进行发送数据(发送HTTP请求)"""
        # 注销掉监控的事件,即取消注册,因为我们已经连接成功了,所以就不需要再监听socket是否是可写的状态了，所以要注销掉，否则会一直监听下去
        selector.unregister(key.fd) # fd是file descriptor文件描述符
        # 发送数据，这里不用try...except...，是因为我们使用事件监听，当回调此方法的时候连接的状态一定是就绪的状态
        self.client.send(f"GET {self.path} HTTP/1.1\r\nHost:{self.host}\r\nConnection:close\r\n\r\n".encode("utf8"))
        # 注册,即使用事件监听,因为我们要接收服务器返回的响应数据，所以要再次监听socket是否是可读的状态,当socket的状态变为可读的时候，就会调用此回调readable方法接收数据，然后打印出来
        selector.register(self.client.fileno(), EVENT_READ, self.readable)

    def readable(self, key):
        """接收数据(接收HTTP响应)，当socket的状态变为可读的时候，就会调用此回调函数，进行接收数据(接收HTTP响应)，然后打印出来"""
        d = self.client.recv(1024)  # 接收数据
        if d:  # 当数据没有读完的时候，继续读取
            self.data += d
        else:  # 当数据读完的时候，就注销掉监控的事件，即取消注册，因为我们已经接收完了，所以就不需要再监听socket是否是可读的状态了，所以要注销掉，否则会一直监听下去
            selector.unregister(key.fd)
            data = self.data.decode("utf8")
            html_data = data.split("\r\n\r\n")[1]
            print(html_data)
            self.client.close()


def loop():
    """回调+事件循环+select(poll/epoll)
    驱动整个程序运行，可以理解为心脏，这样不会去阻塞建立连接、等待请求等IO操作
    """
    # 事件循环，不停的请求socket的状态并调用对应的回调函数
    # 所以这是个主循环
    # 1.select本身是不支持register模式
    # 2.socket状态变化以后的回调是由程序员完成的
    while True:
        # 注意在Windows下使用的是select模式，而select(r,w,w,timeout)的参数如果为空列表会抛出OSError异常
        # 而在Linux或者macOS下会使用epoll模式，就不会抛出OSError异常，会一直阻塞在这里
        # 不停的向操作系统请求有哪些socket已经准备好了
        ready = selector.select()  # 返回的是SelectorKey数据类型，是namedtuple类型
        for key, mask in ready:
            # key是一个SelectorKey类型的对象，包含了文件描述符fd、事件event、回调函数data等属性
            # mask是一个事件的遮罩，表示事件是可读的还是可写的,EVENT_READ或EVENT_WRITE,取决于我们注册的时候监听的是可读还是可写,即key.events
            call_back = key.data  # 获取回调函数,<bound method Fetcher.connected of <__main__.Fetcher object at 0x1025d55b0>>
            call_back(key)  # 执行回调函数,即调用connected方法


if __name__ == "__main__":
    fetcher = Fetcher()
    fetcher.get_url("http://www.baidu.com")
    loop()

