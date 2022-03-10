import seaborn as sns
import matplotlib.pyplot as plt

k = []
target = 4000
div = 1
for i in range(0, target*div):
    k.append(i/div)

def distribute_plot(data, label, type='both'):
    if type == 'both':
        sns.distplot(data[label], bins=k)
        plt.xlim(0, 4000)
        plt.show()
    elif type == 'hist':
        sns.displot(data[label], kde=False)
    elif type == 'kde':
        sns.displot(data[label], hist=False)
    else:
        print('invalid type. please use one of |both|hist|kde|')
