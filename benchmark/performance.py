import sys 
sys.path.append('.')

import aigeanpy.clustering
import aigeanpy.clustering_numpy
import matplotlib.pyplot as plt

from aigeanpy.utils import create_points
from time import time

normal_time = []
numpy_time = []

for i in range(100,10100,100):
    points = create_points(i)

    start = time()
    aigeanpy.clustering.cluster(points=points)
    end = time()
    time_passed = end-start

    normal_time.append(time_passed)

    start = time()
    aigeanpy.clustering_numpy.cluster(points=points)
    end = time()
    time_passed = end-start

    numpy_time.append(time_passed)


x = [i for i in range(100,10100,100)]
plt.figure()
plt.plot(x, normal_time, label='Normal Time')
plt.plot(x, numpy_time, label='Numpy Time')
plt.xlabel('Number of data points')
plt.ylabel('Time taken in seconds')
plt.legend(loc='best')
plt.grid(True)
plt.savefig(fname='benchmark/performance')
plt.show()
