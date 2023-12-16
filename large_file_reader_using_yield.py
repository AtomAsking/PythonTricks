def my_readlines(f, newline):
    buf = ""  # 缓存，记录已经读取的数据量
    while True:
        # 第一次运行时while条件肯定是不成立的
        while newline in buf:  # 查询缓存中的数据是否包含了分隔符，如果“是”
            # 说明分隔符存在
            pos = buf.index(newline)  # 我们会把分隔符的位置找到
            yield buf[:pos]  # 从第0个位置开始到分隔符的位置截止，将字符串切片进行yield出来，所以就会在print中打印出来
            buf = buf[pos + len(newline) :]  # 将缓存更新，因为4096极有可能将2行数据都读到buf中，所以要将之前已经取出来的数据丢弃
        chunk = f.read(4096)  # 读取4096这么长的字符
        if not chunk:  # 判断chunk是否读到，即边界条件
            # 说明已经读到了文件结尾
            yield buf
            break
        buf += chunk  # 将读取到的数据加到缓存中


with open("input.txt") as f:
    for line in my_readlines(f, "{|}"):  # f是文件的句柄，第二个参数是文件的分隔符
        print(line)
