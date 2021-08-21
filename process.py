import matplotlib
matplotlib.use('Qt5Agg')
import pandas as pd
ardata = pd.read_csv("ardata.csv")
from sklearn.neural_network import MLPRegressor

data = pd.read_csv("data.csv")
# print(data)
from matplotlib import pyplot as plt
j = 0
X = []
y = []
for i in range(len(ardata)):
    while ardata.iloc[i, 0] > data.iloc[j, 0] and j < len(data) - 5:
        # print(j, len(ardata))
        j += 1
    labels = data.iloc[j, 1:].tolist()
    src = ardata.iloc[i, [1, 2]].tolist()
    print(src, labels)
    X.append(src)
    y.append([labels[0], labels[3]])
import  pandas as pd
X = pd.DataFrame(X)
X /= 1024
y = pd.DataFrame(y)
y = (y >= 0.5).astype('float')

print(X)
print(y)
src_x =X.copy()
for i in range(1, 32):
    # print(len(X[1:]), len(src_x[:-i]))
    X = X[1:].reset_index().join((src_x[:-i].reset_index()), lsuffix="_first", rsuffix=("_second"))
    for z in X.columns:
        # print(z)
        if 'index' in str(z):
            del X[z]
    print(X)
    y = y[1:]
model = MLPRegressor(hidden_layer_sizes=(512, 512))
model.fit(X, y)
y_ = model.predict(X)
y_ = (y_ >= 0.5).astype("float") * 0.95
plt.plot(src_x)
plt.plot(y)
plt.plot(y_)
plt.show()
exit()
for i in [2, 1]:  # TODO
    plt.plot(ardata.iloc[:, i])
plt.show()
plt.clf()
from matplotlib import pyplot as plt
for i in range(1, 6+1):
    plt.plot(data.iloc[:, i])
plt.show()