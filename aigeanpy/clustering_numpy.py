import numpy as np
from argparse import ArgumentParser
from pathlib import Path

def cluster(points, clusters=3, max_iterations=10):
    '''From a list of tuples, choose 'clusters' random points to be centres.
    Then assign each tuple in list to the centre it is closest to, recalculate
    the centre, then iterate over 'max_iterations' number of times.

    This version uses the numpy library and is cosiderably faster than the
    non-numpy version, especially when there are large number of data points.

    Parameters
    ----------
    points : list[tuples(float)]
        list of points that need to be assigned to a centre
    clusters : int, optional
        number of clusters, by default 3
    max_iterations : int, optional
        maximum number of times to iterate over the function, by default 10

    Returns
    -------
    numpy.array()
        the final centres of the clusters
    '''

    if type(points) != list:
        raise TypeError("points must be a list")

    if type(clusters) != int and type(max_iterations) != int:
        raise TypeError("Clusters and iterations must be integers")

    if clusters <= 0:
        raise ValueError("There must be at least one cluster")
    
    if max_iterations <= 0:
        raise ValueError("Function must iterate atleast once")

    points = np.array(points)
    m = points[np.random.choice(points.shape[0], size = clusters, replace = False)]

    ITERATIONS = 0

    while ITERATIONS < max_iterations:
        points_transformed = np.tile(points,(3,1))
        points_transformed = np.reshape(points_transformed,(np.shape(points)[0],clusters,np.shape(points)[1]),order='F')

        points_to_centres = np.linalg.norm((points_transformed - m),axis=2)

        alloc = np.argmin(points_to_centres, axis=1)

        for i in range(clusters):
            m[i] = np.mean(points[alloc==i], axis=0)
        ITERATIONS = max_iterations + 1
    
    m = []
    all_alloc_points = []
    for j in range(clusters):
        alloc_points=[p for k, p in enumerate(points) if alloc[k] == j]
        all_alloc_points.append(alloc_points)
        m.append(np.mean(points[alloc==j], axis=0))

    return np.array(m), all_alloc_points

def cli():
    parser = ArgumentParser(description="Call the normal cluster function")
    parser.add_argument('filename', type=str, help='Name of the file that contains the points')
    parser.add_argument('-i', '--iters', type=int, default=10, help='Maximum number of times to iterate over the function, by default 10')

    arguments = parser.parse_args()

    file_path = Path(arguments.filename).absolute()

    lines = open(file_path, 'r').readlines()
    points = []

    for line in lines:
        points.append(tuple(map(float, line.strip().split(','))))

    centres, all_alloc_points = cluster(points=points, max_iterations=arguments.iters)

    print(f'The clusters are centred at {centres}')
    print()
    print(f'The clusters are {all_alloc_points}')


if __name__ == '__main__':
    cli()