print('hello world')


'''
迭代器、生成器 2019-03-22
'''
class IteTest:

    # num = 0

    def __init__(self,num):
        self.num = num

    def __iter__(self):
        return self    #注意这里返回的是self实例对象
    
    def __next__(self):
        while self.num > 0:
            self.num -= 1
            return self.num
        else:
            raise StopIteration

def  gen(num):
    while num > 0:
        yield num   #注意这里返回的是具体的值
        num -= 1
    # else:
    #     raise StopIteration
genFun =  gen(10)  # genFun 是一个生成器返回的可迭代的对象  <class 'generator'>
while True:
    try:
        print(next(genFun), end=" ")   #这里执行了next()方法
    except StopIteration:
        break

it =  IteTest(10)
for x in it: print(x, end=",")
print('')

# 全局变量  局部变量 以及 相应关键字使用
num = 100
def outer():
    num = 10   #global 可以设置在这里
    def inner():
        nonlocal num   #global 不可以设置在这里， nonlocal可以在闭包函数内的函数数，用于方法闭包函数内的局部变量
        num = 200
        print(num)
    inner()
    print(num)
outer()
print(num)

