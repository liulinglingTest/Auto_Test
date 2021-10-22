# 注释的作用：增强代码的可读性
"""
单行注释：#
多行注释：一对连续的三个引号' """""" '
"""
# 算数运算符
"""
+ 加、- 减、* 乘、/ 除、// 取整除、% 取余数、** 幂(次方、乘方)
"""
# 变量的类型
"""
数字型：
整型(int)
浮点型(float)
布尔型(bool)：真(true：非0数)、假(false：0)

非数字型：
字符串
列表
元组
字典
"""
# 变量间的计算
"""
1.数字型变量可以直接计算
2.拼接字符串的两种方式：直接使用'+'，字符串变量可以和整数使用*重复拼接相同的字符串
3.数字型变量和字符串之间不能进行其他计算
"""
# 变量的格式化输出
"""
1.%s：字符串
2.%d：有符号十进制整数
3.%f：浮点数，%.02f表示小数点后只显示两位
4.%%：输出%
"""
# 变量的命名和规则
"""
1.标识符：由字母、下划线和数字组成，不能以数字开头，不能与关键字重名
2.关键字：具有特殊的功能和含义
3.规则：
1).python中的标识符是区分大小写的
2).在定义变量时，为了保证代码格式，=的左右应该各留一个空格
3).变量名需要由两个或多个单词组成时，可以按照以下方式命名
每个单词都是用小写字母，单词与单词之间使用_下划线连接，例如，first_name、last_name
4).驼峰命名法：firstName(小驼峰命名法)、FirstName(大驼峰命名法)
"""
# 判断if语句,else处理条件不满足的情况，elif
"""
格式：
if 条件1:
    条件1成立时，要执行的程序
elif 条件2:
    条件2成立时，要执行的程序
else:
    条件不成立时，要执行的程序
"""
# 运算符
"""
1.比较(关系)运算符：==、!=、>、<、>=、<=
2.逻辑运算符：与and、或or、非not
3.运算符的优先级
"""
# 随机数
"""
import random
"""
# 完整的for循环语法
"""
for 变量 in 集合:
    循环体代码
else:
    没有通过break退出循环，循环结束后，会执行的代码
"""
# import keyword
"""from pip._vendor.distlib.compat import raw_input"""
if __name__ == '__main__':
    """变量间的计算"""
    # s1 = "123"
    # s2 = "234"
    # print(s1+s2)  # 123234
    # s3 = "-"
    # print(s3 * 10)  # ----------
    """变量的格式化输出"""
    # name = "小明"
    # print("我的名字叫%s，请多多关照！" % name)  # 我的名字叫小明，请多多关照！
    #
    # stu_no = 1
    # print("我的学号是%06d" % stu_no)  # 我的学号是000001
    #
    # price = 9.00
    # weight = 5.00
    # money = 45.00
    # print("苹果单价%.02f/斤，购买了%.02f斤，需要支付%.02f元" %(price, weight, money))
    # #  苹果单价9.00/斤，购买了5.00斤，需要支付45.00元
    #
    # scale = 0.1
    # print("数据比例是%0.2f%%" %(scale*100))  # 数据比例是10.00%
    """查看关键字"""
    # print(keyword.kwlist)
    """if-else语句"""
    # age = 12
    # if age >= 18:
    #     print("允许进入网吧玩游戏！")
    # else:
    #     print("未满18岁不能进入网吧！")
    """逻辑运算符"""
    # age = 121
    # if age >= 0 and age <= 120:  # 0<= age <=120
    #     print("年龄正确")
    # else:
    #     print("年龄不正确")

    # py_score = 50
    # c_score = 60
    # if py_score > 60 or c_score > 60:
    #     print("成绩合格")
    # else:
    #     print("成绩不合格")

    # is_em = True
    # if not is_em:
    #     print("不得入内")
    # else:
    #     print("可以进入")
    """for循环语法"""
    # for num in [1, 2, 3]:
    #     print(num)
    #     if num == 2:
    #         break
    # else:
    #     # 如果循环体内部使用break退出了循环
    #     # else 下方的代码就不会执行
    #     print("会执行吗？")
    # print("循环结束")
    # rows = int(raw_input('输入列数： '))
    rows = 4
    i = j = k = 1  # 声明变量，i用于控制外层循环（图形行数），j用于控制空格的个数，k用于控制*的个数
    # # 等腰直角三角形1
    # print("1.等腰直角三角形")
    # for i in range(0, rows):
    #     for k in range(0, rows - i):
    #         print("*", end=" ")  # 注意这里的","，一定不能省略，可以起到不换行的作用
    #         k += 1
    #     i += 1
    #     print("")

    # 打印实心等边三角形
    # print("2.空心等边三角形，这里去掉if-else条件判断就是实心的")
    # for i in range(0, rows + 1):  # 变量i控制行数
    #     for j in range(0, rows - i):  # (1,rows-i)
    #         print(" ", end=" ")
    #         j += 1
    #     for k in range(0, 2 * i - 1):  # (1,2*i)
    #         if k == 0 or k == 2 * i - 2 or i == rows:
    #             if i == rows:
    #                 if k % 2 == 0:  # 因为第一个数是从0开始的，所以要是偶数打印*，奇数打印空格
    #                     print("*", end=" ")
    #                 else:
    #                     print(" ", end=" ")  # 注意这里的","，一定不能省略，可以起到不换行的作用
    #             else:
    #                 print("*", end=" ")
    #         else:
    #             print(" ", end=" ")
    #         k += 1
    #     print("")
    #     i += 1
    #
    # # 打印菱形
    # print("3.空心等菱形，这里去掉if-else条件判断就是实心的")
    # for i in range(rows):  # 变量i控制行数
    #     for j in range(rows - i):  # (1,rows-i)
    #         print(" ", end=" ")
    #         j += 1
    #     for k in range(2 * i - 1):  # (1,2*i)
    #         if k == 0 or k == 2 * i - 2:
    #             print("*", end=" ")
    #         else:
    #             print(" ", end=" ")
    #         k += 1
    #     print("")
    #     i += 1
    #     # 菱形的下半部分
    # for i in range(rows):
    #     for j in range(i):  # (1,rows-i)
    #         print(" ", end=" ")
    #         j += 1
    #     for k in range(2 * (rows - i) - 1):  # (1,2*i)
    #         if k == 0 or k == 2 * (rows - i) - 2:
    #             print("*", end=" ")
    #         else:
    #             print(" ", end=" ")
    #         k += 1
    #     print("")
    #     i += 1
    # # 实心正方形
    # print("4.实心正方形")
    # for i in range(0, rows):
    #     for k in range(0, rows):
    #         print(" * ", end=" ")  # 注意这里的","，一定不能省略，可以起到不换行的作用
    #         k += 1
    #     i += 1
    #     print("")
    #
    # # 空心正方形
    # print("5.空心正方形")
    # for i in range(0, rows):
    #     for k in range(0, rows):
    #         if i != 0 and i != rows - 1:
    #             if k == 0 or k == rows - 1:
    #                 # 由于视觉效果看起来更像正方形，所以这里*两侧加了空格，增大距离
    #                 print(" * ", end=" ")  # 注意这里的","，一定不能省略，可以起到不换行的作用
    #             else:
    #                 print("   ", end=" ")  # 该处有三个空格
    #         else:
    #             print(" * ", end=" ")  # 这里*两侧加了空格
    #         k += 1
    #     i += 1
    #     print("")
