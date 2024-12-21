from argparse import ArgumentParser
from math import sqrt
from pathlib import Path
from random import randrange

def cluster(points, clusters=3 ,max_iterations=10):
    '''From a list of tuples, choose 'clusters' random points to be centres.
    Then assign each tuple in list to the centre it is closest to, recalculate
    the centre, then iterate over 'max_iterations' number of times.

    This version does not use the numpy library and is cosiderably slower than the
    numpy version, especially when there are large number of data points.

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
    list(tuple(float))
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

    m = [points[randrange(len(points))], points[randrange(len(points))], points[randrange(len(points))]]

    alloc = [None]*len(points)

    # Finds the distance of each points to each of the clusters
    def distance_to_centre(clusters=3):
        d = [None] * clusters

        for j in range(clusters):
            d[j] = sqrt((p[0]-m[j][0])**2 + (p[1]-m[j][1])**2 + (p[2]-m[j][2])**2)
        return d


    ITERATIONS = 0

    while ITERATIONS < max_iterations:

        for i, p in enumerate(points):

            d = distance_to_centre(clusters=clusters)
            alloc[i] = d.index(min(d))

        for i in range(clusters):
            alloc_points = [p for j, p in enumerate(points) if alloc[j] == i]

            new_mean = (
                sum([a[0] for a in alloc_points]) / len(alloc_points),
                sum([a[1] for a in alloc_points]) / len(alloc_points),
                sum([a[2] for a in alloc_points]) / len(alloc_points)
                )

            m[i] = new_mean

        ITERATIONS += 1


    all_alloc_points = []
    centres = []
    for i in range(clusters):

        alloc_points=[p for j, p in enumerate(points) if alloc[j] == i]

        all_alloc_points.append(alloc_points)
        centres.append((str(m[i])))

    return centres, all_alloc_points



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