def plot(n, t, interpolation):
    from matplotlib import pyplot as plt

    interpolated = list(map(interpolation, n))
    # plotting the points
    plt.plot(n, t, color='r', label='actual')
    plt.plot(n, interpolated, color='g', label='interpolated')
    plt.legend()

    # naming the x axis
    plt.xlabel('input size (n)')
    # naming the y axis
    plt.ylabel('run time')

    # giving a title to my graph
    plt.title('time complexity')

    # function to show the plot
    plt.show()
