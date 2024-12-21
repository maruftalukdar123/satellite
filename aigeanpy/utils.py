import numpy as np

def create_points(rows, columns=3):
    '''Given a number of rows and columns it creates a list of tuples
    of shape (rows, columns), where each element is a random float
    taken from a uniform distribution.

    The maximum and minimum of each column is given by the maximum and
    minimum in the corresponding column in the samples.csv file.

    Bearing in mind that no random seed has been set in place
    so, create_points() will give a different output everytime

    Parameters
    ----------
    rows : int
        The number of rows the output list should
        have when viewd as a 2d array
    
    columns: int
        The number of rows the output list should have
        when viewd as a 2d array. Default is 3

    Returns
    -------
    list(tuple)
        a list of tuples, ( with shape (rows, column) when viewd as a 2d array)
        where each element is a random float taken from a uniform distribution.


    Example
    --------
    >>> points = create_points(20)

    >>> print(len(points))
    20

    >>> print(len(points[0]))
    3

    >>> print(type(points[0][0]))
    <class 'numpy.float64'>
    '''

    column_1 = np.random.uniform(low=-4.4,high=6.7,size=rows)
    column_2 = np.random.uniform(low=-1.4,high=7.0,size=rows)
    column_3 = np.random.uniform(low=-2.4,high=6.5,size=rows)

    points = []

    for x,y,z in zip(column_1,column_2,column_3):
        points.append((x,y,z))
    
    return points