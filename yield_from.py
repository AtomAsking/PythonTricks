"""使用 yield from 将统计结果变成如下形式，主要用于体验main调用方直接越过middle委托生成器与sales_sum子生成器之间建立连接
{'面膜': (5700, [1200, 1500, 3000]), '手机': (289, [28, 55, 98, 108]), '大衣': (1688, [280, 560, 778, 70])}
"""
final_result = {}


def sales_sum(pro_name):
    """子生成器
    将传入的每一个品类的数据进行统计并return
    pro_name: 商品名称
    """
    total = 0
    nums = []
    while True: # 不停的从外界接收值
        x = yield
        print(pro_name + "销量: ", x)
        if not x: # 如果外界传递进来的是None, 则break
            break
        total += x
        nums.append(x)
    return total, nums # 将值返回到29行


def middle(key):
    """委托生成器
    将统计后的结果放到final_result里
    """
    while True:
        final_result[key] = yield from sales_sum(key)
        print(key + "销量统计完成!!")


def main():
    """调用方
    """
    # 代表品类和对应的销量
    data_sets = {
        "面膜": [1200, 1500, 3000],
        "手机": [28, 55, 98, 108],
        "大衣": [280, 560, 778, 70],
    }
    for key, data_set in data_sets.items():
        print("start key:", key)
        m = middle(key)
        # 预激middle协程, 也可以直接调用next()
        m.send(None)  # 预激后会卡在yield from sales_sum(key), 建立了双向通道
        for value in data_set:
            m.send(value)  # 给协程传递每一组的值, 是直接send到子生成器里面, 即发送到15行代码中
        m.send(None) # 让子生成器结束
    print("final_result:", final_result)


if __name__ == "__main__":
    main()
# start key: 面膜
# 面膜销量:  1200
# 面膜销量:  1500
# 面膜销量:  3000
# 面膜销量:  None
# 面膜销量统计完成!!
# start key: 手机
# 手机销量:  28
# 手机销量:  55
# 手机销量:  98
# 手机销量:  108
# 手机销量:  None
# 手机销量统计完成!!
# start key: 大衣
# 大衣销量:  280
# 大衣销量:  560
# 大衣销量:  778
# 大衣销量:  70
# 大衣销量:  None
# 大衣销量统计完成!!
# final_result: {'面膜': (5700, [1200, 1500, 3000]), '手机': (289, [28, 55, 98, 108]), '大衣': (1688, [280, 560, 778, 70])}
