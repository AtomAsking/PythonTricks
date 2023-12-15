# 使用Condition实现：天猫精灵说完一句话后通知小爱说，小爱说完通知天猫精灵说，...
import threading


class XiaoAi(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="小爱")
        self.cond = cond

    def run(self):
        with self.cond:  # 相当于self.cond.acquire()，这里会使用Condition的底层锁进行加锁
            self.cond.wait()
            print(f"{self.name}: 在")
            self.cond.notify()

            self.cond.wait()
            print(f"{self.name}: 好啊")
            self.cond.notify()

            self.cond.wait()
            print(f"{self.name}: 君住长江尾")
            self.cond.notify()

            self.cond.wait()
            print(f"{self.name}: 共饮长江水")
            self.cond.notify()


class TianMao(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        with self.cond:  # 相当于self.cond.acquire()，这里会使用Condition的底层锁进行加锁
            print(f"{self.name}: 小爱同学")
            self.cond.notify()
            self.cond.wait()  # wait方法会把Condition的底层锁进行释放，否则10行代码就进不来；与此同时会分配另外一把锁放到Condition的self._waiters双向队列中，等待notify方法的唤醒

            print(f"{self.name}: 我们来对古诗吧")
            self.cond.notify()
            self.cond.wait()

            print(f"{self.name}: 我住长江头")
            self.cond.notify()
            self.cond.wait()

            print(f"{self.name}: 日日思君不见君")
            self.cond.notify()
            self.cond.wait()
        # 相当于self.cond.release()


if __name__ == "__main__":
    cond = threading.Condition()

    xiaoai = XiaoAi(cond)
    tianmao = TianMao(cond)

    xiaoai.start()
    tianmao.start()  # 注意如果tianmao先于xiaoai进行start()，整个过程就会卡住，因为36行的wait方法只有notify方法才能唤醒，而xiaoai是在tianmao的wait方法之后才启动的，而xiaoai也是在wait，没有人唤醒xiaoai，xiaoai也就不会notify去唤醒tianmao，所以启动顺序很重要
