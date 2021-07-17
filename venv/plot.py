def plot(n, t, loglog=False, interpolation=lambda x: x ** 2):
    from matplotlib import pyplot as plt
    from math import log2

    quadratic = list(map(lambda x: x**2, n))
    cq = quadratic[0]
    quadratic = list(map(lambda x: x/cq, quadratic))
    linear = list(map(lambda x: x, n))
    cl = linear[0]
    linear = list(map(lambda x: x/cl, linear))
    # logLinear = list(map(lambda x: x * log2(x), n))
    # cll = logLinear[0]
    # logLinear = list(map(lambda x: x/cll, logLinear))
    karatsuba = list(map(lambda x: x**1.59, n))
    ck = karatsuba[0]
    karatsuba = list(map(lambda x: x/ck, karatsuba))
    # plotting the points
    plt.plot(n, t, color='k', label='actual')
    plt.plot(n, quadratic, color='r', label='quadratic')
    plt.plot(n, linear, color='b', label='linear')
    # plt.plot(n, logLinear, color='g', label='log linear')
    plt.plot(n, karatsuba, color='g', label='karatsuba')
    plt.legend()

    if loglog:
        plt.loglog(n, t)
    # naming the x axis
    plt.xlabel('input size (n)')
    # naming the y axis
    plt.ylabel('run time')

    # giving a title to my graph
    plt.title('time complexity')

    # function to show the plot
    plt.show()
