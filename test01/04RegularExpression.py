#正则表达式
"""
re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；
而re.search匹配整个字符串，直到找到一个匹配。
re.sub用于替换字符串中的匹配项.
re.compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用
findall在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。
注意： match 和 search 是匹配一次 findall 匹配所有。

re.finditer和 findall 类似，在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回。
re.split方法按照能够匹配的子串将字符串分割后返回列表

[0-9] 匹配任何数字
[a-z] 匹配任何小写字母
[A-Z] 匹配任何大写字母
[a-zA-Z0-9] 匹配任何字母及数字
[^0-9] 匹配除了数字外的字符

\d 匹配一个数字字符
\D 匹配一个非数字字符
\s 匹配任何空白字符
\S 匹配任何非空白字符
\w 匹配包括下划线的任何单词字符
\W 匹配任何非单词字符
"""
import re

# 将匹配的数字乘以 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)
if __name__ == '__main__':
    # print(re.match('www', 'www.rund.com').span())  # 在起始位置匹配
    # print(re.match('com', 'www.run.com'))  # 不在起始位置匹配
    # line = "Cats are smarter than dogs"
    # matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
    # if matchObj:
    #     print("matchObj.group() : ", matchObj.group())
    #     print("matchObj.group(1) : ", matchObj.group(1))
    #     print("matchObj.group(2) : ", matchObj.group(2))
    # else:
    #     print("No match!!")

    # print(re.search('www', 'www.runoob.com').span())  # 在起始位置匹配 （0,3）
    # print(re.search('com', 'www.runoob.com').span())  # 不在起始位置匹配 （11,14）

    s = 'A23G4HFD567'
    print(re.sub('(?P<value>\d+)', double, s))  # A46G8HFD1134
