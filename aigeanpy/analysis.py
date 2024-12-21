from aigeanpy.clustering import cluster
from pathlib import Path

def kmeans(filename, clusters=3, iterations=10):
    '''Given a filen a file that can be converted into a list of tuples,
    from said list of tuples, choose 'clusters' random points to be centres.
    Then assign each tuple in list to the centre it is closest to, recalculate
    the centre, then iterate over 'max_iterations' number of times.

    Parameters
    ----------
    filename : str or path object
        the name of the file that contains the points

    clusters : int, optional
        number of centres, by default 3

    iterations : int, optional
        maximum number of times to iterate over the function, by default 10

    Returns
    -------
    list(tuple(float))
        the points belonging to each centre
    '''

    if type(filename) != str:
        raise TypeError("filename must be a string")

    if type(clusters) != int and type(iterations) != int:
        raise TypeError("Clusters and iterations must be integers")

    if clusters <= 0:
        raise ValueError("There must be at least one cluster")
    
    if iterations <= 0:
        raise ValueError("Function must iterate atleast once")

    file_path = Path(filename).absolute()

    lines = open(file_path, 'r').readlines()
    points = []

    for line in lines:
        points.append(tuple(map(float, line.strip().split(','))))

    centres, all_alloc_points = cluster(points, clusters, iterations)

    return all_alloc_points
