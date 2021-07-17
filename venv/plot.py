def plot(n, t, loglog=False, interpolation=lambda x: 1.2 * 1e-6 * (x ** 2)):
    from matplotlib import pyplot as plt
    from math import log2

    interpolated = list(map(interpolation, n))
    linear = list(map(lambda x: 1.2 * 1e-6 * x, n))
    logLinear = list(map(lambda x: 1.2 * 1e-6 * x * log2(x), n))
    # plotting the points
    plt.plot(n, t, color='k', label='actual')
    plt.plot(n, interpolated, color='r', label='quadratic')
    plt.plot(n, linear, color='b', label='linear')
    plt.plot(n, logLinear, color='g', label='log linear')
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
