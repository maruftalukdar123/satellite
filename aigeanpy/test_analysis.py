import aigeanpy.analysis as analysis

def test_kmeans():
    points = analysis.kmeans('samples.csv',3, 10)
    total_points = len(points[0]) + len(points[1]) + len(points[2])
    assert total_points == 300, 'Did not get the number of points expected. kmeans is not working as it should'