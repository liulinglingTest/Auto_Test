# 高级变量
# 列表
"""
列表:List,专门用于存储一串信息，用[]定义，数据之间使用逗号分隔，列表的索引从0开始
增加：
列表.append(数据)  在列表的末尾追加数据
列表.insert(索引, 数据)  在列表的指定索引位置插入数据
列表.extend(列表1)  把其他列表的完整内容，追加到当前列表的末尾
修改：
列表[索引] = 数据  修改指定索引的数据
删除：
del 列表[索引]  使用del关键字，删除指定索引的数据
列表.remove(数据) 删除第一个出现的指定数据
列表.pop()  删除末尾数据
列表.pop(索引)  删除指定索引的数据
列表.clear  清空列表
排序：
列表.sort() 升序排序
列表.sort(reverse=True) 降序排序
列表.reverse()  反转/逆序
统计：
len(列表)  列表长度
列表.count(数据)  数据在列表中出现的次数
"""
# 元组
"""
元组：Tuple，用于存储一串信息，元组的元素不能修改，用()定义，数据之间用逗号隔开，元组的索引从0开始
通常保存不同类型的数据
统计：
len(元组)  元组长度
元组.count(数据)  数据在元组中出现的次数
"""
# 字典
"""
字典：是无序的对象集合，用{}定义，使用键值对存储数据，键值之间使用逗号分隔
键key是索引，值value是数据，键和值之间使用:分隔，键必须是唯一的，值可以取任何数据类型，但键只能使用字符串、数字或元组
字典.keys()  所有key列表
字典.values()  所有values列表
字典.items()  所有(key, values)元组列表
删除：字典.pop()
统计：len(字典)
合并字典：字典.update(字典1)
清空：字典.clear()
"""
# 字符串
"""
字符串：一串字符，可以使用一对双引号"或者一对单引号'定义一个字符串，字符串的索引值是从0开始的
统计：
len(字符串) 获取字符串的长度
字符串.count(字符串) 小字符串在大字符串中出现的次数
字符串[索引] 从字符串中取出单个字符
字符串.index(字符串) 获取字符串出现的位置
切片：适用于字符串、列表、元组，字典不支持切片
字符串[开始索引:结束索引:步长]

"""


def list_x():
    name_list = [1, 2, 3, 5, 3, 5, 0]
    # # 取值和索引
    print(name_list[0])  # 1
    #
    # # 知道数据的内容，想确定数据在列表中的位置
    # # 使用index方法要注意，如果传递的数据不在列表中，程序会报错
    # print(name_list.index(1))  # 0

    # 修改
    # name_list[1] = 4
    # print(name_list)  # [1, 4, 3, 5, 3, 5, 0]

    # 新增
    # name_list.append(-3)  # 在末尾追加数据
    # print(name_list)  # [1, 2, 3, 5, 3, 5, 0, -3]
    # name_list.insert(1, 66)  # 在列表的指定索引位置插入数据
    # print(name_list)  # [1, 66, 2, 3, 5, 3, 5, 0, -3]
    # name_list2 = [7, 2, 4]
    # name_list.extend(name_list2)  # extend方法把其他列表的完整内容，追加到当前列表的末尾
    # print(name_list)  # [1, 66, 2, 3, 5, 3, 5, 0, -3, 7, 2, 4]

    # 删除
    # del name_list[0]
    # print(name_list)  #
    # print(name_list.remove(3))
    # print(name_list.pop())
    # print(name_list.pop(4))

    # 排序
    # name_list.reverse()  # 反转
    # print(name_list)  # [0, 5, 3, 5, 3, 4, 1]
    # name_list.sort()  # 升序
    # print(name_list)  # [0, 1, 3, 3, 4, 5, 5]
    # name_list.sort(reverse=True)  # 降序
    # print(name_list)  # [5, 5, 4, 3, 3, 1, 0]

    # 迭代遍历
    # for name in name_list:
    #     print(name)


def tuple_y():
    # 创建空元组
    # empty_tuple = ()
    # empty1_tuple = tuple()
    # print(type(empty_tuple))  # tuple
    # print(type(empty1_tuple))  # tuple
    # # 这种不是单个元组的定义方式
    # single_tuple = (6)
    # print(type(single_tuple))  # int
    # single_tuple1 = (5,)
    # print(type(single_tuple1))  # tuple
    # 多个元素的定义方式
    info_tuple = ("ss", 12, 1.64, "ss")
    print(type(info_tuple))  # tuple
    # 取值和取索引
    # print(info_tuple[0])  # ss
    # # 已经知道数据的内容，想知道该数据在元组中的索引
    # print(info_tuple.index(12))  # 1
    # # 统计计数
    # print(info_tuple.count("ss"))  # 2
    # # 统计元组中包含元素的个数
    # print(len(info_tuple))  # 4
    # 使用迭代遍历元组
    # for my_info in info_tuple:
    #     # 使用格式字符串拼接my_info这个变量不方便！
    #     # 因为元组中通常保存的数据类型是不相同的
    #     print(my_info)
    # 格式化字符串后面的‘()’本质上就是元组
    # my_tuple = ("小明", 12, 1.64)
    # print("%s年龄是%d，身高是%0.2f" % my_tuple)  # 小明年龄是12，身高是1.64
    # info_str = "%s年龄是%d，身高是%0.2f" % my_tuple
    # print(info_str)  # # 小明年龄是12，身高是1.64
    # 元组和列表之间的转换
    # num_list = [1, 2, 3, 4]
    # print(type(num_list))  # list
    # num_tuple = tuple(num_list)
    # print(type(num_tuple))  # tuple
    # num2_list = list(num_tuple)
    # print(type(num2_list))  # list


def dict_z():
    # 创建空字典
    # nu_dict = {}
    # nm_dict = dict()
    # print(type(nu_dict))  # dict
    # print(type(nm_dict))  # dict
    # 字典是一个无序的数据集合，使用print函数输出字典时，通常输出的顺序和定义的顺序是不一致的！
    # dict_xiao = {"name": "小明",
    #              "age": 18,
    #              "gender": True,
    #              "height": 1.75}
    # print(dict_xiao)
    # 取值
    # print(dict_xiao["name"])  # 小明
    # 在取值的时候，如果指定的key不存在，程序会报错
    # print(dict_xiao["name123"])  #
    # 增加/修改
    # 如果key不存在，会新增键值对
    # dict_xiao["weight"] = 59.5
    # # 如果key存在，会修改已存在的键值对
    # dict_xiao["age"] = 20
    # print(dict_xiao)
    # 删除
    # dict_xiao.pop("gender")
    # print(dict_xiao)  # {'name': '小明', 'age': 18, 'height': 1.75}
    # # 再删除指定键值对的时候，如果指定的key不存在，程序会报错！
    # dict_xiao.pop("gender13")
    # 统计键值对数量
    # print(len(dict_xiao))  # 4
    # # 合并字典
    # temp_dict = {"gender": True,
    #              "age": 25}
    # # 注意：如果被合并的字典中包含已经存在的键值对，会覆盖原有的键值对
    # dict_xiao.update(temp_dict)
    # print(dict_xiao)  # {'name': '小明', 'age': 25, 'gender': True, 'height': 1.75}
    # 清空字典
    # dict_xiao.clear()
    # 循环遍历
    # dict_ao = {"name": "小明",
    #              "qq": "12344",
    #            "phone": "10086"}
    # # 变量k是每一次循环中，获取到的键值对的key
    # for k in dict_ao:
    #     print("%s - %s" % (k, dict_ao[k]))
    # 将多个字典放在一个列表中，再进行遍历
    # card_list = [
    #     {"name": "张三",
    #      "qq": "123456",
    #      "phone": "1100"},
    #     {"name": "李四",
    #      "qq": "43233",
    #      "phone": "10034"}
    # ]
    # for card_info in card_list:
    #     print(card_info)
    """for-else搜索字典列表"""
    # stubs = [{"name": "阿土"},
    #         {"name": "小美"},
    # ]
    # # 在学员列表中搜索指定的姓名
    # find_name = "张三"
    # for student in stubs:
    #     print(student)
    #     if student["name"] == find_name:
    #         print("找到了 %s" % find_name)
    #         # 如果已经找到，应该直接退出循环，而不再遍历后续的元素
    #         break
    #     # else:
    #     #     print("抱歉没有找到 %s" % find_name)
    # else:
    #     # 如果希望在搜索时，所有的字典检查之后，都没有发现需要搜索的目标，还希望得到一个统一的提示！
    #     print("抱歉，没有找到 %s" % find_name)
    # print("循环结束")


def str_f():
    # 创建一个空字符串
    str1 = str()
    print(type(str1))  # str
    # str2 = "Hello Python"
    # for c in str2:
    #     print(c)
    # str3 = 'xxx and"sss"'
    # print(str3)  # xxx and"sss"
    # # 取值
    # print(str3[4])  # a
    # 统计字符串长度
    # str4 = "hello hello"
    # print(len(str4))  # 11
    # # 统计某一个小字符串出现的次数
    # print(str4.count("llo"))  # 2
    # print(str4.count("abd"))  # 0
    # # 某一个子字符串出现的位置
    # print(str4.index("llo"))  # 2
    # # 注意：如果使用index方法传递的子字符串不存在，程序会报错！
    # print(str4.index("abd"))  # 2

    # 判断空白字符和空格，
    # space_str = " \t\n\r"
    # print(space_str.isspace())  # True
    # 判断字符串中是否只包含数字,都不能判断小数
    # num_str = "1"
    # unicode 字符串
    # num_str = "(1)"
    # 中文数字
    # num_str = "一千零一"
    # print(num_str.isdecimal())  # True 只能判断单纯的数字
    # print(num_str.isdigit())  # True  能判断unicode字符串
    # print(num_str.isnumeric())  # True 能判断中文数字

    # hello_str = "hello world"
    # 判断是否以指定字符串开始
    # print(hello_str.startswith("Hello"))  # False
    # # 判断是否以指定字符串结束
    # print(hello_str.endswith("world"))  # True
    # # 查找指定字符串
    # # index同样可以查找指定的字符串在大字符串中的索引
    # print(hello_str.find("llo"))  # 2
    # # index如果指定的字符串不存在，会报错
    # # find如果指定的字符串不存在，会返回-1
    # print(hello_str.find("abc"))  # -1
    # 替换字符串
    # replace方法执行完成之后，会返回一个新的字符串
    # 注意：不会修改原有字符串的内容
    # print(hello_str.replace("world", "python"))  # hello python
    # print(hello_str)  # hello world

    # 文本-对齐
    # poem = ["登鹳雀楼",
    #         "王之涣",
    #         "白日依山尽",
    #         "黄河入海流",
    #         "欲穷千里目",
    #         "更上一层楼"]
    # for pom_str in poem:
    #     # print("|%s|" % pom_str.center(10, "　"))  # 居中对齐
    #     # print("|%s|" % pom_str.ljust(10, "　"))  # 居左对齐
    #     print("|%s|" % pom_str.rjust(10, "　"))  # 居右对齐

    # 去除空白字符
    # poem = ["登鹳雀楼",
    #         "王之涣",
    #         "白日依山尽\t\n",
    #         "黄河入海流",
    #         "欲穷千里目",
    #         "更上一层楼"]
    # for pom_str in poem:
    #     # 先使用strip方法去除字符串中的空白字符
    #     # 再使用center方法居中显示文本
    #     print("|%s|" % pom_str.strip().center(10, "　"))

    # 拆分与合并
    # poem_str = "登鹳雀楼\t 王之涣 \t 白日依山尽 \t \n 黄河入海流 \t\t 欲穷千里目 \t\r 更上一层楼\n"
    # print(poem_str)
    # # 拆分字符串
    # poem_list = poem_str.split()
    # print(poem_list)

    # 切片
    #  num_str = '0123456789'
    # # 截取从2~5位置的字符串
    # # print(num_str[2:6])  # 2345
    # # 截取从2~末尾的字符串
    # print(num_str[2:])  # 23456789
    # # 截取从开始~5的字符串
    # print(num_str[0:6])  # 012345 print(num_str[:6])
    # # 截取完整的字符串
    # print(num_str[0:])  # 0123456789 print(num_str[:])
    # # 从开始位置，每隔一个字符截取字符串
    # print(num_str[::2])  # 02468
    # # 从索引1开始，每隔一个取一个
    # print(num_str[1::2])  # 02468
    # # 截取从2~末尾-1的字符串
    # print(num_str[2:-1])  # 2345678
    # # 截取字符串末尾两个字符
    # print(num_str[-2:])  # 89
    # # 字符串的逆序
    # print(num_str[-1::-1])  # 9876543210 print(num_str[::-1])


if __name__ == '__main__':
    # 列表
    # list_x()

    # 元组
    # tuple_y()

    # 字典
    # dict_z()

    # 字符串
    str_f()
