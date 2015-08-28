import matplotlib.pyplot as plt



b = {111:[2,4,5,7,8], 114:[2,7,2,1,9], 117:[2,12,5,7,11], 119:[2,14,5,7,18],}
xs, ys=zip(*((int(x), k) for k in b for x in b[k]))

plt.plot(ys, xs, 'ro')

plt.legend(ys)
plt.show()