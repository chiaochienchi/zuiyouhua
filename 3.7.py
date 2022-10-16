# 前进后退找区间
# 三次插值极值点
import numpy as np
import math
def f(x):
    return x ** 4 - 4 * x ** 3 - 6 * x ** 2 - 16 * x + 4


def qianjin(a, h):
    a = a + h
    h = 2 * h
    if f(a) > f(a + h):
        qianjin(a, h)
    else:
        return [a, a + h]


def houtui(a, h):
    a = a + h
    h = h + h
    if f(a) > f(a + h):
        houtui(a, h)
    else:
        return [a + h, a]


def jintui(a, h):
    if f(a) >= f(a + h):
        qianjin(a, h)
    elif f(a) < f(a + h):
        h = -h/4
        houtui(a, h)
# 进退法确定了大概区间[a, b]

# 封装了中间一块从uv小于零开始回头的代码
def digui(a, h, v):
    b = a + h
    u = np.polyder(f(b))
    if abs(u) < epsilon:
        return b
    elif u * v >= 0:
        h = 2 * h
        v = u
        a = b
        digui(a, h, v)
    elif u * v < 0:
#         重复插值里的代码，没写完


# 照着p55的框图抄的，没想好封装的函数，在外面要写几个递归
def chazhi(a, h, epsilon):
    a = jintui(a, h)[0]
    b = jintui(a, h)[1]
    v = np.polyder(f(a))
    if v < 0:
        h = abs(h)
    else:
        h = -abs(h)
    if abs(v) < epsilon:
        return a
    else:
        b = a + h
        u = np.polyder(f(b))
        if abs(u) < epsilon:
            return b
        elif u * v < 0:
            s = 3 * (f(a) - f(b)) / (b - a)
            z = s - u - v
            w = math.sqrt(z ** 2 -u * v)
            a = a - (b - a) * v / (z - w * np.sign(v) - v)
            h = h/10
            chazhi(a, h, epsilon)
        else:
            digui(a, h, v)

