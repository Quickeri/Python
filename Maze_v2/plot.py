import matplotlib.pyplot as plt

data = {}
data["5"] = [0, 0, 0, 0, 1.013, 0.960, 0, 0.998, 1.038, 1.225]
data["10"] = [1.995, 1.035, 1.940, 2.989, 2.829, 2.829, 2.885, 1.996, 1.029, 1.992]
data["15"] = [6.159, 3.986, 4.984, 6.206, 4.985, 6.329, 4.115, 4.99, 4.985, 6.007]
data["20"] = [5.228, 6.202, 6.706, 8.08, 3.59, 6.654, 10.851, 6.565, 7.257, 6.998]
data["25"] = [13.95, 21.75, 7.057, 11.838, 6.998, 8.882, 8.998, 15.948, 7.182, 12.005]
data["30"] = [16.997, 18.663, 15.994, 8.665, 6.890, 17.694, 25.877, 18.21, 18.251, 18.979]

def calc_average(values):
    return sum(values) / len(values)

def get_average_times(data_dict):
    avg_times = []
    for key in data_dict.keys():
        avg_times.append(calc_average(data_dict[key])) 
    return avg_times

def setup_plot(title, title2, xlabel, ylabel):
    plt.title("{}\n{}".format(title, title2))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot_data(x, y):
    plt.plot(x, y, label="hej")
    plt.legend()
    plt.show()