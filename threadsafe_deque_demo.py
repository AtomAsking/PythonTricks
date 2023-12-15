"""证明deque是线程安全的例子"""
import collections
import threading
import time

candle = collections.deque(range(5))
print(candle)  # deque([0, 1, 2, 3, 4])


def burn(direction, next_source):
    while True:
        try:
            next = next_source()
        except IndexError:
            break
        else:
            print(f"{direction}: {next}")
            time.sleep(0.1)  # 防止其他线程饥饿
    print(f"{direction} done")


left = threading.Thread(target=burn, args=("Left", candle.popleft))
right = threading.Thread(target=burn, args=("Right", candle.pop))
left.start()
right.start()
left.join()
right.join()
# 注意：打印的结果不固定
# Left: 0
# Right: 4
# Right: 3
# Left: 1
# Right: 2
# Left done
# Right done

