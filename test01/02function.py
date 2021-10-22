# 函数
"""
1.type(变量名):查看变量类型
2.input("提示信息："):实现键盘输入，输入的内容为一个字符串
3.int(x):将x装换成一个整数
4.float(x)：将x装换成一个浮点数
内置函数
len(item): 计算容器中元素个数
del(item): 删除变量
max(item): 返回容器中元素最大值，如果为字典，只针对key比较
min(item): 返回容器中元素最小值，如果为字典，只针对key比较
cmp(item1,item2): 比较两个值,在python 3.x取消了
"""
"""
定义函数的格式：
def 函数名():
    函数封装的代码
    .....
函数名称的命名规则：可以由字母、下划线和数字组成，不能以数字开头，不能与关键字重名
"""


def test(num):
    print("在函数内部 %d 对应的内存地址是 %d" % (num, id(num)))  # 2446774987344
    # 定义一个字符串变量
    result = "hello"
    print("函数要返回数据的内存地址是 %d" % id(result))  # 2072200622000
    # 将字符串变量返回，返回的是数据的引用，而不是数据本身
    return result


if __name__ == '__main__':
    """type函数"""
    # d = 1
    # print(type(d))  # int
    # c = 1.23
    # print(type(c))  # float
    """input函数"""
    # it = input('xx:')
    # print(it)
    """int和float函数"""
    # print(type(int(1.23)))  # int
    # print(type(float(11)))  # float
    """del"""
    # a = [1, 2, 3]
    # del a[1]
    # print(a)  # [1, 3]
    """max和min"""
    # t_str = "saddlebags"
    # print(max(t_str))  # s
    # print(min(t_str))  # a
    # t_list = [1, 3, 9, 0]
    # print(max(t_list))  # 9
    # print(min(t_list))  # 0
    # t_dict = {"a": "z", "b": "y", "c": "x"}
    # print(max(t_dict))  # c
    # print(min(t_dict))  # a

    a = 10
    # 数据的地址本质上就是一个数字
    print("a 变量保存数据的内存地址是 %d" % id(a))  # 2446774987344
    # 调用test函数，本质上传递的是实参保存数据的引用，而不是实参保存的数据
    # test(a)
    # 注意：如果函数有返回值，但是没有定义变量接受，程序不会报错，但是无法获得返回数据
    r = test(a)
    print("%s 变量保存数据的内存地址是 %d" % (r, id(r)))  # 2072200622000
