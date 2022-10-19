# 前进后退找区间
# 三次插值极值点
import numpy as np
import math
import torch
import numpy

def qianjin(a1, h, f1, f2):
    a2 = a1 + h
    h = 2 * h
    f1, f2 = f2, f(a2)
    if f2 < f1:
        a1 = a2 -h
        qianjin(a1, h, f1, f2)
    else:
        return [a1, a2]


def houtui(a1, a2, h, f1):
    a1 = a1 + h
    f2 = f1
    f1 = f(a1)
    if f2 < f1:
        return [a1, a2]
    else:
        a2 = a1 -h
        h = h + h
        houtui(a1, a2, h, f1)


def jintui(a, h):
    a1, a2 = a, a + h
    f1, f2 = f(a1), f(a2)

    if f2 < f1:
        return qianjin(a1, h, f1, f2)
    else:
        h = -h/4
        return houtui(a1, a2, h, f1)
# 进退法确定了大概区间[a, b]


# 封装了中间一块从uv小于零开始回头的代码
def digui(a, h, v, epsilon):
    b = a + h
    # f(b).backward()
    u = f_grad(b)
    if abs(u) < epsilon:
        return b
    elif not u * v < 0:
        h = 2 * h
        v = u
        a = b
        digui(a, h, v, epsilon)
    elif u * v < 0:
        print(a, b, u, h, v)
        a=a.detach().numpy()
        print(a, b)
        return a
#         重复插值里的代码，没写完


def digui1(a, b, h, epsilon):
    # f(a).backward()
    # f(b).backward()
    v = f_grad(a)
    u = f_grad(b)
    if not abs(v) < epsilon:
        h = h/10
        if v < 0:
            h = abs(h)
        else:
            h = -abs(h)
        a=(digui(a, h, v, epsilon))
        print(a)
        s = 3 * (f(a) - f(b)) / (b - a)
        z = s - u - v
        w = math.sqrt(z ** 2 - u * v)
        a = a - (b - a) * v / (z - w * np.sign(v) - v)
        digui1(a, b, h, epsilon)
    else:
        return a


# 照着p55的框图抄的，没想好封装的函数，在外面要写几个递归
def chazhi(a, h, epsilon):
    fanwei = jintui(a, h)
    b = torch.tensor(fanwei[1], requires_grad=True)
    a = torch.tensor(fanwei[0], requires_grad=True)
    return digui1(a, b, h, epsilon)


def f(x):
    return x ** 4 - 4 * x ** 3 - 6 * x ** 2 - 16 * x + 4


def f_grad(x):
    return 4 * x ** 3 - 12 * x ** 2 - 12 * x - 16


if __name__ == '__main__':
    a = 0.0
    h = 1.0
    epsilon = 0.5
    print(chazhi(a, h, epsilon))
