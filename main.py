import numpy as np
from matplotlib import pyplot as plot
from termcolor import colored


def generate(length):
    data = []
    for i in range(length):
        x = np.random.randint(0, length)
        y = np.random.randint(0, length)
        data.append([x, y])
    return data


# Analyze the data and generate clusters
def analyze(data, n):
    cp = data.copy()

    for i in range(n):
        matrix, x, y = generate_matrix(cp)
        product = []
        for j in range(len(matrix)):
            z = matrix[j].index(find_lowest(matrix[j]))
            product.append(cluster_average([cp[j], cp[z]]))
        cleaned = remove_duplicates(product)
        if len(cleaned) > 1:
            cp = cleaned
            # generate_plot_by_iteration(cp, i)
            print(colored('iteration ' + str(i + 1) + ':', 'cyan'), cp)
        else:
            print(colored('Can\'t iterate anymore! Exiting loop.', 'red'))
            break
    return cp


# Run algorithm on user input
def categorise(matrix, needle):
    arr = []
    for i in matrix:
        arr.append(euclidean_distance(i, needle))
    return matrix[arr.index(find_lowest(arr))]


# Find lowest value in a list
def find_lowest(lst):
    lowest = next(x[1] for x in enumerate(lst) if x[1] > 0)
    for x in lst:
        if lowest > x > 0:
            lowest = x
    return lowest


# Remove duplicates
def remove_duplicates(arr):
    tmp = []
    for i in arr:
        if tmp.count(i) == 0:
            tmp.append(i)
        for j in arr:
            if i != j and tmp.count(j) == 0:
                tmp.append(j)
    return tmp


# Convert to matrix
def generate_matrix(data):
    # Declare target lists
    x = []
    y = []
    m = []
    for i in range(len(data)):
        x.append(data[i][0])
        y.append(data[i][1])
    # For each row in the matrix, generate data
    for i in range(len(data)):
        a = []
        for j in range(len(data)):
            a.append(euclidean_distance(data[i], data[j]))
        m.append(a)

    return m, x, y


def cluster_average(cluster):
    sum_x = cluster[1][0] + cluster[0][0]
    sum_y = cluster[1][1] + cluster[0][1]
    avg = [(sum_x / 2), (sum_y / 2)]

    return avg


def euclidean_distance(d1, d2):
    delta_x = d2[0] - d1[0]
    delta_y = d2[1] - d1[1]
    d = np.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
    return d


def generate_plot(data, method, n=0):
    if method == 'ITERATION':
        generate_plot_by_iteration(data, n)
    elif method == 'CATEGORY':
        generate_plot_by_category(data)


def generate_plot_by_iteration(data, n):
    d = np.array(data)
    x, y = d.T
    plot.scatter(x, y, label='#'+str(n))
    plot.legend(loc='upper left')

    # plot.show()


def generate_plot_by_category(data, categories, plot_categories=False):
    arr = []

    if plot_categories:
        d = np.array(categories)
        x, y = d.T
        plot.scatter(x, y, label='Categories')
        plot.legend(loc='upper left')

    for c in range(len(categories)):
        arr.append([])
    for i in data:
        arr[categories.index(categorise(categories, i))].append(i)
    for r in arr:
        n = arr.index(r)
        d = np.array(r)
        x, y = d.T
        plot.scatter(x, y, label='#' + str(n))


if __name__ == '__main__':
    p_data_len = int(input("Data length: "))
    p_iterations = int(input("Iterations: "))
    print("\n")

    p_data = generate(p_data_len)
    print(colored('Generated data:', 'green'), p_data)
    print("\n")

    p_matrix = analyze(p_data, p_iterations)
    print(colored('Matrix:', 'green'), p_matrix)
    print("\n")

    p_test = [int(input("Test coordinate 1: ")), int(input("Test coordinate 2: "))]
    p_test_result = categorise(p_matrix, p_test)
    print(colored("Test result:", 'green'), p_test_result)

    generate_plot_by_category(p_data, p_matrix)

    plot.show()
